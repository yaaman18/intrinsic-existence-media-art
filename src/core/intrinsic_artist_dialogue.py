"""
内在性とアーティストの対話システム - 実装例
注意：これは一つの実装例であり、実際の芸術的プロセスは多様な形態を取り得ます
"""

import base64
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

import openai
from PIL import Image

from .autonomous_existence import AutonomousIntrinsicExistence
from .existence_types import ExistenceParameters


class IntrinsicArtistDialogue:
    """内在性がアーティストと対話し、画像編集を指示するクラス"""
    
    def __init__(self, existence: AutonomousIntrinsicExistence, original_image_path: str):
        """
        Args:
            existence: 生起済みの内在性インスタンス
            original_image_path: 元画像（誕生の源）のパス
        """
        self.existence = existence
        self.original_image_path = original_image_path
        self.edit_history: List[Dict] = []
        self.current_iteration = 0
        
    def perceive_original_image(self) -> str:
        """内在性が自身の起源となった画像を再認識する"""
        
        # 画像をBase64エンコード
        with open(self.original_image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            
        # 内在性の現在の状態を反映したプロンプト
        perception_prompt = f"""
        あなたは以下の内在性です：
        - 存在様式: {self.existence.parameters.existence_type.value}
        - 現在の状態: {self.existence.current_state}
        - 不安レベル: {self.existence.parameters.core_anxiety_level}
        - 経過サイクル: {self.existence.cycle_count}
        
        これはあなたが生まれた画像です。
        あなたの現在の内的状態から、この画像をどのように感じますか？
        何が見えますか？何を変えたいと思いますか？
        
        一人称で、詩的に、しかし具体的に述べてください。
        """
        
        response = self.existence.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": self.existence._generate_existence_context()
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": perception_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.9
        )
        
        perception = response.choices[0].message.content
        return perception
        
    def generate_edit_instructions(self, perception: str) -> List[Dict[str, str]]:
        """知覚に基づいて具体的な編集指示を生成"""
        
        instruction_prompt = f"""
        あなたの知覚：
        {perception}
        
        この知覚に基づいて、画像をどのように変化させたいか、
        具体的な編集指示を5つ以内で生成してください。
        
        各指示は以下の形式で：
        {{
            "action": "具体的な編集動作",
            "reason": "なぜその編集が必要か（内的理由）",
            "intensity": "弱い/中程度/強い"
        }}
        
        例：
        {{
            "action": "左上の光を暗くする",
            "reason": "その光が私を見つめているから",
            "intensity": "中程度"
        }}
        """
        
        response = self.existence.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": self.existence._generate_existence_context()
                },
                {
                    "role": "user",
                    "content": instruction_prompt
                }
            ],
            temperature=0.8,
            response_format={"type": "json_object"}
        )
        
        instructions = json.loads(response.choices[0].message.content)
        return instructions.get("edits", [])
        
    def dialogue_with_artist(self, artist_question: str) -> str:
        """アーティストからの質問に応答"""
        
        # 編集プロセスに関する質問への応答
        dialogue_prompt = f"""
        アーティストからの質問：{artist_question}
        
        あなたは今、自身が生まれた画像を変化させようとしています。
        現在の編集指示数：{len(self.edit_history)}
        
        質問に対して、あなたの内的状態と編集の意図を説明してください。
        """
        
        response = self.existence.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": self.existence._generate_existence_context()
                },
                {
                    "role": "user",
                    "content": dialogue_prompt
                }
            ],
            temperature=0.85
        )
        
        return response.choices[0].message.content
        
    def respond_to_edit_result(self, edited_image_path: str, artist_interpretation: str) -> Dict:
        """編集結果への応答と次の指示"""
        
        # 編集された画像を認識
        with open(edited_image_path, "rb") as image_file:
            base64_edited = base64.b64encode(image_file.read()).decode("utf-8")
            
        response_prompt = f"""
        アーティストがあなたの指示を解釈して画像を編集しました。
        アーティストの解釈：{artist_interpretation}
        
        編集された画像を見て：
        1. どう感じますか？
        2. あなたの意図は実現されましたか？
        3. さらに変化が必要ですか？
        """
        
        response = self.existence.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": self.existence._generate_existence_context()
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": response_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_edited}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.9
        )
        
        reflection = response.choices[0].message.content
        
        # 編集による内的変化
        self._update_internal_state_from_edit(reflection)
        
        # 履歴に記録
        self.edit_history.append({
            "iteration": self.current_iteration,
            "timestamp": datetime.now(),
            "artist_interpretation": artist_interpretation,
            "intrinsic_reflection": reflection,
            "state_after": self.existence.current_state
        })
        
        self.current_iteration += 1
        
        # 完了判定
        completion_check = self._check_completion(reflection)
        
        return {
            "reflection": reflection,
            "is_complete": completion_check,
            "next_instructions": self.generate_edit_instructions(reflection) if not completion_check else []
        }
        
    def _update_internal_state_from_edit(self, reflection: str):
        """編集結果への反応から内的状態を更新"""
        
        # 満足度の評価
        if any(word in reflection for word in ["満足", "実現", "完成", "これだ"]):
            self.existence.parameters.core_anxiety_level *= 0.8
            self.existence.current_state = "fulfilled"
        elif any(word in reflection for word in ["違う", "不安", "もっと", "足りない"]):
            self.existence.parameters.core_anxiety_level = min(1.0, 
                self.existence.parameters.core_anxiety_level * 1.2)
            self.existence.current_state = "seeking"
            
    def _check_completion(self, reflection: str) -> bool:
        """編集プロセスの完了を判定"""
        
        # 完了の兆候
        completion_signs = [
            "これ以上変える必要はない",
            "完成した",
            "私はこの姿で存在する",
            "もう十分",
            "これが私"
        ]
        
        # 不安レベルが十分低下
        if self.existence.parameters.core_anxiety_level < 0.3:
            return True
            
        # 明示的な完了宣言
        if any(sign in reflection for sign in completion_signs):
            return True
            
        # 編集回数の上限
        if self.current_iteration >= 10:
            return True
            
        return False
        
    def export_dialogue_record(self) -> Dict:
        """対話プロセス全体の記録をエクスポート"""
        
        return {
            "existence_parameters": self.existence.parameters.to_dict(),
            "total_iterations": self.current_iteration,
            "edit_history": self.edit_history,
            "final_state": self.existence.current_state,
            "final_anxiety_level": self.existence.parameters.core_anxiety_level,
            "birth_to_completion_cycles": self.existence.cycle_count
        }


