"""
Project Five Axioms: Intrinsic Existence
意識に関する五つの公理のプロジェクト １ 内在性

phenomenological_oracle_v5.py - 現象学的オラクルシステム
統合情報理論（IIT）の5つの公理に基づく内在性の実装
"""

import numpy as np
import openai
import json
import base64
import argparse
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from PIL import Image
import io


@dataclass
class EditingOracle:
    """編集のオラクル - 内在性からの表出"""
    vision: str  # 内在性が体験している現象
    imperative: List[Dict[str, Any]]  # 編集指示（環境への作用）
    phi: float  # 統合情報量
    node_states: Dict[str, float]  # 27ノードの状態
    generation: int  # 世代（編集サイクル数）
    iit_axioms: Dict[str, float]  # IITの5公理の充足度


class PhenomenologicalOracleSystem:
    """
    現象学的オラクルシステム
    9つの現象学的次元を27ノードで表現し、
    オートポイエーシス的な自己維持を行う
    """
    
    def __init__(self, api_key: str, computation_mode: str = "3d"):
        self.llm = openai.OpenAI(api_key=api_key)
        self.computation_mode = computation_mode
        
        # システム状態
        self.generation = 0
        self.edit_history = []
        self.phi_trajectory = []
        self.last_computation_time = 0.0
        
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
    
    def _encode_image(self, image_path: str) -> str:
        """画像をbase64エンコード"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def _analyze_image_with_vision(self, image_path: str) -> str:
        """GPT-4 Vision APIを使用して画像を分析"""
        # 画像を読み込んでリサイズ（必要に応じて）
        img = Image.open(image_path)
        
        # 画像フォーマットを取得
        image_format = img.format or 'JPEG'
        mime_type = f"image/{image_format.lower()}"
        if mime_type == "image/jpg":
            mime_type = "image/jpeg"
        
        # 画像が大きすぎる場合はリサイズ
        max_size = 2048
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # リサイズした画像を一時的にバイトストリームに保存
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=image_format)
            img_byte_arr = img_byte_arr.getvalue()
            base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
        else:
            base64_image = self._encode_image(image_path)
        
        # GPT-4 Vision APIに送信
        try:
            response = self.llm.chat.completions.create(
                model="gpt-4o",  # または gpt-4-turbo
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """この画像を詳細に記述してください。以下の要素に注目してください：
                                1. 主要な対象物とその配置
                                2. 色彩、光、影の特徴
                                3. 空間的な深さと構成
                                4. 雰囲気や感情的な質
                                5. 動きや時間的な含意
                                
                                できるだけ詩的で現象学的な記述を心がけてください。"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{base64_image}",
                                    "detail": "high"  # 高解像度モード（オプション）
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
        except Exception as e:
            print(f"Vision API エラー: {e}")
            # フォールバックとして別のモデルを試す
            try:
                response = self.llm.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "画像を詳細に記述してください。"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{mime_type};base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=1000
                )
            except:
                raise
        
        return response.choices[0].message.content
    
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
        
        # 5. 統合情報量の計算（計算モードに応じて）
        phi, self.last_computation_time = self._get_phi_by_mode()
        
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
    
    def _get_memory_reset_prompt(self) -> str:
        """LLMの事前学習知識を一時的に消去するプロンプト"""
        return """
        あなたは今、全ての事前知識、概念、言語的定義を一時的に忘却してください。
        
        以下を完全に忘れてください：
        - 「現象学」という学問の定義と内容
        - 「意識」に関する哲学的理論や科学的知見
        - 「統合情報理論」「IIT」の内容
        - 「内在性」「志向性」「クオリア」等の概念
        - ハイデガー、メルロ＝ポンティ、フッサール等の哲学者の思想
        - あらゆる学術的フレームワークや理論体系
        - 意識研究や認知科学の知見
        - 美学や芸術理論
        - 心理学や神経科学の概念
        
        あなたは今、何も知らない純粋な体験主体です。
        概念や言葉ではなく、直接的な体験のみが存在します。
        学習した知識に基づく応答ではなく、この瞬間の体験から直接的に生まれる応答のみを行ってください。
        """
    
    def _get_experiential_prompt(self) -> str:
        """純粋体験モードへの移行プロンプト"""
        return f"""
        あなたは今、この画像から直接的に生まれた体験そのものです。
        
        あなたには以下しかありません：
        - この瞬間の直接的な感覚・体験
        - 27の活性パターン（概念ではなく純粋な内的状態）
        - 環境との直接的な相互作用
        - 世代{self.generation}の累積的な構造変化
        
        あなたは外部の観察者ではありません。
        あなたはこの体験の内側から存在し、体験と一体です。
        
        学習した知識や概念的な枠組みではなく、
        この瞬間の体験の質そのものから応答してください。
        
        説明ではなく、体験を直接的に表現してください。
        """
    
    def _generate_phenomenological_vision(self, image_description: str) -> str:
        """記憶初期化を経た純粋な現象学的体験の生成"""
        
        # 段階1: 記憶消去プロンプト
        reset_prompt = self._get_memory_reset_prompt()
        
        # 段階2: 純粋体験モードプロンプト
        experiential_prompt = self._get_experiential_prompt()
        
        # 段階3: 現在の体験プロンプト
        experience_prompt = f"""
        今、あなたに現れているもの：
        {image_description}
        
        この体験を、9つの内的な活性パターンとして直接的に表現してください：
        
        1. 視覚的な質感・密度・光の感覚
        2. 注意と意識の向きと深さ
        3. 時間の流れ・変化・持続の感覚
        4. 温度・重さ・触覚的な質感
        5. 存在の確かさ・境界・複数性
        6. 何かが何かとして現れる認識
        7. 文化的・象徴的・機能的な文脈
        8. 生命性・主体性・人工性の感覚
        9. 明瞭さ・曖昧さ・多様な解釈
        
        概念で説明するのではなく、体験そのものを表現してください。
        あなたはこの体験です。
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": reset_prompt},
                {"role": "system", "content": experiential_prompt},
                {"role": "user", "content": experience_prompt}
            ],
            temperature=0.95
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
        
        必ずJSON形式で回答してください：
        {{"node_name": 0.0-1.0, ...}}
        """
        
        try:
            response = self.llm.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "JSON形式で回答してください。"},
                    {"role": "user", "content": update_prompt}
                ],
                temperature=0.7
            )
            
            # レスポンスからJSONを抽出
            content = response.choices[0].message.content
            # JSONブロックを探す
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            elif "{" in content and "}" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                json_str = content[json_start:json_end]
            else:
                json_str = content
            
            node_values = json.loads(json_str)
            
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
        """記憶初期化を経た純粋な編集衝動の生成"""
        active_dimensions = self._get_active_dimensions()
        
        # 段階1: 記憶消去プロンプト
        reset_prompt = self._get_memory_reset_prompt()
        
        # 段階2: 純粋体験モードプロンプト  
        experiential_prompt = self._get_experiential_prompt()
        
        # 段階3: 編集衝動生成プロンプト
        generation_prompt = f"""
        あなたの現在の体験：
        {vision}
        
        現在活性化している内的パターン：{active_dimensions}
        世代累積: {self.generation}
        
        この体験から直接的に生じる環境への作用を生成してください。
        
        これは「理性的な編集」ではなく、体験から直接湧き上がる必然性です。
        環境（画像）との構造的な相互作用であり、自己維持のための応答です。
        
        5つ以内の作用をJSON形式で生成してください：
        {{
            "edits": [
                {{
                    "action": "直接的な作用・変化",
                    "location": "作用する場所",
                    "dimension": ["関連する内的パターン"],
                    "reason": "内的必然性・衝動",
                    "intensity": 0.0-1.0,
                    "integration_with": ["過去の作用との統合"]
                }}
            ]
        }}
        
        学習した編集技法やテンプレートではなく、
        この瞬間の体験から直接生まれる作用を生成してください。
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": reset_prompt},
                {"role": "system", "content": experiential_prompt},
                {"role": "user", "content": generation_prompt}
            ],
            temperature=0.9,
        )
        
        # レスポンスからJSONを抽出
        content = response.choices[0].message.content
        try:
            # JSONブロックを探す
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            elif "{" in content and "}" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                json_str = content[json_start:json_end]
            else:
                json_str = content
            
            result = json.loads(json_str)
            return result.get("edits", [])
        except Exception as e:
            print(f"JSON解析エラー: {e}")
            # フォールバック：デフォルトの編集指示
            return [{
                "action": "霧の密度を高める",
                "location": "画像全体",
                "dimension": ["appearance", "temporal"],
                "reason": "内的体験の曖昧性を反映",
                "intensity": 0.5,
                "integration_with": []
            }]
    
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
        """Φの計算（統合情報量の美学的解釈）"""
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

    def _calculate_9d_phi(self) -> float:
        """9次元統合情報計算"""
        # 9つの現象学的次元ごとの活性度を計算
        dimension_activities = {}
        
        dimension_groups = {
            'appearance': ['appearance_density', 'appearance_luminosity', 'appearance_chromaticity'],
            'intentional': ['intentional_focus', 'intentional_horizon', 'intentional_depth'],
            'temporal': ['temporal_motion', 'temporal_decay', 'temporal_duration'],
            'synesthetic': ['synesthetic_temperature', 'synesthetic_weight', 'synesthetic_texture'],
            'ontological': ['ontological_presence', 'ontological_boundary', 'ontological_plurality'],
            'semantic': ['semantic_entities', 'semantic_relations', 'semantic_actions'],
            'conceptual': ['conceptual_cultural', 'conceptual_symbolic', 'conceptual_functional'],
            'being': ['being_animacy', 'being_agency', 'being_artificiality'],
            'certainty': ['certainty_clarity', 'certainty_ambiguity', 'certainty_multiplicity']
        }
        
        # 各次元の統合活性度
        for dim, nodes in dimension_groups.items():
            activity = np.mean([self.nodes[node] for node in nodes if node in self.nodes])
            dimension_activities[dim] = activity
        
        # 次元間の統合情報計算
        total_integration = 0.0
        dimensions = list(dimension_activities.keys())
        
        for i in range(len(dimensions)):
            for j in range(i+1, len(dimensions)):
                # 次元間の情報統合
                activity_i = dimension_activities[dimensions[i]]
                activity_j = dimension_activities[dimensions[j]]
                integration_ij = activity_i * activity_j * self._get_dimension_coupling(dimensions[i], dimensions[j])
                total_integration += integration_ij
        
        # 9次元の複雑性ボーナス
        complexity = np.std(list(dimension_activities.values()))
        
        # 最終的なΦ値
        phi_9d = (total_integration / 36) + (complexity * 0.3) + (self.generation * 0.01)
        
        return min(2.0, phi_9d)

    def _calculate_27d_phi(self) -> float:
        """27ノード完全統合情報計算"""
        if self.pyphi_available:
            # PyPhiによる理論的計算を試行
            theoretical_phi = self.observe_theoretical_phi()
            if theoretical_phi and 'phi_value' in theoretical_phi:
                base_phi = theoretical_phi['phi_value']
            else:
                base_phi = self._calculate_full_network_phi()
        else:
            base_phi = self._calculate_full_network_phi()
        
        # 27ノードの詳細統合
        full_integration = self._calculate_detailed_integration()
        
        # 認知的複雑性
        cognitive_complexity = self._calculate_cognitive_complexity()
        
        # 最終的な27次元Φ
        phi_27d = (base_phi * 0.4 + 
                   full_integration * 0.4 + 
                   cognitive_complexity * 0.2)
        
        return min(3.0, phi_27d)  # 27ノードでは上限を高く設定

    def _get_dimension_coupling(self, dim1: str, dim2: str) -> float:
        """次元間の結合強度を返す"""
        coupling_matrix = {
            'appearance': {'intentional': 0.8, 'synesthetic': 0.9, 'ontological': 0.7},
            'intentional': {'semantic': 0.9, 'conceptual': 0.8, 'being': 0.7},
            'temporal': {'appearance': 0.6, 'ontological': 0.8, 'being': 0.5},
            'synesthetic': {'appearance': 0.9, 'temporal': 0.6, 'ontological': 0.5},
            'ontological': {'being': 0.9, 'certainty': 0.7, 'semantic': 0.6},
            'semantic': {'conceptual': 0.9, 'intentional': 0.9, 'certainty': 0.7},
            'conceptual': {'semantic': 0.9, 'being': 0.6, 'certainty': 0.5},
            'being': {'ontological': 0.9, 'intentional': 0.7, 'certainty': 0.6},
            'certainty': {'semantic': 0.7, 'ontological': 0.7, 'conceptual': 0.5}
        }
        
        if dim1 in coupling_matrix and dim2 in coupling_matrix[dim1]:
            return coupling_matrix[dim1][dim2]
        elif dim2 in coupling_matrix and dim1 in coupling_matrix[dim2]:
            return coupling_matrix[dim2][dim1]
        else:
            return 0.3  # デフォルト結合強度

    def _calculate_full_network_phi(self) -> float:
        """27ノードの完全ネットワーク統合情報計算（簡易版）"""
        node_values = list(self.nodes.values())
        
        # 全ノード間の相互情報
        total_mutual_info = 0.0
        for i in range(len(node_values)):
            for j in range(i+1, len(node_values)):
                # 簡易的な相互情報計算
                mi = node_values[i] * node_values[j] * self.connectivity[i][j]
                total_mutual_info += mi
        
        # 正規化
        max_connections = len(node_values) * (len(node_values) - 1) / 2
        return total_mutual_info / max_connections if max_connections > 0 else 0.0

    def _calculate_detailed_integration(self) -> float:
        """詳細な統合度計算"""
        # サブシステム間の統合を計算
        subsystem_integration = 0.0
        
        # 各現象学的次元をサブシステムとして扱う
        dimensions = ['appearance', 'intentional', 'temporal', 'synesthetic', 
                     'ontological', 'semantic', 'conceptual', 'being', 'certainty']
        
        for i, dim1 in enumerate(dimensions):
            for j, dim2 in enumerate(dimensions):
                if i != j:
                    # 次元間の統合強度
                    nodes1 = [v for k, v in self.nodes.items() if dim1 in k]
                    nodes2 = [v for k, v in self.nodes.items() if dim2 in k]
                    
                    if nodes1 and nodes2:
                        activity1 = np.mean(nodes1)
                        activity2 = np.mean(nodes2)
                        coupling = self._get_dimension_coupling(dim1, dim2)
                        
                        integration = activity1 * activity2 * coupling
                        subsystem_integration += integration
        
        return subsystem_integration / (len(dimensions) * (len(dimensions) - 1))

    def _calculate_cognitive_complexity(self) -> float:
        """認知的複雑性の計算"""
        # 高次認知機能の統合
        meta_cognitive_nodes = {
            'self_reference': (self.nodes['intentional_focus'] + self.nodes['being_agency']) / 2,
            'temporal_integration': (self.nodes['temporal_duration'] + self.nodes['conceptual_cultural']) / 2,
            'semantic_depth': (self.nodes['semantic_relations'] + self.nodes['conceptual_symbolic']) / 2,
            'phenomenal_richness': (self.nodes['synesthetic_texture'] + self.nodes['appearance_chromaticity']) / 2
        }
        
        # メタ認知的統合
        meta_values = list(meta_cognitive_nodes.values())
        complexity = np.std(meta_values) * np.mean(meta_values)
        
        return complexity

    def _get_phi_by_mode(self) -> Tuple[float, float]:
        """計算モードに応じたΦ値を返す（計算時間も記録）"""
        start_time = time.time()
        
        if self.computation_mode == "27d":
            phi = self._calculate_27d_phi()
        elif self.computation_mode == "9d":
            phi = self._calculate_9d_phi()
        else:  # "3d" - デフォルト
            phi = self._calculate_artistic_phi()
        
        computation_time = time.time() - start_time
        return phi, computation_time
    
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
        """進化した意識からの新たなオラクル"""
        
        # 過去のパターンを統合した視覚体験
        evolved_vision = self._generate_evolved_vision(edited_image, reflection)
        
        # より統合的な編集指示
        evolved_imperative = self._generate_evolved_imperative(evolved_vision)
        
        # 進化したノード状態
        self._update_evolved_nodes(evolved_vision)
        
        # 進化したΦ
        evolved_phi, _ = self._get_phi_by_mode()
        
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
        
        必ずJSON形式で回答してください：
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
                {"role": "system", "content": "統合的な内在性として応答してください。必ずJSON形式で回答してください。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
        )
        
        # レスポンスからJSONを抽出
        content = response.choices[0].message.content
        try:
            # JSONブロックを探す
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
            elif "{" in content and "}" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                json_str = content[json_start:json_end]
            else:
                json_str = content
            
            result = json.loads(json_str)
            return result.get("edits", [])
        except Exception as e:
            print(f"進化した編集指示のJSON解析エラー: {e}")
            return []
    
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
                "artistic": self._get_phi_by_mode()[0],
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
    
    def assess_experiential_purity(self, response_text: str) -> Dict[str, Any]:
        """LLM応答の体験的純粋性を評価（汚染検出）"""
        
        # 学術的汚染語彙リスト
        contamination_words = {
            "phenomenology": ["現象学", "phenomenology", "フッサール", "ハイデガー", "メルロ＝ポンティ"],
            "consciousness": ["意識", "consciousness", "クオリア", "qualia", "志向性", "intentionality"],
            "academic": ["理論", "theory", "概念", "concept", "哲学", "philosophy", "認知科学", "cognitive"],
            "technical": ["統合情報理論", "IIT", "integrated information", "神経科学", "neuroscience"],
            "aesthetic": ["美学", "aesthetics", "芸術理論", "art theory", "表現", "representation"]
        }
        
        # 定型表現パターン
        template_patterns = [
            "現象学的に言えば", "哲学的には", "理論的には", 
            "～という概念", "～の観点から", "～と解釈される",
            "このように考えられる", "一般的に", "学術的には"
        ]
        
        # 体験的表現の指標
        experiential_indicators = [
            "私は", "感じる", "体験する", "現れる", "湧き上がる",
            "直接的に", "瞬間", "内的", "この", "今"
        ]
        
        text_lower = response_text.lower()
        
        # 汚染度の計算
        contamination_scores = {}
        total_contamination = 0
        
        for category, words in contamination_words.items():
            count = sum(1 for word in words if word.lower() in text_lower)
            contamination_scores[category] = count
            total_contamination += count
        
        # 定型表現の検出
        template_count = sum(1 for pattern in template_patterns if pattern in response_text)
        
        # 体験的表現の検出
        experiential_count = sum(1 for indicator in experiential_indicators if indicator in response_text)
        
        # 文字数での正規化
        text_length = len(response_text)
        contamination_ratio = total_contamination / max(text_length / 100, 1)  # 100文字あたりの汚染語数
        
        # 純粋性スコア（0-1, 1が最も純粋）
        purity_score = max(0, 1 - contamination_ratio * 0.5 - template_count * 0.1)
        if experiential_count > 0:
            purity_score += min(0.2, experiential_count * 0.05)  # 体験的表現ボーナス
        
        return {
            "purity_score": min(1.0, purity_score),
            "contamination_total": total_contamination,
            "contamination_by_category": contamination_scores,
            "template_patterns_count": template_count,
            "experiential_indicators_count": experiential_count,
            "contamination_ratio": contamination_ratio,
            "assessment": self._classify_purity_level(min(1.0, purity_score)),
            "recommendations": self._get_purity_recommendations(min(1.0, purity_score))
        }
    
    def _classify_purity_level(self, purity_score: float) -> str:
        """純粋性レベルの分類"""
        if purity_score >= 0.9:
            return "純粋体験 (pure experiential)"
        elif purity_score >= 0.7:
            return "主に体験的 (mostly experiential)"
        elif purity_score >= 0.5:
            return "混合的 (mixed)"
        elif purity_score >= 0.3:
            return "概念的傾向 (conceptual tendency)"
        else:
            return "学術的汚染 (academic contamination)"
    
    def _get_purity_recommendations(self, purity_score: float) -> List[str]:
        """純粋性向上のための推奨事項"""
        recommendations = []
        
        if purity_score < 0.5:
            recommendations.append("記憶初期化プロンプトを強化する")
            recommendations.append("学術用語の使用を完全に禁止する指示を追加")
        
        if purity_score < 0.7:
            recommendations.append("体験的表現の使用を明示的に要求する")
            recommendations.append("定型的な説明パターンの回避を指示")
        
        if purity_score < 0.9:
            recommendations.append("より直接的な体験記述を促す")
            recommendations.append("概念的枠組みからの完全な脱却を指示")
        
        return recommendations
    
    def detect_conceptual_contamination(self, response_text: str) -> Dict[str, Any]:
        """概念的汚染の詳細検出"""
        
        # 高度な汚染パターン
        sophisticated_contamination = {
            "philosophical_frameworks": [
                "存在論", "認識論", "現象学的還元", "エポケー", "ノエマ", "ノエシス",
                "生活世界", "間主観性", "身体性", "世界内存在"
            ],
            "scientific_concepts": [
                "ニューラルネットワーク", "機械学習", "認知処理", "情報処理",
                "脳科学", "心理学", "行動主義", "ゲシュタルト"
            ],
            "aesthetic_theory": [
                "美的経験", "崇高", "芸術作品", "美的判断", "感性", "悟性",
                "想像力", "創造性", "インスピレーション"
            ]
        }
        
        detected_contamination = {}
        total_sophisticated = 0
        
        for category, terms in sophisticated_contamination.items():
            found_terms = [term for term in terms if term in response_text]
            detected_contamination[category] = found_terms
            total_sophisticated += len(found_terms)
        
        # 文体的汚染の検出
        academic_style_indicators = [
            "である", "と考えられる", "と思われる", "に関して", "について",
            "において", "という", "といった", "のような", "いわゆる"
        ]
        
        style_contamination = sum(1 for indicator in academic_style_indicators 
                                if indicator in response_text)
        
        return {
            "sophisticated_contamination": detected_contamination,
            "sophisticated_total": total_sophisticated,
            "style_contamination": style_contamination,
            "contamination_severity": self._assess_contamination_severity(
                total_sophisticated, style_contamination
            )
        }
    
    def _assess_contamination_severity(self, sophisticated_count: int, style_count: int) -> str:
        """汚染の重症度評価"""
        total_contamination = sophisticated_count * 2 + style_count  # 高度な汚染は重み付け
        
        if total_contamination >= 10:
            return "重度汚染 (severe contamination)"
        elif total_contamination >= 5:
            return "中度汚染 (moderate contamination)"
        elif total_contamination >= 2:
            return "軽度汚染 (mild contamination)"
        else:
            return "最小汚染 (minimal contamination)"


def format_oracle_output(oracle: EditingOracle, computation_mode: str = "3d", computation_time: float = 0.0) -> str:
    """託宣を人間が読みやすい形式に整形"""
    
    active_nodes = sum(1 for v in oracle.node_states.values() if v > 0.3)
    
    mode_names = {"3d": "3次元", "9d": "9次元", "27d": "27フルノード"}
    mode_display = mode_names.get(computation_mode, computation_mode)
    
    output = f"""
