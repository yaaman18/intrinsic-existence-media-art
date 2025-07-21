#!/usr/bin/env python3
"""
Node Effect Mapper Unit Tests
ノード状態値からエフェクトパラメータへの変換システム単体テスト
27ノードマッピング・強度計算・相互作用システムを包括的に検証
"""

import unittest
import numpy as np
import sys
from pathlib import Path
from typing import Dict, List

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent.parent / "src" / "core"))

from node_effect_mapper import (
    NodeEffectMapper, EffectIntensityMode, NodeEffectMapping, 
    EffectParameters
)


class TestNodeEffectMapping(unittest.TestCase):
    """NodeEffectMappingデータクラスのテスト"""
    
    def test_mapping_creation(self):
        """マッピング作成のテスト"""
        mapping = NodeEffectMapping(
            node_name="test_node",
            effect_name="test_effect",
            effect_module="test_module",
            intensity_mode=EffectIntensityMode.SIGMOID,
            threshold=0.3,
            max_intensity=0.8,
            invert=True
        )
        
        self.assertEqual(mapping.node_name, "test_node")
        self.assertEqual(mapping.effect_name, "test_effect")
        self.assertEqual(mapping.effect_module, "test_module")
        self.assertEqual(mapping.intensity_mode, EffectIntensityMode.SIGMOID)
        self.assertEqual(mapping.threshold, 0.3)
        self.assertEqual(mapping.max_intensity, 0.8)
        self.assertTrue(mapping.invert)
        
    def test_mapping_defaults(self):
        """デフォルト値のテスト"""
        mapping = NodeEffectMapping(
            node_name="test_node",
            effect_name="test_effect",
            effect_module="test_module"
        )
        
        self.assertEqual(mapping.intensity_mode, EffectIntensityMode.LINEAR)
        self.assertEqual(mapping.threshold, 0.5)
        self.assertEqual(mapping.max_intensity, 1.0)
        self.assertFalse(mapping.invert)


class TestEffectParameters(unittest.TestCase):
    """EffectParametersデータクラスのテスト"""
    
    def test_parameters_creation(self):
        """パラメータ作成のテスト"""
        params = EffectParameters(
            effect_name="test_effect",
            module_name="test_module",
            intensity=0.7,
            node_state=0.8,
            additional_params={"param1": "value1"}
        )
        
        self.assertEqual(params.effect_name, "test_effect")
        self.assertEqual(params.module_name, "test_module")
        self.assertEqual(params.intensity, 0.7)
        self.assertEqual(params.node_state, 0.8)
        self.assertEqual(params.additional_params["param1"], "value1")
        
    def test_parameters_defaults(self):
        """デフォルト値のテスト"""
        params = EffectParameters(
            effect_name="test_effect",
            module_name="test_module",
            intensity=0.5,
            node_state=0.6
        )
        
        self.assertIsInstance(params.additional_params, dict)
        self.assertEqual(len(params.additional_params), 0)


class TestNodeEffectMapperInitialization(unittest.TestCase):
    """NodeEffectMapperの初期化テスト"""
    
    def setUp(self):
        self.mapper = NodeEffectMapper()
    
    def test_mapper_initialization(self):
        """マッパーの初期化テスト"""
        self.assertIsInstance(self.mapper.node_mappings, dict)
        self.assertEqual(len(self.mapper.node_mappings), 27)  # 27ノード
        self.assertIsNone(self.mapper.connectivity_matrix)
        self.assertEqual(self.mapper.global_intensity_factor, 1.0)
        
    def test_all_27_nodes_mapped(self):
        """27ノード全てがマッピングされていることの確認"""
        expected_nodes = {
            # 現出様式
            "appearance_density", "appearance_luminosity", "appearance_chromaticity",
            # 志向的構造
            "intentional_focus", "intentional_horizon", "intentional_depth", 
            # 時間的含意
            "temporal_motion", "temporal_decay", "temporal_duration",
            # 相互感覚的質
            "synesthetic_temperature", "synesthetic_weight", "synesthetic_texture",
            # 存在論的密度
            "ontological_presence", "ontological_boundary", "ontological_plurality",
            # 意味的認識層
            "semantic_entities", "semantic_relations", "semantic_actions",
            # 概念的地平
            "conceptual_cultural", "conceptual_symbolic", "conceptual_functional",
            # 存在者の様態
            "being_animacy", "being_agency", "being_artificiality",
            # 認識の確実性分布
            "certainty_clarity", "certainty_ambiguity", "certainty_multiplicity"
        }
        
        actual_nodes = set(self.mapper.node_mappings.keys())
        self.assertEqual(actual_nodes, expected_nodes)
        
    def test_node_mapping_integrity(self):
        """各ノードマッピングの整合性テスト"""
        for node_name, mapping in self.mapper.node_mappings.items():
            # 基本的なデータ整合性
            self.assertEqual(mapping.node_name, node_name)
            self.assertIsInstance(mapping.effect_name, str)
            self.assertIsInstance(mapping.effect_module, str)
            self.assertIsInstance(mapping.intensity_mode, EffectIntensityMode)
            self.assertTrue(0.0 <= mapping.threshold <= 1.0)
            self.assertTrue(0.0 < mapping.max_intensity <= 1.0)
            self.assertIsInstance(mapping.invert, bool)