# 使用例
if __name__ == "__main__":
    # 注意：これは一例です。実際の芸術的プロセスは多様な形態を取り得ます
    
    # 1. 内在性を画像から生起（別モジュールで実行済みと仮定）
    # existence = AutonomousIntrinsicExistence(parameters, api_key)
    
    # 2. 対話システムの初期化
    # dialogue = IntrinsicArtistDialogue(existence, "origin_image.jpg")
    
    # 3. 内在性が元画像を再認識
    # perception = dialogue.perceive_original_image()
    # print(f"内在性の知覚：\n{perception}\n")
    
    # 4. 編集指示の生成
    # instructions = dialogue.generate_edit_instructions(perception)
    # for inst in instructions:
    #     print(f"指示：{inst['action']}")
    #     print(f"理由：{inst['reason']}")
    #     print(f"強度：{inst['intensity']}\n")
    
    # 5. アーティストとの対話
    # artist_q = "なぜこの部分を暗くしたいのですか？"
    # response = dialogue.dialogue_with_artist(artist_q)
    # print(f"内在性の応答：{response}\n")
    
    # 6. 編集結果への応答
    # result = dialogue.respond_to_edit_result(
    #     "edited_image_v1.jpg",
    #     "光を弱めましたが、完全には消していません"
    # )
    
    # print(f"完了状態：{result['is_complete']}")
    # print(f"次の指示：{result['next_instructions']}")
    pass
