"""
Phenomenological Compositor - 現象学的コンポジター
27ノード間の相互作用による複合エフェクト生成とconnectivity matrix統合
"""

import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass
import importlib
import json
from pathlib import Path

try:
    from .node_effect_mapper import NodeEffectMapper, EffectParameters
    from .base_effect_library import MaskOperations, BlendModes
except ImportError:
    from node_effect_mapper import NodeEffectMapper, EffectParameters
    from base_effect_library import MaskOperations, BlendModes


@dataclass
class CompositionLayer:
    """合成レイヤーの定義"""
    image: Image.Image
    effect_name: str
    node_name: str
    intensity: float
    blend_mode: str = "normal"
    mask: Optional[np.ndarray] = None
    z_order: int = 0


@dataclass
class InteractionRule:
    """ノード間相互作用ルール"""
    source_nodes: List[str]
    target_node: str
    interaction_type: str  # "amplify", "suppress", "modulate"
    strength: float
    condition: Optional[callable] = None


class PhenomenologicalCompositor:
    """現象学的エフェクトの合成とノード間相互作用の管理"""
    
    def __init__(self, connectivity_matrix: Optional[np.ndarray] = None,
                 node_list: Optional[List[str]] = None):
        self.node_mapper = NodeEffectMapper()
        
        # Connectivity matrixの設定
        if connectivity_matrix is not None and node_list is not None:
            self.connectivity_matrix = connectivity_matrix
            self.node_list = node_list
            self.node_mapper.set_connectivity_matrix(connectivity_matrix, node_list)
        else:
            self.connectivity_matrix = None
            self.node_list = []
            
        # エフェクトモジュールのキャッシュ
        self.effect_modules = {}
        
        # 相互作用ルール
        self.interaction_rules = self._initialize_interaction_rules()
        
        # 合成履歴
        self.composition_history = []
        
    def _initialize_interaction_rules(self) -> List[InteractionRule]:
        """ノード間相互作用ルールの初期化"""
        rules = []
        
        # 現出様式（appearance）による全体への影響
        rules.append(InteractionRule(
            source_nodes=["appearance_density", "appearance_luminosity", "appearance_chromaticity"],
            target_node="global_modulation",
            interaction_type="amplify",
            strength=0.3
        ))
        
        # 志向的構造とセマンティクスの相互作用
        rules.append(InteractionRule(
            source_nodes=["intentional_focus"],
            target_node="semantic_entities",
            interaction_type="amplify",
            strength=0.4,
            condition=lambda states: states.get("intentional_focus", 0) > 0.6
        ))
        
        # 時間的含意と存在論的密度の相互作用
        rules.append(InteractionRule(
            source_nodes=["temporal_decay"],
            target_node="ontological_presence",
            interaction_type="suppress",
            strength=0.3
        ))
        
        # 相互感覚的質の相互強化
        rules.append(InteractionRule(
            source_nodes=["synesthetic_temperature", "synesthetic_weight"],
            target_node="synesthetic_texture",
            interaction_type="modulate",
            strength=0.2
        ))
        
        # 認識の確実性による他ノードの抑制
        rules.append(InteractionRule(
            source_nodes=["certainty_ambiguity"],
            target_node="global_clarity",
            interaction_type="suppress",
            strength=0.4
        ))
        
        return rules
    
    def compose_phenomenological_image(self, source_image: Image.Image,
                                     node_states: Dict[str, float],
                                     composition_mode: str = "layered") -> Image.Image:
        """
        現象学的画像合成のメイン処理
        
        Args:
            source_image: 元画像
            node_states: 27ノードの状態値
            composition_mode: 合成モード ("layered", "sequential", "parallel")
            
        Returns:
            合成された画像
        """
        # ノード状態の検証
        validation_errors = self.node_mapper.validate_node_states(node_states)
        if validation_errors:
            raise ValueError(f"Node state validation errors: {validation_errors}")
        
        # 相互作用ルールの適用
        adjusted_states = self._apply_interaction_rules(node_states)
        
        # エフェクトパラメータの生成
        effect_params = self.node_mapper.map_node_states_to_effects(adjusted_states)
        
        if not effect_params:
            return source_image
        
        # 合成モードに応じた処理
        if composition_mode == "layered":
            return self._compose_layered(source_image, effect_params)
        elif composition_mode == "sequential":
            return self._compose_sequential(source_image, effect_params)
        elif composition_mode == "parallel":
            return self._compose_parallel(source_image, effect_params)
        else:
            raise ValueError(f"Unknown composition mode: {composition_mode}")
    
    def _apply_interaction_rules(self, node_states: Dict[str, float]) -> Dict[str, float]:
        """相互作用ルールを適用してノード状態を調整"""
        adjusted_states = node_states.copy()
        
        for rule in self.interaction_rules:
            # 条件チェック
            if rule.condition and not rule.condition(node_states):
                continue
                
            # ソースノードの平均値を計算
            source_values = []
            for source_node in rule.source_nodes:
                if source_node in node_states:
                    source_values.append(node_states[source_node])
            
            if not source_values:
                continue
                
            source_strength = np.mean(source_values)
            
            # 相互作用の適用
            if rule.target_node == "global_modulation":
                # 全ノードに対するグローバル調整
                modulation = 1.0 + rule.strength * (source_strength - 0.5)
                for node_name in adjusted_states:
                    adjusted_states[node_name] *= modulation
                    adjusted_states[node_name] = np.clip(adjusted_states[node_name], 0.0, 1.0)
                    
            elif rule.target_node == "global_clarity":
                # 明瞭度に関連するノードの調整
                clarity_nodes = ["certainty_clarity", "intentional_focus", "semantic_entities"]
                adjustment = rule.strength * source_strength
                
                for node_name in clarity_nodes:
                    if node_name in adjusted_states:
                        if rule.interaction_type == "suppress":
                            adjusted_states[node_name] *= (1.0 - adjustment)
                        elif rule.interaction_type == "amplify":
                            adjusted_states[node_name] *= (1.0 + adjustment)
                        adjusted_states[node_name] = np.clip(adjusted_states[node_name], 0.0, 1.0)
                        
            elif rule.target_node in adjusted_states:
                # 特定ノードへの相互作用
                target_value = adjusted_states[rule.target_node]
                
                if rule.interaction_type == "amplify":
                    adjustment = rule.strength * source_strength
                    adjusted_states[rule.target_node] = min(1.0, target_value + adjustment)
                elif rule.interaction_type == "suppress":
                    adjustment = rule.strength * source_strength  
                    adjusted_states[rule.target_node] = max(0.0, target_value - adjustment)
                elif rule.interaction_type == "modulate":
                    modulation = 1.0 + rule.strength * (source_strength - 0.5)
                    adjusted_states[rule.target_node] = np.clip(target_value * modulation, 0.0, 1.0)
        
        # Connectivity matrixによる追加調整
        if self.connectivity_matrix is not None:
            adjusted_states = self._apply_connectivity_matrix(adjusted_states)
            
        return adjusted_states
    
    def _apply_connectivity_matrix(self, node_states: Dict[str, float]) -> Dict[str, float]:
        """Connectivity matrixによるノード間相互作用の適用"""
        adjusted_states = node_states.copy()
        
        for i, node_name in enumerate(self.node_list):
            if node_name not in node_states:
                continue
                
            # このノードに影響する他ノードの効果を計算
            influence_sum = 0.0
            total_weight = 0.0
            
            for j, other_node in enumerate(self.node_list):
                if i == j or other_node not in node_states:
                    continue
                    
                connection_strength = self.connectivity_matrix[i, j]
                if connection_strength > 0.1:  # 有意な接続のみ
                    influence_sum += connection_strength * node_states[other_node]
                    total_weight += connection_strength
            
            if total_weight > 0:
                # 影響の正規化と適用
                average_influence = influence_sum / total_weight
                
                # 相互作用の強度（最大20%の変化）
                interaction_factor = 0.2 * (average_influence - 0.5)
                new_value = node_states[node_name] * (1.0 + interaction_factor)
                adjusted_states[node_name] = np.clip(new_value, 0.0, 1.0)
        
        return adjusted_states
    
    def _compose_layered(self, source_image: Image.Image, 
                        effect_params: List[EffectParameters]) -> Image.Image:
        """レイヤー合成モード"""
        layers = []
        
        # 優先順序の決定
        priority_order = self.node_mapper.get_effect_priority_order(effect_params)
        
        # 各エフェクトをレイヤーとして生成
        for priority_index in priority_order:
            param = effect_params[priority_index]
            
            try:
                # エフェクトを適用した画像を生成
                effect_image = self._apply_single_effect(source_image, param)
                
                # マスクの生成（必要に応じて）
                mask = self._generate_effect_mask(source_image, param)
                
                # レイヤーの作成
                layer = CompositionLayer(
                    image=effect_image,
                    effect_name=param.effect_name,
                    node_name=param.effect_name.split('_')[0] + "_" + param.effect_name.split('_')[1],
                    intensity=param.intensity,
                    blend_mode=self._determine_blend_mode(param),
                    mask=mask,
                    z_order=len(priority_order) - priority_index  # 優先度の高いものほど上
                )
                
                layers.append(layer)
                
            except Exception as e:
                print(f"Warning: Failed to apply effect {param.effect_name}: {e}")
                continue
        
        # レイヤーの合成
        result_image = self._composite_layers(source_image, layers)
        
        # 合成履歴の記録
        self.composition_history.append({
            "mode": "layered",
            "effects_applied": len(layers),
            "layer_info": [(l.effect_name, l.intensity, l.blend_mode) for l in layers]
        })
        
        return result_image
    
    def _compose_sequential(self, source_image: Image.Image,
                          effect_params: List[EffectParameters]) -> Image.Image:
        """逐次合成モード（エフェクトを順次適用）"""
        current_image = source_image
        effects_applied = []
        
        # 優先順序に従って順次適用
        priority_order = self.node_mapper.get_effect_priority_order(effect_params)
        
        for priority_index in priority_order:
            param = effect_params[priority_index]
            
            try:
                # エフェクトの適用
                current_image = self._apply_single_effect(current_image, param)
                effects_applied.append((param.effect_name, param.intensity))
                
            except Exception as e:
                print(f"Warning: Failed to apply effect {param.effect_name}: {e}")
                continue
        
        # 履歴記録
        self.composition_history.append({
            "mode": "sequential",
            "effects_applied": len(effects_applied),
            "effect_sequence": effects_applied
        })
        
        return current_image
    
    def _compose_parallel(self, source_image: Image.Image,
                         effect_params: List[EffectParameters]) -> Image.Image:
        """並列合成モード（同じソースから複数エフェクトを生成して合成）"""
        effect_images = []
        weights = []
        
        for param in effect_params:
            try:
                # 各エフェクトを元画像に適用
                effect_image = self._apply_single_effect(source_image, param)
                effect_images.append(effect_image)
                weights.append(param.intensity)
                
            except Exception as e:
                print(f"Warning: Failed to apply effect {param.effect_name}: {e}")
                continue
        
        if not effect_images:
            return source_image
        
        # 重み付き平均による合成
        result_image = self._weighted_average_composition(source_image, effect_images, weights)
        
        # 履歴記録
        self.composition_history.append({
            "mode": "parallel", 
            "effects_applied": len(effect_images),
            "weights": weights
        })
        
        return result_image
    
    def _apply_single_effect(self, image: Image.Image, 
                           param: EffectParameters) -> Image.Image:
        """単一エフェクトの適用"""
        # エフェクトモジュールの取得
        if param.module_name not in self.effect_modules:
            try:
                module_path = f"src.core.{param.module_name}"
                module = importlib.import_module(module_path)
                self.effect_modules[param.module_name] = module
            except ImportError:
                # フォールバック：直接importを試行
                try:
                    if param.module_name == "appearance_effects":
                        from .appearance_effects import AppearanceEffects
                        self.effect_modules[param.module_name] = AppearanceEffects
                    # 他のモジュールも同様に追加可能
                except ImportError as e:
                    raise ImportError(f"Cannot import effect module {param.module_name}: {e}")
        
        effect_module = self.effect_modules[param.module_name]
        
        # エフェクトメソッドの取得と実行
        if hasattr(effect_module, param.effect_name):
            effect_method = getattr(effect_module, param.effect_name)
            return effect_method(image, param.intensity, param.node_state)
        else:
            raise AttributeError(f"Effect method {param.effect_name} not found in {param.module_name}")
    
    def _generate_effect_mask(self, image: Image.Image, 
                            param: EffectParameters) -> Optional[np.ndarray]:
        """エフェクト用マスクの生成"""
        # パラメータに基づくマスク生成
        additional_params = param.additional_params or {}
        
        if "mask_type" in additional_params:
            mask_type = additional_params["mask_type"]
            size = (image.height, image.width)
            
            if mask_type == "center":
                radius = additional_params.get("radius", 0.5)
                return MaskOperations.create_circular_mask(size, (0.5, 0.5), radius, 0.1)
            elif mask_type == "gradient":
                direction = additional_params.get("direction", "radial")
                return MaskOperations.create_gradient_mask(size, direction)
            
        # デフォルトではマスクなし
        return None
    
    def _determine_blend_mode(self, param: EffectParameters) -> str:
        """エフェクトに適したブレンドモードの決定"""
        effect_name = param.effect_name
        
        if "luminosity" in effect_name or "brightness" in effect_name:
            return "screen" if param.node_state > 0.5 else "multiply"
        elif "chromaticity" in effect_name or "color" in effect_name:
            return "overlay"
        elif "density" in effect_name:
            return "normal"
        else:
            return "normal"
    
    def _composite_layers(self, base_image: Image.Image, 
                         layers: List[CompositionLayer]) -> Image.Image:
        """レイヤー合成の実行"""
        # z_orderでソート
        layers.sort(key=lambda l: l.z_order)
        
        result_array = np.array(base_image).astype(np.float32)
        
        for layer in layers:
            layer_array = np.array(layer.image).astype(np.float32)
            
            # ブレンドモードに応じた合成
            if layer.blend_mode == "normal":
                blended = BlendModes.normal_blend(result_array, layer_array, layer.intensity)
            elif layer.blend_mode == "multiply":
                blended = BlendModes.multiply_blend(result_array, layer_array, layer.intensity)
            elif layer.blend_mode == "screen":
                blended = BlendModes.screen_blend(result_array, layer_array, layer.intensity)
            elif layer.blend_mode == "overlay":
                blended = BlendModes.overlay_blend(result_array, layer_array, layer.intensity)
            else:
                blended = BlendModes.normal_blend(result_array, layer_array, layer.intensity)
            
            # マスクの適用
            if layer.mask is not None:
                if len(layer.mask.shape) == 2:
                    mask = np.stack([layer.mask] * 3, axis=2)
                else:
                    mask = layer.mask
                    
                result_array = result_array * (1 - mask) + blended * mask
            else:
                result_array = blended
        
        result_array = np.clip(result_array, 0, 255).astype(np.uint8)
        return Image.fromarray(result_array)
    
    def _weighted_average_composition(self, base_image: Image.Image,
                                    effect_images: List[Image.Image], 
                                    weights: List[float]) -> Image.Image:
        """重み付き平均合成"""
        # 重みの正規化
        total_weight = sum(weights) + 1.0  # ベース画像の重み
        normalized_weights = [w / total_weight for w in weights]
        base_weight = 1.0 / total_weight
        
        # 画像配列への変換
        result_array = np.array(base_image).astype(np.float32) * base_weight
        
        for effect_image, weight in zip(effect_images, normalized_weights):
            effect_array = np.array(effect_image).astype(np.float32)
            result_array += effect_array * weight
        
        result_array = np.clip(result_array, 0, 255).astype(np.uint8)
        return Image.fromarray(result_array)
    
    def get_composition_history(self) -> List[Dict[str, Any]]:
        """合成履歴の取得"""
        return self.composition_history
    
    def clear_composition_history(self):
        """合成履歴のクリア"""
        self.composition_history = []
        
    def save_composition_config(self, filepath: str, node_states: Dict[str, float]):
        """合成設定の保存"""
        config = {
            "node_states": node_states,
            "connectivity_matrix": self.connectivity_matrix.tolist() if self.connectivity_matrix is not None else None,
            "node_list": self.node_list,
            "interaction_rules": [
                {
                    "source_nodes": rule.source_nodes,
                    "target_node": rule.target_node,
                    "interaction_type": rule.interaction_type,
                    "strength": rule.strength
                }
                for rule in self.interaction_rules
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)