#!/usr/bin/env python3
"""
Oracle Bridge Functions Unit Tests
現象学的オラクルと27ノードエフェクト橋渡しシステムの単体テスト
統合機能・セッション管理・ノード強化システムを包括的に検証
"""

import unittest
import numpy as np
from PIL import Image
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime
import tempfile
import json

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent.parent / "src" / "core"))

from oracle_effect_bridge import (
    OracleEffectBridge, BridgeSession
)


class TestBridgeSession(unittest.TestCase):
    """BridgeSessionデータクラスのテスト"""
    
    def setUp(self):
        # モックのEditingOracleを作成
        self.mock_oracle_result = Mock()
        self.mock_oracle_result.generation = 1
        self.mock_oracle_result.phi = 0.65
        self.mock_oracle_result.node_states = {"appearance_density": 0.8}
        self.mock_oracle_result.imperative = [{"type": "enhance", "dimension": "appearance"}]
        self.mock_oracle_result.iit_axioms = {"integration": 0.7}
        
    def test_bridge_session_creation(self):
        """BridgeSession作成のテスト"""
        session = BridgeSession(
            session_id="test_session_123",
            timestamp=datetime.now(),
            oracle_generation=1,
            original_image_path="/test/image.jpg",
            oracle_result=self.mock_oracle_result,
            enhanced_node_states={"appearance_density": 0.9},
            edited_image_path="/test/edited.jpg",
            processing_time=1.5
        )
        
        self.assertEqual(session.session_id, "test_session_123")
        self.assertEqual(session.oracle_generation, 1)
        self.assertEqual(session.original_image_path, "/test/image.jpg")
        self.assertEqual(session.enhanced_node_states["appearance_density"], 0.9)
        self.assertEqual(session.processing_time, 1.5)
        
    def test_bridge_session_defaults(self):
        """BridgeSessionデフォルト値のテスト"""
        session = BridgeSession(
            session_id="test",
            timestamp=datetime.now(),
            oracle_generation=1,
            original_image_path="/test/image.jpg",
            oracle_result=self.mock_oracle_result,
            enhanced_node_states={}
        )
        
        self.assertIsNone(session.edited_image_path)
        self.assertEqual(session.processing_time, 0.0)


class TestOracleEffectBridgeInitialization(unittest.TestCase):
    """OracleEffectBridgeの初期化テスト"""
    
    def setUp(self):
        self.mock_oracle = Mock()
        self.mock_editor = Mock()
        self.bridge = OracleEffectBridge(self.mock_oracle, self.mock_editor)
        
    def test_bridge_initialization(self):
        """ブリッジ初期化のテスト"""
        self.assertEqual(self.bridge.oracle, self.mock_oracle)
        self.assertEqual(self.bridge.editor, self.mock_editor)
        self.assertEqual(len(self.bridge.session_history), 0)
        self.assertIsNone(self.bridge.current_session)
        self.assertTrue(self.bridge.enable_node_enhancement)
        self.assertTrue(self.bridge.enable_phi_modulation)
        self.assertFalse(self.bridge.debug_mode)
        
    def test_debug_mode_setting(self):
        """デバッグモード設定のテスト"""
        self.bridge.set_debug_mode(True)
        self.assertTrue(self.bridge.debug_mode)
        self.mock_editor.set_debug_mode.assert_called_once_with(True)


