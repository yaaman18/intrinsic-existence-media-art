#!/usr/bin/env python3
"""
TDD Test Suite for Phenomenological Autonomous Creative Apparatus
現象学的自律創造機構のt-wada式TDDテストスイート
"""

import unittest
import sys
import tempfile
import os
import json
from pathlib import Path
from PIL import Image
import numpy as np
from unittest.mock import Mock, patch

# プロジェクトのsrc/coreディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent / "src" / "core"))

# テスト対象クラス（まだ存在しない）
try:
    from phenomenological_autonomous_creative_apparatus import (
        PhenomenologicalAutonomousCreativeApparatus,
        IntrinsicPersona,
        PhenomenologicalPalette,
        CreativeResult,
        AestheticMemory
    )
except ImportError as e:
    # テスト実行時に必要なクラスが存在しないことを確認
    print(f"Expected Import Error: {e}")
    print("これはTDD Red Phaseなので期待される動作です")


class TestPhenomenologicalAutonomousCreativeApparatus(unittest.TestCase):
    """現象学的自律創造機構のメインテストクラス"""
    
    def setUp(self):
        """各テストの前に実行される準備処理"""
        # テスト用の画像を作成
        self.test_image = Image.new('RGB', (100, 100), color='red')
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_image_path = self.temp_dir / "test_image.jpg"
        self.test_image.save(self.test_image_path)
        
        # モックAPIキーを設定
        os.environ['OPENAI_API_KEY'] = 'test_api_key'
    
    def tearDown(self):
        """各テストの後に実行されるクリーンアップ処理"""
        if self.test_image_path.exists():
            self.test_image_path.unlink()
        if self.temp_dir.exists():
            self.temp_dir.rmdir()
    
    def test_apparatus_class_exists(self):
        """RED: PhenomenologicalAutonomousCreativeApparatusクラスが存在することを確認"""
        self.assertTrue(
            'PhenomenologicalAutonomousCreativeApparatus' in globals(),
            "PhenomenologicalAutonomousCreativeApparatusクラスが存在しません"
        )
    
    def test_apparatus_initialization(self):
        """RED: 機構が正しく初期化されることを確認"""
        apparatus = PhenomenologicalAutonomousCreativeApparatus()
        
        # 必要な構成要素が初期化されているか確認
        self.assertIsNotNone(apparatus.intrinsic_persona, "内在性ペルソナが初期化されていません")
        self.assertIsNotNone(apparatus.palette_functions, "パレット関数が初期化されていません")
        self.assertIsNotNone(apparatus.aesthetic_memory, "美的記憶が初期化されていません")
    
    def test_create_from_image_method_exists(self):
        """RED: create_from_imageメソッドが存在することを確認"""
        apparatus = PhenomenologicalAutonomousCreativeApparatus()
        self.assertTrue(
            hasattr(apparatus, 'create_from_image'),
            "create_from_imageメソッドが存在しません"
        )
    
    def test_create_from_image_returns_creative_result(self):
        """RED: create_from_imageが適切なCreativeResultを返すことを確認"""
        apparatus = PhenomenologicalAutonomousCreativeApparatus()
        
        with patch('openai.OpenAI') as mock_openai:
            # OpenAI APIのモック設定
            mock_choice = Mock()
            mock_choice.message.content = json.dumps([
                {"function": "conscious_focus", "intensity": 0.8, "reason": "意識の焦点化"}
            ])
            mock_response = Mock()
            mock_response.choices = [mock_choice]
            mock_openai.return_value.chat.completions.create.return_value = mock_response
            
            result = apparatus.create_from_image(str(self.test_image_path))
            
            # CreativeResultの構造を確認
            self.assertIsInstance(result, CreativeResult, "戻り値がCreativeResultではありません")
            self.assertEqual(result.original_image, str(self.test_image_path), "元画像パスが正しくありません")
            self.assertIsNotNone(result.created_image, "作成された画像がありません")
            self.assertIsInstance(result.operations, list, "操作リストが適切ではありません")


