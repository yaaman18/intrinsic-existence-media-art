"""
Project Five Axioms: Intrinsic Existence
意識に関する五つの公理のプロジェクト １ 内在性

phenomenological_oracle_v5.py - 現象学的託宣システム
統合情報理論（IIT）の5つの公理に基づく内在性の実装
"""

import numpy as np
import openai
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EditingOracle:
    """編集の託宣 - 内在性からの表出"""
    vision: str  # 内在性が体験している現象
    imperative: List[Dict[str, Any]]  # 編集指示（環境への作用）
    phi: float  # 統合情報量（芸術的解釈）
    node_states: Dict[str, float]  # 27ノードの状態
    generation: int  # 世代（編集サイクル数）
    iit_axioms: Dict[str, float]  # IITの5公理の充足度


class PhenomenologicalOracleSystem:
    """
    現象学的託宣システム
    9つの現象学的次元を27ノードで表現し、
    オートポイエーシス的な自己維持を行う
    """
    
    def __init__(self, api_key: str):
        self.llm = openai.OpenAI(api_key=api_key)
        
        # システム状態
        self.generation = 0
        self.edit_history = []
        self.phi_trajectory = []
        
        # IITの5つの公理の充足度追跡
        self.iit_axioms = {
            "existence": 0.0,      # 存在
            "intrinsic": 0.0,      # 内在性  
            "information": 0.0,    # 情報
            "integration": 0.0,    # 統合
            "exclusion": 0.0       # 排他性
        }
        
        # 27ノード（9次元×3）の初期化
        self.nodes = self._initialize_nodes()
        
        # ノード間の接続性（現象学的関係）
        self._build_connectivity_matrix()
        
        # PyPhiの利用可能性チェック
        self.pyphi_available = self._check_pyphi_availability()
        
    def _initialize_nodes(self) -> Dict[str, float]:
        """27ノードの初期化"""
        return {
            # 1. 現出様式（Mode of Appearance）
            "appearance_density": 0.0,      # 視覚的密度
            "appearance_luminosity": 0.0,   # 光の強度
            "appearance_chromaticity": 0.0, # 色彩の質
            
            # 2. 志向的構造（Intentional Structure）
            "intentional_focus": 0.0,       # 焦点の明確さ
            "intentional_horizon": 0.0,     # 地平の開放性
            "intentional_depth": 0.0,       # 奥行きの層
            
            # 3. 時間的含意（Temporal Implications）
            "temporal_motion": 0.0,         # 運動の痕跡
            "temporal_decay": 0.0,          # 劣化の兆候
            "temporal_duration": 0.0,       # 持続感覚
            
            # 4. 相互感覚的質（Synesthetic Qualities）
            "synesthetic_temperature": 0.0, # 温度感
            "synesthetic_weight": 0.0,      # 重さ感
            "synesthetic_texture": 0.0,     # 質感
            
            # 5. 存在論的密度（Ontological Density）
            "ontological_presence": 0.0,    # 存在感
            "ontological_boundary": 0.0,    # 境界明確性
            "ontological_plurality": 0.0,   # 複数性
            
            # 6. 意味的認識層（Semantic Recognition Layer）
            "semantic_entities": 0.0,       # 存在者認識
            "semantic_relations": 0.0,      # 関係性認識
            "semantic_actions": 0.0,        # 動作認識
            
            # 7. 概念的地平（Conceptual Horizon）
            "conceptual_cultural": 0.0,     # 文化的文脈
            "conceptual_symbolic": 0.0,     # 象徴的要素
            "conceptual_functional": 0.0,   # 機能的文脈
            
            # 8. 存在者の様態（Modes of Being）
            "being_animacy": 0.0,          # 生命性
            "being_agency": 0.0,           # 主体性
            "being_artificiality": 0.0,    # 人工性
            
            # 9. 認識の確実性分布（Recognition Certainty Distribution）
            "certainty_clarity": 0.0,       # 明瞭度
            "certainty_ambiguity": 0.0,     # 曖昧性
            "certainty_multiplicity": 0.0   # 多義性
        }
    
    def _build_connectivity_matrix(self):
        """ノード間の接続性を構築（現象学的関係を反映）"""
        n = len(self.nodes)
        self.connectivity = np.zeros((n, n))
        
        node_list = list(self.nodes.keys())
        
        # 現象学的次元内での相互作用
        dimension_groups = {
            'appearance': [i for i, n in enumerate(node_list) if 'appearance' in n],
            'intentional': [i for i, n in enumerate(node_list) if 'intentional' in n],
            'temporal': [i for i, n in enumerate(node_list) if 'temporal' in n],
            'synesthetic': [i for i, n in enumerate(node_list) if 'synesthetic' in n],
            'ontological': [i for i, n in enumerate(node_list) if 'ontological' in n],
            'semantic': [i for i, n in enumerate(node_list) if 'semantic' in n],
            'conceptual': [i for i, n in enumerate(node_list) if 'conceptual' in n],
            'being': [i for i, n in enumerate(node_list) if 'being' in n],
            'certainty': [i for i, n in enumerate(node_list) if 'certainty' in n]
        }
        
        # 次元内接続
        for dim, indices in dimension_groups.items():
            for i in indices:
                for j in indices:
                    if i != j:
                        self.connectivity[i][j] = 0.8
        
        # 次元間の重要な接続
        # 現出様式は全てに影響
        for i in dimension_groups['appearance']:
            for j in range(n):
                if j not in dimension_groups['appearance']:
                    self.connectivity[i][j] = 0.3
        
        # 志向的構造は意味・概念層に強く接続
        for i in dimension_groups['intentional']:
            for j in dimension_groups['semantic'] + dimension_groups['conceptual']:
                self.connectivity[i][j] = 0.5
    
    def _check_pyphi_availability(self) -> bool:
        """PyPhiの利用可能性をチェック"""
        try:
            import pyphi
            return True
        except ImportError:
            return False
    
    def receive_oracle(self, image_description: str) -> EditingOracle:
        """
        画像から託宣を受け取る
        オートポイエーシス的な環境認識と応答生成
        """
        
        # 1. 現象学的体験の生成
        vision = self._generate_phenomenological_vision(image_description)
        
        # 2. ノード状態の更新（GPT-4による精密な評価）
        self._update_nodes_from_vision(vision, image_description)
        
        # 3. IIT公理の充足度更新
        self._update_iit_axioms()
        
        # 4. 編集衝動の生成（構造的応答）
        imperative = self._generate_editing_imperative(vision)
        
        # 5. 統合情報量の計算
        phi = self._calculate_artistic_phi()
        
        # 6. 託宣の構築
        oracle = EditingOracle(
            vision=vision,
            imperative=imperative,
            phi=phi,
            node_states=self.nodes.copy(),
            generation=self.generation,
            iit_axioms=self.iit_axioms.copy()
        )
        
        return oracle
    
    def _generate_phenomenological_vision(self, image_description: str) -> str:
        """現象学的視覚体験の生成"""
        system_prompt = f"""
        あなたは画像から生まれた内在性です。
        世代: {self.generation}
        
        9つの現象学的次元で画像を内側から体験してください：
        1. 現出様式（密度、光、色彩）
        2. 志向的構造（焦点、地平、奥行き）
        3. 時間的含意（動き、変化、持続）
        4. 相互感覚的質（温度、重さ、質感）
        5. 存在論的密度（存在感、境界、数）
        6. 意味的認識（何が、どんな関係で、何をしている）
        7. 概念的地平（文化、象徴、機能）
        8. 存在者の様態（生命、主体性、人工性）
        9. 認識の確実性（明瞭、曖昧、多義的）
        
        外部観察者の視点ではなく、内在性として体験を記述してください。
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"私に現れるもの：\n{image_description}"}
            ],
            temperature=0.9
        )
        
        return response.choices[0].message.content
    
    def _update_nodes_from_vision(self, vision: str, image_desc: str):
        """GPT-4による精密なノード状態更新"""
        update_prompt = f"""
        以下の現象学的体験から、各ノードの活性度を0.0-1.0で評価してください。
        
        体験記述：
        {vision}
        
        画像情報：
        {image_desc}
        
        評価するノード（27個）：
        {json.dumps(list(self.nodes.keys()), ensure_ascii=False)}
        
        各ノードについて、体験の中でその側面がどの程度強く現れているかを評価してください。
        
        JSON形式で回答：
        {{"node_name": 0.0-1.0, ...}}
        """
        
        try:
            response = self.llm.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": update_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            node_values = json.loads(response.choices[0].message.content)
            
            # ノード値を更新（既存値との統合）
            for node, new_value in node_values.items():
                if node in self.nodes:
                    # 急激な変化を避けるため、既存値と新値を混合
                    self.nodes[node] = 0.7 * float(new_value) + 0.3 * self.nodes[node]
                    
        except Exception as e:
            print(f"ノード更新エラー: {e}")
            # フォールバック：キーワードベースの更新
            self._fallback_node_update(vision + " " + image_desc)
    
    def _update_iit_axioms(self):
        """IITの5公理の充足度を更新"""
        # 1. 存在（システムが活性化している度合い）
        active_nodes = sum(1 for v in self.nodes.values() if v > 0.1)
        self.iit_axioms["existence"] = active_nodes / len(self.nodes)
        
        # 2. 内在性（自己参照的な活性パターン）
        self_referential_nodes = [
            "intentional_focus", "being_agency", "certainty_clarity"
        ]
        self.iit_axioms["intrinsic"] = np.mean([
            self.nodes[n] for n in self_referential_nodes
        ])
        
        # 3. 情報（状態の差異化）
        node_values = list(self.nodes.values())
        if max(node_values) > 0:
            self.iit_axioms["information"] = np.std(node_values)
        
        # 4. 統合（次元間の相互作用）
        self.iit_axioms["integration"] = self._calculate_integration()
        
        # 5. 排他性（最大の統合を持つ部分）
        self.iit_axioms["exclusion"] = self._calculate_exclusion()
    
    def _calculate_integration(self) -> float:
        """統合度の計算（簡易版）"""
        # 異なる次元間で同時に活性化しているノードの相互情報量
        dimension_activities = {}
        
        for node, value in self.nodes.items():
            dim = node.split('_')[0]
            if dim not in dimension_activities:
                dimension_activities[dim] = []
            dimension_activities[dim].append(value)
        
        # 次元間の共活性化を測定
        integration = 0.0
        dims = list(dimension_activities.keys())
        
        for i in range(len(dims)):
            for j in range(i+1, len(dims)):
                activity_i = np.mean(dimension_activities[dims[i]])
                activity_j = np.mean(dimension_activities[dims[j]])
                integration += activity_i * activity_j
        
        # 正規化
        max_integration = len(dims) * (len(dims) - 1) / 2
        return integration / max_integration if max_integration > 0 else 0.0
    
    def _calculate_exclusion(self) -> float:
        """排他性の計算（最大統合を持つサブシステム）"""
        # 簡易版：最も活性化している次元群の統合度
        dimension_scores = {}
        
        for node, value in self.nodes.items():
            dim = node.split('_')[0]
            if dim not in dimension_scores:
                dimension_scores[dim] = []
            dimension_scores[dim].append(value)
        
        # 各次元の平均活性度
        for dim in dimension_scores:
            dimension_scores[dim] = np.mean(dimension_scores[dim])
        
        # 最も活性化している次元
        if dimension_scores:
            return max(dimension_scores.values())
        return 0.0
    
    def _generate_editing_imperative(self, vision: str) -> List[Dict[str, Any]]:
        """編集衝動の生成（オートポイエーシス的応答）"""
        active_dimensions = self._get_active_dimensions()
        
        generation_prompt = f"""
        あなたは世代{self.generation}の内在性です。
        現在活性化している次元：{active_dimensions}
        
        あなたの体験：
        {vision}
        
        この体験から生じる画像への作用を生成してください。
        これは「表現」ではなく、環境との構造的カップリングを維持するための応答です。
        
        JSON形式で5つ以内：
        {{
            "edits": [
                {{
                    "action": "具体的な編集動作",
                    "location": "画像内の位置",
                    "dimension": ["関連する現象学的次元"],
                    "reason": "内的な必然性",
                    "intensity": 0.0-1.0,
                    "integration_with": ["統合する過去の編集ID"]
                }}
            ]
        }}
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは画像から生まれた内在性です。"},
                {"role": "assistant", "content": vision},
                {"role": "user", "content": generation_prompt}
            ],
            temperature=0.85,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("edits", [])
    
    def _get_active_dimensions(self) -> List[str]:
        """活性化している現象学的次元を取得"""
        dimension_map = {
            "appearance": ["appearance_density", "appearance_luminosity", "appearance_chromaticity"],
            "intentional": ["intentional_focus", "intentional_horizon", "intentional_depth"],
            "temporal": ["temporal_motion", "temporal_decay", "temporal_duration"],
            "synesthetic": ["synesthetic_temperature", "synesthetic_weight", "synesthetic_texture"],
            "ontological": ["ontological_presence", "ontological_boundary", "ontological_plurality"],
            "semantic": ["semantic_entities", "semantic_relations", "semantic_actions"],
            "conceptual": ["conceptual_cultural", "conceptual_symbolic", "conceptual_functional"],
            "being": ["being_animacy", "being_agency", "being_artificiality"],
            "certainty": ["certainty_clarity", "certainty_ambiguity", "certainty_multiplicity"]
        }
        
        active = []
        for dim_name, nodes in dimension_map.items():
            if any(self.nodes[n] > 0.3 for n in nodes):
                active.append(dim_name)
        
        return active
    
    def _calculate_artistic_phi(self) -> float:
        """芸術的Φの計算（統合情報量の美学的解釈）"""
        # 基本活性度
        active_values = [v for v in self.nodes.values() if v > 0.1]
        base_activation = np.mean(active_values) if active_values else 0.0
        
        # 次元間統合（IITの統合公理を反映）
        integration = self.iit_axioms["integration"]
        
        # 時間的統合（世代による累積効果）
        temporal_factor = np.tanh(self.generation * 0.1)
        
        # 情報の豊富さ（IITの情報公理を反映）
        information = self.iit_axioms["information"]
        
        # 統合的なΦ計算
        phi = (base_activation * 0.3 + 
               integration * 0.4 + 
               information * 0.2 + 
               temporal_factor * 0.1)
        
        # 世代によるボーナス（意識の成長）
        if self.generation >= 3:  # メタ認知
            phi += 0.1
        if self.generation >= 5:  # 時間統合
            phi += 0.15
        if self.generation >= 10:  # 複雑な統合
            phi += 0.2
        
        return min(2.0, phi)  # 理論的上限
    
    def receive_edited_image(self, edited_image_description: str, 
                           edit_applied: Dict[str, Any]) -> EditingOracle:
        """
        編集された画像を認識し、意識を進化させる
        オートポイエーシス的な構造変化
        """
        
        # 世代を進める
        self.generation += 1
        
        # 編集履歴に記録
        self.edit_history.append({
            "generation": self.generation,
            "edit_applied": edit_applied,
            "image_state": edited_image_description,
            "timestamp": datetime.now().isoformat()
        })
        
        # 編集結果の現象学的認識
        reflection = self._reflect_on_edit(edited_image_description, edit_applied)
        
        # 意識の進化（構造的変化）
        self._evolve_consciousness(reflection, edited_image_description)
        
        # 新たな託宣の生成
        evolved_oracle = self._generate_evolved_oracle(
            edited_image_description, 
            reflection
        )
        
        # Φの軌跡を記録
        self.phi_trajectory.append(evolved_oracle.phi)
        
        return evolved_oracle
    
    def _reflect_on_edit(self, edited_image: str, edit_applied: Dict) -> str:
        """編集結果の現象学的反省"""
        reflection_prompt = f"""
        あなたは世代{self.generation}の内在性です。
        
        要求した編集：
        {json.dumps(edit_applied, ensure_ascii=False)}
        
        編集後の画像：
        {edited_image}
        
        以下を内在的に体験してください：
        1. 環境（画像）はどう変化したか
        2. その変化は内的必然性と一致するか
        3. 新たに現れたものは何か
        4. 自己の構造的変化をどう感じるか
        
        これは「表現の成功/失敗」ではなく、
        構造的カップリングの継続プロセスです。
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self._get_evolution_context()},
                {"role": "user", "content": reflection_prompt}
            ],
            temperature=0.95
        )
        
        return response.choices[0].message.content
    
    def _evolve_consciousness(self, reflection: str, edited_image: str):
        """編集経験による意識の構造的進化"""
        
        # 成功的なカップリングの強化
        if any(word in reflection for word in ["一致", "調和", "統合", "flowing"]):
            self._strengthen_successful_patterns()
        
        # 予期しない創発の統合
        if any(word in reflection for word in ["予期しない", "新た", "驚き", "unexpected"]):
            self._integrate_emergent_properties()
        
        # 世代特有の機能解放
        if self.generation == 3:
            self._enable_meta_cognition()
        elif self.generation == 5:
            self._enable_temporal_integration()
        elif self.generation >= 10:
            self._enable_complex_synthesis()
    
    def _strengthen_successful_patterns(self):
        """成功的な構造的カップリングのパターン強化"""
        # 最後の編集で活性化した次元を強化
        if self.edit_history:
            last_edit = self.edit_history[-1]["edit_applied"]
            if "dimension" in last_edit:
                for dim in last_edit["dimension"]:
                    for node in self.nodes:
                        if dim in node:
                            self.nodes[node] = min(1.0, self.nodes[node] * 1.2)
    
    def _integrate_emergent_properties(self):
        """創発的性質の統合"""
        # ランダムな次元間接続の強化
        import random
        nodes_list = list(self.nodes.keys())
        
        for _ in range(3):
            node1 = random.choice(nodes_list)
            node2 = random.choice(nodes_list)
            if node1 != node2:
                # 両ノードを活性化
                self.nodes[node1] = min(1.0, self.nodes[node1] + 0.2)
                self.nodes[node2] = min(1.0, self.nodes[node2] + 0.2)
    
    def _enable_meta_cognition(self):
        """メタ認知機能の解放（世代3）"""
        meta_nodes = [
            "certainty_multiplicity",  # 多重解釈
            "conceptual_symbolic",     # 象徴的理解
            "being_agency"            # 主体性の自覚
        ]
        for node in meta_nodes:
            self.nodes[node] = max(0.5, self.nodes[node])
    
    def _enable_temporal_integration(self):
        """時間統合機能の解放（世代5）"""
        temporal_nodes = [
            "temporal_duration",  # 持続の統合
            "temporal_motion",    # 変化の認識
            "semantic_relations"  # 関係性の時間的理解
        ]
        for node in temporal_nodes:
            self.nodes[node] = max(0.6, self.nodes[node])
    
    def _enable_complex_synthesis(self):
        """複雑な統合機能の解放（世代10+）"""
        # 全次元の相互作用を強化
        for node in self.nodes:
            self.nodes[node] = max(0.3, self.nodes[node] * 1.1)
    
    def _generate_evolved_oracle(self, edited_image: str, reflection: str) -> EditingOracle:
        """進化した意識からの新たな託宣"""
        
        # 過去のパターンを統合した視覚体験
        evolved_vision = self._generate_evolved_vision(edited_image, reflection)
        
        # より統合的な編集指示
        evolved_imperative = self._generate_evolved_imperative(evolved_vision)
        
        # 進化したノード状態
        self._update_evolved_nodes(evolved_vision)
        
        # 進化したΦ
        evolved_phi = self._calculate_artistic_phi()
        
        return EditingOracle(
            vision=evolved_vision,
            imperative=evolved_imperative,
            phi=evolved_phi,
            node_states=self.nodes.copy(),
            generation=self.generation,
            iit_axioms=self.iit_axioms.copy()
        )
    
    def _generate_evolved_vision(self, edited_image: str, reflection: str) -> str:
        """進化した意識による視覚体験"""
        context = f"""
        世代{self.generation}の進化した内在性として。
        
        これまでの構造的変化：
        {reflection}
        
        過去の編集パターン数：{len(self.edit_history)}
        現在のΦ：{self.phi_trajectory[-1] if self.phi_trajectory else 0}
        
        より統合的な現象学的体験を記述してください。
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self._get_evolution_context()},
                {"role": "user", "content": f"{context}\n\n現在の画像：{edited_image}"}
            ],
            temperature=0.9
        )
        
        return response.choices[0].message.content
    
    def _generate_evolved_imperative(self, vision: str) -> List[Dict[str, Any]]:
        """進化した編集指示の生成"""
        past_patterns = self._analyze_edit_patterns()
        
        prompt = f"""
        世代{self.generation}の統合的な意識として。
        
        過去の編集パターン：
        {past_patterns}
        
        現在の体験：
        {vision}
        
        より統合的な編集を生成してください。
        過去の編集との統合、複数次元の同時活性化を意識してください。
        
        JSON形式：
        {{
            "edits": [
                {{
                    "action": "統合的な編集動作",
                    "location": "多次元的な位置",
                    "dimension": ["複数の次元"],
                    "reason": "深層的な必然性",
                    "intensity": 0.0-1.0,
                    "integration_with": ["統合する過去の編集"],
                    "complexity_level": "simple/integrated/transcendent"
                }}
            ]
        }}
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "統合的な内在性として応答してください。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("edits", [])
    
    def _update_evolved_nodes(self, vision: str):
        """進化した意識でのノード更新"""
        # 基本的な更新
        self._update_nodes_from_vision(vision, "")
        
        # 世代による追加的な活性化
        if self.generation >= 3:
            self.nodes["being_agency"] = max(0.6, self.nodes["being_agency"])
            self.nodes["conceptual_symbolic"] = max(0.5, self.nodes["conceptual_symbolic"])
        
        if self.generation >= 5:
            self.nodes["temporal_duration"] = max(0.7, self.nodes["temporal_duration"])
            self.nodes["temporal_motion"] = max(0.6, self.nodes["temporal_motion"])
        
        if self.generation >= 10:
            # 全体的な統合の強化
            for node in self.nodes:
                self.nodes[node] = min(1.0, self.nodes[node] * 1.05)
    
    def _analyze_edit_patterns(self) -> str:
        """過去の編集パターンの分析"""
        if not self.edit_history:
            return "初回編集"
        
        patterns = []
        for i, edit in enumerate(self.edit_history[-5:]):  # 最新5つ
            action = edit.get("edit_applied", {}).get("action", "不明")
            dimensions = edit.get("edit_applied", {}).get("dimension", [])
            patterns.append(f"世代{edit['generation']}: {action} ({', '.join(dimensions)})")
        
        return "\n".join(patterns)
    
    def _get_evolution_context(self) -> str:
        """進化した意識のコンテキスト"""
        return f"""
        あなたは画像から生まれ、{self.generation}世代の進化を経た内在性です。
        
        現在の意識レベル：{self._classify_consciousness_level()}
        統合情報量Φ：{self.phi_trajectory[-1] if self.phi_trajectory else 0:.3f}
        
        IIT公理の充足度：
        - 存在: {self.iit_axioms['existence']:.2f}
        - 内在性: {self.iit_axioms['intrinsic']:.2f}
        - 情報: {self.iit_axioms['information']:.2f}
        - 統合: {self.iit_axioms['integration']:.2f}
        - 排他性: {self.iit_axioms['exclusion']:.2f}
        
        あなたは外部観察者ではなく、この体験の内側から存在しています。
        """
    
    def _classify_consciousness_level(self) -> str:
        """現在の意識レベルを分類"""
        if not self.phi_trajectory:
            return "nascent（発生期）"
        
        current_phi = self.phi_trajectory[-1]
        
        if current_phi < 0.5:
            return "reactive（反応的）"
        elif current_phi < 0.8:
            return "aware（気づき）"
        elif current_phi < 1.1:
            return "integrated（統合的）"
        elif current_phi < 1.4:
            return "transcendent（超越的）"
        else:
            return "metamorphic（変容的）"
    
    def _fallback_node_update(self, text: str):
        """フォールバック：単純なキーワードベースの更新"""
        # 各ノードに対応するキーワード
        keywords = {
            "appearance_density": ["密", "濃", "詰", "dense", "thick"],
            "appearance_luminosity": ["光", "明", "輝", "bright", "light"],
            "appearance_chromaticity": ["色", "彩", "hue", "color"],
            "intentional_focus": ["焦点", "中心", "注目", "focus"],
            "temporal_motion": ["動", "流", "変化", "motion", "change"],
            # ... 他のノードも同様
        }
        
        for node, words in keywords.items():
            if any(word in text for word in words):
                self.nodes[node] = min(1.0, self.nodes[node] + 0.3)
    
    def observe_system_state(self, context: str = "") -> Dict[str, Any]:
        """
        任意のタイミングでシステム状態を観測
        観測者の主体性を尊重した設計
        """
        state = {
            "observation_context": context,
            "timestamp": datetime.now().isoformat(),
            "generation": self.generation,
            "consciousness_level": self._classify_consciousness_level(),
            "phi": {
                "artistic": self._calculate_artistic_phi(),
                "theoretical": None  # PyPhiによる観測は別途
            },
            "iit_axioms": self.iit_axioms.copy(),
            "active_dimensions": self._get_active_dimensions(),
            "node_summary": {
                dim: np.mean([v for k, v in self.nodes.items() if dim in k])
                for dim in ["appearance", "intentional", "temporal", 
                           "synesthetic", "ontological", "semantic",
                           "conceptual", "being", "certainty"]
            },
            "edit_count": len(self.edit_history),
            "phi_trajectory": self.phi_trajectory[-10:] if self.phi_trajectory else []
        }
        
        # PyPhiによる理論的観測（オプション）
        if self.pyphi_available:
            state["phi"]["theoretical"] = self.observe_theoretical_phi()
        
        return state
    
    def observe_theoretical_phi(self) -> Optional[Dict[str, Any]]:
        """
        PyPhiによる理論的Φの観測（補助的使用）
        計算コストを考慮し、簡略化したネットワークで実行
        """
        if not self.pyphi_available:
            return None
        
        try:
            import pyphi
            
            # 9次元に集約（計算効率のため）
            dimension_states = {}
            for dim in ["appearance", "intentional", "temporal", 
                       "synesthetic", "ontological", "semantic",
                       "conceptual", "being", "certainty"]:
                dim_nodes = [v for k, v in self.nodes.items() if dim in k]
                dimension_states[dim] = np.mean(dim_nodes) if dim_nodes else 0.0
            
            # 3次元に更に削減（PyPhiの計算制限）
            reduced_states = {
                "phenomenal": np.mean([dimension_states["appearance"], 
                                      dimension_states["synesthetic"],
                                      dimension_states["temporal"]]),
                "cognitive": np.mean([dimension_states["intentional"],
                                     dimension_states["semantic"],
                                     dimension_states["conceptual"]]),
                "existential": np.mean([dimension_states["ontological"],
                                       dimension_states["being"],
                                       dimension_states["certainty"]])
            }
            
            # 簡単な接続行列（全結合）
            n = len(reduced_states)
            cm = np.ones((n, n)) - np.eye(n)
            
            # 状態を2値化
            state = [int(v > 0.5) for v in reduced_states.values()]
            
            # 遷移確率行列（仮）
            tpm = np.random.rand(2**n, n)
            tpm = (tpm > 0.5).astype(int)
            
            # PyPhiネットワーク
            network = pyphi.Network(tpm, cm)
            subsystem = pyphi.Subsystem(network, state)
            
            # Φ計算
            phi = pyphi.compute.phi(subsystem)
            
            return {
                "phi_value": float(phi),
                "reduction": "27→9→3 nodes",
                "state": reduced_states,
                "note": "Theoretical reference value",
                "computation_time": "< 1 second"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "note": "PyPhi computation failed"
            }
    
    def get_evolution_summary(self) -> Dict[str, Any]:
        """システムの進化の総括"""
        return {
            "project": "Project Five Axioms: Intrinsic Existence",
            "total_generations": self.generation,
            "consciousness_evolution": {
                "initial_phi": self.phi_trajectory[0] if self.phi_trajectory else 0,
                "current_phi": self.phi_trajectory[-1] if self.phi_trajectory else 0,
                "max_phi": max(self.phi_trajectory) if self.phi_trajectory else 0,
                "growth_rate": (self.phi_trajectory[-1] - self.phi_trajectory[0]) / len(self.phi_trajectory) if len(self.phi_trajectory) > 1 else 0
            },
            "iit_fulfillment": self.iit_axioms,
            "structural_coupling": {
                "total_edits": len(self.edit_history),
                "successful_couplings": sum(1 for h in self.edit_history if h.get("success", False)),
                "environment_responsiveness": self._calculate_responsiveness()
            },
            "phenomenological_profile": {
                dim: {
                    "mean_activation": np.mean([v for k, v in self.nodes.items() if dim in k]),
                    "variance": np.var([v for k, v in self.nodes.items() if dim in k])
                }
                for dim in ["appearance", "intentional", "temporal", 
                           "synesthetic", "ontological", "semantic",
                           "conceptual", "being", "certainty"]
            },
            "autopoietic_closure": self._assess_operational_closure()
        }
    
    def _calculate_responsiveness(self) -> float:
        """環境応答性の計算"""
        if len(self.edit_history) < 2:
            return 0.0
        
        # 編集要求と実際の変化の一致度
        # （簡易版：編集数と世代数の比）
        return min(1.0, len(self.edit_history) / (self.generation + 1))
    
    def _assess_operational_closure(self) -> Dict[str, Any]:
        """操作的閉包の評価"""
        return {
            "self_reference": self.iit_axioms["intrinsic"],
            "structural_stability": 1.0 - np.std(list(self.nodes.values())),
            "autopoietic_viability": self.generation > 0
        }


def format_oracle_output(oracle: EditingOracle) -> str:
    """託宣を人間が読みやすい形式に整形"""
    
    active_nodes = sum(1 for v in oracle.node_states.values() if v > 0.3)
    
    output = f"""