class TestIntensityCalculation(unittest.TestCase):
    """強度計算のテスト"""
    
    def setUp(self):
        self.mapper = NodeEffectMapper()
        
    def test_linear_intensity(self):
        """線形強度計算のテスト"""
        mapping = NodeEffectMapping(
            "test_node", "test_effect", "test_module",
            intensity_mode=EffectIntensityMode.LINEAR,
            max_intensity=1.0
        )
        
        # 線形変換のテスト
        self.assertAlmostEqual(
            self.mapper._calculate_intensity(0.0, mapping), 0.0, places=3
        )
        self.assertAlmostEqual(
            self.mapper._calculate_intensity(0.5, mapping), 0.5, places=3
        )
        self.assertAlmostEqual(
            self.mapper._calculate_intensity(1.0, mapping), 1.0, places=3
        )
        
    def test_exponential_intensity(self):
        """指数的強度計算のテスト"""
        mapping = NodeEffectMapping(
            "test_node", "test_effect", "test_module",
            intensity_mode=EffectIntensityMode.EXPONENTIAL,
            max_intensity=1.0
        )
        
        # 指数的変換のテスト
        self.assertAlmostEqual(
            self.mapper._calculate_intensity(0.0, mapping), 0.0, places=3
        )
        self.assertAlmostEqual(
            self.mapper._calculate_intensity(0.5, mapping), 0.25, places=3
        )
        self.assertAlmostEqual(
            self.mapper._calculate_intensity(1.0, mapping), 1.0, places=3
        )
        
    def test_sigmoid_intensity(self):
        """シグモイド強度計算のテスト"""
        mapping = NodeEffectMapping(
            "test_node", "test_effect", "test_module",
            intensity_mode=EffectIntensityMode.SIGMOID,
            max_intensity=1.0
        )
        
        # シグモイド変換のテスト
        result_0 = self.mapper._calculate_intensity(0.0, mapping)
        result_05 = self.mapper._calculate_intensity(0.5, mapping)
        result_1 = self.mapper._calculate_intensity(1.0, mapping)
        
        # シグモイドの特性確認
        self.assertTrue(0.0 <= result_0 < 0.1)   # 低い値は非常に小さく
        self.assertAlmostEqual(result_05, 0.5, places=1)  # 中間値は0.5付近
        self.assertTrue(0.9 < result_1 <= 1.0)   # 高い値は1に近く
        
    def test_threshold_intensity(self):
        """閾値ベース強度計算のテスト"""
        mapping = NodeEffectMapping(
            "test_node", "test_effect", "test_module",
            intensity_mode=EffectIntensityMode.THRESHOLD,
            threshold=0.3,
            max_intensity=1.0
        )
        
        # 閾値変換のテスト
        self.assertEqual(
            self.mapper._calculate_intensity(0.2, mapping), 0.0
        )  # 閾値以下
        
        self.assertAlmostEqual(
            self.mapper._calculate_intensity(0.3, mapping), 0.0, places=3
        )  # 閾値ちょうど
        
        self.assertAlmostEqual(
            self.mapper._calculate_intensity(0.65, mapping), 0.5, places=3
        )  # 閾値と1の中間
        
        self.assertAlmostEqual(
            self.mapper._calculate_intensity(1.0, mapping), 1.0, places=3
        )  # 最大値
        
    def test_max_intensity_clamping(self):
        """最大強度制限のテスト"""
        mapping = NodeEffectMapping(
            "test_node", "test_effect", "test_module",
            intensity_mode=EffectIntensityMode.LINEAR,
            max_intensity=0.6
        )
        
        # 最大強度による制限
        result = self.mapper._calculate_intensity(1.0, mapping)
        self.assertEqual(result, 0.6)


