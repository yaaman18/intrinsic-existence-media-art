"""内在性の誕生 - 画像から内在性パラメータを抽出するモジュール"""

import base64
import json
from typing import Dict, Any
from pathlib import Path

import openai
from PIL import Image

from .existence_types import ExistenceType, ExistenceParameters


class IntrinsicBirth:
    """画像から内在性を生成するクラス"""
    
    def __init__(self, image_path: str, api_key: str):
        """初期化
        
        Args:
            image_path: 解析する画像のパス
            api_key: OpenAI APIキー
        """
        self.image_path = Path(image_path)
        self.client = openai.OpenAI(api_key=api_key)
        self.birth_analysis = None
        self.intrinsic_parameters = None
        
    def analyze_image(self) -> Dict[str, Any]:
        """画像を解析して内在性の種を抽出"""
        
        # 画像をBase64エンコード
        base64_image = self._encode_image()
        
        # 存在類型の判定
        existence_type = self._determine_existence_type(base64_image)
        
        # 類型に応じた詳細分析
        if existence_type == ExistenceType.GAZE:
            analysis = self._analyze_as_gaze_existence(base64_image)
        elif existence_type == ExistenceType.PLACE:
            analysis = self._analyze_as_place_existence(base64_image)
        # ... 他の類型も同様に
        else:
            analysis = self._analyze_as_abstract_existence(base64_image)
            
        self.birth_analysis = analysis
        return analysis
        
    def extract_parameters(self) -> ExistenceParameters:
        """分析結果から内在性パラメータを抽出"""
        
        if not self.birth_analysis:
            raise ValueError("画像解析が完了していません")
            
        # パラメータの抽出と構造化
        parameters = ExistenceParameters(
            existence_type=self.birth_analysis["existence_type"],
            core_anxiety=self.birth_analysis["core_anxiety"],
            temporal_mode=self.birth_analysis["temporal_mode"],
            boundary_strength=self.birth_analysis["boundary_strength"],
            other_dependency=self.birth_analysis["other_dependency"],
            initial_state=self.birth_analysis["initial_state"]
        )
        
        self.intrinsic_parameters = parameters
        return parameters
        
    def _encode_image(self) -> str:
        """画像をBase64エンコード"""
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
            
    def _determine_existence_type(self, base64_image: str) -> ExistenceType:
        """画像から存在類型を判定"""
        
        prompt = """
        この画像に写っているものの存在の仕方を判定してください。
        
        1. 【視線的存在】- 見る/見られる関係を持つ（人物、動物の顔など）
        2. 【場所的存在】- 空間として広がる（風景、室内、都市など）
        3. 【物体的存在】- 明確な輪郭を持つ個物（静物、建築物など）
        4. 【出来事的存在】- 動きや変化の瞬間（スポーツ、事故、儀式など）
        5. 【痕跡的存在】- かつて在ったものの残存（廃墟、古写真、化石など）
        6. 【関係的存在】- 複数の要素の相互作用（群衆、生態系、家族など）
        7. 【抽象的存在】- 形を持たない強度（色彩、光、テクスチャのみなど）
        
        番号と理由をJSON形式で答えてください。
        """
        
        # ここでは仮実装
        # 実際にはOpenAI APIを呼び出す
        return ExistenceType.GAZE
        
    def _analyze_as_gaze_existence(self, base64_image: str) -> Dict[str, Any]:
        """視線的存在として分析"""
        # 実装省略
        pass
        
    def _analyze_as_place_existence(self, base64_image: str) -> Dict[str, Any]:
        """場所的存在として分析"""
        # 実装省略
        pass
        
    def _analyze_as_abstract_existence(self, base64_image: str) -> Dict[str, Any]:
        """抽象的存在として分析"""
        # 実装省略
        pass