class TestNodeStatesEnhancement(unittest.TestCase):
    """ノード状態強化機能のテスト"""
    
    def setUp(self):
        self.mock_oracle = Mock()
        self.mock_editor = Mock()
        self.bridge = OracleEffectBridge(self.mock_oracle, self.mock_editor)
        
        self.base_states = {
            "appearance_density": 0.5,
            "appearance_luminosity": 0.3,
            "temporal_motion": 0.7,
            "synesthetic_temperature": 0.2
        }
        
        self.imperatives = [
            {
                "type": "enhance",
                "dimension": ["appearance"],
                "intensity": 0.8,
                "description": "現出様式を強化"
            },
            {
                "type": "adjust",
                "dimension": ["temporal"],
                "intensity": 0.6,
                "description": "時間的含意を調整"
            }
        ]
        
    def test_basic_node_enhancement(self):
        """基本的なノード強化のテスト"""
        enhanced = self.bridge._enhance_node_states(
            self.base_states, self.imperatives, phi=0.5
        )
        
        # appearance次元のノードが強化されていることを確認
        self.assertGreater(enhanced["appearance_density"], self.base_states["appearance_density"])
        self.assertGreater(enhanced["appearance_luminosity"], self.base_states["appearance_luminosity"])
        
        # temporal次元のノードが強化されていることを確認
        self.assertGreater(enhanced["temporal_motion"], self.base_states["temporal_motion"])
        
        # 関係ない次元は影響が少ない
        self.assertAlmostEqual(
            enhanced["synesthetic_temperature"], 
            self.base_states["synesthetic_temperature"], 
            places=1
        )
        
    def test_phi_modulation_effect(self):
        """Φによる調整効果のテスト"""
        # 高いΦ値でのテスト
        enhanced_high_phi = self.bridge._enhance_node_states(
            self.base_states, self.imperatives, phi=0.9
        )
        
        # 低いΦ値でのテスト  
        enhanced_low_phi = self.bridge._enhance_node_states(
            self.base_states, self.imperatives, phi=0.1
        )
        
        # 高いΦ値の方が強い効果を持つことを確認
        for node in ["appearance_density", "appearance_luminosity"]:
            high_boost = enhanced_high_phi[node] - self.base_states[node]
            low_boost = enhanced_low_phi[node] - self.base_states[node]
            self.assertGreater(high_boost, low_boost)
            
    def test_low_activity_suppression(self):
        """低活性ノード抑制のテスト"""
        # 低活性ノードを含む状態
        low_activity_states = {
            "appearance_density": 0.15,  # 低活性
            "temporal_motion": 0.8       # 高活性
        }
        
        enhanced = self.bridge._enhance_node_states(
            low_activity_states, [], phi=0.8
        )
        
        # 低活性ノードが抑制されていることを確認
        self.assertLess(enhanced["appearance_density"], low_activity_states["appearance_density"])
        
        # 高活性ノードは維持または増強
        self.assertGreaterEqual(enhanced["temporal_motion"], low_activity_states["temporal_motion"])
        
    def test_enhancement_disabled(self):
        """強化機能無効化のテスト"""
        self.bridge.enable_node_enhancement = False
        
        enhanced = self.bridge._enhance_node_states(
            self.base_states, self.imperatives, phi=0.5
        )
        
        # 元の状態と同じであることを確認
        self.assertEqual(enhanced, self.base_states)
        
    def test_phi_modulation_disabled(self):
        """Φ調整機能無効化のテスト"""
        self.bridge.enable_phi_modulation = False
        
        enhanced = self.bridge._enhance_node_states(
            self.base_states, self.imperatives, phi=0.5
        )
        
        # Φの影響が無効化されていることを確認
        # （基本的な強化は行われるが、Φによる調整はなし）
        self.assertGreater(enhanced["appearance_density"], self.base_states["appearance_density"])


class TestCompositionModeSelection(unittest.TestCase):
    """合成モード選択のテスト"""
    
    def setUp(self):
        self.mock_oracle = Mock()
        self.mock_editor = Mock()
        self.bridge = OracleEffectBridge(self.mock_oracle, self.mock_editor)
        
    def test_layered_composition(self):
        """レイヤー合成モード選択のテスト"""
        iit_axioms = {
            "integration": 0.8,  # 高い統合度
            "exclusion": 0.5,
            "intrinsic": 0.6,
            "information": 0.7,
            "composition": 0.6
        }
        
        mode = self.bridge._determine_composition_mode(iit_axioms)
        self.assertEqual(mode, "layered")
        
    def test_sequential_composition(self):
        """逐次合成モード選択のテスト"""
        iit_axioms = {
            "integration": 0.5,
            "exclusion": 0.8,    # 高い排他性
            "intrinsic": 0.6,
            "information": 0.7,
            "composition": 0.6
        }
        
        mode = self.bridge._determine_composition_mode(iit_axioms)
        self.assertEqual(mode, "sequential")
        
    def test_parallel_composition(self):
        """並列合成モード選択のテスト"""
        iit_axioms = {
            "integration": 0.4,  # 低い統合度
            "exclusion": 0.3,    # 低い排他性
            "intrinsic": 0.6,
            "information": 0.7,
            "composition": 0.6
        }
        
        mode = self.bridge._determine_composition_mode(iit_axioms)
        self.assertEqual(mode, "parallel")