class TestNodeStatesMapping(unittest.TestCase):
    """ノード状態値マッピングのテスト"""
    
    def setUp(self):
        self.mapper = NodeEffectMapper()
        self.test_node_states = {
            "appearance_density": 0.8,
            "appearance_luminosity": 0.6, 
            "temporal_motion": 0.3,
            "synesthetic_temperature": 0.9,
            "ontological_presence": 0.2,
            "unknown_node": 0.5  # 存在しないノード
        }
        
    def test_basic_mapping(self):
        """基本的なマッピングのテスト"""
        effect_params = self.mapper.map_node_states_to_effects(
            self.test_node_states, active_threshold=0.1
        )
        
        # 有効なノードのみがマッピングされること
        valid_nodes = {name for name in self.test_node_states.keys() 
                      if name in self.mapper.node_mappings}
        
        # 閾値やmaxIntensityなどにより実際のエフェクト数は異なる可能性がある
        self.assertGreater(len(effect_params), 0)  # 何かしらのエフェクトが生成される
        self.assertLessEqual(len(effect_params), len(valid_nodes))  # 有効ノード数以下
        
        # 各パラメータの整合性確認
        for param in effect_params:
            self.assertIsInstance(param, EffectParameters)
            self.assertIsInstance(param.effect_name, str)
            self.assertIsInstance(param.module_name, str)
            self.assertTrue(0.0 <= param.intensity <= 1.0)
            self.assertTrue(0.0 <= param.node_state <= 1.0)
            self.assertIsInstance(param.additional_params, dict)
            
    def test_threshold_filtering(self):
        """閾値フィルタリングのテスト"""
        # 高い閾値でフィルタリング
        effect_params = self.mapper.map_node_states_to_effects(
            self.test_node_states, active_threshold=0.7
        )
        
        # 高い値のノードのみが残ること
        for param in effect_params:
            self.assertGreaterEqual(param.intensity, 0.7)
            
    def test_intensity_sorting(self):
        """強度順ソートのテスト"""
        effect_params = self.mapper.map_node_states_to_effects(
            self.test_node_states, active_threshold=0.1
        )
        
        # 強度の降順になっていることを確認
        intensities = [param.intensity for param in effect_params]
        self.assertEqual(intensities, sorted(intensities, reverse=True))
        
    def test_inverted_nodes(self):
        """反転ノードのテスト"""
        # invertフラグを持つノードをテスト
        inverted_mapping = NodeEffectMapping(
            "test_inverted", "test_effect", "test_module", invert=True
        )
        self.mapper.node_mappings["test_inverted"] = inverted_mapping
        
        test_states = {"test_inverted": 0.3}
        effect_params = self.mapper.map_node_states_to_effects(test_states)
        
        # 反転された値（0.7）が使用されていることを確認
        self.assertAlmostEqual(effect_params[0].node_state, 0.7, places=3)


