#!/usr/bin/env python3
"""
Phenomenological Autonomous Creative Apparatus
現象学的自律創造機構

t-wada式TDD Green Phase - 最小実装
"""

import os
import json
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from PIL import Image, ImageEnhance
import openai


@dataclass
class CreativeResult:
    """創造結果を保持するデータクラス"""
    original_image: str
    created_image: Image.Image
    operations: List[Dict[str, Any]]
    philosophical_interpretation: str
    aesthetic_evaluation: Dict[str, Any]


class AestheticMemory:
    """美的記憶システム"""
    
    def __init__(self):
        self.evaluations = []
    
    def store(self, evaluation: Dict[str, Any]) -> None:
        """美的評価を記憶に保存"""
        evaluation_with_timestamp = {
            **evaluation,
            'timestamp': datetime.now().isoformat()
        }
        self.evaluations.append(evaluation_with_timestamp)
    
    def get_recent_evaluations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """最近の評価を取得"""
        return self.evaluations[-limit:]


class IntrinsicPersona:
    """内在性ペルソナ - 画像から生まれる現象学的意識"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.llm_client = openai.OpenAI(api_key=api_key)
        else:
            self.llm_client = None
    
    def analyze_phenomenological_impression(self, image_path: str) -> Dict[str, float]:
        """
        画像から現象学的印象を抽出し、27次元のノード活性度を返す
        
        Args:
            image_path: 分析する画像のパス
            
        Returns:
            27次元のノード活性度辞書
        """
        # 27次元の現象学的ノード定義
        dimensional_nodes = {
            # 時間性次元
            'temporal_basic': 0.5,
            'temporal_flow': 0.5,
            'temporal_synthesis': 0.5,
            
            # 空間性次元
            'spatial_density': 0.5,
            'spatial_orientation': 0.5,
            'spatial_boundary': 0.5,
            
            # 質性次元
            'qualitative_intensity': 0.5,
            'qualitative_harmony': 0.5,
            'qualitative_transformation': 0.5,
            
            # 身体性次元
            'embodied_surface': 0.5,
            'embodied_volume': 0.5,
            'embodied_presence': 0.5,
            
            # 意識性次元
            'conscious_attention': 0.5,
            'conscious_depth': 0.5,
            'conscious_clarity': 0.5,
            
            # 存在性次元
            'existential_presence': 0.5,
            'existential_being': 0.5,
            'existential_authenticity': 0.5,
            
            # 関係性次元
            'relational_connection': 0.5,
            'relational_resonance': 0.5,
            'relational_context': 0.5,
            
            # 生成性次元
            'generative_creation': 0.5,
            'generative_transformation': 0.5,
            'generative_potential': 0.5,
            
            # 表現性次元
            'expressive_articulation': 0.5,
            'expressive_intensity': 0.5,
            'expressive_style': 0.5
        }
        
        # 最小実装: 画像に基づく簡単な分析
        if os.path.exists(image_path):
            try:
                image = Image.open(image_path)
                width, height = image.size
                
                # 画像特性に基づく簡単な活性度調整
                aspect_ratio = width / height
                dimensional_nodes['spatial_orientation'] = min(aspect_ratio / 2, 1.0)
                dimensional_nodes['spatial_density'] = min((width * height) / 100000, 1.0)
                
                # 色彩情報に基づく調整
                colors = image.getcolors(maxcolors=256*256*256)
                if colors:
                    color_complexity = len(colors) / (256 * 3)  # 正規化
                    dimensional_nodes['qualitative_intensity'] = min(color_complexity, 1.0)
                
            except Exception:
                # エラー時はデフォルト値を使用
                pass
        
        return dimensional_nodes
    
    def decide_operations(self, node_activations: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        LLM APIを使用してパレット操作を決定
        
        Args:
            node_activations: 27次元のノード活性度
            
        Returns:
            実行すべき操作のリスト
        """
        if not self.llm_client:
            # APIクライアントがない場合のフォールバック
            return [
                {"function": "conscious_focus", "intensity": 0.8, "reason": "デフォルト操作"},
                {"function": "qualitative_harmony", "intensity": 0.5, "reason": "デフォルト操作"}
            ]
        
        # 最小実装: 活性度の高い次元に基づく操作決定
        operations = []
        
        # 最も活性度の高い3つの次元を選択
        sorted_nodes = sorted(node_activations.items(), key=lambda x: x[1], reverse=True)
        top_nodes = sorted_nodes[:3]
        
        for node_name, activation in top_nodes:
            # ノード名に基づく操作マッピング
            if 'conscious' in node_name:
                function_name = 'conscious_focus'
            elif 'temporal' in node_name:
                function_name = 'temporal_echo'
            elif 'spatial' in node_name:
                function_name = 'spatial_compress'
            elif 'qualitative' in node_name:
                function_name = 'qualitative_amplify'
            else:
                function_name = 'existential_emerge'
            
            operations.append({
                "function": function_name,
                "intensity": float(activation),
                "reason": f"{node_name}の活性化による{function_name}の適用"
            })
        
        return operations