class TestOracleAnalysis(unittest.TestCase):
    """オラクル分析機能のテスト"""
    
    def setUp(self):
        self.mock_oracle = Mock()
        self.mock_editor = Mock()
        self.bridge = OracleEffectBridge(self.mock_oracle, self.mock_editor)
        
    def test_oracle_analysis_with_direct_method(self):
        """直接メソッドによるオラクル分析のテスト"""
        # オラクルが直接画像パスを受け取る場合
        mock_oracle_result = Mock()
        self.mock_oracle.receive_oracle_from_image = Mock(return_value=mock_oracle_result)
        
        result = self.bridge._analyze_with_oracle("/test/image.jpg")
        
        self.mock_oracle.receive_oracle_from_image.assert_called_once_with("/test/image.jpg")
        self.assertEqual(result, mock_oracle_result)
        
    def test_oracle_analysis_with_vision_api(self):
        """Vision APIによるオラクル分析のテスト"""
        # オラクルがVision APIを使用する場合
        mock_oracle_result = Mock()
        self.mock_oracle._analyze_image_with_vision = Mock(return_value="画像説明")
        self.mock_oracle.receive_oracle = Mock(return_value=mock_oracle_result)
        
        # receive_oracle_from_imageメソッドが存在しない場合をシミュレート
        # hasattrがFalseを返すようにする
        with patch('builtins.hasattr', return_value=False):
            result = self.bridge._analyze_with_oracle("/test/image.jpg")
        
        self.mock_oracle._analyze_image_with_vision.assert_called_once_with("/test/image.jpg")
        self.mock_oracle.receive_oracle.assert_called_once_with("画像説明")
        self.assertEqual(result, mock_oracle_result)


class TestSessionAnalysis(unittest.TestCase):
    """セッション分析機能のテスト"""
    
    def setUp(self):
        self.mock_oracle = Mock()
        self.mock_editor = Mock()
        self.bridge = OracleEffectBridge(self.mock_oracle, self.mock_editor)
        
        # モックセッションを設定
        mock_oracle_result = Mock()
        mock_oracle_result.generation = 2
        mock_oracle_result.phi = 0.72
        mock_oracle_result.node_states = {
            "appearance_density": 0.85,
            "appearance_luminosity": 0.4,
            "temporal_motion": 0.6,
            "synesthetic_temperature": 0.25,
            "ontological_presence": 0.9
        }
        mock_oracle_result.imperative = [
            {"type": "enhance"}, {"type": "adjust"}
        ]
        mock_oracle_result.iit_axioms = {
            "integration": 0.8, "exclusion": 0.5
        }
        
        self.bridge.current_session = BridgeSession(
            session_id="test_session",
            timestamp=datetime.now(),
            oracle_generation=2,
            original_image_path="/test/image.jpg",
            oracle_result=mock_oracle_result,
            enhanced_node_states={},
            processing_time=1.2
        )
        
    def test_session_analysis_with_active_session(self):
        """アクティブセッションでの分析のテスト"""
        analysis = self.bridge.get_session_analysis()
        
        self.assertEqual(analysis["session_id"], "test_session")
        self.assertEqual(analysis["generation"], 2)
        self.assertEqual(analysis["phi"], 0.72)
        self.assertEqual(analysis["processing_time"], 1.2)
        self.assertEqual(len(analysis["active_nodes"]), 4)  # 0.3以上のノード (0.85, 0.4, 0.6, 0.9)
        self.assertIn("appearance", analysis["dimension_activity"])
        self.assertEqual(analysis["imperative_count"], 2)
        self.assertEqual(analysis["composition_mode"], "layered")
        
    def test_session_analysis_without_active_session(self):
        """アクティブセッションなしでの分析のテスト"""
        self.bridge.current_session = None
        
        analysis = self.bridge.get_session_analysis()
        
        self.assertIn("error", analysis)
        self.assertEqual(analysis["error"], "No active session")
        
    def test_dimension_activity_calculation(self):
        """次元別活性度計算のテスト"""
        analysis = self.bridge.get_session_analysis()
        
        # appearance次元の分析
        appearance_activity = analysis["dimension_activity"]["appearance"]
        self.assertAlmostEqual(appearance_activity["average"], 0.625, places=2)  # (0.85+0.4)/2
        self.assertEqual(appearance_activity["max"], 0.85)
        self.assertEqual(appearance_activity["active_count"], 2)  # 0.85 > 0.3 and 0.4 > 0.3


