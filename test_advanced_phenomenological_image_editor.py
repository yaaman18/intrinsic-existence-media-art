#!/usr/bin/env python3
"""
TDD Test Suite for AdvancedPhenomenologicalImageEditor
t-wada式TDDによるedit_imageメソッドの実装テスト
"""

import unittest
import sys
import tempfile
import os
from pathlib import Path
from PIL import Image
import numpy as np

# プロジェクトのsrc/coreディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent / "src" / "core"))

try:
    from advanced_phenomenological_image_editor import AdvancedPhenomenologicalImageEditor
except ImportError as e:
    print(f"Import Error: {e}")
    print("テストを実行するにはadvanced_phenomenological_image_editor.pyが必要です")
    sys.exit(1)


class TestAdvancedPhenomenologicalImageEditor(unittest.TestCase):
    """AdvancedPhenomenologicalImageEditorのTDDテストクラス"""
    
    def setUp(self):
        """各テストの前に実行される準備処理"""
        self.editor = AdvancedPhenomenologicalImageEditor()
        
        # テスト用の画像を作成
        self.test_image = Image.new('RGB', (100, 100), color='red')
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_image_path = self.temp_dir / "test_image.jpg"
        self.test_image.save(self.test_image_path)
        
        # テスト用のプロンプト
        self.test_prompt = "青い色調に変更して、ぼかし効果を適用してください"
    
    def tearDown(self):
        """各テストの後に実行されるクリーンアップ処理"""
        # テスト用ファイルを削除
        if self.test_image_path.exists():
            self.test_image_path.unlink()
        if self.temp_dir.exists():
            self.temp_dir.rmdir()
    
    def test_edit_image_method_exists(self):
        """RED: edit_imageメソッドが存在することを確認"""
        self.assertTrue(
            hasattr(self.editor, 'edit_image'),
            "AdvancedPhenomenologicalImageEditorにedit_imageメソッドが存在しません"
        )
    
    def test_edit_image_is_callable(self):
        """RED: edit_imageメソッドが呼び出し可能であることを確認"""
        self.assertTrue(
            callable(getattr(self.editor, 'edit_image', None)),
            "edit_imageメソッドが呼び出し可能ではありません"
        )
    
    def test_edit_image_accepts_image_path_and_prompt(self):
        """RED: edit_imageメソッドが画像パスとプロンプトを受け取ることを確認"""
        try:
            # メソッドが正しい引数を受け取るかテスト
            result = self.editor.edit_image(str(self.test_image_path), self.test_prompt)
            # ここでは例外が発生しないことを確認
            self.assertIsNotNone(result, "edit_imageメソッドの戻り値がNoneです")
        except TypeError as e:
            self.fail(f"edit_imageメソッドが正しい引数を受け取れません: {e}")
        except AttributeError as e:
            self.fail(f"edit_imageメソッドが存在しません: {e}")
    
    def test_edit_image_returns_expected_format(self):
        """RED: edit_imageメソッドが期待される形式の戻り値を返すことを確認"""
        result = self.editor.edit_image(str(self.test_image_path), self.test_prompt)
        
        # 戻り値が辞書形式であることを確認
        self.assertIsInstance(result, dict, "edit_imageの戻り値が辞書ではありません")
        
        # 必要なキーが含まれていることを確認
        expected_keys = ['output_path', 'edit_info']
        for key in expected_keys:
            self.assertIn(key, result, f"戻り値に必要なキー '{key}' が含まれていません")
    
    def test_edit_image_creates_output_file(self):
        """RED: edit_imageメソッドが出力ファイルを作成することを確認"""
        result = self.editor.edit_image(str(self.test_image_path), self.test_prompt)
        
        # 出力パスが有効であることを確認
        output_path = Path(result['output_path'])
        self.assertTrue(output_path.exists(), "出力画像ファイルが作成されていません")
        self.assertTrue(output_path.is_file(), "出力パスがファイルではありません")
        
        # 画像として開けることを確認
        try:
            edited_image = Image.open(output_path)
            self.assertEqual(edited_image.format, 'JPEG', "出力画像がJPEG形式ではありません")
        except Exception as e:
            self.fail(f"出力画像を開くことができません: {e}")
    
    def test_edit_image_with_various_prompts(self):
        """RED: 様々なプロンプトでedit_imageメソッドが動作することを確認"""
        test_prompts = [
            "明度を上げて、コントラストを強くしてください",
            "セピア調に変更してください",
            "ぼかし効果を適用してください",
            "色温度を暖かくしてください"
        ]
        
        for prompt in test_prompts:
            with self.subTest(prompt=prompt):
                result = self.editor.edit_image(str(self.test_image_path), prompt)
                self.assertIsInstance(result, dict, f"プロンプト '{prompt}' での処理が失敗しました")
                self.assertIn('output_path', result, f"プロンプト '{prompt}' で出力パスが返されませんでした")
    
    def test_edit_image_edit_info_structure(self):
        """RED: edit_infoが適切な構造を持つことを確認"""
        result = self.editor.edit_image(str(self.test_image_path), self.test_prompt)
        
        edit_info = result['edit_info']
        self.assertIsInstance(edit_info, dict, "edit_infoが辞書ではありません")
        
        # edit_infoに期待されるキーが含まれていることを確認
        expected_info_keys = ['active_nodes', 'phi', 'generation']
        for key in expected_info_keys:
            self.assertIn(key, edit_info, f"edit_infoに必要なキー '{key}' が含まれていません")
    
    def test_edit_image_handles_invalid_image_path(self):
        """RED: 無効な画像パスに対する適切なエラーハンドリングを確認"""
        invalid_path = "/path/to/nonexistent/image.jpg"
        
        with self.assertRaises((FileNotFoundError, IOError, ValueError)):
            self.editor.edit_image(invalid_path, self.test_prompt)
    
    def test_edit_image_handles_empty_prompt(self):
        """RED: 空のプロンプトに対する適切なハンドリングを確認"""
        empty_prompt = ""
        
        # 空のプロンプトでも例外を発生させずに処理するか、
        # 適切な例外を発生させるかを確認
        try:
            result = self.editor.edit_image(str(self.test_image_path), empty_prompt)
            # 空のプロンプトでも何らかの結果を返すことを期待
            self.assertIsInstance(result, dict, "空のプロンプトでも辞書を返すべきです")
        except ValueError:
            # または適切なValueErrorを発生させることも許容
            pass


