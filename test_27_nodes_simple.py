#!/usr/bin/env python3
"""
27ノード現象学的画像エフェクトシステムの簡単なテスト
基本的な動作確認のみ
"""

import sys
import numpy as np
from pathlib import Path
from PIL import Image

# パスの設定
sys.path.append(str(Path(__file__).parent / "src" / "core"))

# 直接インポート
from appearance_effects import AppearanceEffects


def test_appearance_effects():
    """現出様式エフェクトのテスト"""
    print("🧪 現出様式エフェクトテスト")
    print("=" * 40)
    
    # テスト画像の読み込み
    image_path = Path("examples/images/shibuya-1.jpg")
    if not image_path.exists():
        print(f"❌ テスト画像が見つかりません: {image_path}")
        return False
    
    image = Image.open(image_path)
    print(f"✅ テスト画像読み込み: {image.size}")
    
    # 出力ディレクトリの作成
    output_dir = Path("output/27nodes_simple_test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # テストケース
    test_cases = [
        {
            "name": "高密度エフェクト",
            "effect": AppearanceEffects.density_effect,
            "intensity": 0.8,
            "node_state": 0.9,
            "filename": "density_high.jpg"
        },
        {
            "name": "低密度エフェクト", 
            "effect": AppearanceEffects.density_effect,
            "intensity": 0.6,
            "node_state": 0.2,
            "filename": "density_low.jpg"
        },
        {
            "name": "高輝度エフェクト",
            "effect": AppearanceEffects.luminosity_effect,
            "intensity": 0.7,
            "node_state": 0.8,
            "filename": "luminosity_high.jpg"
        },
        {
            "name": "低輝度エフェクト",
            "effect": AppearanceEffects.luminosity_effect,
            "intensity": 0.5,
            "node_state": 0.3,
            "filename": "luminosity_low.jpg"
        },
        {
            "name": "高色度エフェクト",
            "effect": AppearanceEffects.chromaticity_effect,
            "intensity": 0.6,
            "node_state": 0.7,
            "filename": "chromaticity_high.jpg"
        },
        {
            "name": "低色度エフェクト",
            "effect": AppearanceEffects.chromaticity_effect,
            "intensity": 0.4,
            "node_state": 0.3,
            "filename": "chromaticity_low.jpg"
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        
        try:
            # エフェクトの適用
            result_image = test_case['effect'](
                image, 
                test_case['intensity'], 
                test_case['node_state']
            )
            
            # 結果の保存
            output_path = output_dir / test_case['filename']
            result_image.save(output_path, quality=95)
            
            print(f"   ✅ 保存完了: {output_path}")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*40}")
    print(f"🎯 テスト結果: {success_count}/{len(test_cases)} 成功")
    
    if success_count == len(test_cases):
        print("🎉 現出様式エフェクトは正常に動作しています！")
        return True
    else:
        print(f"⚠️  {len(test_cases) - success_count}個のテストが失敗しました")
        return False


def test_parameter_variations():
    """パラメータ変動テスト"""
    print("\n🧪 パラメータ変動テスト")
    print("=" * 40)
    
    image_path = Path("examples/images/shibuya-1.jpg")
    image = Image.open(image_path)
    
    output_dir = Path("output/27nodes_simple_test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 密度エフェクトのパラメータ変動
    print("\n📊 密度エフェクトのパラメータ変動")
    
    node_states = [0.1, 0.3, 0.5, 0.7, 0.9]
    intensities = [0.3, 0.5, 0.8]
    
    for intensity in intensities:
        for node_state in node_states:
            try:
                result = AppearanceEffects.density_effect(image, intensity, node_state)
                filename = f"density_i{intensity:.1f}_n{node_state:.1f}.jpg"
                output_path = output_dir / filename
                result.save(output_path, quality=85)
                print(f"   ✅ intensity={intensity:.1f}, node_state={node_state:.1f}")
            except Exception as e:
                print(f"   ❌ intensity={intensity:.1f}, node_state={node_state:.1f}: {e}")
    
    print("✅ パラメータ変動テスト完了")
    return True


def show_generated_files():
    """生成されたファイルの表示"""
    print("\n📁 生成されたファイル")
    print("=" * 40)
    
    output_dir = Path("output/27nodes_simple_test")
    if not output_dir.exists():
        print("出力ディレクトリが見つかりません")
        return
    
    files = list(output_dir.glob("*.jpg"))
    if not files:
        print("生成されたファイルが見つかりません")
        return
    
    total_size = 0
    for file_path in sorted(files):
        size_kb = file_path.stat().st_size / 1024
        total_size += size_kb
        print(f"   {file_path.name} ({size_kb:.1f}KB)")
    
    print(f"\n合計: {len(files)}ファイル, {total_size/1024:.2f}MB")


def main():
    """メインテスト実行"""
    print("🚀 27ノード現象学的画像エフェクトシステム - 簡単テスト")
    print("=" * 60)
    
    results = []
    
    # 基本エフェクトテスト
    result1 = test_appearance_effects()
    results.append(("現出様式エフェクト", result1))
    
    # パラメータ変動テスト
    result2 = test_parameter_variations() 
    results.append(("パラメータ変動", result2))
    
    # ファイル表示
    show_generated_files()
    
    # 総合結果
    print(f"\n{'='*60}")
    print("🏁 総合結果")
    print("="*60)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    print(f"\n📊 成功率: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n🎉 全テスト成功！基本的な27ノードエフェクトが動作しています。")
        print("\n💡 次のステップ:")
        print("   1. 残りの24ノードエフェクト実装")
        print("   2. ノード間相互作用システムの完成")
        print("   3. 現象学的オラクルシステムとの統合")
    else:
        print(f"\n⚠️  基本エフェクトに問題があります。修正が必要です。")


if __name__ == "__main__":
    main()