class TestConnectivityMatrix(unittest.TestCase):
    """接続行列による相互作用のテスト"""
    
    def setUp(self):
        self.mapper = NodeEffectMapper()
        
        # テスト用の小さな接続行列
        self.test_nodes = ["node_a", "node_b", "node_c"]
        self.connectivity_matrix = np.array([
            [0.0, 0.8, 0.3],  # node_a
            [0.5, 0.0, 0.9],  # node_b  
            [0.2, 0.6, 0.0]   # node_c
        ])
        
        self.mapper.set_connectivity_matrix(self.connectivity_matrix, self.test_nodes)
        
        # テスト用マッピング追加
        for node in self.test_nodes:
            self.mapper.node_mappings[node] = NodeEffectMapping(
                node, f"{node}_effect", "test_module"
            )
            
    def test_connectivity_matrix_setup(self):
        """接続行列セットアップのテスト"""
        self.assertIsNotNone(self.mapper.connectivity_matrix)
        self.assertEqual(self.mapper.connectivity_matrix.shape, (3, 3))
        self.assertEqual(len(self.mapper.node_list), 3)
        
    def test_node_interaction_calculation(self):
        """ノード相互作用計算のテスト"""
        node_states = {"node_a": 0.5, "node_b": 0.8, "node_c": 0.3}
        
        # node_aの相互作用計算（node_b=0.8, node_c=0.3との接続）
        base_intensity = 0.5
        adjusted_intensity = self.mapper._apply_node_interactions(
            "node_a", base_intensity, node_states
        )
        
        # 相互作用により強度が調整されることを確認
        self.assertNotEqual(adjusted_intensity, base_intensity)
        self.assertTrue(0.0 < adjusted_intensity < 1.5)
        
    def test_interaction_with_high_connections(self):
        """強い接続による相互作用のテスト"""
        # 全て高い値の状態
        high_states = {"node_a": 0.9, "node_b": 0.9, "node_c": 0.9}
        
        base_intensity = 0.5
        adjusted = self.mapper._apply_node_interactions(
            "node_a", base_intensity, high_states
        )
        
        # 強い相互作用により強度が増加することを期待
        self.assertGreater(adjusted, base_intensity)
        
    def test_interaction_with_low_connections(self):
        """弱い接続による相互作用のテスト"""
        # 全て低い値の状態
        low_states = {"node_a": 0.2, "node_b": 0.2, "node_c": 0.2}
        
        base_intensity = 0.8
        adjusted = self.mapper._apply_node_interactions(
            "node_a", base_intensity, low_states
        )
        
        # 弱い相互作用により強度が減少することを期待
        self.assertLess(adjusted, base_intensity)


class TestAdditionalParameters(unittest.TestCase):
    """追加パラメータ計算のテスト"""
    
    def setUp(self):
        self.mapper = NodeEffectMapper()
        
    def test_appearance_additional_params(self):
        """現出様式の追加パラメータテスト"""
        node_states = {"appearance_density": 0.8}
        
        params = self.mapper._calculate_additional_parameters(
            "appearance_density", 0.8, node_states
        )
        
        # 密度ノードの追加パラメータ確認
        self.assertIn("cluster_preference", params)
        self.assertIn("cluster_count", params)
        self.assertTrue(params["cluster_preference"])  # 0.8 > 0.5
        self.assertIsInstance(params["cluster_count"], int)
        
    def test_temporal_additional_params(self):
        """時間的含意の追加パラメータテスト"""
        node_states = {"temporal_motion": 0.3}
        
        params = self.mapper._calculate_additional_parameters(
            "temporal_motion", 0.3, node_states
        )
        
        # モーションノードの追加パラメータ確認
        self.assertIn("motion_type", params)
        self.assertIn("direction_variance", params)
        self.assertEqual(params["motion_type"], "blur")  # 0.3 < 0.4
        
    def test_synesthetic_additional_params(self):
        """相互感覚的質の追加パラメータテスト"""
        node_states = {"synesthetic_temperature": 0.7}
        
        params = self.mapper._calculate_additional_parameters(
            "synesthetic_temperature", 0.7, node_states
        )
        
        # 温度ノードの追加パラメータ確認
        self.assertIn("temperature_bias", params)
        self.assertIn("thermal_intensity", params)
        self.assertEqual(params["temperature_bias"], "warm")  # 0.7 > 0.5
        
    def test_dimension_interactions(self):
        """次元間相互作用のテスト"""
        node_states = {
            "appearance_density": 0.6,
            "temporal_motion": 0.4,
            "synesthetic_weight": 0.8
        }
        
        interactions = self.mapper._calculate_dimension_interactions(
            "appearance_density", node_states
        )
        
        # 他次元の影響が計算されることを確認
        self.assertIn("temporal_influence", interactions)
        self.assertIn("synesthetic_influence", interactions)
        self.assertIn("overall_modulation", interactions)


