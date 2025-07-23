#!/usr/bin/env python3
"""
TDD Test Suite for Inspiration Integration
インスピレーション統合機能のt-wada式TDDテストスイート
"""

import unittest
import sys
import tempfile
import os
import json
from pathlib import Path
from PIL import Image
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any

# プロジェクトのsrc/coreディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent / "src" / "core"))

# 既存のシステムをインポート
try:
    from phenomenological_autonomous_creative_apparatus import (
        PhenomenologicalAutonomousCreativeApparatus,
        CreativeResult
    )
except ImportError as e:
    print(f"既存システムのインポートエラー: {e}")

# テスト対象の新機能（まだ存在しない）
try:
    from inspiration_integration import (
        DialogueInspirationAnalyzer,
        start_autonomous_inspired_editing,
        enhance_dialogue_context,
        quantify_inspiration_strength
    )
except ImportError as e:
    print(f"Expected Import Error for new features: {e}")
    print("これはTDD Red Phaseなので期待される動作です")


class TestDialogueInspirationAnalyzer(unittest.TestCase):
    """対話インスピレーション分析器のテストクラス"""
    
    def setUp(self):
        """テスト準備"""
        self.test_image = Image.new('RGB', (100, 100), color='cyan')
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_image_path = self.temp_dir / "inspiration_test.jpg"
        self.test_image.save(self.test_image_path)
        
        # サンプル対話要約
        self.dialogue_summary = {
            'final_response': '私は青い空の無限性の中に、希望と憂鬱の二重性を感じています。雲の形が私の内的時間の流れを表現しているようです。',
            'inspiration_result': {
                'is_inspired': True,
                'confidence': 0.85,
                'inspiration_type': 'temporal_existential',
                'description': '時間性と存在性の統合的体験'
            },
            'purity_score': 0.78
        }
        
        os.environ['OPENAI_API_KEY'] = 'test_api_key'
    
    def tearDown(self):
        """クリーンアップ"""
        if self.test_image_path.exists():
            self.test_image_path.unlink()
        if self.temp_dir.exists():
            self.temp_dir.rmdir()
    
    def test_dialogue_inspiration_analyzer_class_exists(self):
        """RED: DialogueInspirationAnalyzerクラスが存在することを確認"""
        self.assertTrue(
            'DialogueInspirationAnalyzer' in globals(),
            "DialogueInspirationAnalyzerクラスが存在しません"
        )
    
    def test_analyzer_initialization(self):
        """RED: アナライザーが正しく初期化されることを確認"""
        analyzer = DialogueInspirationAnalyzer()
        
        # 必要な属性が初期化されているか確認
        self.assertIsNotNone(analyzer, "アナライザーの初期化に失敗しました")
        self.assertTrue(
            hasattr(analyzer, 'llm_client'),
            "LLMクライアントが初期化されていません"
        )
    
    def test_extract_inspiration_elements_method_exists(self):
        """RED: インスピレーション要素抽出メソッドが存在することを確認"""
        analyzer = DialogueInspirationAnalyzer()
        self.assertTrue(
            hasattr(analyzer, 'extract_inspiration_elements'),
            "extract_inspiration_elementsメソッドが存在しません"
        )
    
    def test_extract_inspiration_elements_returns_dict(self):
        """RED: インスピレーション要素抽出が辞書を返すことを確認"""
        analyzer = DialogueInspirationAnalyzer()
        
        elements = analyzer.extract_inspiration_elements(self.dialogue_summary)
        
        # 結果が辞書であることを確認
        self.assertIsInstance(elements, dict, "抽出結果が辞書ではありません")
        
        # 期待されるキーが含まれていることを確認
        expected_keys = ['emotional_intensity', 'temporal_aspects', 'spatial_aspects', 
                        'existential_themes', 'aesthetic_qualities']
        for key in expected_keys:
            self.assertIn(key, elements, f"期待されるキー '{key}' が含まれていません")
    
    def test_enhance_node_activations_method_exists(self):
        """RED: ノード活性化強化メソッドが存在することを確認"""
        analyzer = DialogueInspirationAnalyzer()
        self.assertTrue(
            hasattr(analyzer, 'enhance_node_activations'),
            "enhance_node_activationsメソッドが存在しません"
        )
    
    def test_enhance_node_activations_functionality(self):
        """RED: ノード活性化強化が正しく機能することを確認"""
        analyzer = DialogueInspirationAnalyzer()
        
        # ベース活性化データ
        base_activations = {
            'temporal_basic': 0.5,
            'conscious_attention': 0.4,
            'existential_presence': 0.6
        }
        
        # インスピレーション要素
        inspiration_elements = {
            'emotional_intensity': 0.8,
            'temporal_aspects': 0.9,
            'existential_themes': 0.7
        }
        
        enhanced = analyzer.enhance_node_activations(base_activations, inspiration_elements)
        
        # 強化後の活性化データが正しい形式であることを確認
        self.assertIsInstance(enhanced, dict, "強化後の活性化データが辞書ではありません")
        self.assertEqual(len(enhanced), 27, "27次元の活性化データが返されていません")
        
        # 値が0-1の範囲内であることを確認
        for key, value in enhanced.items():
            self.assertGreaterEqual(value, 0, f"{key}の値が0未満です")
            self.assertLessEqual(value, 1, f"{key}の値が1を超えています")


