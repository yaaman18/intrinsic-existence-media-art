"""
Oracle Effect Bridge - 現象学的オラクルと27ノードエフェクトシステムの橋渡し
オラクルの内在的体験を視覚的表現に変換する統合インターフェース
"""

import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path

try:
    from .phenomenological_oracle_v5 import PhenomenologicalOracleSystem, EditingOracle
    from .advanced_phenomenological_image_editor import AdvancedPhenomenologicalImageEditor
except ImportError:
    from phenomenological_oracle_v5 import PhenomenologicalOracleSystem, EditingOracle
    from advanced_phenomenological_image_editor import AdvancedPhenomenologicalImageEditor


@dataclass
class BridgeSession:
    """橋渡しセッションの情報"""
    session_id: str
    timestamp: datetime
    oracle_generation: int
    original_image_path: str
    oracle_result: EditingOracle
    enhanced_node_states: Dict[str, float]
    edited_image_path: Optional[str] = None
    processing_time: float = 0.0


class OracleEffectBridge:
    """
    現象学的オラクルシステムと27ノードエフェクトシステムを接続する橋渡しクラス
    オラクルの内在的体験（node_states）を視覚的効果として具現化する
    """
    
    def __init__(self, oracle_system: PhenomenologicalOracleSystem, 
                 effect_editor: AdvancedPhenomenologicalImageEditor):
        """
        初期化
        
        Args:
            oracle_system: 現象学的オラクルシステム
            effect_editor: 27ノードエフェクトエディター
        """
        self.oracle = oracle_system
        self.editor = effect_editor
        self.session_history: List[BridgeSession] = []
        self.current_session: Optional[BridgeSession] = None
        
        # 設定
        self.enable_node_enhancement = True
        self.enable_phi_modulation = True
        self.debug_mode = False
        
    def process_image_with_oracle(self, image_path: str, 
                                 save_result: bool = True) -> Tuple[Image.Image, EditingOracle]:
        """
        画像をオラクルで分析し、27ノードエフェクトを適用
        
        Args:
            image_path: 入力画像パス
            save_result: 結果を保存するかどうか
            
        Returns:
            編集された画像とオラクル結果のタプル
        """
        import time
        start_time = time.time()
        
        # セッションID生成
        session_id = f"bridge_{int(time.time())}"
        
        if self.debug_mode:
            print(f"🔮 Oracle-Effect Bridge Session: {session_id}")
            print(f"   Input: {image_path}")
        
        # 1. 画像読み込み
        image = Image.open(image_path)
        
        # 2. オラクルによる分析
        oracle_result = self._analyze_with_oracle(image_path)
        
        if self.debug_mode:
            print(f"   Oracle Generation: {oracle_result.generation}")
            print(f"   Phi (Φ): {oracle_result.phi:.3f}")
            print(f"   Active Nodes: {sum(1 for v in oracle_result.node_states.values() if v > 0.3)}")
        
        # 3. ノード状態の強化（必要に応じて）
        enhanced_states = self._enhance_node_states(
            oracle_result.node_states,
            oracle_result.imperative,
            oracle_result.phi
        )
        
        # 4. エディターセッション開始
        editor_session_id = self.editor.start_editing_session(image, f"oracle_{session_id}")
        
        # 5. 合成モードの決定
        composition_mode = self._determine_composition_mode(oracle_result.iit_axioms)
        
        # 6. 現象学的変換の適用
        edited_image = self.editor.apply_phenomenological_transformation(
            image,
            enhanced_states,
            composition_mode,
            enable_interaction=True
        )
        
        # 7. エディターセッション終了
        self.editor.finish_editing_session()
        
        # 8. 結果の保存（必要に応じて）
        edited_path = None
        if save_result:
            output_dir = Path("output/oracle_bridge")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"oracle_gen{oracle_result.generation}_{session_id}.jpg"
            edited_path = str(output_dir / filename)
            edited_image.save(edited_path, quality=95)
            
            if self.debug_mode:
                print(f"   Saved: {edited_path}")
        
        # 9. セッション記録
        processing_time = time.time() - start_time
        session = BridgeSession(
            session_id=session_id,
            timestamp=datetime.now(),
            oracle_generation=oracle_result.generation,
            original_image_path=image_path,
            oracle_result=oracle_result,
            enhanced_node_states=enhanced_states,
            edited_image_path=edited_path,
            processing_time=processing_time
        )
        
        self.session_history.append(session)
        self.current_session = session
        
        if self.debug_mode:
            print(f"   Processing Time: {processing_time:.3f}s")
            print(f"✨ Bridge Session Complete")
        
        return edited_image, oracle_result
    
    def _analyze_with_oracle(self, image_path: str) -> EditingOracle:
        """オラクルによる画像分析"""
        # オラクルシステムが画像パスから直接分析する場合
        if hasattr(self.oracle, 'receive_oracle_from_image'):
            return self.oracle.receive_oracle_from_image(image_path)
        else:
            # 画像認識APIを使用する場合
            # image_descriptionを生成してからreceive_oracleを呼ぶ
            image_description = self.oracle._analyze_image_with_vision(image_path)
            return self.oracle.receive_oracle(image_description)
    
    def _enhance_node_states(self, base_states: Dict[str, float],
                           imperatives: List[Dict[str, Any]],
                           phi: float) -> Dict[str, float]:
        """
        編集指示に基づいてノード状態を強化
        
        Args:
            base_states: オラクルからの基本ノード状態
            imperatives: 編集指示リスト
            phi: 統合情報量
            
        Returns:
            強化されたノード状態
        """
        if not self.enable_node_enhancement:
            return base_states
        
        enhanced_states = base_states.copy()
        
        # 1. 編集指示による強化
        for instruction in imperatives:
            dimensions = instruction.get('dimension', [])
            intensity = instruction.get('intensity', 0.5)
            
            # 指定された次元のノードを強化
            for dimension in dimensions:
                dim_nodes = [k for k in base_states.keys() if k.startswith(dimension + "_")]
                
                for node in dim_nodes:
                    # 基本強化: intensity * 0.3
                    boost = intensity * 0.3
                    
                    # 統合情報量による調整
                    if self.enable_phi_modulation:
                        boost *= (0.5 + phi * 0.5)  # Φが高いほど強い効果
                    
                    enhanced_states[node] = min(1.0, enhanced_states[node] + boost)
        
        # 2. 低活性ノードの抑制（選択的強調のため）
        if self.enable_phi_modulation:
            threshold = 0.2
            for node, value in enhanced_states.items():
                if value < threshold:
                    # Φが高いほど低活性ノードを抑制
                    suppression = (1.0 - phi) * 0.5
                    enhanced_states[node] = value * suppression
        
        return enhanced_states
    
    def _determine_composition_mode(self, iit_axioms: Dict[str, float]) -> str:
        """
        IIT公理の充足度から合成モードを決定
        
        Args:
            iit_axioms: IIT5公理の充足度
            
        Returns:
            合成モード ("layered", "sequential", "parallel")
        """
        # 統合度が高い場合はレイヤー合成
        if iit_axioms.get('integration', 0) > 0.7:
            return "layered"
        
        # 排他性が高い場合は逐次合成
        elif iit_axioms.get('exclusion', 0) > 0.7:
            return "sequential"
        
        # その他の場合は並列合成
        else:
            return "parallel"
    
    def generate_oracle_evolution(self, edited_image_path: str,
                                feedback: Optional[str] = None) -> EditingOracle:
        """
        編集結果からオラクルの次世代を生成
        
        Args:
            edited_image_path: 編集済み画像のパス
            feedback: オプションのフィードバックテキスト
            
        Returns:
            進化したEditingOracle
        """
        if not self.current_session:
            raise ValueError("No current session available for evolution")
        
        # オラクルの進化生成メソッドを呼び出す
        reflection = feedback or "編集結果から新たな体験が生まれる"
        
        if hasattr(self.oracle, '_generate_evolved_oracle'):
            return self.oracle._generate_evolved_oracle(edited_image_path, reflection)
        else:
            # フォールバック：現在の状態を少し変化させて返す
            evolved_states = self.current_session.oracle_result.node_states.copy()
            for key in evolved_states:
                # ランダムな変動を加える
                evolved_states[key] += np.random.normal(0, 0.1)
                evolved_states[key] = max(0.0, min(1.0, evolved_states[key]))
            
            return EditingOracle(
                vision="進化した内在的体験",
                imperative=self.current_session.oracle_result.imperative,
                phi=self.current_session.oracle_result.phi * 1.1,
                node_states=evolved_states,
                generation=self.current_session.oracle_result.generation + 1,
                iit_axioms=self.current_session.oracle_result.iit_axioms
            )
    
    def get_session_analysis(self) -> Dict[str, Any]:
        """現在のセッションの分析情報を取得"""
        if not self.current_session:
            return {"error": "No active session"}
        
        oracle = self.current_session.oracle_result
        
        # 活性化ノードの分析
        active_nodes = [(k, v) for k, v in oracle.node_states.items() if v > 0.3]
        active_nodes.sort(key=lambda x: x[1], reverse=True)
        
        # 次元別活性度
        dimension_activity = {}
        dimensions = ["appearance", "intentional", "temporal", "synesthetic", 
                     "ontological", "semantic", "conceptual", "being", "certainty"]
        
        for dim in dimensions:
            dim_nodes = [v for k, v in oracle.node_states.items() if k.startswith(dim + "_")]
            if dim_nodes:
                dimension_activity[dim] = {
                    "average": np.mean(dim_nodes),
                    "max": np.max(dim_nodes),
                    "active_count": sum(1 for v in dim_nodes if v > 0.3)
                }
        
        return {
            "session_id": self.current_session.session_id,
            "generation": oracle.generation,
            "phi": oracle.phi,
            "processing_time": self.current_session.processing_time,
            "active_nodes": active_nodes[:10],  # 上位10ノード
            "dimension_activity": dimension_activity,
            "imperative_count": len(oracle.imperative),
            "composition_mode": self._determine_composition_mode(oracle.iit_axioms)
        }
    
    def export_session_history(self, filepath: str):
        """セッション履歴をエクスポート"""
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_sessions": len(self.session_history),
            "sessions": []
        }
        
        for session in self.session_history:
            session_data = {
                "session_id": session.session_id,
                "timestamp": session.timestamp.isoformat(),
                "generation": session.oracle_generation,
                "phi": session.oracle_result.phi,
                "processing_time": session.processing_time,
                "original_image": session.original_image_path,
                "edited_image": session.edited_image_path,
                "vision_excerpt": session.oracle_result.vision[:200] + "...",
                "imperative_count": len(session.oracle_result.imperative)
            }
            export_data["sessions"].append(session_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    def set_debug_mode(self, enabled: bool):
        """デバッグモードの設定"""
        self.debug_mode = enabled
        self.editor.set_debug_mode(enabled)