#!/usr/bin/env python3
"""
自動実行による画像編集デモ
shibuya-1.jpgを使用した複数パラメーターテスト
"""

import sys
from pathlib import Path
from PIL import Image

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent / "src" / "core"))

from phenomenological_image_editor import PhenomenologicalImageEditor


def load_shibuya_image():
    """shibuya-1.jpgの読み込み"""
    image_path = Path("examples/images/shibuya-1.jpg")
    
    if not image_path.exists():
        print(f"❌ 画像ファイルが見つかりません: {image_path}")
        return None
    
    try:
        image = Image.open(image_path)
        print(f"✅ 画像を読み込みました: {image_path1}")
        print(f"   サイズ: {image.size[0]} x {image.size[1]} pixels")
        print(f"   モード: {image.mode}")
        return image
    except Exception as e:
        print(f"❌ 画像読み込みエラー: {e}")
        return None


def apply_edit_with_params(image, editor, effect_name, intensity, location, output_name, description):
    """指定されたパラメーターで編集を適用"""
    print(f"\n🎨 {description}")
    print(f"   エフェクト: {effect_name}")
    print(f"   強度: {intensity}")
    print(f"   位置: {location}")
    
    try:
        # 現象学的指示として構築
        instruction = {
            'action': f"{effect_name}を適用",
            'location': location,
            'dimension': ['appearance', 'temporal'],  # 適切な次元を設定
            'intensity': intensity
        }
        
        # 編集実行
        result = editor.apply_phenomenological_edit(image, instruction)
        
        # 出力ディレクトリ作成
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # ファイル保存
        output_path = output_dir / output_name
        result.save(output_path, quality=95)
        
        print(f"   ✅ 保存完了: {output_path}")
        
        # 適用されたエフェクトの詳細表示
        if editor.edit_history:
            last_edit = editor.edit_history[-1]
            effects = last_edit.get('effects', [])
            print(f"   → 実際に適用されたエフェクト: {len(effects)}個")
            for effect in effects:
                print(f"     • {effect['name']} (強度: {effect['intensity']:.2f})")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 編集エラー: {e}")
        return False


def run_parameter_variations():
    """パラメーター変化のデモンストレーション"""
    print("🎛️  現象学的画像編集システム - パラメーター変化デモ")
    print("=" * 60)
    
    # 画像読み込み
    original = load_shibuya_image()
    if original is None:
        return
    
    # エディター初期化
    editor = PhenomenologicalImageEditor()
    
    # 元画像を出力ディレクトリに保存
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    original_path = output_dir / "demo_original_shibuya.jpg"
    original.save(original_path, quality=95)
    print(f"📁 元画像を保存: {original_path}")
    
    print("\n🔄 様々なパラメーターで編集テストを実行します...")
    
    # テストケース定義
    test_cases = [
        # 霧効果の強度変化
        ('fog_effect', 0.3, '画像全体', 'demo_fog_weak.jpg', '霧効果（弱）'),
        ('fog_effect', 0.6, '画像全体', 'demo_fog_medium.jpg', '霧効果（中）'),
        ('fog_effect', 0.9, '画像全体', 'demo_fog_strong.jpg', '霧効果（強）'),
        
        # ガウシアンブラーの強度変化  
        ('gaussian_blur', 0.2, '画像全体', 'demo_blur_light.jpg', 'ブラー（軽微）'),
        ('gaussian_blur', 0.5, '画像全体', 'demo_blur_medium.jpg', 'ブラー（中程度）'),
        ('gaussian_blur', 0.8, '画像全体', 'demo_blur_heavy.jpg', 'ブラー（重い）'),
        
        # 色温度調整の変化
        ('color_temperature', 0.2, '画像全体', 'demo_temp_cool.jpg', '色温度（寒色寄り）'),
        ('color_temperature', 0.5, '画像全体', 'demo_temp_neutral.jpg', '色温度（中性）'),
        ('color_temperature', 0.8, '画像全体', 'demo_temp_warm.jpg', '色温度（暖色寄り）'),
        
        # 位置の違い
        ('vignette', 0.7, '画像全体', 'demo_vignette_full.jpg', 'ビネット（全体）'),
        ('edge_enhance', 0.6, '中央部', 'demo_enhance_center.jpg', 'エッジ強調（中央）'),
        ('brightness_adjust', 0.7, '境界領域', 'demo_bright_edge.jpg', '明度調整（境界）'),
        
        # 複雑なエフェクト
        ('glitch_effect', 0.4, '画像全体', 'demo_glitch_mild.jpg', 'グリッチ効果（控えめ）'),
        ('chromatic_aberration', 0.5, '画像全体', 'demo_chromatic.jpg', '色収差効果'),
        ('texture_overlay', 0.6, '画像全体', 'demo_texture.jpg', 'テクスチャオーバーレイ'),
    ]
    
    # 全テストケース実行
    success_count = 0
    total_count = len(test_cases)
    
    for i, (effect, intensity, location, filename, description) in enumerate(test_cases, 1):
        print(f"\n[{i:2d}/{total_count}]", end=" ")
        
        success = apply_edit_with_params(
            original, editor, effect, intensity, location, filename, description
        )
        
        if success:
            success_count += 1
    
    # 結果サマリー
    print(f"\n{'=' * 60}")
    print(f"🎯 テスト結果: {success_count}/{total_count} 成功")
    print(f"📁 生成された画像: {success_count}個")
    print(f"📂 保存先: output/ ディレクトリ")
    
    if success_count == total_count:
        print("✨ 全てのパラメーターテストが正常に完了しました！")
    else:
        print(f"⚠️  {total_count - success_count}個のテストでエラーが発生しました")
    
    return success_count, total_count


def show_generated_files():
    """生成されたファイル一覧を表示"""
    output_dir = Path("output")
    
    if not output_dir.exists():
        print("📁 出力ディレクトリが見つかりません")
        return
    
    demo_files = list(output_dir.glob("demo_*.jpg"))
    
    if demo_files:
        print(f"\n📋 生成されたデモ画像一覧 ({len(demo_files)}個):")
        for file in sorted(demo_files):
            file_size = file.stat().st_size / 1024  # KB
            print(f"   • {file.name} ({file_size:.1f} KB)")
    else:
        print("\n📁 デモ画像ファイルが見つかりません")


def main():
    """メイン実行関数"""
    try:
        # パラメーター変化デモの実行
        success_count, total_count = run_parameter_variations()
        
        # 生成ファイル一覧表示
        show_generated_files()
        
        print(f"\n{'=' * 60}")
        print("🎨 現象学的画像編集システムのデモが完了しました！")
        print("\n💡 このシステムの特徴:")
        print("   • 13種類の豊富なエフェクト")
        print("   • 強度パラメーターによる細かい調整")
        print("   • 位置指定による部分的な適用")
        print("   • 自然言語による編集指示の解釈")
        print("\n🚀 オラクルシステムとの統合準備完了！")
        
    except Exception as e:
        print(f"\n❌ 実行エラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()