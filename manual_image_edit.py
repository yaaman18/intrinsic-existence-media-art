#!/usr/bin/env python3
"""
手動パラメーター調整による画像編集テスト
shibuya-1.jpgを使用したインタラクティブな編集
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
        print(f"✅ 画像を読み込みました: {image_path}")
        print(f"   サイズ: {image.size[0]} x {image.size[1]}")
        print(f"   モード: {image.mode}")
        return image
    except Exception as e:
        print(f"❌ 画像読み込みエラー: {e}")
        return None


def show_available_effects():
    """利用可能なエフェクト一覧を表示"""
    effects = [
        "gaussian_blur - ガウシアンブラー",
        "motion_blur - モーションブラー", 
        "brightness_adjust - 明度調整",
        "contrast_adjust - コントラスト調整",
        "color_adjust - 彩度調整",
        "color_temperature - 色温度調整",
        "add_noise - ノイズ追加",
        "edge_enhance - エッジ強調",
        "vignette - ビネット効果",
        "chromatic_aberration - 色収差",
        "fog_effect - 霧効果",
        "glitch_effect - グリッチ効果",
        "texture_overlay - テクスチャオーバーレイ"
    ]
    
    print("\n📋 利用可能なエフェクト:")
    for i, effect in enumerate(effects, 1):
        print(f"  {i:2d}. {effect}")
    print()


def get_user_input():
    """ユーザー入力を取得"""
    try:
        print("🎛️  編集パラメーターを入力してください:")
        
        # エフェクト選択
        effect = input("エフェクト名 (例: fog_effect): ").strip()
        if not effect:
            effect = "fog_effect"  # デフォルト
        
        # 強度設定
        intensity_str = input("強度 0.0-1.0 (例: 0.5): ").strip()
        try:
            intensity = float(intensity_str) if intensity_str else 0.5
            intensity = max(0.0, min(1.0, intensity))  # 0.0-1.0に制限
        except ValueError:
            intensity = 0.5
        
        # 位置設定
        location = input("位置 (画像全体/中央部/境界領域): ").strip()
        if not location:
            location = "画像全体"
        
        # 出力ファイル名
        output_name = input("出力ファイル名 (例: test_edit.jpg): ").strip()
        if not output_name:
            output_name = f"{effect}_{intensity:.1f}.jpg"
        
        return {
            'effect': effect,
            'intensity': intensity,
            'location': location,
            'output_name': output_name
        }
        
    except KeyboardInterrupt:
        print("\n\n👋 編集を終了します。")
        return None


def apply_manual_edit(image, editor, params):
    """手動パラメーターで編集を適用"""
    print(f"\n🔄 編集を適用中...")
    print(f"   エフェクト: {params['effect']}")
    print(f"   強度: {params['intensity']}")
    print(f"   位置: {params['location']}")
    
    try:
        # 現象学的指示として構築
        instruction = {
            'action': f"{params['effect']}を適用",
            'location': params['location'],
            'dimension': ['appearance'],  # デフォルト次元
            'intensity': params['intensity']
        }
        
        # 編集実行
        result = editor.apply_phenomenological_edit(image, instruction)
        
        # 出力ディレクトリ作成
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # ファイル保存
        output_path = output_dir / params['output_name']
        result.save(output_path, quality=95)
        
        print(f"✅ 編集完了！保存先: {output_path}")
        
        # 編集履歴の表示
        if editor.edit_history:
            last_edit = editor.edit_history[-1]
            effects = last_edit.get('effects', [])
            print(f"   適用されたエフェクト数: {len(effects)}")
            for effect in effects:
                print(f"     • {effect['name']} (強度: {effect['intensity']:.2f})")
        
        return True
        
    except Exception as e:
        print(f"❌ 編集エラー: {e}")
        return False


def manual_editing_mode():
    """手動編集モード"""
    print("🎨 現象学的画像編集システム - 手動モード")
    print("=" * 50)
    
    # 画像読み込み
    original = load_shibuya_image()
    if original is None:
        return
    
    # エディター初期化
    editor = PhenomenologicalImageEditor()
    
    # 元画像を出力ディレクトリに保存
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    original_path = output_dir / "original_shibuya.jpg"
    original.save(original_path, quality=95)
    print(f"📁 元画像を保存: {original_path}")
    
    # エフェクト一覧表示
    show_available_effects()
    
    while True:
        print("\n" + "-" * 50)
        
        # ユーザー入力取得
        params = get_user_input()
        if params is None:
            break
        
        # 編集実行
        success = apply_manual_edit(original, editor, params)
        
        if success:
            # 続行確認
            continue_choice = input("\n🔄 別の編集を試しますか？ (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes', 'はい']:
                break
        else:
            # エラー時の続行確認
            retry_choice = input("\n🔄 再試行しますか？ (y/n): ").strip().lower()
            if retry_choice not in ['y', 'yes', 'はい']:
                break


def quick_test_mode():
    """クイックテストモード（パラメーター例）"""
    print("\n🚀 クイックテストモード")
    print("いくつかの編集例を自動実行します...")
    
    original = load_shibuya_image()
    if original is None:
        return
    
    editor = PhenomenologicalImageEditor()
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # テスト例
    test_cases = [
        {
            'effect': 'fog_effect',
            'intensity': 0.6,
            'location': '画像全体',
            'output_name': 'quick_fog_06.jpg',
            'description': '霧効果（強度0.6）'
        },
        {
            'effect': 'gaussian_blur',
            'intensity': 0.4,
            'location': '画像全体', 
            'output_name': 'quick_blur_04.jpg',
            'description': 'ガウシアンブラー（強度0.4）'
        },
        {
            'effect': 'color_temperature',
            'intensity': 0.7,
            'location': '画像全体',
            'output_name': 'quick_temp_07.jpg',
            'description': '色温度調整（強度0.7）'
        },
        {
            'effect': 'vignette',
            'intensity': 0.8,
            'location': '画像全体',
            'output_name': 'quick_vignette_08.jpg',
            'description': 'ビネット効果（強度0.8）'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['description']}")
        success = apply_manual_edit(original, editor, test)
        if not success:
            print("   ⚠️ このテストをスキップします")


def main():
    """メイン関数"""
    try:
        print("現象学的画像編集システム")
        print("shibuya-1.jpg 手動編集モード")
        print("=" * 50)
        
        print("\nモードを選択してください:")
        print("1. 手動編集モード（パラメーター入力）")
        print("2. クイックテストモード（自動実行）")
        
        choice = input("\n選択 (1 or 2): ").strip()
        
        if choice == "2":
            quick_test_mode()
        else:
            manual_editing_mode()
        
        print(f"\n{'=' * 50}")
        print("🎨 編集セッションを終了しました！")
        print("📁 結果は 'output' ディレクトリで確認できます")
        
    except KeyboardInterrupt:
        print("\n\n👋 プログラムを終了します。")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")


if __name__ == "__main__":
    main()