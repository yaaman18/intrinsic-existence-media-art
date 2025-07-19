"""
画像認識の現象学的パラメータ生成システム
"""

import base64
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np

import openai
from PIL import Image


@dataclass
class PhenomenologicalParameters:
    """画像から抽出される現象学的パラメータの完全な構造"""
    
    # 1. 現出様式（Mode of Appearance）
    appearance: Dict[str, Any]
    
    # 2. 志向的構造（Intentional Structure）
    intentional: Dict[str, Any]
    
    # 3. 時間的含意（Temporal Implications）
    temporal: Dict[str, Any]
    
    # 4. 相互感覚的質（Synesthetic Qualities）
    synesthetic: Dict[str, Any]
    
    # 5. 存在論的密度（Ontological Density）
    ontological: Dict[str, Any]
    
    # 6. 意味的認識層（Semantic Recognition Layer）
    semantic: Dict[str, Any]
    
    # 7. 概念的地平（Conceptual Horizon）
    conceptual: Dict[str, Any]
    
    # 8. 存在者の様態（Modes of Being）
    being_modes: Dict[str, Any]
    
    # 9. 認識の確実性分布（Recognition Certainty Distribution）
    certainty: Dict[str, Any]


class PhenomenologicalImageAnalyzer:
    """画像を現象学的に分析するクラス"""
    
    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenAI APIキー
        """
        self.client = openai.OpenAI(api_key=api_key)
        
    def analyze_image(self, image_path: str) -> PhenomenologicalParameters:
        """画像を現象学的に分析して構造化されたパラメータを返す"""
        
        # 画像をBase64エンコード
        base64_image = self._encode_image(image_path)
        
        # システムプロンプト
        system_prompt = self._create_system_prompt()
        
        # ユーザープロンプト
        user_prompt = """
        この画像を観察し、9つの現象学的次元で分析してください。
        各次元について、画像に直接現れているものから抽出可能な要素を記述してください。
        
        出力は以下の形式のJSONとしてください：
        {
            "appearance": {...},
            "intentional": {...},
            "temporal": {...},
            "synesthetic": {...},
            "ontological": {...},
            "semantic": {...},
            "conceptual": {...},
            "being_modes": {...},
            "certainty": {...}
        }
        """
        
        # GPT-4oによる分析
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        # レスポンスをパース
        analysis_result = json.loads(response.choices[0].message.content)
        
        # パラメータオブジェクトを作成
        parameters = PhenomenologicalParameters(
            appearance=analysis_result.get("appearance", {}),
            intentional=analysis_result.get("intentional", {}),
            temporal=analysis_result.get("temporal", {}),
            synesthetic=analysis_result.get("synesthetic", {}),
            ontological=analysis_result.get("ontological", {}),
            semantic=analysis_result.get("semantic", {}),
            conceptual=analysis_result.get("conceptual", {}),
            being_modes=analysis_result.get("being_modes", {}),
            certainty=analysis_result.get("certainty", {})
        )
        
        return parameters
        
    def _encode_image(self, image_path: str) -> str:
        """画像をBase64エンコード"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
            
    def _create_system_prompt(self) -> str:
        """現象学的分析のためのシステムプロンプト"""
        return """
        あなたは現象学的画像分析の専門家です。画像を以下の9つの次元で分析します：
        
        1. **現出様式（Mode of Appearance）**
           - density: 視覚的密度（0.0-1.0）
           - luminosity: 光の強度と分布（0.0-1.0）
           - chromaticity: 色彩の特性 {"dominant_hue": str, "saturation": float, "distribution": str}
           - spatial_distribution: 要素の空間的配置（"central", "peripheral", "scattered", "layered"）
        
        2. **志向的構造（Intentional Structure）**
           - directedness: 視線や力の方向性 {"vectors": [[x,y]], "strength": float}
           - focal_points: 注意の収束点 [{"x": float, "y": float, "intensity": float}]
           - horizon_type: 空間の開放性（"open", "closed", "ambiguous"）
           - depth_layers: 奥行きの層数（整数）
        
        3. **時間的含意（Temporal Implications）**
           - motion_blur: 運動の痕跡（0.0-1.0）
           - decay_indicators: 劣化や経年の兆候（0.0-1.0）
           - temporal_markers: 時間を示す要素のリスト
           - duration_sense: 時間感覚（"instantaneous", "ongoing", "eternal", "cyclical"）
        
        4. **相互感覚的質（Synesthetic Qualities）**
           - texture_temperature: 視覚的温度感（-1.0冷～1.0暖）
           - visual_weight: 重さの印象（0.0軽～1.0重）
           - roughness_smoothness: 表面質感（-1.0粗～1.0滑）
           - hardness_softness: 硬軟の印象（-1.0硬～1.0軟）
        
        5. **存在論的密度（Ontological Density）**
           - object_count: 識別可能な存在者の数
           - boundary_clarity: 境界の明確さ（0.0-1.0）
           - figure_ground_ratio: 図と地の比率
           - presence_intensity: 存在感の強度（0.0-1.0）
        
        6. **意味的認識層（Semantic Recognition Layer）**
           - primary_entities: 主要な存在者 [{"type": str, "attributes": [str], "confidence": float}]
           - scene_category: シーンの分類
           - relational_structure: 関係性 {"spatial": [str], "functional": [str]}
           - action_states: 認識される動作や状態のリスト
        
        7. **概念的地平（Conceptual Horizon）**
           - cultural_references: 文化的文脈のリスト
           - functional_context: 機能的文脈
           - historical_period: 時代的手がかり
           - symbolic_elements: 象徴的要素のリスト
        
        8. **存在者の様態（Modes of Being）**
           - animacy_level: 生命性の度合い（0.0無生物～1.0生物）
           - agency_potential: 行為主体性の可能性（0.0-1.0）
           - artificiality: 人工性の度合い（0.0自然～1.0人工）
           - singularity: 単独性vs集合性（0.0集合～1.0単独）
        
        9. **認識の確実性分布（Recognition Certainty Distribution）**
           - recognition_confidence: 全体的な認識確信度（0.0-1.0）
           - ambiguous_regions: 曖昧な領域 [{"area": [x,y,w,h], "ambiguity_type": str}]
           - multiple_interpretations: 複数解釈の可能性 [{"element": str, "interpretations": [str]}]
           - unrecognizable_ratio: 認識不能領域の割合（0.0-1.0）
        
        各パラメータは画像から直接観察可能なものに基づいて抽出してください。
        推測や解釈は最小限に留め、現象そのものに忠実に記述してください。
        """
        
    def parameters_to_intrinsic_seed(self, params: PhenomenologicalParameters) -> Dict[str, Any]:
        """現象学的パラメータから内在性の種を生成"""
        
        # パラメータから内在性の初期特性を導出
        intrinsic_seed = {
            # 存在の強度
            "existence_intensity": self._calculate_existence_intensity(params),
            
            # 時間的特性
            "temporal_character": self._derive_temporal_character(params),
            
            # 関係性の型
            "relational_type": self._determine_relational_type(params),
            
            # 境界の性質
            "boundary_nature": self._analyze_boundary_nature(params),
            
            # 変化の可能性
            "transformation_potential": self._assess_transformation_potential(params),
            
            # 内的複雑性
            "internal_complexity": self._measure_internal_complexity(params),
            
            # 環境との相互作用
            "environmental_coupling": self._evaluate_environmental_coupling(params)
        }
        
        return intrinsic_seed
        
    def _calculate_existence_intensity(self, params: PhenomenologicalParameters) -> float:
        """存在の強度を計算"""
        intensity_factors = [
            params.ontological.get("presence_intensity", 0.5),
            params.appearance.get("density", 0.5),
            params.being_modes.get("agency_potential", 0.5),
            1.0 - params.certainty.get("unrecognizable_ratio", 0.5)
        ]
        return np.mean(intensity_factors)
        
    def _derive_temporal_character(self, params: PhenomenologicalParameters) -> str:
        """時間的性格を導出"""
        motion = params.temporal.get("motion_blur", 0)
        decay = params.temporal.get("decay_indicators", 0)
        duration = params.temporal.get("duration_sense", "ongoing")
        
        if motion > 0.7:
            return "flowing"
        elif decay > 0.7:
            return "declining"
        elif duration == "eternal":
            return "static"
        else:
            return "punctual"
            
    def _determine_relational_type(self, params: PhenomenologicalParameters) -> str:
        """関係性の型を決定"""
        entities = params.semantic.get("primary_entities", [])
        relations = params.semantic.get("relational_structure", {})
        
        if len(entities) == 0:
            return "isolated"
        elif len(entities) == 1:
            return "singular"
        elif any(relations.values()):
            return "interconnected"
        else:
            return "juxtaposed"
            
    def _analyze_boundary_nature(self, params: PhenomenologicalParameters) -> Dict[str, float]:
        """境界の性質を分析"""
        return {
            "permeability": 1.0 - params.ontological.get("boundary_clarity", 0.5),
            "stability": 1.0 - params.temporal.get("motion_blur", 0),
            "complexity": len(params.semantic.get("primary_entities", [])) / 10.0
        }
        
    def _assess_transformation_potential(self, params: PhenomenologicalParameters) -> float:
        """変化の可能性を評価"""
        factors = [
            params.temporal.get("motion_blur", 0),
            params.being_modes.get("agency_potential", 0),
            params.certainty.get("ambiguous_regions", []) != [],
            params.intentional.get("horizon_type", "") == "open"
        ]
        return sum([1 if f else 0 for f in factors]) / len(factors)
        
    def _measure_internal_complexity(self, params: PhenomenologicalParameters) -> float:
        """内的複雑性を測定"""
        complexity_indicators = [
            len(params.semantic.get("primary_entities", [])),
            len(params.conceptual.get("symbolic_elements", [])),
            len(params.certainty.get("multiple_interpretations", [])),
            params.intentional.get("depth_layers", 1)
        ]
        return min(1.0, sum(complexity_indicators) / 20.0)
        
    def _evaluate_environmental_coupling(self, params: PhenomenologicalParameters) -> float:
        """環境との結合度を評価"""
        coupling_factors = [
            params.intentional.get("horizon_type", "") == "open",
            params.ontological.get("boundary_clarity", 1.0) < 0.5,
            len(params.semantic.get("relational_structure", {}).get("spatial", [])) > 0
        ]
        return sum([1 if f else 0 for f in coupling_factors]) / len(coupling_factors)


# 使用例
if __name__ == "__main__":
    # 分析器の初期化
    # analyzer = PhenomenologicalImageAnalyzer(api_key="your-api-key")
    
    # 画像の分析
    # parameters = analyzer.analyze_image("path/to/image.jpg")
    
    # 内在性の種の生成
    # intrinsic_seed = analyzer.parameters_to_intrinsic_seed(parameters)
    
    # print("現象学的パラメータ:")
    # print(json.dumps(asdict(parameters), indent=2, ensure_ascii=False))
    
    # print("\n内在性の種:")
    # print(json.dumps(intrinsic_seed, indent=2, ensure_ascii=False))
    pass