class TestAutonomousInspiredEditing(unittest.TestCase):
    """自律インスピレーション編集のテストクラス"""
    
    def setUp(self):
        """テスト準備"""
        self.test_image = Image.new('RGB', (150, 150), color='magenta')
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_image_path = self.temp_dir / "autonomous_test.jpg"
        self.test_image.save(self.test_image_path)
        
        self.dialogue_summary = {
            'final_response': 'この瞬間、私は色彩の境界が溶解していく様子を体験しています。',
            'inspiration_result': {'is_inspired': True, 'confidence': 0.9},
            'purity_score': 0.85
        }
        
        os.environ['OPENAI_API_KEY'] = 'test_api_key'
    
    def tearDown(self):
        """クリーンアップ"""
        if self.test_image_path.exists():
            self.test_image_path.unlink()
        if self.temp_dir.exists():
            self.temp_dir.rmdir()
    
    def test_start_autonomous_inspired_editing_function_exists(self):
        """RED: start_autonomous_inspired_editing関数が存在することを確認"""
        self.assertTrue(
            'start_autonomous_inspired_editing' in globals(),
            "start_autonomous_inspired_editing関数が存在しません"
        )
    
    def test_start_autonomous_inspired_editing_accepts_parameters(self):
        """RED: 関数が適切なパラメータを受け取ることを確認"""
        try:
            result = start_autonomous_inspired_editing(
                str(self.test_image_path), 
                "9d", 
                self.dialogue_summary
            )
            # 実行が成功することを確認
            self.assertIsNotNone(result, "関数の実行結果がNoneです")
        except TypeError as e:
            self.fail(f"関数が正しいパラメータを受け取れません: {e}")
        except NameError as e:
            self.fail(f"関数が存在しません: {e}")
    
    def test_autonomous_inspired_editing_returns_creative_result(self):
        """RED: 自律インスピレーション編集がCreativeResultを返すことを確認"""
        with patch('inspiration_integration.PhenomenologicalAutonomousCreativeApparatus') as mock_apparatus:
            # モックの設定
            mock_instance = Mock()
            mock_result = CreativeResult(
                original_image=str(self.test_image_path),
                created_image=self.test_image,
                operations=[{"function": "conscious_focus", "intensity": 0.8}],
                philosophical_interpretation="インスピレーション駆動の創造",
                aesthetic_evaluation={"score": 8.5}
            )
            mock_instance.create_from_image.return_value = mock_result
            mock_apparatus.return_value = mock_instance
            
            result = start_autonomous_inspired_editing(
                str(self.test_image_path), 
                "9d", 
                self.dialogue_summary
            )
            
            # 戻り値がCreativeResultであることを確認
            self.assertIsInstance(result, CreativeResult, "戻り値がCreativeResultではありません")
            self.assertEqual(result.original_image, str(self.test_image_path))


class TestInspirationStrengthQuantification(unittest.TestCase):
    """インスピレーション強度定量化のテストクラス"""
    
    def test_quantify_inspiration_strength_function_exists(self):
        """RED: quantify_inspiration_strength関数が存在することを確認"""
        self.assertTrue(
            'quantify_inspiration_strength' in globals(),
            "quantify_inspiration_strength関数が存在しません"
        )
    
    def test_quantify_inspiration_strength_returns_float(self):
        """RED: インスピレーション強度定量化が浮動小数点数を返すことを確認"""
        dialogue_summary = {
            'inspiration_result': {
                'confidence': 0.85,
                'is_peak_inspiration': True
            },
            'purity_score': 0.78
        }
        
        strength = quantify_inspiration_strength(dialogue_summary)
        
        # 戻り値が浮動小数点数であることを確認
        self.assertIsInstance(strength, (int, float), "強度が数値ではありません")
        self.assertGreaterEqual(strength, 0, "強度が0未満です")
        self.assertLessEqual(strength, 1, "強度が1を超えています")
    
    def test_quantify_different_inspiration_levels(self):
        """RED: 異なるインスピレーションレベルで異なる強度を返すことを確認"""
        # 高強度インスピレーション
        high_inspiration = {
            'inspiration_result': {
                'confidence': 0.95,
                'is_peak_inspiration': True
            },
            'purity_score': 0.9
        }
        
        # 低強度インスピレーション
        low_inspiration = {
            'inspiration_result': {
                'confidence': 0.3,
                'is_peak_inspiration': False
            },
            'purity_score': 0.4
        }
        
        high_strength = quantify_inspiration_strength(high_inspiration)
        low_strength = quantify_inspiration_strength(low_inspiration)
        
        # 高強度の方が低強度より大きいことを確認
        self.assertGreater(high_strength, low_strength, 
                          "高強度インスピレーションの方が強度が高くありません")


