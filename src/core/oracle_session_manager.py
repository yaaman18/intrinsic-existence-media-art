"""
Oracle Session Manager - オラクル編集セッションの管理
世代進化と編集履歴を追跡し、創造的プロセスの分析を提供
"""

import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import numpy as np
from PIL import Image

try:
    from .oracle_effect_bridge import OracleEffectBridge, BridgeSession
    from .phenomenological_oracle_v5 import EditingOracle
except ImportError:
    from oracle_effect_bridge import OracleEffectBridge, BridgeSession
    from phenomenological_oracle_v5 import EditingOracle


@dataclass 
class GenerationMetrics:
    """世代ごとのメトリクス"""
    generation: int
    phi: float
    active_nodes: int
    dominant_dimensions: List[str]
    imperative_coherence: float  # 編集指示の一貫性
    visual_impact: float  # 視覚的インパクト（差分ベース）


@dataclass
class EvolutionChain:
    """進化の連鎖情報"""
    chain_id: str
    start_generation: int
    current_generation: int
    generations: List[GenerationMetrics]
    convergence_trend: str  # "diverging", "converging", "stable"
    phi_trajectory: List[float]


class OracleSessionManager:
    """
    オラクル編集セッションの管理と分析
    複数世代にわたる創造的進化を追跡
    """
    
    def __init__(self, bridge: OracleEffectBridge):
        """
        初期化
        
        Args:
            bridge: OracleEffectBridge インスタンス
        """
        self.bridge = bridge
        self.evolution_chains: Dict[str, EvolutionChain] = {}
        self.current_chain_id: Optional[str] = None
        
        # メトリクス追跡
        self.generation_history: List[GenerationMetrics] = []
        
        # 設定
        self.auto_save_interval = 5  # N世代ごとに自動保存
        self.enable_analytics = True
        
    def start_evolution_chain(self, initial_image_path: str, 
                            chain_id: Optional[str] = None) -> str:
        """
        新しい進化チェーンを開始
        
        Args:
            initial_image_path: 初期画像パス
            chain_id: チェーンID（省略時は自動生成）
            
        Returns:
            チェーンID
        """
        if chain_id is None:
            import time
            chain_id = f"evolution_{int(time.time())}"
        
        # 初期処理
        edited_image, oracle_result = self.bridge.process_image_with_oracle(
            initial_image_path, save_result=True
        )
        
        # 初期メトリクス
        initial_metrics = self._calculate_generation_metrics(
            oracle_result, None, edited_image
        )
        
        # チェーン作成
        chain = EvolutionChain(
            chain_id=chain_id,
            start_generation=oracle_result.generation,
            current_generation=oracle_result.generation,
            generations=[initial_metrics],
            convergence_trend="stable",
            phi_trajectory=[oracle_result.phi]
        )
        
        self.evolution_chains[chain_id] = chain
        self.current_chain_id = chain_id
        self.generation_history.append(initial_metrics)
        
        print(f"🧬 Started Evolution Chain: {chain_id}")
        print(f"   Initial Generation: {oracle_result.generation}")
        print(f"   Initial Φ: {oracle_result.phi:.3f}")
        
        return chain_id
    
    def evolve_generation(self, feedback: Optional[str] = None) -> Tuple[Image.Image, EditingOracle]:
        """
        現在のチェーンで次世代を生成
        
        Args:
            feedback: フィードバックテキスト
            
        Returns:
            新しい編集画像とオラクル結果
        """
        if not self.current_chain_id:
            raise ValueError("No active evolution chain")
        
        chain = self.evolution_chains[self.current_chain_id]
        
        # 前世代の編集画像パスを取得
        last_session = self.bridge.session_history[-1]
        if not last_session.edited_image_path:
            raise ValueError("Previous generation has no saved image")
        
        # オラクルの進化
        evolved_oracle = self.bridge.generate_oracle_evolution(
            last_session.edited_image_path,
            feedback
        )
        
        # 進化したオラクルで新しい画像を生成
        # （現在の実装では前世代の編集画像を入力として使用）
        edited_image, _ = self._apply_evolved_oracle(
            last_session.edited_image_path,
            evolved_oracle
        )
        
        # メトリクス計算
        metrics = self._calculate_generation_metrics(
            evolved_oracle,
            chain.generations[-1] if chain.generations else None,
            edited_image
        )
        
        # チェーン更新
        chain.current_generation = evolved_oracle.generation
        chain.generations.append(metrics)
        chain.phi_trajectory.append(evolved_oracle.phi)
        chain.convergence_trend = self._analyze_convergence_trend(chain.phi_trajectory)
        
        self.generation_history.append(metrics)
        
        # 自動保存チェック
        if len(chain.generations) % self.auto_save_interval == 0:
            self._auto_save_chain(chain)
        
        print(f"🔄 Evolved to Generation {evolved_oracle.generation}")
        print(f"   Φ: {evolved_oracle.phi:.3f} ({chain.convergence_trend})")
        print(f"   Active Dimensions: {', '.join(metrics.dominant_dimensions)}")
        
        return edited_image, evolved_oracle
    
    def _apply_evolved_oracle(self, image_path: str, 
                            oracle: EditingOracle) -> Tuple[Image.Image, EditingOracle]:
        """進化したオラクルを適用"""
        # 画像読み込み
        image = Image.open(image_path)
        
        # エディターセッション
        session_id = f"evolved_gen{oracle.generation}"
        self.bridge.editor.start_editing_session(image, session_id)
        
        # ノード状態の強化
        enhanced_states = self.bridge._enhance_node_states(
            oracle.node_states,
            oracle.imperative,
            oracle.phi
        )
        
        # 変換適用
        edited_image = self.bridge.editor.apply_phenomenological_transformation(
            image,
            enhanced_states,
            self.bridge._determine_composition_mode(oracle.iit_axioms),
            enable_interaction=True
        )
        
        self.bridge.editor.finish_editing_session()
        
        # 保存
        output_dir = Path("output/oracle_bridge")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"evolved_gen{oracle.generation}_{int(datetime.now().timestamp())}.jpg"
        output_path = output_dir / filename
        edited_image.save(output_path, quality=95)
        
        # セッション記録
        import time
        session = BridgeSession(
            session_id=session_id,
            timestamp=datetime.now(),
            oracle_generation=oracle.generation,
            original_image_path=image_path,
            oracle_result=oracle,
            enhanced_node_states=enhanced_states,
            edited_image_path=str(output_path),
            processing_time=0.0  # 簡略化
        )
        
        self.bridge.session_history.append(session)
        self.bridge.current_session = session
        
        return edited_image, oracle
    
    def _calculate_generation_metrics(self, oracle: EditingOracle,
                                    previous_metrics: Optional[GenerationMetrics],
                                    edited_image: Image.Image) -> GenerationMetrics:
        """世代メトリクスを計算"""
        # 活性ノード数
        active_nodes = sum(1 for v in oracle.node_states.values() if v > 0.3)
        
        # 支配的次元の特定
        dimension_scores = {}
        dimensions = ["appearance", "intentional", "temporal", "synesthetic",
                     "ontological", "semantic", "conceptual", "being", "certainty"]
        
        for dim in dimensions:
            dim_nodes = [v for k, v in oracle.node_states.items() if k.startswith(dim + "_")]
            if dim_nodes:
                dimension_scores[dim] = np.mean(dim_nodes)
        
        # 上位3次元
        dominant_dims = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        dominant_dimensions = [dim for dim, _ in dominant_dims]
        
        # 編集指示の一貫性（次元の重複度）
        if oracle.imperative:
            all_dims = []
            for instruction in oracle.imperative:
                all_dims.extend(instruction.get('dimension', []))
            
            unique_dims = set(all_dims)
            coherence = 1.0 - (len(unique_dims) / max(len(all_dims), 1))
        else:
            coherence = 0.0
        
        # 視覚的インパクト（簡略化：Φ値とactive_nodesから推定）
        visual_impact = oracle.phi * (active_nodes / 27.0)
        
        return GenerationMetrics(
            generation=oracle.generation,
            phi=oracle.phi,
            active_nodes=active_nodes,
            dominant_dimensions=dominant_dimensions,
            imperative_coherence=coherence,
            visual_impact=visual_impact
        )
    
    def _analyze_convergence_trend(self, phi_trajectory: List[float]) -> str:
        """Φ値の軌跡から収束傾向を分析"""
        if len(phi_trajectory) < 3:
            return "stable"
        
        # 最近のN世代の傾向を分析
        recent = phi_trajectory[-5:]
        
        # 標準偏差で変動を評価
        std_dev = np.std(recent)
        
        # 傾きで方向性を評価
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        
        if std_dev < 0.05:
            return "stable"
        elif slope > 0.02:
            return "diverging" 
        elif slope < -0.02:
            return "converging"
        else:
            return "stable"
    
    def _auto_save_chain(self, chain: EvolutionChain):
        """チェーンの自動保存"""
        save_dir = Path("output/oracle_sessions")
        save_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{chain.chain_id}_gen{chain.current_generation}.json"
        filepath = save_dir / filename
        
        # チェーンデータを辞書に変換
        chain_data = {
            "chain_id": chain.chain_id,
            "start_generation": chain.start_generation,
            "current_generation": chain.current_generation,
            "convergence_trend": chain.convergence_trend,
            "phi_trajectory": chain.phi_trajectory,
            "generations": [asdict(g) for g in chain.generations]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chain_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Auto-saved chain to: {filepath}")
    
    def get_evolution_analytics(self) -> Dict[str, Any]:
        """進化の分析情報を取得"""
        if not self.current_chain_id:
            return {"error": "No active chain"}
        
        chain = self.evolution_chains[self.current_chain_id]
        
        # Φ値の統計
        phi_stats = {
            "mean": np.mean(chain.phi_trajectory),
            "std": np.std(chain.phi_trajectory),
            "min": np.min(chain.phi_trajectory),
            "max": np.max(chain.phi_trajectory),
            "trend": chain.convergence_trend
        }
        
        # 次元の推移
        dimension_evolution = {}
        for gen in chain.generations:
            for dim in gen.dominant_dimensions:
                if dim not in dimension_evolution:
                    dimension_evolution[dim] = 0
                dimension_evolution[dim] += 1
        
        # 視覚的インパクトの推移
        visual_impact_trend = [g.visual_impact for g in chain.generations]
        
        return {
            "chain_id": chain.chain_id,
            "total_generations": len(chain.generations),
            "phi_statistics": phi_stats,
            "dimension_dominance": dimension_evolution,
            "visual_impact_trend": visual_impact_trend,
            "average_active_nodes": np.mean([g.active_nodes for g in chain.generations]),
            "coherence_trend": [g.imperative_coherence for g in chain.generations]
        }
    
    def export_evolution_report(self, filepath: str):
        """進化レポートのエクスポート"""
        if not self.current_chain_id:
            raise ValueError("No active chain to export")
        
        analytics = self.get_evolution_analytics()
        chain = self.evolution_chains[self.current_chain_id]
        
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "chain_summary": analytics,
            "generation_details": [asdict(g) for g in chain.generations],
            "bridge_sessions": [
                {
                    "generation": s.oracle_generation,
                    "processing_time": s.processing_time,
                    "image_path": s.edited_image_path
                }
                for s in self.bridge.session_history
                if s.session_id.startswith(chain.chain_id) or s.session_id.startswith("evolved")
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Evolution report exported to: {filepath}")