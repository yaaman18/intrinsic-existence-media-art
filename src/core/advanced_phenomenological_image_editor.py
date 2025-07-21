"""
Advanced Phenomenological Image Editor - 高度現象学的画像編集システム
27ノード専用エフェクトシステムのメインインターフェース
"""

import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass
import json
from pathlib import Path
import time
from datetime import datetime

try:
    from .phenomenological_compositor import PhenomenologicalCompositor
    from .node_effect_mapper import NodeEffectMapper, EffectParameters
    from .appearance_effects import AppearanceEffects
except ImportError:
    from phenomenological_compositor import PhenomenologicalCompositor
    from node_effect_mapper import NodeEffectMapper, EffectParameters
    from appearance_effects import AppearanceEffects


@dataclass
class EditingSession:
    """編集セッションの情報"""
    session_id: str
    start_time: datetime
    original_image_size: Tuple[int, int]
    node_states_history: List[Dict[str, float]]
    effects_applied: List[str]
    composition_mode: str
    total_processing_time: float = 0.0


class AdvancedPhenomenologicalImageEditor:
    """
    高度現象学的画像編集システム
    27ノード状態値に基づく哲学的に厳密な画像エフェクト処理
    """
    
    def __init__(self, connectivity_matrix: Optional[np.ndarray] = None,
                 node_list: Optional[List[str]] = None):
        """
        初期化
        
        Args:
            connectivity_matrix: ノード間接続行列
            node_list: ノード名のリスト
        """
        self.compositor = PhenomenologicalCompositor(connectivity_matrix, node_list)
        self.node_mapper = self.compositor.node_mapper
        
        # セッション管理
        self.current_session: Optional[EditingSession] = None
        self.session_history: List[EditingSession] = []
        
        # キャッシュ設定
        self.enable_caching = True
        self.effect_cache: Dict[str, Image.Image] = {}
        
        # デバッグモード
        self.debug_mode = False
        
    def start_editing_session(self, image: Image.Image, session_id: str = None) -> str:
        """
        編集セッションを開始
        
        Args:
            image: 編集対象画像
            session_id: セッションID（指定しない場合は自動生成）
            
        Returns:
            セッションID
        """
        if session_id is None:
            session_id = f"session_{int(time.time())}"
            
        self.current_session = EditingSession(
            session_id=session_id,
            start_time=datetime.now(),
            original_image_size=(image.width, image.height),
            node_states_history=[],
            effects_applied=[],
            composition_mode="layered"
        )
        
        if self.debug_mode:
            print(f"📸 Started editing session: {session_id}")
            print(f"   Image size: {image.width}x{image.height}")
            
        return session_id
    
    def apply_phenomenological_transformation(self, 
                                           image: Image.Image,
                                           node_states: Dict[str, float],
                                           composition_mode: str = "layered",
                                           enable_interaction: bool = True) -> Image.Image:
        """
        現象学的変換の適用
        
        Args:
            image: 入力画像
            node_states: 27ノードの状態値
            composition_mode: 合成モード ("layered", "sequential", "parallel")
            enable_interaction: ノード間相互作用の有効化
            
        Returns:
            変換された画像
        """
        start_time = time.time()
        
        # セッション情報の更新
        if self.current_session:
            self.current_session.node_states_history.append(node_states.copy())
            self.current_session.composition_mode = composition_mode
        
        try:
            # ノード状態の検証
            validation_errors = self.node_mapper.validate_node_states(node_states)
            if validation_errors:
                raise ValueError(f"Node validation failed: {validation_errors}")
            
            # 現象学的合成の実行
            if enable_interaction:
                result_image = self.compositor.compose_phenomenological_image(
                    image, node_states, composition_mode
                )
            else:
                # 相互作用なしの単純適用
                result_image = self._apply_effects_without_interaction(
                    image, node_states
                )
            
            # 処理時間の記録
            processing_time = time.time() - start_time
            if self.current_session:
                self.current_session.total_processing_time += processing_time
                
            if self.debug_mode:
                print(f"⚡ Phenomenological transformation completed in {processing_time:.3f}s")
                active_nodes = [k for k, v in node_states.items() if v > 0.1]
                print(f"   Active nodes ({len(active_nodes)}): {active_nodes[:5]}{'...' if len(active_nodes) > 5 else ''}")
                
            return result_image
            
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Transformation failed: {e}")
            raise
    
    def _apply_effects_without_interaction(self, image: Image.Image,
                                         node_states: Dict[str, float]) -> Image.Image:
        """相互作用なしでエフェクトを適用"""
        effect_params = self.node_mapper.map_node_states_to_effects(node_states)
        
        if not effect_params:
            return image
            
        current_image = image
        
        # 現在実装されているエフェクトのみ適用
        for param in effect_params:
            if param.effect_name in ["density_effect", "luminosity_effect", "chromaticity_effect"]:
                try:
                    if param.effect_name == "density_effect":
                        current_image = AppearanceEffects.density_effect(
                            current_image, param.intensity, param.node_state
                        )
                    elif param.effect_name == "luminosity_effect":
                        current_image = AppearanceEffects.luminosity_effect(
                            current_image, param.intensity, param.node_state
                        )
                    elif param.effect_name == "chromaticity_effect":
                        current_image = AppearanceEffects.chromaticity_effect(
                            current_image, param.intensity, param.node_state
                        )
                        
                    if self.current_session:
                        self.current_session.effects_applied.append(param.effect_name)
                        
                except Exception as e:
                    if self.debug_mode:
                        print(f"Warning: Failed to apply {param.effect_name}: {e}")
                    continue
        
        return current_image
    
    def apply_dimensional_focus(self, image: Image.Image,
                              node_states: Dict[str, float],
                              target_dimension: str,
                              focus_intensity: float = 0.8) -> Image.Image:
        """
        特定次元への集中エフェクト
        
        Args:
            image: 入力画像
            node_states: ノード状態値
            target_dimension: 対象次元 ("appearance", "intentional", etc.)
            focus_intensity: 集中強度
            
        Returns:
            次元集中エフェクトが適用された画像
        """
        # 対象次元のノードのみを強調
        focused_states = {}
        
        for node_name, value in node_states.items():
            if node_name.startswith(target_dimension + "_"):
                # 対象次元のノードを強調
                focused_states[node_name] = min(1.0, value * (1 + focus_intensity))
            else:
                # その他のノードを抑制
                focused_states[node_name] = value * (1 - focus_intensity * 0.5)
        
        return self.apply_phenomenological_transformation(
            image, focused_states, "layered", True
        )
    
    def create_phenomenological_blend(self, images: List[Image.Image],
                                    node_states_list: List[Dict[str, float]],
                                    blend_weights: Optional[List[float]] = None) -> Image.Image:
        """
        複数画像の現象学的ブレンド
        
        Args:
            images: 入力画像リスト
            node_states_list: 各画像のノード状態値リスト
            blend_weights: ブレンド重み（省略時は均等）
            
        Returns:
            ブレンドされた画像
        """
        if len(images) != len(node_states_list):
            raise ValueError("Images and node_states_list must have same length")
        
        if blend_weights is None:
            blend_weights = [1.0 / len(images)] * len(images)
        elif len(blend_weights) != len(images):
            raise ValueError("Blend weights must match number of images")
        
        # 各画像に現象学的変換を適用
        transformed_images = []
        for image, node_states in zip(images, node_states_list):
            transformed = self.apply_phenomenological_transformation(
                image, node_states, "parallel", True
            )
            transformed_images.append(transformed)
        
        # 重み付きブレンド
        return self._weighted_blend_images(transformed_images, blend_weights)
    
    def _weighted_blend_images(self, images: List[Image.Image], 
                              weights: List[float]) -> Image.Image:
        """重み付き画像ブレンド"""
        # 重みの正規化
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        
        # 最初の画像をベースに設定
        base_array = np.array(images[0]).astype(np.float32) * normalized_weights[0]
        
        # 残りの画像を重み付きで加算
        for image, weight in zip(images[1:], normalized_weights[1:]):
            image_array = np.array(image).astype(np.float32)
            base_array += image_array * weight
        
        result_array = np.clip(base_array, 0, 255).astype(np.uint8)
        return Image.fromarray(result_array)
    
    def analyze_phenomenological_state(self, node_states: Dict[str, float]) -> Dict[str, Any]:
        """
        現象学的状態の分析
        
        Args:
            node_states: ノード状態値
            
        Returns:
            分析結果
        """
        analysis = {
            "dimensional_analysis": {},
            "dominant_nodes": [],
            "philosophical_interpretation": {},
            "recommended_effects": []
        }
        
        # 次元別分析
        dimensions = ["appearance", "intentional", "temporal", "synesthetic", 
                     "ontological", "semantic", "conceptual", "being", "certainty"]
        
        for dimension in dimensions:
            dim_nodes = [k for k in node_states.keys() if k.startswith(dimension + "_")]
            if dim_nodes:
                dim_values = [node_states[k] for k in dim_nodes]
                analysis["dimensional_analysis"][dimension] = {
                    "average": np.mean(dim_values),
                    "max": np.max(dim_values),
                    "dominant_node": dim_nodes[np.argmax(dim_values)],
                    "activity_level": "high" if np.mean(dim_values) > 0.6 else "medium" if np.mean(dim_values) > 0.3 else "low"
                }
        
        # 支配的ノードの特定
        sorted_nodes = sorted(node_states.items(), key=lambda x: x[1], reverse=True)
        analysis["dominant_nodes"] = sorted_nodes[:5]  # 上位5ノード
        
        # 哲学的解釈
        analysis["philosophical_interpretation"] = self._generate_philosophical_interpretation(node_states)
        
        # 推奨エフェクト
        effect_params = self.node_mapper.map_node_states_to_effects(node_states)
        analysis["recommended_effects"] = [
            {"effect": p.effect_name, "intensity": p.intensity, "node": p.node_state}
            for p in effect_params[:3]  # 上位3つ
        ]
        
        return analysis
    
    def _generate_philosophical_interpretation(self, node_states: Dict[str, float]) -> Dict[str, str]:
        """哲学的解釈の生成"""
        interpretation = {}
        
        # 現出様式の解釈
        appearance_avg = np.mean([v for k, v in node_states.items() if k.startswith("appearance_")])
        if appearance_avg > 0.7:
            interpretation["appearance"] = "高度な現象学的充実 - 意識の志向的作用が強く集中している状態"
        elif appearance_avg > 0.4:
            interpretation["appearance"] = "中程度の現出 - バランスの取れた現象学的現れ"
        else:
            interpretation["appearance"] = "低い現出度 - 地平的背景への沈降傾向"
        
        # 存在論的解釈
        ontological_avg = np.mean([v for k, v in node_states.items() if k.startswith("ontological_")])
        if ontological_avg > 0.6:
            interpretation["ontological"] = "強い存在論的密度 - 存在者の明確な現前性"
        else:
            interpretation["ontological"] = "存在論的希薄化 - 存在忘却の傾向"
        
        # 時間的解釈  
        temporal_avg = np.mean([v for k, v in node_states.items() if k.startswith("temporal_")])
        if node_states.get("temporal_decay", 0) > 0.5:
            interpretation["temporal"] = "頽落的時間性 - ハイデガー的な非本来的時間への沈降"
        elif temporal_avg > 0.5:
            interpretation["temporal"] = "動的時間性 - 生きられた時間の活性化"
        else:
            interpretation["temporal"] = "静的時間性 - 時間意識の低下"
        
        return interpretation
    
    def finish_editing_session(self) -> Optional[EditingSession]:
        """編集セッションを終了"""
        if self.current_session is None:
            return None
            
        finished_session = self.current_session
        self.session_history.append(finished_session)
        self.current_session = None
        
        if self.debug_mode:
            print(f"📋 Finished session: {finished_session.session_id}")
            print(f"   Total effects applied: {len(finished_session.effects_applied)}")
            print(f"   Total processing time: {finished_session.total_processing_time:.3f}s")
            
        return finished_session
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """セッション統計の取得"""
        if not self.session_history:
            return {"message": "No completed sessions"}
        
        total_sessions = len(self.session_history)
        total_effects = sum(len(s.effects_applied) for s in self.session_history)
        total_time = sum(s.total_processing_time for s in self.session_history)
        avg_time_per_session = total_time / total_sessions
        
        # 最も使用されたエフェクト
        all_effects = []
        for session in self.session_history:
            all_effects.extend(session.effects_applied)
        
        from collections import Counter
        effect_counts = Counter(all_effects)
        most_used_effects = effect_counts.most_common(5)
        
        return {
            "total_sessions": total_sessions,
            "total_effects_applied": total_effects,
            "total_processing_time": f"{total_time:.3f}s",
            "average_time_per_session": f"{avg_time_per_session:.3f}s",
            "most_used_effects": most_used_effects,
            "average_effects_per_session": total_effects / total_sessions if total_sessions > 0 else 0
        }
    
    def export_session_data(self, filepath: str, include_node_states: bool = True):
        """セッションデータのエクスポート"""
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_sessions": len(self.session_history),
            "sessions": []
        }
        
        for session in self.session_history:
            session_data = {
                "session_id": session.session_id,
                "start_time": session.start_time.isoformat(),
                "original_image_size": session.original_image_size,
                "effects_applied": session.effects_applied,
                "composition_mode": session.composition_mode,
                "total_processing_time": session.total_processing_time
            }
            
            if include_node_states:
                session_data["node_states_history"] = session.node_states_history
                
            export_data["sessions"].append(session_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
            
        if self.debug_mode:
            print(f"📁 Session data exported to: {filepath}")
    
    def set_debug_mode(self, enabled: bool):
        """デバッグモードの設定"""
        self.debug_mode = enabled
        self.compositor.debug_mode = enabled if hasattr(self.compositor, 'debug_mode') else False
        
    def clear_cache(self):
        """エフェクトキャッシュのクリア"""
        self.effect_cache.clear()
        if self.debug_mode:
            print("🧹 Effect cache cleared")