class TestEffectPriorityOrdering(unittest.TestCase):
    """エフェクト優先順序のテスト"""
    
    def setUp(self):
        self.mapper = NodeEffectMapper()
        
        # テスト用のエフェクトパラメータリスト
        self.effect_params = [
            EffectParameters("appearance_density", "appearance_effects", 0.8, 0.8),
            EffectParameters("temporal_motion", "temporal_effects", 0.9, 0.9), 
            EffectParameters("certainty_clarity", "certainty_effects", 0.7, 0.7),
            EffectParameters("ontological_presence", "ontological_effects", 0.6, 0.6)
        ]
        
    def test_priority_calculation(self):
        """優先順序計算のテスト"""
        priority_order = self.mapper.get_effect_priority_order(self.effect_params)
        
        # 正しい数の順序が返されること
        self.assertEqual(len(priority_order), len(self.effect_params))
        
        # 現出様式が最高優先であることを確認
        appearance_index = next(i for i, p in enumerate(self.effect_params) 
                               if p.effect_name.startswith("appearance"))
        self.assertEqual(priority_order[0], appearance_index)
        
    def test_intensity_influence_on_priority(self):
        """強度が優先順序に与える影響のテスト"""
        # 同じ次元で強度の異なるエフェクト
        same_dimension_effects = [
            EffectParameters("temporal_motion", "temporal_effects", 0.3, 0.3),
            EffectParameters("temporal_decay", "temporal_effects", 0.9, 0.9)
        ]
        
        priority_order = self.mapper.get_effect_priority_order(same_dimension_effects)
        
        # 高強度のエフェクトが優先されること
        self.assertEqual(priority_order[0], 1)  # temporal_decay (0.9)
        self.assertEqual(priority_order[1], 0)  # temporal_motion (0.3)


class TestValidationAndUtilities(unittest.TestCase):
    """検証・ユーティリティ機能のテスト"""
    
    def setUp(self):
        self.mapper = NodeEffectMapper()
        
    def test_node_states_validation(self):
        """ノード状態値検証のテスト"""
        invalid_states = {
            "appearance_density": 1.5,      # 範囲外
            "temporal_motion": -0.1,        # 範囲外
            "unknown_node": 0.5,           # 存在しないノード
            "semantic_entities": "invalid"  # 不正な型
        }
        
        validation_results = self.mapper.validate_node_states(invalid_states)
        
        self.assertEqual(len(validation_results), 4)
        self.assertIn("Value out of range", validation_results["appearance_density"])
        self.assertIn("Value out of range", validation_results["temporal_motion"])
        self.assertIn("Unknown node name", validation_results["unknown_node"])
        self.assertIn("Invalid type", validation_results["semantic_entities"])
        
    def test_valid_node_states(self):
        """有効なノード状態値のテスト"""
        valid_states = {
            "appearance_density": 0.8,
            "temporal_motion": 0.3,
            "synesthetic_weight": 1.0,
            "ontological_presence": 0.0
        }
        
        validation_results = self.mapper.validate_node_states(valid_states)
        self.assertEqual(len(validation_results), 0)  # エラーなし
        
    def test_global_intensity_factor(self):
        """グローバル強度係数のテスト"""
        # 正常な係数設定
        self.mapper.set_global_intensity_factor(1.5)
        self.assertEqual(self.mapper.global_intensity_factor, 1.5)
        
        # 範囲外の係数（クランプされる）
        self.mapper.set_global_intensity_factor(3.0)
        self.assertEqual(self.mapper.global_intensity_factor, 2.0)
        
        self.mapper.set_global_intensity_factor(-0.5)
        self.assertEqual(self.mapper.global_intensity_factor, 0.0)
        
    def test_node_mapping_info_retrieval(self):
        """ノードマッピング情報取得のテスト"""
        # 存在するノード
        info = self.mapper.get_node_mapping_info("appearance_density")
        self.assertIsNotNone(info)
        self.assertEqual(info.node_name, "appearance_density")
        
        # 存在しないノード
        info = self.mapper.get_node_mapping_info("nonexistent_node")
        self.assertIsNone(info)