class TestIntrinsicPersona(unittest.TestCase):
    """内在性ペルソナのテストクラス"""
    
    def setUp(self):
        """テスト準備"""
        self.test_image = Image.new('RGB', (100, 100), color='blue')
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_image_path = self.temp_dir / "persona_test.jpg"
        self.test_image.save(self.test_image_path)
        
        os.environ['OPENAI_API_KEY'] = 'test_api_key'
    
    def tearDown(self):
        """クリーンアップ"""
        if self.test_image_path.exists():
            self.test_image_path.unlink()
        if self.temp_dir.exists():
            self.temp_dir.rmdir()
    
    def test_intrinsic_persona_class_exists(self):
        """RED: IntrinsicPersonaクラスが存在することを確認"""
        self.assertTrue(
            'IntrinsicPersona' in globals(),
            "IntrinsicPersonaクラスが存在しません"
        )
    
    def test_analyze_phenomenological_impression(self):
        """RED: 現象学的印象分析メソッドが存在し、27次元データを返すことを確認"""
        persona = IntrinsicPersona()
        
        with patch('openai.OpenAI') as mock_openai:
            impression = persona.analyze_phenomenological_impression(str(self.test_image_path))
            
            # 27次元の辞書が返されることを確認
            self.assertIsInstance(impression, dict, "印象分析の結果が辞書ではありません")
            self.assertEqual(len(impression), 27, "27次元のデータが返されていません")
            
            # 各次元の値が0-1の範囲内であることを確認
            for key, value in impression.items():
                self.assertIsInstance(value, (int, float), f"{key}の値が数値ではありません")
                self.assertGreaterEqual(value, 0, f"{key}の値が0未満です")
                self.assertLessEqual(value, 1, f"{key}の値が1を超えています")
    
    def test_decide_operations_with_llm_api(self):
        """RED: LLM APIを使用してパレット操作を決定することを確認"""
        persona = IntrinsicPersona()
        
        mock_activations = {
            'temporal_basic': 0.7,
            'conscious_attention': 0.9,
            'existential_presence': 0.5
        }
        
        with patch('openai.OpenAI') as mock_openai:
            # LLM APIの応答をモック
            mock_choice = Mock()
            mock_choice.message.content = json.dumps([
                {"function": "conscious_focus", "intensity": 0.8, "reason": "意識の焦点化により存在感を強調"},
                {"function": "temporal_echo", "intensity": 0.3, "reason": "時間の残響で記憶の層を表現"}
            ])
            mock_response = Mock()
            mock_response.choices = [mock_choice]
            mock_openai.return_value.chat.completions.create.return_value = mock_response
            
            operations = persona.decide_operations(mock_activations)
            
            # 操作リストの構造を確認
            self.assertIsInstance(operations, list, "操作リストがリストではありません")
            self.assertGreater(len(operations), 0, "操作が生成されていません")
            
            for op in operations:
                self.assertIn('function', op, "操作に関数名が含まれていません")
                self.assertIn('intensity', op, "操作に強度が含まれていません")
                self.assertIn('reason', op, "操作に理由が含まれていません")


