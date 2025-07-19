"""画像解析専用モジュール"""

import base64
import json
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image
import numpy as np

from .openai_client import OpenAIClient


class ImageAnalyzer:
    """画像から内在性パラメータを抽出する解析器"""
    
    def __init__(self, openai_client: OpenAIClient):
        """初期化
        
        Args:
            openai_client: OpenAIクライアント
        """
        self.client = openai_client
        
    def encode_image(self, image_path: str) -> str:
        """画像をBase64エンコード
        
        Args:
            image_path: 画像ファイルパス
            
        Returns:
            Base64エンコードされた画像文字列
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
            
    def get_image_metadata(self, image_path: str) -> Dict[str, Any]:
        """画像のメタデータを取得
        
        Args:
            image_path: 画像ファイルパス
            
        Returns:
            メタデータ辞書
        """
        img = Image.open(image_path)
        
        return {
            "size": img.size,
            "mode": img.mode,
            "format": img.format,
            "info": img.info
        }
        
    async def analyze_existence_type(self, image_path: str) -> Dict[str, Any]:
        """画像から存在類型を判定
        
        Args:
            image_path: 画像ファイルパス
            
        Returns:
            存在類型と判定理由
        """
        base64_image = self.encode_image(image_path)
        
        prompt = """
        この画像に写っているものの存在の仕方を判定してください。
        
        以下のカテゴリから最も適切なものを選び、その理由を説明してください：
        
        1. 【視線的存在】- 見る/見られる関係を持つ（人物、動物の顔など）
        2. 【場所的存在】- 空間として広がる（風景、室内、都市など）
        3. 【物体的存在】- 明確な輪郭を持つ個物（静物、建築物など）
        4. 【出来事的存在】- 動きや変化の瞬間（スポーツ、事故、儀式など）
        5. 【痕跡的存在】- かつて在ったものの残存（廃墟、古写真、化石など）
        6. 【関係的存在】- 複数の要素の相互作用（群衆、生態系、家族など）
        7. 【抽象的存在】- 形を持たない強度（色彩、光、テクスチャのみなど）
        
        JSON形式で以下の情報を出力してください：
        {
            "type_number": 選択した番号,
            "type_name": "存在類型名",
            "confidence": 0.0-1.0の確信度,
            "reason": "判定理由",
            "sub_elements": ["補助的な要素"]
        }
        """
        
        response = await self.client.analyze_image(base64_image, prompt)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # JSONパースに失敗した場合
            return {
                "type_number": 7,
                "type_name": "抽象的存在",
                "confidence": 0.5,
                "reason": "解析エラー",
                "sub_elements": []
            }
            
    async def analyze_intrinsic_properties(self, image_path: str, existence_type: str) -> Dict[str, Any]:
        """存在類型に応じた内在的特性を分析
        
        Args:
            image_path: 画像ファイルパス
            existence_type: 判定された存在類型
            
        Returns:
            内在的特性の分析結果
        """
        base64_image = self.encode_image(image_path)
        
        # 存在類型に応じたプロンプトを選択
        if "視線" in existence_type:
            prompt = self._get_gaze_analysis_prompt()
        elif "場所" in existence_type:
            prompt = self._get_place_analysis_prompt()
        elif "痕跡" in existence_type:
            prompt = self._get_trace_analysis_prompt()
        else:
            prompt = self._get_abstract_analysis_prompt()
            
        response = await self.client.analyze_image(base64_image, prompt)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return self._get_default_properties(existence_type)
            
    def _get_gaze_analysis_prompt(self) -> str:
        """視線的存在の分析プロンプト"""
        return """
        この肖像写真から、視線を持つ存在としての内在性を抽出します。
        
        以下の観点から分析し、JSON形式で出力してください：
        
        {
            "gaze_quality": {
                "direction": "視線の方向（camera_facing/averted/inward）",
                "intensity": 0.0-1.0,
                "temporality": "瞬間的/持続的/永遠的"
            },
            "relationship": {
                "viewer_awareness": 0.0-1.0,
                "seeking": "承認/拒否/無関心",
                "distance": "親密/社会的/疎遠"
            },
            "inner_expression": {
                "visible_emotion": "表出している感情",
                "suppressed": "抑制されているもの",
                "overflowing": "溢れ出ているもの"
            },
            "existential_anxiety": {
                "primary_fear": "being_unseen/being_seen/losing_sight",
                "intensity": 0.0-1.0
            },
            "core_parameters": {
                "boundary_strength": 0.0-1.0,
                "other_dependency": 0.0-1.0,
                "temporal_mode": "momentary/continuous/eternal",
                "initial_state": "状態を表す形容詞"
            }
        }
        """
        
    def _get_place_analysis_prompt(self) -> str:
        """場所的存在の分析プロンプト"""
        return """
        この風景写真から、場所として在る存在の内在性を抽出します。
        
        以下の観点から分析し、JSON形式で出力してください：
        
        {
            "spatial_quality": {
                "inclusiveness": "包み込む/排除する",
                "openness": "開かれている/閉じている",
                "invitation": "招き入れる/拒絶する"
            },
            "temporal_flow": {
                "time_quality": "静止した永遠/ゆったりとした変化/激しい変動",
                "change_rate": 0.0-1.0
            },
            "element_relations": {
                "harmony": "調和的統合/緊張的共存/無関心な並存",
                "dominant_element": "支配的な要素"
            },
            "place_memory": {
                "remembers": "何を覚えている場所か",
                "forgets": "何を忘れた場所か",
                "awaits": "何を待っている場所か"
            },
            "core_parameters": {
                "boundary_strength": 0.0-1.0,
                "other_dependency": 0.0-1.0,
                "temporal_mode": "enduring/cyclical/fading",
                "initial_state": "状態を表す形容詞"
            }
        }
        """
        
    def _get_trace_analysis_prompt(self) -> str:
        """痕跡的存在の分析プロンプト"""
        # 実装省略
        return """
        痕跡としての存在を分析...
        """
        
    def _get_abstract_analysis_prompt(self) -> str:
        """抽象的存在の分析プロンプト"""
        # 実装省略
        return """
        抽象的な存在を分析...
        """
        
    def _get_default_properties(self, existence_type: str) -> Dict[str, Any]:
        """デフォルトの特性値を返す"""
        return {
            "core_parameters": {
                "boundary_strength": 0.5,
                "other_dependency": 0.5,
                "temporal_mode": "continuous",
                "initial_state": "nascent"
            },
            "analysis_status": "default_values_used"
        }