class TestAdvancedPhenomenologicalImageEditorIntegration(unittest.TestCase):
    """統合テスト"""
    
    def setUp(self):
        """統合テスト用の準備"""
        self.editor = AdvancedPhenomenologicalImageEditor()
        
        # より現実的なテスト画像を作成
        self.realistic_image = Image.new('RGB', (256, 256))
        pixels = []
        for y in range(256):
            for x in range(256):
                # グラデーション画像を作成
                r = int((x / 256) * 255)
                g = int((y / 256) * 255)
                b = 128
                pixels.append((r, g, b))
        self.realistic_image.putdata(pixels)
        
        self.temp_dir = Path(tempfile.mkdtemp())
        self.realistic_image_path = self.temp_dir / "realistic_test.jpg"
        self.realistic_image.save(self.realistic_image_path)
    
    def tearDown(self):
        """統合テスト用のクリーンアップ"""
        if self.realistic_image_path.exists():
            self.realistic_image_path.unlink()
        if self.temp_dir.exists():
            self.temp_dir.rmdir()
    
    def test_real_world_editing_scenario(self):
        """RED: 実際の使用シナリオでのテスト"""
        complex_prompt = """
        この画像の明度を20%上げて、青い色調を強調してください。
        さらに軽いぼかし効果を適用し、周囲にビネット効果を追加してください。
        最終的に温かみのある色温度に調整してください。
        """
        
        result = self.editor.edit_image(str(self.realistic_image_path), complex_prompt)
        
        # 複雑な編集処理の結果を検証
        self.assertIsInstance(result, dict)
        self.assertIn('output_path', result)
        self.assertIn('edit_info', result)
        
        # 出力画像が適切に処理されていることを確認
        output_path = Path(result['output_path'])
        self.assertTrue(output_path.exists())
        
        # 編集情報が適切に記録されていることを確認
        edit_info = result['edit_info']
        self.assertIsInstance(edit_info.get('phi'), (int, float))
        self.assertIsInstance(edit_info.get('generation'), int)


if __name__ == '__main__':
    print("=" * 60)
    print("TDD Test Suite for AdvancedPhenomenologicalImageEditor")
    print("t-wada式TDD: RED Phase (失敗するテストを実行)")
    print("=" * 60)
    print()
    
    # テストを実行
    unittest.main(verbosity=2)