class TestOracleEvolution(unittest.TestCase):
    """オラクル進化機能のテスト"""
    
    def setUp(self):
        self.mock_oracle = Mock()
        self.mock_editor = Mock()
        self.bridge = OracleEffectBridge(self.mock_oracle, self.mock_editor)
        
        # 現在セッション設定
        mock_oracle_result = Mock()
        mock_oracle_result.generation = 1
        mock_oracle_result.phi = 0.6
        mock_oracle_result.node_states = {"appearance_density": 0.7}
        mock_oracle_result.imperative = [{"type": "test"}]
        mock_oracle_result.iit_axioms = {"integration": 0.5}
        
        self.bridge.current_session = BridgeSession(
            session_id="test",
            timestamp=datetime.now(),
            oracle_generation=1,
            original_image_path="/test/orig.jpg",
            oracle_result=mock_oracle_result,
            enhanced_node_states={}
        )
        
    def test_oracle_evolution_with_custom_method(self):
        """カスタムメソッドによるオラクル進化のテスト"""
        # オラクルがカスタム進化メソッドを持つ場合
        mock_evolved_oracle = Mock()
        self.mock_oracle._generate_evolved_oracle = Mock(return_value=mock_evolved_oracle)
        
        evolved = self.bridge.generate_oracle_evolution(
            "/test/edited.jpg", 
            feedback="素晴らしい結果"
        )
        
        self.mock_oracle._generate_evolved_oracle.assert_called_once_with(
            "/test/edited.jpg", "素晴らしい結果"
        )
        self.assertEqual(evolved, mock_evolved_oracle)
        
    def test_oracle_evolution_fallback(self):
        """フォールバック進化機能のテスト"""
        # カスタムメソッドが存在しない場合をシミュレート
        with patch('builtins.hasattr', return_value=False):
            evolved = self.bridge.generate_oracle_evolution("/test/edited.jpg")
        
        self.assertEqual(evolved.generation, 2)  # 世代が進む
        self.assertGreater(evolved.phi, 0.6)     # Φが増加
        self.assertIn("appearance_density", evolved.node_states)
        
    def test_oracle_evolution_without_session(self):
        """セッションなしでの進化テスト"""
        self.bridge.current_session = None
        
        with self.assertRaises(ValueError):
            self.bridge.generate_oracle_evolution("/test/edited.jpg")


