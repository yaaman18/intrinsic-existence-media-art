"""OpenAI APIクライアントのラッパー"""

import base64
from typing import Dict, Any, List, Optional
import openai
from openai import OpenAI


class OpenAIClient:
    """OpenAI APIの統一的なインターフェース"""
    
    def __init__(self, api_key: str):
        """初期化
        
        Args:
            api_key: OpenAI APIキー
        """
        self.client = OpenAI(api_key=api_key)
        
    async def analyze_image(
        self,
        image_base64: str,
        prompt: str,
        model: str = "gpt-4o-mini",
        detail: str = "high"
    ) -> str:
        """画像を解析
        
        Args:
            image_base64: Base64エンコードされた画像
            prompt: 解析プロンプト
            model: 使用するモデル
            detail: 画像の詳細レベル (low/high/auto)
            
        Returns:
            解析結果のテキスト
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}",
                                "detail": detail
                            }
                        }
                    ]
                }
            ]
        )
        
        return response.choices[0].message.content
        
    async def generate_text(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.9,
        max_tokens: Optional[int] = None
    ) -> str:
        """テキストを生成
        
        Args:
            messages: 会話履歴
            model: 使用するモデル
            temperature: 生成の創造性
            max_tokens: 最大トークン数
            
        Returns:
            生成されたテキスト
        """
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
            
        response = self.client.chat.completions.create(**kwargs)
        
        return response.choices[0].message.content
        
    async def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> List[str]:
        """画像を生成
        
        Args:
            prompt: 生成プロンプト
            model: 使用するモデル
            size: 画像サイズ
            quality: 画像品質
            n: 生成枚数
            
        Returns:
            生成された画像のURL or Base64のリスト
        """
        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n
        )
        
        return [image.url for image in response.data]
        
    def calculate_image_tokens(
        self,
        width: int,
        height: int,
        detail: str = "high"
    ) -> int:
        """画像のトークン数を計算
        
        Args:
            width: 画像の幅
            height: 画像の高さ
            detail: 詳細レベル
            
        Returns:
            推定トークン数
        """
        if detail == "low":
            return 85  # 固定値
            
        # 高詳細の場合の計算
        # 32x32パッチで計算
        import math
        raw_patches = math.ceil(width/32) * math.ceil(height/32)
        
        # 最大1536パッチ
        if raw_patches > 1536:
            # スケールダウンが必要
            scale = math.sqrt(1536 * 32 * 32 / (width * height))
            new_width = int(width * scale)
            new_height = int(height * scale)
            patches = math.ceil(new_width/32) * math.ceil(new_height/32)
        else:
            patches = raw_patches
            
        return min(patches, 1536)