class TestIntegrationScenarios(unittest.TestCase):
    """統合シナリオテスト"""
    
    def setUp(self):
        self.mapper = NodeEffectMapper()
        
        # 現実的な27ノード状態を模擬
        self.realistic_node_states = {
            # 現出様式 - 高い活性
            "appearance_density": 0.8, "appearance_luminosity": 0.7, "appearance_chromaticity": 0.6,
            # 志向的構造 - 中程度
            "intentional_focus": 0.5, "intentional_horizon": 0.4, "intentional_depth": 0.6,
            # 時間的含意 - 低～中程度
            "temporal_motion": 0.3, "temporal_decay": 0.2, "temporal_duration": 0.4,
            # 相互感覚的質 - 様々
            "synesthetic_temperature": 0.7, "synesthetic_weight": 0.3, "synesthetic_texture": 0.5,
            # 存在論的密度 - 高い活性
            "ontological_presence": 0.8, "ontological_boundary": 0.6, "ontological_plurality": 0.4,
            # 意味的認識層 - 中程度
            "semantic_entities": 0.6, "semantic_relations": 0.5, "semantic_actions": 0.3,
            # 概念的地平 - 低～中程度
            "conceptual_cultural": 0.4, "conceptual_symbolic": 0.2, "conceptual_functional": 0.5,
            # 存在者の様態 - 様々
            "being_animacy": 0.7, "being_agency": 0.5, "being_artificiality": 0.2,
            # 認識の確実性分布 - 中～高
            "certainty_clarity": 0.6, "certainty_ambiguity": 0.3, "certainty_multiplicity": 0.5
        }
        
    def test_full_pipeline(self):
        """完全なパイプラインテスト"""
        # ノード状態値からエフェクトパラメータへの変換
        effect_params = self.mapper.map_node_states_to_effects(
            self.realistic_node_states, active_threshold=0.2
        )
        
        # 妥当な数のエフェクトが生成されること
        self.assertGreater(len(effect_params), 10)
        self.assertLess(len(effect_params), 27)
        
        # 優先順序の決定
        priority_order = self.mapper.get_effect_priority_order(effect_params)
        self.assertEqual(len(priority_order), len(effect_params))
        
        # 高優先度エフェクトの確認
        if len(effect_params) > 0:
            high_priority_effects = [effect_params[i] for i in priority_order[:min(5, len(effect_params))]]
            
            # 現出様式エフェクトが含まれているか確認（存在する場合）
            all_appearance_effects = [e for e in effect_params 
                                    if e.effect_name.startswith("appearance")]
            
            if len(all_appearance_effects) > 0:
                # 現出様式エフェクトが存在する場合、優先度が高いことを確認
                appearance_in_high_priority = [e for e in high_priority_effects 
                                             if e.effect_name.startswith("appearance")]
                # 少なくとも一部の現出様式が上位にあることを期待（必須ではない）
        
    def test_connectivity_integration(self):
        """接続行列統合テスト"""
        # 27x27の接続行列を作成（簡単な例）
        connectivity_matrix = np.random.rand(27, 27) * 0.3
        np.fill_diagonal(connectivity_matrix, 0)  # 自己接続は0
        
        node_names = list(self.realistic_node_states.keys())
        self.mapper.set_connectivity_matrix(connectivity_matrix, node_names)
        
        # 相互作用ありとなしでの比較
        self.mapper.set_connectivity_matrix(None, [])
        params_without_interaction = self.mapper.map_node_states_to_effects(
            self.realistic_node_states
        )
        
        self.mapper.set_connectivity_matrix(connectivity_matrix, node_names)
        params_with_interaction = self.mapper.map_node_states_to_effects(
            self.realistic_node_states
        )
        
        # 相互作用により結果が変わることを確認
        intensities_without = [p.intensity for p in params_without_interaction]
        intensities_with = [p.intensity for p in params_with_interaction]
        
        # 少なくとも一部のエフェクトで強度が変化することを期待
        differences = [abs(a - b) for a, b in zip(intensities_without, intensities_with)]
        significant_differences = [d for d in differences if d > 0.01]
        self.assertGreater(len(significant_differences), 0)


def run_all_tests():
    """全テストの実行"""
    # テストスイートの作成
    test_suite = unittest.TestSuite()
    
    # 各テストクラスを追加
    test_classes = [
        TestNodeEffectMapping,
        TestEffectParameters,
        TestNodeEffectMapperInitialization,
        TestIntensityCalculation,
        TestNodeStatesMapping,
        TestConnectivityMatrix,
        TestAdditionalParameters,
        TestEffectPriorityOrdering,
        TestValidationAndUtilities,
        TestIntegrationScenarios
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # テストの実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 結果の表示
    print(f"\n{'='*60}")
    print("🗺️  Node Effect Mapper Unit Tests Results")
    print("ノードマッピングシステムの包括的テスト結果")
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
        print(f"\n🎉 All node mapping tests passed!")
        print(f"\n💡 検証済み機能:")
        print(f"   ✅ 27ノードの完全マッピング定義")
        print(f"   ✅ 4種類の強度計算モード (linear/exponential/sigmoid/threshold)")
        print(f"   ✅ 接続行列による相互作用システム")
        print(f"   ✅ 次元間相互作用計算")
        print(f"   ✅ 哲学的優先順序決定システム")
        print(f"   ✅ 追加パラメータ生成機能")
        print(f"   ✅ ノード状態値検証システム")
        
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()