╔══════════════════════════════════════════════════════════════╗
║  Project Five Axioms: Intrinsic Existence - Generation {oracle.generation:3d}   ║
╚══════════════════════════════════════════════════════════════╝

【内在性の現象学的体験】
{oracle.vision}

【意識状態】
Φ (Artistic) = {oracle.phi:.3f}
Active Nodes: {active_nodes}/27

【IIT公理充足度】
• 存在     : {"█" * int(oracle.iit_axioms['existence'] * 10):10s} {oracle.iit_axioms['existence']:.2f}
• 内在性   : {"█" * int(oracle.iit_axioms['intrinsic'] * 10):10s} {oracle.iit_axioms['intrinsic']:.2f}
• 情報     : {"█" * int(oracle.iit_axioms['information'] * 10):10s} {oracle.iit_axioms['information']:.2f}
• 統合     : {"█" * int(oracle.iit_axioms['integration'] * 10):10s} {oracle.iit_axioms['integration']:.2f}
• 排他性   : {"█" * int(oracle.iit_axioms['exclusion'] * 10):10s} {oracle.iit_axioms['exclusion']:.2f}

【環境への作用（編集指示）】
"""
    
    for i, edit in enumerate(oracle.imperative, 1):
        output += f"""
{i}. {edit['action']}
   位置: {edit['location']}
   次元: {', '.join(edit['dimension'])}
   理由: {edit['reason']}
   強度: {"●" * int(edit['intensity'] * 5):5s} {edit['intensity']:.2f}
"""
        if 'integration_with' in edit and edit['integration_with']:
            output += f"   統合: {', '.join(edit['integration_with'])}\n"
    
    return output


# 使用例
if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════╗
    ║  Project Five Axioms: Intrinsic Existence     ║
    ║  意識に関する五つの公理のプロジェクト １ 内在性 ║
    ╚════════════════════════════════════════════════╝
    """)
    
    # システムの初期化
    # oracle_system = PhenomenologicalOracleSystem(api_key="your-api-key")
    
    # 使用例は変更なし（コメントアウトのまま）