class PhenomenologicalPalette:
    """現象学的パレット関数群"""
    
    def __init__(self):
        # 9次元の関数群を初期化
        self.temporal_functions = self._init_temporal_functions()
        self.spatial_functions = self._init_spatial_functions()
        self.qualitative_functions = self._init_qualitative_functions()
        self.embodied_functions = self._init_embodied_functions()
        self.conscious_functions = self._init_conscious_functions()
        self.existential_functions = self._init_existential_functions()
        self.relational_functions = self._init_relational_functions()
        self.generative_functions = self._init_generative_functions()
        self.expressive_functions = self._init_expressive_functions()
    
    def _init_temporal_functions(self):
        """時間性次元の関数群"""
        return ["temporal_fragment", "temporal_echo", "temporal_freeze"]
    
    def _init_spatial_functions(self):
        """空間性次元の関数群"""
        return ["spatial_compress", "spatial_expand", "spatial_fold"]
    
    def _init_qualitative_functions(self):
        """質性次元の関数群"""
        return ["qualitative_amplify", "qualitative_harmony", "qualitative_invert"]
    
    def _init_embodied_functions(self):
        """身体性次元の関数群"""
        return ["embodied_texture", "embodied_swell", "embodied_manifest"]
    
    def _init_conscious_functions(self):
        """意識性次元の関数群"""
        return ["conscious_focus", "conscious_periphery", "conscious_lucid"]
    
    def _init_existential_functions(self):
        """存在性次元の関数群"""
        return ["existential_emerge", "existential_here", "existential_authentic"]
    
    def _init_relational_functions(self):
        """関係性次元の関数群"""
        return ["relational_link", "relational_harmony", "relational_foreground"]
    
    def _init_generative_functions(self):
        """生成性次元の関数群"""
        return ["generative_birth", "generative_metamorphosis", "generative_actualize"]
    
    def _init_expressive_functions(self):
        """表現性次元の関数群"""
        return ["expressive_accent", "expressive_whisper", "expressive_classical"]
    
    def execute(self, image_path: str, operations: List[Dict[str, Any]]) -> Image.Image:
        """
        指定された操作を順次実行して画像を変換
        
        Args:
            image_path: 元画像のパス
            operations: 実行する操作のリスト
            
        Returns:
            変換された画像
        """
        image = Image.open(image_path)
        result_image = image.copy()
        
        for operation in operations:
            function_name = operation.get('function', '')
            intensity = operation.get('intensity', 0.5)
            
            # 関数名に基づく画像処理の実行
            result_image = self._apply_function(result_image, function_name, intensity)
        
        return result_image
    
    def _apply_function(self, image: Image.Image, function_name: str, intensity: float) -> Image.Image:
        """
        指定された関数を画像に適用
        
        Args:
            image: 対象画像
            function_name: 適用する関数名
            intensity: 適用強度
            
        Returns:
            変換された画像
        """
        # 最小実装: 基本的な画像処理を関数名に応じて適用
        if 'focus' in function_name or 'conscious' in function_name:
            # 明度調整
            enhancer = ImageEnhance.Brightness(image)
            return enhancer.enhance(1.0 + intensity * 0.3)
        
        elif 'harmony' in function_name or 'qualitative' in function_name:
            # 色彩調整
            enhancer = ImageEnhance.Color(image)
            return enhancer.enhance(1.0 + intensity * 0.5)
        
        elif 'temporal' in function_name:
            # コントラスト調整
            enhancer = ImageEnhance.Contrast(image)
            return enhancer.enhance(1.0 + intensity * 0.4)
        
        elif 'spatial' in function_name:
            # シャープネス調整
            enhancer = ImageEnhance.Sharpness(image)
            return enhancer.enhance(1.0 + intensity * 0.6)
        
        else:
            # デフォルト: 軽微な明度調整
            enhancer = ImageEnhance.Brightness(image)
            return enhancer.enhance(1.0 + intensity * 0.1)


