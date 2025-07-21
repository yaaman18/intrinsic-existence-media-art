"""
Node Effect Mapper - ノード状態値からエフェクトパラメータへの変換システム
現象学的オラクルシステムの27ノード状態値を画像エフェクトのパラメータに変換する
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum


class EffectIntensityMode(Enum):
    """エフェクト強度の計算モード"""
    LINEAR = "linear"           # 線形変換
    EXPONENTIAL = "exponential" # 指数的変換
    SIGMOID = "sigmoid"         # シグモイド変換
    THRESHOLD = "threshold"     # 閾値ベース


@dataclass
class NodeEffectMapping:
    """ノードとエフェクトのマッピング定義"""
    node_name: str
    effect_name: str
    effect_module: str
    intensity_mode: EffectIntensityMode = EffectIntensityMode.LINEAR
    threshold: float = 0.5
    max_intensity: float = 1.0
    invert: bool = False  # True時は(1-node_state)を使用
    
    
@dataclass
class EffectParameters:
    """エフェクトパラメータの統一データクラス"""
    effect_name: str
    module_name: str
    intensity: float
    node_state: float
    additional_params: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.additional_params is None:
            self.additional_params = {}


class NodeEffectMapper:
    """27ノードの状態値を画像エフェクトパラメータに変換するマッパー"""
    
    def __init__(self):
        # 27ノードのエフェクトマッピング定義
        self.node_mappings = self._initialize_node_mappings()
        
        # ノード間の相互作用強度（connectivity matrixから取得）
        self.connectivity_matrix = None
        
        # エフェクト強度の調整係数
        self.global_intensity_factor = 1.0
        
    def _initialize_node_mappings(self) -> Dict[str, NodeEffectMapping]:
        """27ノードのエフェクトマッピングを初期化"""
        return {
            # 1. 現出様式（Mode of Appearance）
            "appearance_density": NodeEffectMapping(
                "appearance_density", "density_effect", "appearance_effects",
                intensity_mode=EffectIntensityMode.SIGMOID, max_intensity=0.8
            ),
            "appearance_luminosity": NodeEffectMapping(
                "appearance_luminosity", "luminosity_effect", "appearance_effects",
                intensity_mode=EffectIntensityMode.LINEAR, max_intensity=1.0
            ),
            "appearance_chromaticity": NodeEffectMapping(
                "appearance_chromaticity", "chromaticity_effect", "appearance_effects",
                intensity_mode=EffectIntensityMode.EXPONENTIAL, max_intensity=0.9
            ),
            
            # 2. 志向的構造（Intentional Structure）
            "intentional_focus": NodeEffectMapping(
                "intentional_focus", "focus_effect", "intentional_effects",
                intensity_mode=EffectIntensityMode.THRESHOLD, threshold=0.3
            ),
            "intentional_horizon": NodeEffectMapping(
                "intentional_horizon", "horizon_effect", "intentional_effects",
                intensity_mode=EffectIntensityMode.LINEAR, max_intensity=0.7
            ),
            "intentional_depth": NodeEffectMapping(
                "intentional_depth", "depth_effect", "intentional_effects",
                intensity_mode=EffectIntensityMode.SIGMOID, max_intensity=1.0
            ),
            
            # 3. 時間的含意（Temporal Implications）
            "temporal_motion": NodeEffectMapping(
                "temporal_motion", "motion_effect", "temporal_effects",
                intensity_mode=EffectIntensityMode.EXPONENTIAL, max_intensity=0.8
            ),
            "temporal_decay": NodeEffectMapping(
                "temporal_decay", "decay_effect", "temporal_effects",
                intensity_mode=EffectIntensityMode.LINEAR, max_intensity=0.9
            ),
            "temporal_duration": NodeEffectMapping(
                "temporal_duration", "duration_effect", "temporal_effects",
                intensity_mode=EffectIntensityMode.SIGMOID, max_intensity=0.6
            ),
            
            # 4. 相互感覚的質（Synesthetic Qualities）
            "synesthetic_temperature": NodeEffectMapping(
                "synesthetic_temperature", "temperature_effect", "synesthetic_effects",
                intensity_mode=EffectIntensityMode.LINEAR, max_intensity=0.8
            ),
            "synesthetic_weight": NodeEffectMapping(
                "synesthetic_weight", "weight_effect", "synesthetic_effects",
                intensity_mode=EffectIntensityMode.SIGMOID, max_intensity=0.7
            ),
            "synesthetic_texture": NodeEffectMapping(
                "synesthetic_texture", "texture_effect", "synesthetic_effects",
                intensity_mode=EffectIntensityMode.THRESHOLD, threshold=0.4
            ),
            
            # 5. 存在論的密度（Ontological Density）
            "ontological_presence": NodeEffectMapping(
                "ontological_presence", "presence_effect", "ontological_effects",
                intensity_mode=EffectIntensityMode.EXPONENTIAL, max_intensity=1.0
            ),
            "ontological_boundary": NodeEffectMapping(
                "ontological_boundary", "boundary_effect", "ontological_effects",
                intensity_mode=EffectIntensityMode.THRESHOLD, threshold=0.5
            ),
            "ontological_plurality": NodeEffectMapping(
                "ontological_plurality", "plurality_effect", "ontological_effects",
                intensity_mode=EffectIntensityMode.SIGMOID, max_intensity=0.6
            ),
            
            # 6. 意味的認識層（Semantic Recognition Layer）
            "semantic_entities": NodeEffectMapping(
                "semantic_entities", "entities_effect", "semantic_effects",
                intensity_mode=EffectIntensityMode.THRESHOLD, threshold=0.6
            ),
            "semantic_relations": NodeEffectMapping(
                "semantic_relations", "relations_effect", "semantic_effects",
                intensity_mode=EffectIntensityMode.LINEAR, max_intensity=0.8
            ),
            "semantic_actions": NodeEffectMapping(
                "semantic_actions", "actions_effect", "semantic_effects",
                intensity_mode=EffectIntensityMode.EXPONENTIAL, max_intensity=0.7
            ),
            
            # 7. 概念的地平（Conceptual Horizon）
            "conceptual_cultural": NodeEffectMapping(
                "conceptual_cultural", "cultural_effect", "conceptual_effects",
                intensity_mode=EffectIntensityMode.SIGMOID, max_intensity=0.9
            ),
            "conceptual_symbolic": NodeEffectMapping(
                "conceptual_symbolic", "symbolic_effect", "conceptual_effects",
                intensity_mode=EffectIntensityMode.THRESHOLD, threshold=0.4
            ),
            "conceptual_functional": NodeEffectMapping(
                "conceptual_functional", "functional_effect", "conceptual_effects",
                intensity_mode=EffectIntensityMode.LINEAR, max_intensity=0.6
            ),
            
            # 8. 存在者の様態（Modes of Being）
            "being_animacy": NodeEffectMapping(
                "being_animacy", "animacy_effect", "being_effects",
                intensity_mode=EffectIntensityMode.EXPONENTIAL, max_intensity=0.8
            ),
            "being_agency": NodeEffectMapping(
                "being_agency", "agency_effect", "being_effects",
                intensity_mode=EffectIntensityMode.SIGMOID, max_intensity=0.7
            ),
            "being_artificiality": NodeEffectMapping(
                "being_artificiality", "artificiality_effect", "being_effects",
                intensity_mode=EffectIntensityMode.THRESHOLD, threshold=0.5
            ),
            
            # 9. 認識の確実性分布（Recognition Certainty Distribution）
            "certainty_clarity": NodeEffectMapping(
                "certainty_clarity", "clarity_effect", "certainty_effects",
                intensity_mode=EffectIntensityMode.LINEAR, max_intensity=1.0
            ),
            "certainty_ambiguity": NodeEffectMapping(
                "certainty_ambiguity", "ambiguity_effect", "certainty_effects",
                intensity_mode=EffectIntensityMode.SIGMOID, max_intensity=0.8,
                invert=False  # 曖昧性は高い値で強くなる
            ),
            "certainty_multiplicity": NodeEffectMapping(
                "certainty_multiplicity", "multiplicity_effect", "certainty_effects",
                intensity_mode=EffectIntensityMode.EXPONENTIAL, max_intensity=0.6
            )
        }
    
    def set_connectivity_matrix(self, connectivity_matrix: np.ndarray, 
                               node_list: List[str]):
        """接続行列を設定"""
        self.connectivity_matrix = connectivity_matrix
        self.node_list = node_list
        
    def map_node_states_to_effects(self, node_states: Dict[str, float], 
                                  active_threshold: float = 0.1) -> List[EffectParameters]:
        """
        ノード状態値をエフェクトパラメータにマッピング
        
        Args:
            node_states: 27ノードの状態値辞書
            active_threshold: エフェクトを適用する最小閾値
            
        Returns:
            エフェクトパラメータのリスト
        """
        effect_params_list = []
        
        for node_name, node_value in node_states.items():
            if node_name not in self.node_mappings:
                continue
                
            mapping = self.node_mappings[node_name]
            
            # ノード状態値の反転処理
            effective_value = (1.0 - node_value) if mapping.invert else node_value
            
            # 強度計算
            intensity = self._calculate_intensity(effective_value, mapping)
            
            # 相互作用による強度調整
            if self.connectivity_matrix is not None:
                intensity = self._apply_node_interactions(node_name, intensity, node_states)
            
            # グローバル調整
            intensity *= self.global_intensity_factor
            
            # 閾値チェック
            if intensity >= active_threshold:
                # 追加パラメータの計算
                additional_params = self._calculate_additional_parameters(
                    node_name, effective_value, node_states
                )
                
                effect_param = EffectParameters(
                    effect_name=mapping.effect_name,
                    module_name=mapping.effect_module,
                    intensity=min(intensity, 1.0),
                    node_state=effective_value,
                    additional_params=additional_params
                )
                
                effect_params_list.append(effect_param)
        
        # 強度順でソート（強い効果を優先）
        effect_params_list.sort(key=lambda x: x.intensity, reverse=True)
        
        return effect_params_list
    
    def _calculate_intensity(self, node_value: float, 
                           mapping: NodeEffectMapping) -> float:
        """強度計算（変換モードに応じた処理）"""
        if mapping.intensity_mode == EffectIntensityMode.LINEAR:
            intensity = node_value
            
        elif mapping.intensity_mode == EffectIntensityMode.EXPONENTIAL:
            # 指数的変換（低い値は更に低く、高い値は強調）
            intensity = node_value ** 2
            
        elif mapping.intensity_mode == EffectIntensityMode.SIGMOID:
            # シグモイド変換（中間値を滑らかに変換）
            x = (node_value - 0.5) * 12  # -6 to 6の範囲
            intensity = 1.0 / (1.0 + np.exp(-x))
            
        elif mapping.intensity_mode == EffectIntensityMode.THRESHOLD:
            # 閾値ベース変換
            if node_value >= mapping.threshold:
                intensity = (node_value - mapping.threshold) / (1.0 - mapping.threshold)
            else:
                intensity = 0.0
        else:
            intensity = node_value
        
        # 最大強度で制限
        return min(intensity * mapping.max_intensity, mapping.max_intensity)
    
    def _apply_node_interactions(self, node_name: str, base_intensity: float,
                               node_states: Dict[str, float]) -> float:
        """ノード間相互作用による強度調整"""
        if node_name not in self.node_list:
            return base_intensity
        
        node_index = self.node_list.index(node_name)
        interaction_factor = 0.0
        total_weight = 0.0
        
        # 接続された他ノードの影響を計算
        for i, other_node in enumerate(self.node_list):
            if i == node_index:
                continue
                
            connection_strength = self.connectivity_matrix[node_index, i]
            if connection_strength > 0.1:  # 有意な接続のみ考慮
                other_state = node_states.get(other_node, 0.0)
                interaction_factor += connection_strength * other_state
                total_weight += connection_strength
        
        if total_weight > 0:
            # 平均相互作用強度を計算
            avg_interaction = interaction_factor / total_weight
            
            # 相互作用による調整（最大30%の増減）
            interaction_adjustment = 1.0 + 0.3 * (avg_interaction - 0.5)
            return base_intensity * max(0.1, min(1.5, interaction_adjustment))
        
        return base_intensity
    
    def _calculate_additional_parameters(self, node_name: str, node_value: float,
                                       node_states: Dict[str, float]) -> Dict[str, Any]:
        """ノード固有の追加パラメータを計算"""
        additional_params = {}
        
        # ノード名に基づく特殊パラメータの設定
        if "appearance" in node_name:
            # 現出様式の追加パラメータ
            if node_name == "appearance_density":
                additional_params["cluster_preference"] = node_value > 0.5
                additional_params["cluster_count"] = int(3 + node_value * 5)
            elif node_name == "appearance_luminosity":
                additional_params["disclosure_mode"] = "enhance" if node_value > 0.5 else "conceal"
                additional_params["selective_enhancement"] = node_value > 0.7
            elif node_name == "appearance_chromaticity":
                additional_params["interaction_mode"] = "chiasme" if node_value > 0.5 else "separation"
                additional_params["color_depth"] = node_value
                
        elif "temporal" in node_name:
            # 時間的含意の追加パラメータ
            if node_name == "temporal_motion":
                additional_params["motion_type"] = "blur" if node_value < 0.4 else "trail"
                additional_params["direction_variance"] = node_value * 180  # 度数
            elif node_name == "temporal_decay":
                additional_params["decay_pattern"] = "uniform" if node_value < 0.5 else "selective"
                additional_params["aging_factor"] = node_value
                
        elif "synesthetic" in node_name:
            # 相互感覚的質の追加パラメータ
            if node_name == "synesthetic_temperature":
                additional_params["temperature_bias"] = "warm" if node_value > 0.5 else "cool"
                additional_params["thermal_intensity"] = abs(node_value - 0.5) * 2
            elif node_name == "synesthetic_weight":
                additional_params["gravity_direction"] = "down" if node_value > 0.5 else "up"
                additional_params["mass_factor"] = node_value
                
        # 次元間の相互作用を考慮した調整
        dimension_interactions = self._calculate_dimension_interactions(node_name, node_states)
        additional_params.update(dimension_interactions)
        
        return additional_params
    
    def _calculate_dimension_interactions(self, node_name: str, 
                                        node_states: Dict[str, float]) -> Dict[str, Any]:
        """次元間相互作用の計算"""
        interactions = {}
        
        # ノードの次元を特定
        dimension = node_name.split('_')[0]
        
        # 他の次元との相互作用を計算
        dimension_averages = {}
        for other_node, value in node_states.items():
            other_dimension = other_node.split('_')[0]
            if other_dimension != dimension:
                if other_dimension not in dimension_averages:
                    dimension_averages[other_dimension] = []
                dimension_averages[other_dimension].append(value)
        
        # 次元平均の計算
        for dim, values in dimension_averages.items():
            avg_value = np.mean(values)
            interactions[f"{dim}_influence"] = avg_value
        
        # 特別な相互作用の計算
        if dimension == "appearance":
            # 現出様式は他の全次元に影響
            overall_intensity = np.mean(list(node_states.values()))
            interactions["overall_modulation"] = overall_intensity
            
        elif dimension == "intentional":
            # 志向的構造は意味的認識と強く相互作用
            if "semantic" in dimension_averages:
                interactions["semantic_focus_boost"] = dimension_averages["semantic"][0] if dimension_averages["semantic"] else 0.0
        
        return interactions
    
    def get_effect_priority_order(self, effect_params_list: List[EffectParameters]) -> List[int]:
        """エフェクト適用の優先順序を決定"""
        # 哲学的重要度に基づく優先順序
        priority_weights = {
            "appearance": 10,   # 現出様式は最優先
            "intentional": 9,   # 志向的構造
            "ontological": 8,   # 存在論的密度
            "temporal": 7,      # 時間的含意
            "semantic": 6,      # 意味的認識
            "synesthetic": 5,   # 相互感覚的質
            "conceptual": 4,    # 概念的地平
            "being": 3,         # 存在者の様態
            "certainty": 2      # 認識の確実性分布
        }
        
        # 優先度スコアを計算
        priority_scores = []
        for i, effect_param in enumerate(effect_params_list):
            dimension = effect_param.effect_name.split('_')[0]
            base_priority = priority_weights.get(dimension, 1)
            intensity_bonus = effect_param.intensity * 5
            priority_score = base_priority + intensity_bonus
            priority_scores.append((priority_score, i))
        
        # スコア順でソート
        priority_scores.sort(key=lambda x: x[0], reverse=True)
        
        return [i for score, i in priority_scores]
    
    def set_global_intensity_factor(self, factor: float):
        """グローバル強度調整係数を設定"""
        self.global_intensity_factor = max(0.0, min(2.0, factor))
        
    def get_node_mapping_info(self, node_name: str) -> Optional[NodeEffectMapping]:
        """指定ノードのマッピング情報を取得"""
        return self.node_mappings.get(node_name)
        
    def validate_node_states(self, node_states: Dict[str, float]) -> Dict[str, str]:
        """ノード状態値の検証"""
        validation_results = {}
        
        for node_name, value in node_states.items():
            if not isinstance(value, (int, float)):
                validation_results[node_name] = f"Invalid type: {type(value)}"
            elif not 0.0 <= value <= 1.0:
                validation_results[node_name] = f"Value out of range: {value}"
            elif node_name not in self.node_mappings:
                validation_results[node_name] = "Unknown node name"
                
        return validation_results