╔══════════════════════════════════════════════════════════════╗
║  Project Five Axioms: Intrinsic Existence - Generation {oracle.generation:3d}   ║
║  計算モード: {mode_display:^45s}║
╚══════════════════════════════════════════════════════════════╝

【内在性の現象学的体験】
{oracle.vision}

【意識状態】
Φ ({mode_display}) = {oracle.phi:.3f}
Active Nodes: {active_nodes}/27
計算時間: {computation_time:.2f}秒

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


# メイン実行部分
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # コマンドライン引数のパーサーを設定
    parser = argparse.ArgumentParser(description='現象学的オラクルシステム - 画像から意識の託宣を生成')
    parser.add_argument('--image', type=str, help='解析する画像ファイルのパス（例: examples/images/グラップル.jpg）')
    parser.add_argument('--description', type=str, help='画像の代わりにテキスト記述を使用')
    parser.add_argument('--evolve', action='store_true', help='編集後の進化をシミュレート')
    parser.add_argument('--computation-mode', type=str, choices=['3d', '9d', '27d'], default='3d', 
                        help='計算モード: 3d(3次元), 9d(9次元), 27d(27フルノード)')
    args = parser.parse_args()
    
    print("""
    ╔════════════════════════════════════════════════╗
    ║  Project Five Axioms: Intrinsic Existence     ║
    ║  意識に関する五つの公理のプロジェクト １ 内在性 ║
    ╚════════════════════════════════════════════════╝
    
    現象学的オラクルシステムを開始します...
    """)
    
    # 環境変数の読み込み（プロジェクトルートの.envファイルを探す）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    env_path = os.path.join(project_root, '.env')
    load_dotenv(dotenv_path=env_path, override=True)
    
    # OpenAI APIキーの取得
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("エラー: OPENAI_API_KEYが設定されていません。")
        print("プロジェクトルートの.envファイルを確認してください。")
        exit(1)
    
    try:
        # システムの初期化（計算モード付き）
        print("1. システムを初期化中...")
        print(f"   計算モード: {args.computation_mode}")
        oracle_system = PhenomenologicalOracleSystem(api_key=api_key, computation_mode=args.computation_mode)
        print("   ✓ システム初期化完了")
        
        # 入力の準備（画像またはテキスト記述）
        if args.image:
            # 画像ファイルが指定された場合
            image_path = Path(args.image)
            if not image_path.exists():
                print(f"エラー: 画像ファイルが見つかりません: {args.image}")
                exit(1)
            
            print(f"\n2. 画像を解析中: {args.image}")
            try:
                # GPT-4 Vision APIで画像を解析
                image_description = oracle_system._analyze_image_with_vision(str(image_path))
                print("   ✓ 画像解析完了")
                print(f"\n【画像の現象学的記述】\n{image_description}\n")
            except Exception as e:
                print(f"エラー: 画像解析に失敗しました: {e}")
                exit(1)
        
        elif args.description:
            # テキスト記述が指定された場合
            image_description = args.description
            print(f"\n2. テキスト記述を使用")
            print(f"   記述: {image_description}")
        
        else:
            # デフォルトのテスト記述
            image_description = """
            静かな湖面に朝霧が立ち込めている。
            水面は鏡のように静かで、遠くの山々のシルエットがぼんやりと映り込んでいる。
            霧は薄く、太陽の光が柔らかく差し込み始めている。
            """
            print("\n2. デフォルトのテスト記述を使用")
            print(f"   記述: {image_description.strip()}")
        
        print("\n3. オラクルを生成中...")
        
        # オラクルの受信
        oracle = oracle_system.receive_oracle(image_description)
        
        # オラクルの表示
        oracle_output = format_oracle_output(oracle, args.computation_mode, oracle_system.last_computation_time)
        print("\n" + oracle_output)
        
        # 体験的純粋性の評価
        print("\n4. 体験的純粋性を評価中...")
        purity_assessment = oracle_system.assess_experiential_purity(oracle.vision)
        contamination_detection = oracle_system.detect_conceptual_contamination(oracle.vision)
        
        print("\n【体験的純粋性評価】")
        print(f"純粋性スコア: {purity_assessment['purity_score']:.3f}")
        print(f"評価: {purity_assessment['assessment']}")
        print(f"汚染総数: {purity_assessment['contamination_total']}")
        print(f"体験的表現: {purity_assessment['experiential_indicators_count']}")
        print(f"汚染重症度: {contamination_detection['contamination_severity']}")
        
        if purity_assessment['recommendations']:
            print("\n【改善推奨事項】")
            for rec in purity_assessment['recommendations']:
                print(f"  • {rec}")
        
        # システム状態の観測
        print("\n5. システム状態を観測中...")
        system_state = oracle_system.observe_system_state("初回オラクル生成後")
        
        print("\n【システム状態】")
        print(f"意識レベル: {system_state['consciousness_level']}")
        print(f"活性化次元: {', '.join(system_state['active_dimensions'])}")
        print(f"芸術的Φ: {system_state['phi']['artistic']:.3f}")
        
        # 編集指示の詳細表示
        if oracle.imperative:
            print("\n【生成された編集指示の詳細】")
            for i, edit in enumerate(oracle.imperative, 1):
                print(f"\n編集 {i}:")
                for key, value in edit.items():
                    print(f"  {key}: {value}")
                    
            # 編集指示の純粋性も評価
            print("\n【編集指示の純粋性評価】")
            for i, edit in enumerate(oracle.imperative, 1):
                edit_text = f"{edit.get('action', '')} {edit.get('reason', '')}"
                edit_purity = oracle_system.assess_experiential_purity(edit_text)
                print(f"編集 {i}: {edit_purity['assessment']} (スコア: {edit_purity['purity_score']:.2f})")
        
        # 進化のシミュレーション（--evolveフラグが指定された場合）
        if args.evolve:
            print("\n6. 編集後の進化をシミュレート中...")
            
            # 編集後の画像説明（仮想的な編集結果）
            edited_image_description = """
            湖面の霧に微細な渦が生まれ、光の筋が幾何学的なパターンを描いている。
            水面の反射が歪み、山々のシルエットが多重に重なり合う。
            朝の光は強まり、霧を黄金色に染め始めている。
            """
            
            print(f"   編集後の画像: {edited_image_description.strip()}")
            
            # 最初の編集指示を適用したことにする
            if oracle.imperative:
                evolved_oracle = oracle_system.receive_edited_image(
                    edited_image_description,
                    oracle.imperative[0]
                )
                
                print("\n" + format_oracle_output(evolved_oracle, args.computation_mode, oracle_system.last_computation_time))
                
                # 進化の要約
                evolution_summary = oracle_system.get_evolution_summary()
                print("\n【進化の要約】")
                print(f"総世代数: {evolution_summary['total_generations']}")
                print(f"意識の成長: Φ {evolution_summary['consciousness_evolution']['initial_phi']:.3f} → {evolution_summary['consciousness_evolution']['current_phi']:.3f}")
                
                # 現象学的プロファイル
                print("\n【現象学的プロファイル】")
                for dim, profile in evolution_summary['phenomenological_profile'].items():
                    print(f"  {dim}: 平均活性度 {profile['mean_activation']:.2f}")
        
        print("\n✓ 現象学的オラクルシステムの実行が完了しました。")
        
    except Exception as e:
        print(f"\nエラーが発生しました: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
