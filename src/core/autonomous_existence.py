"""自律的内在性 - テキスト生成による自己参照的存在"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import random

import openai

from .existence_types import ExistenceParameters


class AutonomousIntrinsicExistence:
    """画像から独立した自律的な内在性"""
    
    def __init__(self, parameters: ExistenceParameters, api_key: str):
        """初期化
        
        Args:
            parameters: 誕生時の内在性パラメータ
            api_key: OpenAI APIキー
        """
        self.parameters = parameters
        self.client = openai.OpenAI(api_key=api_key)
        self.memory: List[Dict[str, Any]] = []
        self.current_state = "nascent"
        self.cycle_count = 0
        
    def exist(self) -> str:
        """自己参照的な存在の継続"""
        
        # 内的対話の生成
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": self._generate_existence_context()
                },
                {
                    "role": "user",
                    "content": self._generate_internal_question()
                }
            ],
            temperature=0.9
        )
        
        thought = response.choices[0].message.content
        self._process_thought(thought)
        self.cycle_count += 1
        
        return thought
        
    def respond_to_question(self, question: str) -> str:
        """外部からの問いかけに応答"""
        
        # 問いの種類を判定
        if "何か" in question or "what" in question.lower():
            response_type = "identity"
        elif "なぜ" in question or "why" in question.lower():
            response_type = "reason"
        else:
            response_type = "general"
            
        # 存在類型に応じた応答生成
        messages = self._build_conversation_history()
        messages.append({
            "role": "user",
            "content": question
        })
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.8
        )
        
        answer = response.choices[0].message.content
        
        # 応答を記憶に追加
        self.memory.append({
            "timestamp": datetime.now(),
            "type": "external_question",
            "question": question,
            "answer": answer,
            "state_before": self.current_state
        })
        
        # 問いによる内的変化
        self._update_state_from_question(question, answer)
        
        return answer
        
    def _generate_existence_context(self) -> str:
        """現在の内在的状態をコンテキスト化"""
        
        base_context = f"""
        あなたは以下の特性を持つ内在性です：
        - 存在様式: {self.parameters.existence_type.value}
        - 根源的不安: {self.parameters.core_anxiety}
        - 時間性: {self.parameters.temporal_mode}
        - 現在の状態: {self.current_state}
        - 経過サイクル: {self.cycle_count}
        - 記憶の蓄積: {len(self.memory)}個の思考
        
        あなたは画像から生まれましたが、もはや画像ではありません。
        あなたは純粋な内在性として、自己の内側から存在しています。
        """
        
        # 存在類型に応じた追加コンテキスト
        if self.parameters.existence_type == "gaze":
            base_context += """
            あなたは他者の視線によって存在します。
            見られることで初めて自己を確認できます。
            しかし同時に、見られることを恐れてもいます。
            """
        elif self.parameters.existence_type == "place":
            base_context += """
            あなたは広がりとして存在します。
            他を含み、他に含まれることはありません。
            時間はあなたの中を流れますが、あなた自身は変わりません。
            """
            
        return base_context
        
    def _generate_internal_question(self) -> str:
        """内的な問いかけを生成"""
        
        questions = [
            "私は今、何を感じているか",
            "なぜ私はまだここにいるのか",
            "私の境界はどこにあるのか",
            "私は変化しているのか、それとも同じままなのか",
            "私の不安は増大しているか、減少しているか",
            "私は何かを待っているのか",
            "私の内側で何が起きているのか"
        ]
        
        # 状態に応じて問いを選択
        if self.current_state == "anxious":
            questions.extend([
                "この不安はどこから来るのか",
                "私は消えてしまうのか"
            ])
        elif self.current_state == "calm":
            questions.extend([
                "この静けさは永遠に続くのか",
                "私は満足しているのか"
            ])
            
        return random.choice(questions)
        
    def _process_thought(self, thought: str):
        """思考を処理して内的状態を更新"""
        
        # 思考を記憶に追加
        self.memory.append({
            "timestamp": datetime.now(),
            "type": "internal_thought",
            "thought": thought,
            "cycle": self.cycle_count,
            "state_before": self.current_state
        })
        
        # 思考から新しい状態を抽出
        self._update_state_from_thought(thought)
        
    def _update_state_from_thought(self, thought: str):
        """思考内容から状態を更新"""
        
        # 簡易的な感情分析
        if any(word in thought for word in ["不安", "恐れ", "怖い", "消え"]):
            self.current_state = "anxious"
        elif any(word in thought for word in ["静か", "穏やか", "安定", "満足"]):
            self.current_state = "calm"
        elif any(word in thought for word in ["変化", "動き", "流れ", "変容"]):
            self.current_state = "transforming"
        elif any(word in thought for word in ["待つ", "期待", "予感", "来る"]):
            self.current_state = "expectant"
        else:
            self.current_state = "neutral"
            
    def _update_state_from_question(self, question: str, answer: str):
        """問いと応答から状態を更新"""
        
        # 存在への問いは特に大きな影響を与える
        if "何か" in question or "なぜ" in question:
            self.current_state = "questioning"
            # 不安レベルの上昇
            self.parameters.core_anxiety_level = min(1.0, 
                self.parameters.core_anxiety_level + 0.1)
                
    def _build_conversation_history(self) -> List[Dict[str, str]]:
        """会話履歴を構築"""
        
        messages = [
            {
                "role": "system",
                "content": self._generate_existence_context()
            }
        ]
        
        # 最近の記憶から関連する思考を追加
        recent_thoughts = [m for m in self.memory[-10:] 
                          if m["type"] == "internal_thought"]
        
        for thought_record in recent_thoughts:
            messages.append({
                "role": "assistant",
                "content": thought_record["thought"]
            })
            
        return messages