class TestPhenomenologicalPalette(unittest.TestCase):
    """現象学的パレットのテストクラス"""
    
    def setUp(self):
        """テスト準備"""
        self.test_image = Image.new('RGB', (100, 100), color='green')
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_image_path = self.temp_dir / "palette_test.jpg"
        self.test_image.save(self.test_image_path)
    
    def tearDown(self):
        """クリーンアップ"""
        if self.test_image_path.exists():
            self.test_image_path.unlink()
        if self.temp_dir.exists():
            self.temp_dir.rmdir()
    
    def test_phenomenological_palette_class_exists(self):
        """RED: PhenomenologicalPaletteクラスが存在することを確認"""
        self.assertTrue(
            'PhenomenologicalPalette' in globals(),
            "PhenomenologicalPaletteクラスが存在しません"
        )
    
    def test_palette_has_27_dimensional_functions(self):
        """RED: パレットが27次元の関数を持つことを確認"""
        palette = PhenomenologicalPalette()
        
        # 9次元×3ノード=27の関数カテゴリが存在することを確認
        expected_dimensions = [
            'temporal', 'spatial', 'qualitative', 'embodied', 'conscious',
            'existential', 'relational', 'generative', 'expressive'
        ]
        
        for dimension in expected_dimensions:
            self.assertTrue(
                hasattr(palette, f'{dimension}_functions'),
                f"{dimension}次元の関数群が存在しません"
            )
    
    def test_execute_palette_operations(self):
        """RED: パレット操作の実行メソッドが存在し、画像を変換することを確認"""
        palette = PhenomenologicalPalette()
        
        test_operations = [
            {"function": "conscious_focus", "intensity": 0.8, "reason": "テスト用操作"},
            {"function": "temporal_echo", "intensity": 0.3, "reason": "テスト用操作"}
        ]
        
        result_image = palette.execute(str(self.test_image_path), test_operations)
        
        # 結果が画像であることを確認
        self.assertIsInstance(result_image, Image.Image, "実行結果が画像ではありません")
        self.assertEqual(result_image.size, self.test_image.size, "画像サイズが変更されています")


class TestCreativeResult(unittest.TestCase):
    """創造結果クラスのテスト"""
    
    def test_creative_result_class_exists(self):
        """RED: CreativeResultクラスが存在することを確認"""
        self.assertTrue(
            'CreativeResult' in globals(),
            "CreativeResultクラスが存在しません"
        )
    
    def test_creative_result_structure(self):
        """RED: CreativeResultが適切な構造を持つことを確認"""
        # テスト用データ
        test_image = Image.new('RGB', (50, 50), color='yellow')
        test_operations = [{"function": "test", "intensity": 0.5, "reason": "test"}]
        
        result = CreativeResult(
            original_image="test.jpg",
            created_image=test_image,
            operations=test_operations,
            philosophical_interpretation="テスト解釈",
            aesthetic_evaluation={"score": 8.5}
        )
        
        # 必要な属性が存在することを確認
        self.assertEqual(result.original_image, "test.jpg")
        self.assertEqual(result.created_image, test_image)
        self.assertEqual(result.operations, test_operations)
        self.assertEqual(result.philosophical_interpretation, "テスト解釈")
        self.assertEqual(result.aesthetic_evaluation, {"score": 8.5})


class TestAestheticMemory(unittest.TestCase):
    """美的記憶システムのテスト"""
    
    def test_aesthetic_memory_class_exists(self):
        """RED: AestheticMemoryクラスが存在することを確認"""
        self.assertTrue(
            'AestheticMemory' in globals(),
            "AestheticMemoryクラスが存在しません"
        )
    
    def test_aesthetic_memory_storage(self):
        """RED: 美的記憶の保存・取得機能を確認"""
        memory = AestheticMemory()
        
        test_evaluation = {
            "phenomenological_appropriateness": 8.5,
            "visual_harmony": 7.2,
            "creative_originality": 9.0,
            "improvement_suggestions": ["より深い時間性の表現", "空間的統合の改善"]
        }
        
        # 記憶の保存
        memory.store(test_evaluation)
        
        # 記憶の取得
        retrieved = memory.get_recent_evaluations(limit=1)
        self.assertEqual(len(retrieved), 1, "記憶が正しく保存・取得されていません")
        
        # タイムスタンプ以外の内容が正しいことを確認
        retrieved_without_timestamp = {k: v for k, v in retrieved[0].items() if k != 'timestamp'}
        self.assertEqual(retrieved_without_timestamp, test_evaluation, "保存された記憶が正しくありません")


if __name__ == '__main__':
    print("=" * 80)
    print("🎭 Phenomenological Autonomous Creative Apparatus")
    print("現象学的自律創造機構 - t-wada式TDD Red Phase")
    print("=" * 80)
    print()
    
    # テストを実行
    unittest.main(verbosity=2)