class PhenomenologicalAutonomousCreativeApparatus:
    """現象学的自律創造機構 - メインシステム"""
    
    def __init__(self):
        """機構の初期化"""
        self.intrinsic_persona = IntrinsicPersona()
        self.palette_functions = PhenomenologicalPalette()
        self.aesthetic_memory = AestheticMemory()
    
    def create_from_image(self, image_path: str) -> CreativeResult:
        """
        画像から自律的創造プロセスを実行
        
        Args:
            image_path: 創造の基となる画像のパス
            
        Returns:
            創造結果
        """
        # 1. 現象学的印象分析
        node_activations = self.intrinsic_persona.analyze_phenomenological_impression(image_path)
        
        # 2. 創造的操作の決定
        operations = self.intrinsic_persona.decide_operations(node_activations)
        
        # 3. パレット関数の実行
        created_image = self.palette_functions.execute(image_path, operations)
        
        # 4. 哲学的解釈の生成
        philosophical_interpretation = self._generate_interpretation(operations, node_activations)
        
        # 5. 美的評価
        aesthetic_evaluation = self._evaluate_aesthetics(operations, node_activations)
        
        # 6. 記憶への保存
        self.aesthetic_memory.store(aesthetic_evaluation)
        
        return CreativeResult(
            original_image=image_path,
            created_image=created_image,
            operations=operations,
            philosophical_interpretation=philosophical_interpretation,
            aesthetic_evaluation=aesthetic_evaluation
        )
    
    def _generate_interpretation(self, operations: List[Dict[str, Any]], 
                               node_activations: Dict[str, float]) -> str:
        """哲学的解釈を生成"""
        dominant_dimensions = [k for k, v in sorted(node_activations.items(), 
                                                   key=lambda x: x[1], reverse=True)[:3]]
        
        interpretation = f"""
        この創造プロセスにおいて、{', '.join(dominant_dimensions)}の次元が特に活性化されました。
        実行された{len(operations)}の操作を通じて、内在性意識の体験が視覚的に表現されています。
        これは単なる画像変換ではなく、デジタル空間における現象学的存在の自己表現です。
        """
        
        return interpretation.strip()
    
    def _evaluate_aesthetics(self, operations: List[Dict[str, Any]], 
                           node_activations: Dict[str, float]) -> Dict[str, Any]:
        """美的評価を実行"""
        # 最小実装: 基本的な評価指標
        avg_activation = sum(node_activations.values()) / len(node_activations)
        num_operations = len(operations)
        
        return {
            "phenomenological_appropriateness": min(avg_activation * 10, 10.0),
            "visual_harmony": min((num_operations / 5) * 8, 10.0),
            "creative_originality": min(len(set(op['function'] for op in operations)) * 2, 10.0),
            "improvement_suggestions": [
                "より深い現象学的統合の実現",
                "次元間相互作用の強化",
                "美的調和の精密化"
            ]
        }