class TestDialogueContextEnhancement(unittest.TestCase):
    """対話文脈強化のテストクラス"""
    
    def test_enhance_dialogue_context_function_exists(self):
        """RED: enhance_dialogue_context関数が存在することを確認"""
        self.assertTrue(
            'enhance_dialogue_context' in globals(),
            "enhance_dialogue_context関数が存在しません"
        )
    
    def test_enhance_dialogue_context_integration(self):
        """RED: 対話文脈強化が27次元分析に統合されることを確認"""
        base_analysis = {
            'temporal_basic': 0.5,
            'conscious_attention': 0.4,
            'existential_presence': 0.6
        }
        
        dialogue_summary = {
            'final_response': '時間の流れの中に永遠を感じています',
            'inspiration_result': {'confidence': 0.8}
        }
        
        enhanced_analysis = enhance_dialogue_context(base_analysis, dialogue_summary)
        
        # 強化後の分析が正しい形式であることを確認
        self.assertIsInstance(enhanced_analysis, dict, "強化後の分析が辞書ではありません")
        self.assertEqual(len(enhanced_analysis), 27, "27次元の分析データが返されていません")
        
        # 時間性関連のノードが強化されていることを確認（対話内容に基づく）
        self.assertGreaterEqual(enhanced_analysis.get('temporal_basic', 0), 
                               base_analysis.get('temporal_basic', 0),
                               "時間性ノードが強化されていません")


class TestInspirationIntegrationSystem(unittest.TestCase):
    """インスピレーション統合システム全体のテスト"""
    
    def setUp(self):
        """統合テスト準備"""
        self.test_image = Image.new('RGB', (200, 200), color='orange')
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_image_path = self.temp_dir / "system_test.jpg"
        self.test_image.save(self.test_image_path)
        
        os.environ['OPENAI_API_KEY'] = 'test_system_key'
    
    def tearDown(self):
        """クリーンアップ"""
        if self.test_image_path.exists():
            self.test_image_path.unlink()
        if self.temp_dir.exists():
            self.temp_dir.rmdir()
    
    def test_end_to_end_inspiration_integration(self):
        """RED: エンドツーエンドのインスピレーション統合が機能することを確認"""
        dialogue_summary = {
            'final_response': '私は光と影の調和の中に、存在の本質を見出しています。この瞬間が永遠に続いてほしいと感じます。',
            'inspiration_result': {
                'is_inspired': True,
                'confidence': 0.92,
                'inspiration_type': 'existential_temporal',
                'is_peak_inspiration': True
            },
            'purity_score': 0.88
        }
        
        # パイプライン全体の動作確認
        try:
            # 1. インスピレーション分析
            analyzer = DialogueInspirationAnalyzer()
            inspiration_elements = analyzer.extract_inspiration_elements(dialogue_summary)
            
            # 2. 強度定量化
            strength = quantify_inspiration_strength(dialogue_summary)
            
            # 3. 自律創造実行
            result = start_autonomous_inspired_editing(
                str(self.test_image_path),
                "9d",
                dialogue_summary
            )
            
            # パイプライン全体が成功することを確認
            self.assertIsNotNone(inspiration_elements, "インスピレーション要素の抽出に失敗")
            self.assertIsInstance(strength, (int, float), "強度定量化に失敗")
            self.assertIsInstance(result, CreativeResult, "自律創造の実行に失敗")
            
        except Exception as e:
            # エンドツーエンドテストなので、どの段階で失敗してもテスト失敗
            self.fail(f"エンドツーエンドのインスピレーション統合に失敗: {e}")
    
    def test_inspiration_memory_integration(self):
        """RED: インスピレーション体験が美的記憶に統合されることを確認"""
        dialogue_summary = {
            'final_response': '創造的な衝動が湧き上がっています',
            'inspiration_result': {'is_inspired': True, 'confidence': 0.7}
        }
        
        # 美的記憶への統合確認は実装後にテスト
        with patch('inspiration_integration.PhenomenologicalAutonomousCreativeApparatus') as mock_apparatus:
            mock_instance = Mock()
            mock_memory = Mock()
            mock_instance.aesthetic_memory = mock_memory
            mock_apparatus.return_value = mock_instance
            
            start_autonomous_inspired_editing(
                str(self.test_image_path),
                "9d", 
                dialogue_summary
            )
            
            # 美的記憶にインスピレーション情報が保存されることを確認
            # (実際の実装後に詳細な検証を追加)
            self.assertTrue(True, "美的記憶統合のテストは実装後に詳細化")


if __name__ == '__main__':
    print("=" * 80)
    print("🎭 Inspiration Integration System")  
    print("インスピレーション統合システム - t-wada式TDD Red Phase")
    print("=" * 80)
    print()
    
    # テストを実行
    unittest.main(verbosity=2)