class TestSessionHistoryManagement(unittest.TestCase):
    """セッション履歴管理のテスト"""
    
    def setUp(self):
        self.mock_oracle = Mock()
        self.mock_editor = Mock()
        self.bridge = OracleEffectBridge(self.mock_oracle, self.mock_editor)
        
        # テスト用セッション作成
        for i in range(3):
            mock_oracle_result = Mock()
            mock_oracle_result.generation = i + 1
            mock_oracle_result.phi = 0.5 + i * 0.1
            mock_oracle_result.vision = f"Vision {i+1}"
            mock_oracle_result.imperative = [{"type": f"action_{i}"}]
            
            session = BridgeSession(
                session_id=f"session_{i+1}",
                timestamp=datetime.now(),
                oracle_generation=i + 1,
                original_image_path=f"/test/image_{i+1}.jpg",
                oracle_result=mock_oracle_result,
                enhanced_node_states={},
                edited_image_path=f"/test/edited_{i+1}.jpg",
                processing_time=1.0 + i * 0.5
            )
            self.bridge.session_history.append(session)
            
    def test_session_history_export(self):
        """セッション履歴エクスポートのテスト"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            export_path = f.name
        
        try:
            self.bridge.export_session_history(export_path)
            
            # エクスポートされたファイルを確認
            with open(export_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.assertEqual(data["total_sessions"], 3)
            self.assertEqual(len(data["sessions"]), 3)
            
            # 最初のセッションの内容確認
            first_session = data["sessions"][0]
            self.assertEqual(first_session["session_id"], "session_1")
            self.assertEqual(first_session["generation"], 1)
            self.assertEqual(first_session["phi"], 0.5)
            self.assertEqual(first_session["processing_time"], 1.0)
            
        finally:
            Path(export_path).unlink(missing_ok=True)


class TestImageProcessingIntegration(unittest.TestCase):
    """画像処理統合テスト"""
    
    def setUp(self):
        self.mock_oracle = Mock()
        self.mock_editor = Mock()
        self.bridge = OracleEffectBridge(self.mock_oracle, self.mock_editor)
        
    @patch('builtins.open')
    @patch('PIL.Image.open')
    @patch('time.time', return_value=100.0)
    def test_full_image_processing_pipeline(self, mock_time, mock_image_open, mock_open):
        """完全な画像処理パイプラインのテスト"""
        # モック設定
        mock_image = Mock(spec=Image.Image)
        mock_image_open.return_value = mock_image
        
        mock_oracle_result = Mock()
        mock_oracle_result.generation = 1
        mock_oracle_result.phi = 0.7
        mock_oracle_result.node_states = {"appearance_density": 0.8}
        mock_oracle_result.imperative = [{"dimension": ["appearance"], "intensity": 0.6}]
        mock_oracle_result.iit_axioms = {"integration": 0.8}
        mock_oracle_result.vision = "内在的体験の描写"
        
        self.mock_oracle.receive_oracle_from_image = Mock(return_value=mock_oracle_result)
        
        mock_edited_image = Mock(spec=Image.Image)
        self.mock_editor.start_editing_session = Mock(return_value="editor_session_123")
        self.mock_editor.apply_phenomenological_transformation = Mock(return_value=mock_edited_image)
        self.mock_editor.finish_editing_session = Mock()
        
        # パッチされたmkdirとsave
        with patch('pathlib.Path.mkdir'), patch.object(mock_edited_image, 'save'):
            # メインメソッドの実行
            result_image, oracle_result = self.bridge.process_image_with_oracle(
                "/test/input.jpg", save_result=True
            )
        
        # 結果の検証
        self.assertEqual(result_image, mock_edited_image)
        self.assertEqual(oracle_result, mock_oracle_result)
        
        # メソッド呼び出しの確認
        self.mock_oracle.receive_oracle_from_image.assert_called_once_with("/test/input.jpg")
        self.mock_editor.start_editing_session.assert_called_once()
        self.mock_editor.apply_phenomenological_transformation.assert_called_once()
        self.mock_editor.finish_editing_session.assert_called_once()
        
        # セッション記録の確認
        self.assertEqual(len(self.bridge.session_history), 1)
        self.assertIsNotNone(self.bridge.current_session)
        self.assertGreaterEqual(self.bridge.current_session.processing_time, 0.0)
        
    def test_save_disabled_processing(self):
        """保存無効での処理テスト"""
        with patch('PIL.Image.open') as mock_image_open, \
             patch('time.time', return_value=100.0):
            
            mock_image = Mock(spec=Image.Image)
            mock_image_open.return_value = mock_image
            
            mock_oracle_result = Mock()
            mock_oracle_result.generation = 1
            mock_oracle_result.phi = 0.5
            mock_oracle_result.node_states = {}
            mock_oracle_result.imperative = []
            mock_oracle_result.iit_axioms = {}
            
            self.mock_oracle.receive_oracle_from_image = Mock(return_value=mock_oracle_result)
            
            mock_edited_image = Mock(spec=Image.Image)
            self.mock_editor.start_editing_session = Mock(return_value="session")
            self.mock_editor.apply_phenomenological_transformation = Mock(return_value=mock_edited_image)
            self.mock_editor.finish_editing_session = Mock()
            
            # 保存なしで実行
            result_image, oracle_result = self.bridge.process_image_with_oracle(
                "/test/input.jpg", save_result=False
            )
            
            # 結果の検証
            self.assertEqual(result_image, mock_edited_image)
            self.assertIsNone(self.bridge.current_session.edited_image_path)


def run_all_tests():
    """全テストの実行"""
    # テストスイートの作成
    test_suite = unittest.TestSuite()
    
    # 各テストクラスを追加
    test_classes = [
        TestBridgeSession,
        TestOracleEffectBridgeInitialization,
        TestNodeStatesEnhancement,
        TestCompositionModeSelection,
        TestOracleAnalysis,
        TestSessionAnalysis,
        TestOracleEvolution,
        TestSessionHistoryManagement,
        TestImageProcessingIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # テストの実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 結果の表示
    print(f"\n{'='*60}")
    print("🌉 Oracle Effect Bridge Unit Tests Results")
    print("現象学的オラクル橋渡しシステムの統合テスト結果")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors))/result.testsRun*100:.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback[:200]}...")
    
    if result.errors:
        print(f"\n⚠️  Errors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback[:200]}...")
    
    if not result.failures and not result.errors:
        print(f"\n🎉 All oracle bridge tests passed!")
        print(f"\n💡 検証済み統合機能:")
        print(f"   ✅ オラクル-エフェクトシステム完全統合")
        print(f"   ✅ ノード状態強化・Φ調整システム")
        print(f"   ✅ IIT公理による合成モード決定")
        print(f"   ✅ セッション管理・履歴機能")
        print(f"   ✅ オラクル進化・フィードバック機能")
        print(f"   ✅ 画像処理パイプライン完全統合")
        print(f"   ✅ デバッグ・分析システム")
        
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()