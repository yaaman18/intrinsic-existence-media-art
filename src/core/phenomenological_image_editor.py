"""
Phenomenological Image Editor - 現象学的画像編集エンジン
統合情報理論（IIT）の内在性概念に基づく画像編集システム
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
from PIL.ImageFilter import GaussianBlur, UnsharpMask, BLUR, SMOOTH_MORE
import cv2
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
import json
from pathlib import Path
import random
from scipy import ndimage
from scipy.signal import convolve2d
import colorsys


@dataclass
class EditParameters:
    """編集パラメータのデータクラス"""
    effect_type: str
    intensity: float = 0.5
    params: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.params is None:
            self.params = {}


class EffectLibrary:
    """画像エフェクトのライブラリ"""
    
    @staticmethod
    def gaussian_blur(image: Image.Image, radius: float = 5.0, sigma: Optional[float] = None) -> Image.Image:
        """ガウシアンブラー効果"""
        if sigma is None:
            sigma = radius * 0.3
        return image.filter(GaussianBlur(radius=radius))
    
    @staticmethod
    def motion_blur(image: Image.Image, angle: float = 0, distance: int = 15) -> Image.Image:
        """モーションブラー効果"""
        # OpenCVを使用
        img_array = np.array(image)
        
        # モーションブラーカーネルの作成
        rad = np.deg2rad(angle)
        dx = np.cos(rad) * distance
        dy = np.sin(rad) * distance
        
        kernel = np.zeros((distance, distance))
        cv2.line(kernel, (0, 0), (int(dx), int(dy)), 1, 1)
        kernel = kernel / kernel.sum()
        
        # 各チャンネルに適用
        if len(img_array.shape) == 3:
            result = np.zeros_like(img_array)
            for i in range(img_array.shape[2]):
                result[:, :, i] = convolve2d(img_array[:, :, i], kernel, mode='same', boundary='symm')
        else:
            result = convolve2d(img_array, kernel, mode='same', boundary='symm')
        
        return Image.fromarray(result.astype(np.uint8))
    
    @staticmethod
    def brightness_adjust(image: Image.Image, factor: float = 1.0) -> Image.Image:
        """明度調整"""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def contrast_adjust(image: Image.Image, factor: float = 1.0) -> Image.Image:
        """コントラスト調整"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def color_adjust(image: Image.Image, factor: float = 1.0) -> Image.Image:
        """彩度調整"""
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def color_temperature(image: Image.Image, temperature: float = 0) -> Image.Image:
        """色温度調整 (-1.0: 寒色, 0: 中性, 1.0: 暖色)"""
        img_array = np.array(image)
        
        # 色温度マトリックス
        if temperature > 0:  # 暖色
            matrix = [
                1.0 + 0.1 * temperature, 0, 0,
                0, 1.0, 0,
                0, 0, 1.0 - 0.1 * temperature
            ]
        else:  # 寒色
            matrix = [
                1.0 + 0.1 * temperature, 0, 0,
                0, 1.0, 0,
                0, 0, 1.0 - 0.1 * temperature
            ]
        
        # RGBチャンネルの調整
        result = img_array.copy()
        result[:, :, 0] = np.clip(img_array[:, :, 0] * matrix[0], 0, 255)
        result[:, :, 1] = np.clip(img_array[:, :, 1] * matrix[4], 0, 255)
        result[:, :, 2] = np.clip(img_array[:, :, 2] * matrix[8], 0, 255)
        
        return Image.fromarray(result.astype(np.uint8))
    
    @staticmethod
    def add_noise(image: Image.Image, noise_type: str = "gaussian", amount: float = 0.1) -> Image.Image:
        """ノイズ追加"""
        img_array = np.array(image)
        
        if noise_type == "gaussian":
            noise = np.random.normal(0, amount * 255, img_array.shape)
            result = img_array + noise
        elif noise_type == "salt_pepper":
            result = img_array.copy()
            # 塩ノイズ
            salt = np.random.random(img_array.shape[:2]) < amount / 2
            result[salt] = 255
            # 胡椒ノイズ
            pepper = np.random.random(img_array.shape[:2]) < amount / 2
            result[pepper] = 0
        else:
            result = img_array
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
    
    @staticmethod
    def edge_enhance(image: Image.Image, factor: float = 1.0) -> Image.Image:
        """エッジ強調"""
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(1 + factor)
    
    @staticmethod
    def vignette(image: Image.Image, intensity: float = 0.5, radius: float = 0.8) -> Image.Image:
        """ビネット効果（周辺減光）"""
        width, height = image.size
        center_x, center_y = width // 2, height // 2
        
        # マスク作成
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        # グラデーション円を描画
        for i in range(int(min(width, height) * radius), 0, -1):
            alpha = int(255 * (1 - (i / (min(width, height) * radius)) ** 2))
            draw.ellipse(
                [center_x - i, center_y - i, center_x + i, center_y + i],
                fill=alpha
            )
        
        # マスクを反転して適用
        mask = ImageOps.invert(mask)
        black = Image.new('RGB', (width, height), (0, 0, 0))
        
        # ブレンド
        result = Image.composite(black, image, mask)
        return Image.blend(image, result, intensity)
    
    @staticmethod
    def chromatic_aberration(image: Image.Image, shift: int = 5) -> Image.Image:
        """色収差効果"""
        r, g, b = image.split()
        
        # 赤チャンネルを左にシフト
        r_array = np.array(r)
        r_shifted = np.roll(r_array, -shift, axis=1)
        
        # 青チャンネルを右にシフト
        b_array = np.array(b)
        b_shifted = np.roll(b_array, shift, axis=1)
        
        # 再結合
        return Image.merge('RGB', [
            Image.fromarray(r_shifted),
            g,
            Image.fromarray(b_shifted)
        ])
    
    @staticmethod
    def fog_effect(image: Image.Image, density: float = 0.5, color: Tuple[int, int, int] = (220, 220, 220)) -> Image.Image:
        """霧効果"""
        # ブラー適用
        blurred = EffectLibrary.gaussian_blur(image, radius=density * 20)
        
        # 霧の色レイヤー作成
        fog_layer = Image.new('RGB', image.size, color)
        
        # ブレンド
        result = Image.blend(image, blurred, density * 0.5)
        result = Image.blend(result, fog_layer, density * 0.3)
        
        # 明度を上げる
        return EffectLibrary.brightness_adjust(result, 1 + density * 0.2)
    
    @staticmethod
    def glitch_effect(image: Image.Image, intensity: float = 0.5) -> Image.Image:
        """グリッチ効果"""
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        
        result = img_array.copy()
        
        # ランダムな水平線のシフト
        num_glitches = int(height * intensity * 0.1)
        for _ in range(num_glitches):
            y = random.randint(0, height - 10)
            h = random.randint(5, 20)
            shift = random.randint(-int(width * 0.1), int(width * 0.1))
            
            if y + h < height:
                result[y:y+h] = np.roll(result[y:y+h], shift, axis=1)
        
        # 色チャンネルのずれ
        if random.random() < intensity:
            result = np.array(EffectLibrary.chromatic_aberration(
                Image.fromarray(result), 
                shift=int(intensity * 10)
            ))
        
        return Image.fromarray(result)
    
    @staticmethod
    def texture_overlay(image: Image.Image, texture_type: str = "grain", intensity: float = 0.5) -> Image.Image:
        """テクスチャオーバーレイ"""
        width, height = image.size
        
        if texture_type == "grain":
            # フィルムグレイン効果
            grain = np.random.normal(128, intensity * 30, (height, width))
            grain = np.clip(grain, 0, 255).astype(np.uint8)
            grain_img = Image.fromarray(grain).convert('RGB')
            return Image.blend(image, grain_img, intensity * 0.3)
        
        elif texture_type == "canvas":
            # キャンバステクスチャ
            texture = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(texture)
            
            # 縦横の線を描画
            for x in range(0, width, 3):
                draw.line([(x, 0), (x, height)], fill=(240, 240, 240), width=1)
            for y in range(0, height, 3):
                draw.line([(0, y), (width, y)], fill=(240, 240, 240), width=1)
            
            return Image.blend(image, texture, intensity * 0.2)
        
        return image
    
    # ==================== RGB色彩編集機能 ====================
    
    @staticmethod
    def adjust_rgb_channels(image: Image.Image, r_factor: float = 1.0, g_factor: float = 1.0, b_factor: float = 1.0) -> Image.Image:
        """RGBチャンネルの個別調整"""
        img_array = np.array(image)
        
        # 各チャンネルに係数を適用
        result = img_array.copy().astype(np.float32)
        result[:, :, 0] *= r_factor  # 赤チャンネル
        result[:, :, 1] *= g_factor  # 緑チャンネル
        result[:, :, 2] *= b_factor  # 青チャンネル
        
        # 0-255の範囲に制限
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    @staticmethod
    def adjust_rgb_offset(image: Image.Image, r_offset: int = 0, g_offset: int = 0, b_offset: int = 0) -> Image.Image:
        """RGBチャンネルのオフセット調整（加算）"""
        img_array = np.array(image)
        
        result = img_array.copy().astype(np.int32)
        result[:, :, 0] += r_offset  # 赤チャンネルに加算
        result[:, :, 1] += g_offset  # 緑チャンネルに加算
        result[:, :, 2] += b_offset  # 青チャンネルに加算
        
        # 0-255の範囲に制限
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    @staticmethod
    def color_balance(image: Image.Image, shadows: Tuple[float, float, float] = (1.0, 1.0, 1.0),
                     midtones: Tuple[float, float, float] = (1.0, 1.0, 1.0),
                     highlights: Tuple[float, float, float] = (1.0, 1.0, 1.0)) -> Image.Image:
        """シャドウ・ミッドトーン・ハイライトの色バランス調整"""
        img_array = np.array(image).astype(np.float32)
        
        # 輝度を計算（0-1の範囲）
        luminance = (0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]) / 255.0
        
        # シャドウ、ミッドトーン、ハイライトのマスクを作成
        shadow_mask = np.where(luminance < 0.33, 1.0 - luminance * 3, 0.0)
        highlight_mask = np.where(luminance > 0.67, (luminance - 0.67) * 3, 0.0)
        midtone_mask = 1.0 - shadow_mask - highlight_mask
        
        result = img_array.copy()
        
        # 各チャンネルにマスクを適用
        for c in range(3):
            shadow_adjust = img_array[:, :, c] * shadows[c]
            midtone_adjust = img_array[:, :, c] * midtones[c]
            highlight_adjust = img_array[:, :, c] * highlights[c]
            
            result[:, :, c] = (shadow_adjust * shadow_mask + 
                              midtone_adjust * midtone_mask + 
                              highlight_adjust * highlight_mask)
        
        # 0-255の範囲に制限
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    @staticmethod
    def hue_shift(image: Image.Image, shift_degrees: float = 0) -> Image.Image:
        """色相シフト（HSV色空間での操作）"""
        # RGBをHSVに変換
        img_array = np.array(image).astype(np.float32) / 255.0
        
        # NumPyでHSV変換を手動実装
        result_hsv = np.zeros_like(img_array)
        
        for y in range(img_array.shape[0]):
            for x in range(img_array.shape[1]):
                r, g, b = img_array[y, x]
                h, s, v = colorsys.rgb_to_hsv(r, g, b)
                
                # 色相をシフト（0-1の範囲で正規化）
                h = (h + shift_degrees / 360.0) % 1.0
                
                r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
                result_hsv[y, x] = [r_new, g_new, b_new]
        
        # 0-255の範囲に戻す
        result = (result_hsv * 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    @staticmethod
    def saturation_adjust(image: Image.Image, factor: float = 1.0) -> Image.Image:
        """彩度調整"""
        img_array = np.array(image).astype(np.float32)
        
        # グレースケール値を計算
        gray = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]
        gray = np.stack([gray, gray, gray], axis=2)
        
        # 元画像とグレースケールの線形補間
        result = gray + factor * (img_array - gray)
        
        # 0-255の範囲に制限
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    @staticmethod
    def selective_color_replace(image: Image.Image, target_color: Tuple[int, int, int], 
                               replacement_color: Tuple[int, int, int], threshold: float = 30.0) -> Image.Image:
        """特定色の選択的置換"""
        img_array = np.array(image)
        result = img_array.copy()
        
        target = np.array(target_color)
        replacement = np.array(replacement_color)
        
        # 各ピクセルとターゲット色の距離を計算
        diff = img_array.astype(np.float32) - target.astype(np.float32)
        distance = np.sqrt(np.sum(diff ** 2, axis=2))
        
        # しきい値以下のピクセルを置換
        mask = distance <= threshold
        
        # マスクに基づいて色を置換（グラデーション効果付き）
        for c in range(3):
            blend_factor = np.maximum(0, 1 - distance / threshold)
            result[:, :, c] = np.where(mask, 
                                     img_array[:, :, c] * (1 - blend_factor) + replacement[c] * blend_factor,
                                     img_array[:, :, c])
        
        return Image.fromarray(result.astype(np.uint8))
    
    @staticmethod
    def channel_mixer(image: Image.Image, red_mix: Tuple[float, float, float] = (1.0, 0.0, 0.0),
                     green_mix: Tuple[float, float, float] = (0.0, 1.0, 0.0),
                     blue_mix: Tuple[float, float, float] = (0.0, 0.0, 1.0)) -> Image.Image:
        """RGBチャンネルミキサー"""
        img_array = np.array(image).astype(np.float32)
        
        result = np.zeros_like(img_array)
        
        # 各出力チャンネルを入力チャンネルの混合として計算
        result[:, :, 0] = (img_array[:, :, 0] * red_mix[0] + 
                          img_array[:, :, 1] * red_mix[1] + 
                          img_array[:, :, 2] * red_mix[2])
        
        result[:, :, 1] = (img_array[:, :, 0] * green_mix[0] + 
                          img_array[:, :, 1] * green_mix[1] + 
                          img_array[:, :, 2] * green_mix[2])
        
        result[:, :, 2] = (img_array[:, :, 0] * blue_mix[0] + 
                          img_array[:, :, 1] * blue_mix[1] + 
                          img_array[:, :, 2] * blue_mix[2])
        
        # 0-255の範囲に制限
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    @staticmethod
    def sepia_effect(image: Image.Image, intensity: float = 1.0) -> Image.Image:
        """セピア効果（古い写真風）"""
        sepia_mix = (
            (0.393, 0.769, 0.189),  # 赤チャンネル
            (0.349, 0.686, 0.168),  # 緑チャンネル
            (0.272, 0.534, 0.131)   # 青チャンネル
        )
        
        sepia = EffectLibrary.channel_mixer(image, sepia_mix[0], sepia_mix[1], sepia_mix[2])
        
        # 強度に応じて元画像とブレンド
        return Image.blend(image, sepia, intensity)
    
    @staticmethod
    def monochrome_tint(image: Image.Image, tint_color: Tuple[int, int, int] = (255, 255, 255), intensity: float = 1.0) -> Image.Image:
        """モノクローム着色"""
        # グレースケール変換
        gray = image.convert('L')
        gray_rgb = gray.convert('RGB')
        
        # ティント色でカラーライズ
        tinted = ImageOps.colorize(gray, black=(0, 0, 0), white=tint_color)
        
        # 強度に応じて元画像とブレンド
        return Image.blend(image, tinted, intensity)
    
    @staticmethod
    def color_grade_cinematic(image: Image.Image, style: str = "warm", intensity: float = 0.5) -> Image.Image:
        """映画的カラーグレーディング"""
        img_array = np.array(image).astype(np.float32)
        
        if style == "warm":
            # 暖色系（オレンジ&ティール）
            shadows = (1.1, 0.95, 0.8)     # シャドウを暖色に
            highlights = (0.9, 1.0, 1.2)   # ハイライトを寒色に
        elif style == "cool":
            # 寒色系（ブルー&イエロー）
            shadows = (0.8, 0.9, 1.2)      # シャドウを寒色に
            highlights = (1.2, 1.1, 0.8)   # ハイライトを暖色に
        elif style == "vintage":
            # ヴィンテージ
            shadows = (1.0, 0.9, 0.7)      # 温かいシャドウ
            highlights = (1.1, 1.0, 0.9)   # 柔らかいハイライト
        else:
            # デフォルト
            shadows = (1.0, 1.0, 1.0)
            highlights = (1.0, 1.0, 1.0)
        
        # カラーバランス適用
        graded = EffectLibrary.color_balance(image, shadows=shadows, highlights=highlights)
        
        # 強度に応じてブレンド
        return Image.blend(image, graded, intensity)


class MaskGenerator:
    """位置マスク生成クラス"""
    
    @staticmethod
    def full_mask(size: Tuple[int, int]) -> np.ndarray:
        """全体マスク"""
        return np.ones(size, dtype=np.float32)
    
    @staticmethod
    def center_mask(size: Tuple[int, int], radius_ratio: float = 0.5, feather: float = 0.2) -> np.ndarray:
        """中央マスク（円形グラデーション）"""
        width, height = size
        center_x, center_y = width // 2, height // 2
        
        y, x = np.ogrid[:height, :width]
        mask = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        
        # 正規化
        max_radius = min(width, height) * radius_ratio / 2
        mask = 1 - (mask / max_radius)
        
        # フェザリング
        if feather > 0:
            mask = np.clip((mask - (1 - feather)) / feather, 0, 1)
        else:
            mask = np.clip(mask, 0, 1)
        
        return mask.astype(np.float32)
    
    @staticmethod
    def edge_mask(size: Tuple[int, int], thickness: float = 0.2) -> np.ndarray:
        """境界マスク"""
        width, height = size
        mask = np.ones((height, width), dtype=np.float32)
        
        # 内側の矩形を0にする
        border = int(min(width, height) * thickness)
        mask[border:-border, border:-border] = 0
        
        # ガウシアンブラーでソフトに
        mask = ndimage.gaussian_filter(mask, sigma=border * 0.3)
        
        return mask
    
    @staticmethod
    def gradient_mask(size: Tuple[int, int], direction: str = "vertical", reverse: bool = False) -> np.ndarray:
        """グラデーションマスク"""
        width, height = size
        
        if direction == "vertical":
            mask = np.linspace(0, 1, height).reshape(-1, 1)
            mask = np.repeat(mask, width, axis=1)
        elif direction == "horizontal":
            mask = np.linspace(0, 1, width).reshape(1, -1)
            mask = np.repeat(mask, height, axis=0)
        elif direction == "radial":
            return MaskGenerator.center_mask(size, radius_ratio=1.0, feather=1.0)
        else:
            mask = np.ones((height, width))
        
        if reverse:
            mask = 1 - mask
        
        return mask.astype(np.float32)
    
    @staticmethod
    def custom_mask(size: Tuple[int, int], regions: List[Dict[str, Any]]) -> np.ndarray:
        """カスタムマスク（複数領域の組み合わせ）"""
        mask = np.zeros(size[::-1], dtype=np.float32)  # height, width
        
        for region in regions:
            region_type = region.get('type', 'rectangle')
            
            if region_type == 'rectangle':
                x, y, w, h = region['bounds']
                mask[y:y+h, x:x+w] = region.get('opacity', 1.0)
            
            elif region_type == 'circle':
                cx, cy, r = region['center_x'], region['center_y'], region['radius']
                y, x = np.ogrid[:size[1], :size[0]]
                circle_mask = (x - cx)**2 + (y - cy)**2 <= r**2
                mask[circle_mask] = region.get('opacity', 1.0)
        
        # スムージング
        if any(r.get('smooth', False) for r in regions):
            mask = ndimage.gaussian_filter(mask, sigma=5)
        
        return mask


class PhenomenologicalImageEditor:
    """現象学的画像編集エンジン"""
    
    def __init__(self):
        self.effects = EffectLibrary()
        self.mask_gen = MaskGenerator()
        self.edit_history = []
        self.layer_stack = []
        
    def apply_effect(self, 
                    image: Image.Image, 
                    effect_name: str, 
                    intensity: float = 0.5,
                    params: Optional[Dict[str, Any]] = None,
                    mask: Optional[np.ndarray] = None) -> Image.Image:
        """単一エフェクトの適用"""
        
        if params is None:
            params = {}
        
        # エフェクトの取得と実行
        effect_func = getattr(self.effects, effect_name, None)
        if effect_func is None:
            print(f"Warning: Effect '{effect_name}' not found")
            return image
        
        # デフォルトパラメータの調整
        adjusted_params = self._adjust_parameters(effect_name, intensity, params)
        
        # エフェクト適用
        try:
            effected = effect_func(image, **adjusted_params)
        except Exception as e:
            print(f"Error applying effect {effect_name}: {e}")
            return image
        
        # マスク適用
        if mask is not None:
            effected = self._apply_mask(image, effected, mask, intensity)
        else:
            # 全体的な強度調整
            effected = Image.blend(image, effected, intensity)
        
        return effected
    
    def _adjust_parameters(self, effect_name: str, intensity: float, params: Dict[str, Any]) -> Dict[str, Any]:
        """エフェクトパラメータの調整"""
        adjusted = params.copy()
        
        # エフェクトごとのデフォルト値と強度マッピング
        defaults = {
            'gaussian_blur': {
                'radius': lambda i: i * 20,
                'sigma': lambda i: i * 6
            },
            'motion_blur': {
                'angle': lambda i: params.get('angle', 45),
                'distance': lambda i: int(i * 30)
            },
            'brightness_adjust': {
                'factor': lambda i: 1 + (i - 0.5) * 2  # 0-2の範囲
            },
            'contrast_adjust': {
                'factor': lambda i: 1 + (i - 0.5) * 2
            },
            'color_adjust': {
                'factor': lambda i: 1 + (i - 0.5) * 2
            },
            'color_temperature': {
                'temperature': lambda i: (i - 0.5) * 2  # -1 to 1
            },
            'add_noise': {
                'noise_type': lambda i: params.get('noise_type', 'gaussian'),
                'amount': lambda i: i * 0.3
            },
            'edge_enhance': {
                'factor': lambda i: i * 2
            },
            'vignette': {
                'intensity': lambda i: i,
                'radius': lambda i: 0.5 + i * 0.5
            },
            'chromatic_aberration': {
                'shift': lambda i: int(i * 15)
            },
            'fog_effect': {
                'density': lambda i: i,
                'color': lambda i: params.get('color', (220, 220, 220))
            },
            'glitch_effect': {
                'intensity': lambda i: i
            },
            'texture_overlay': {
                'texture_type': lambda i: params.get('texture_type', 'grain'),
                'intensity': lambda i: i
            },
            # RGB色彩編集機能
            'adjust_rgb_channels': {
                'r_factor': lambda i: params.get('r_factor', 1.0),
                'g_factor': lambda i: params.get('g_factor', 1.0),
                'b_factor': lambda i: params.get('b_factor', 1.0)
            },
            'adjust_rgb_offset': {
                'r_offset': lambda i: int(params.get('r_offset', 0)),
                'g_offset': lambda i: int(params.get('g_offset', 0)),
                'b_offset': lambda i: int(params.get('b_offset', 0))
            },
            'color_balance': {
                'shadows': lambda i: params.get('shadows', (1.0, 1.0, 1.0)),
                'midtones': lambda i: params.get('midtones', (1.0, 1.0, 1.0)),
                'highlights': lambda i: params.get('highlights', (1.0, 1.0, 1.0))
            },
            'hue_shift': {
                'shift_degrees': lambda i: (i - 0.5) * 360  # -180 to 180度
            },
            'saturation_adjust': {
                'factor': lambda i: i * 2  # 0-2の範囲
            },
            'selective_color_replace': {
                'target_color': lambda i: params.get('target_color', (255, 0, 0)),
                'replacement_color': lambda i: params.get('replacement_color', (0, 255, 0)),
                'threshold': lambda i: i * 100  # 0-100の閾値
            },
            'channel_mixer': {
                'red_mix': lambda i: params.get('red_mix', (1.0, 0.0, 0.0)),
                'green_mix': lambda i: params.get('green_mix', (0.0, 1.0, 0.0)),
                'blue_mix': lambda i: params.get('blue_mix', (0.0, 0.0, 1.0))
            },
            'sepia_effect': {
                'intensity': lambda i: i
            },
            'monochrome_tint': {
                'tint_color': lambda i: params.get('tint_color', (255, 255, 255)),
                'intensity': lambda i: i
            },
            'color_grade_cinematic': {
                'style': lambda i: params.get('style', 'warm'),
                'intensity': lambda i: i
            }
        }
        
        if effect_name in defaults:
            for param, func in defaults[effect_name].items():
                if param not in adjusted:
                    adjusted[param] = func(intensity)
        
        return adjusted
    
    def _apply_mask(self, 
                   original: Image.Image, 
                   effected: Image.Image, 
                   mask: np.ndarray, 
                   intensity: float) -> Image.Image:
        """マスクを使用したエフェクトの適用"""
        # マスクを画像サイズに合わせる
        if mask.shape != (original.height, original.width):
            mask = cv2.resize(mask, (original.width, original.height))
        
        # 強度調整
        mask = mask * intensity
        
        # PILイメージとして変換
        mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
        
        # コンポジット
        return Image.composite(effected, original, mask_img)
    
    def apply_multiple_effects(self,
                             image: Image.Image,
                             effects: List[Dict[str, Any]],
                             blend_mode: str = "normal") -> Image.Image:
        """複数エフェクトの適用"""
        result = image.copy()
        
        for effect in effects:
            effect_name = effect.get('name', '')
            intensity = effect.get('intensity', 0.5)
            params = effect.get('params', {})
            
            # マスクの生成
            mask = None
            if 'mask' in effect:
                mask_config = effect['mask']
                mask = self._generate_mask(image.size, mask_config)
            
            # エフェクト適用
            if blend_mode == "layer":
                # レイヤーとして管理
                layer = self.apply_effect(image, effect_name, intensity, params, mask)
                self.layer_stack.append({
                    'image': layer,
                    'opacity': effect.get('opacity', 1.0),
                    'blend_mode': effect.get('blend_mode', 'normal')
                })
            else:
                # 順次適用
                result = self.apply_effect(result, effect_name, intensity, params, mask)
        
        # レイヤーの合成
        if blend_mode == "layer" and self.layer_stack:
            result = self._composite_layers(image)
        
        return result
    
    def _generate_mask(self, size: Tuple[int, int], mask_config: Dict[str, Any]) -> np.ndarray:
        """マスクの生成"""
        mask_type = mask_config.get('type', 'full')
        
        if mask_type == 'full':
            return self.mask_gen.full_mask(size)
        elif mask_type == 'center':
            return self.mask_gen.center_mask(
                size, 
                radius_ratio=mask_config.get('radius', 0.5),
                feather=mask_config.get('feather', 0.2)
            )
        elif mask_type == 'edge':
            return self.mask_gen.edge_mask(
                size,
                thickness=mask_config.get('thickness', 0.2)
            )
        elif mask_type == 'gradient':
            return self.mask_gen.gradient_mask(
                size,
                direction=mask_config.get('direction', 'vertical'),
                reverse=mask_config.get('reverse', False)
            )
        elif mask_type == 'custom':
            return self.mask_gen.custom_mask(
                size,
                regions=mask_config.get('regions', [])
            )
        else:
            return self.mask_gen.full_mask(size)
    
    def _composite_layers(self, base: Image.Image) -> Image.Image:
        """レイヤーの合成"""
        result = base.copy()
        
        for layer in self.layer_stack:
            layer_img = layer['image']
            opacity = layer['opacity']
            
            if opacity < 1.0:
                layer_img = Image.blend(result, layer_img, opacity)
            
            result = layer_img
        
        # レイヤースタックをクリア
        self.layer_stack.clear()
        
        return result
    
    def apply_phenomenological_edit(self,
                                  image: Image.Image,
                                  instruction: Dict[str, Any]) -> Image.Image:
        """現象学的編集指示の適用"""
        # 編集指示の解析
        action = instruction.get('action', '')
        intensity = instruction.get('intensity', 0.5)
        dimensions = instruction.get('dimension', [])
        location = instruction.get('location', '画像全体')
        
        # 位置からマスクを生成
        mask = self._parse_location_to_mask(image.size, location)
        
        # アクションから具体的なエフェクトに変換
        effects = self._parse_action_to_effects(action, intensity, dimensions)
        
        # エフェクトの適用
        result = image.copy()
        for effect in effects:
            effect['mask'] = mask
            result = self.apply_effect(
                result,
                effect['name'],
                effect['intensity'],
                effect.get('params', {}),
                mask
            )
        
        # 履歴に記録
        self.edit_history.append({
            'instruction': instruction,
            'effects': effects,
            'timestamp': np.datetime64('now')
        })
        
        return result
    
    def _parse_location_to_mask(self, size: Tuple[int, int], location: str) -> np.ndarray:
        """位置指定をマスクに変換"""
        location_lower = location.lower()
        
        if '全体' in location_lower or 'all' in location_lower:
            return self.mask_gen.full_mask(size)
        elif '中央' in location_lower or 'center' in location_lower:
            return self.mask_gen.center_mask(size)
        elif '境界' in location_lower or 'edge' in location_lower:
            return self.mask_gen.edge_mask(size)
        elif '上部' in location_lower or 'top' in location_lower:
            return self.mask_gen.gradient_mask(size, 'vertical', reverse=True)
        elif '下部' in location_lower or 'bottom' in location_lower:
            return self.mask_gen.gradient_mask(size, 'vertical', reverse=False)
        else:
            return self.mask_gen.full_mask(size)
    
    def _parse_action_to_effects(self, action: str, intensity: float, dimensions: List[str]) -> List[Dict[str, Any]]:
        """アクションを具体的なエフェクトに変換"""
        effects = []
        action_lower = action.lower()
        
        # キーワードベースの変換
        if '霧' in action or 'fog' in action_lower:
            effects.append({
                'name': 'fog_effect',
                'intensity': intensity,
                'params': {'density': intensity}
            })
        
        if 'ぼかし' in action or 'blur' in action_lower:
            blur_type = 'motion_blur' if '動' in action else 'gaussian_blur'
            effects.append({
                'name': blur_type,
                'intensity': intensity,
                'params': {}
            })
        
        if '明' in action or 'bright' in action_lower:
            effects.append({
                'name': 'brightness_adjust',
                'intensity': intensity,
                'params': {'factor': 1 + intensity * 0.5}
            })
        
        if '暗' in action or 'dark' in action_lower:
            effects.append({
                'name': 'brightness_adjust',
                'intensity': intensity,
                'params': {'factor': 1 - intensity * 0.5}
            })
        
        if 'コントラスト' in action or 'contrast' in action_lower:
            effects.append({
                'name': 'contrast_adjust',
                'intensity': intensity,
                'params': {}
            })
        
        if '色' in action or 'color' in action_lower:
            if '温度' in action or 'temperature' in action_lower:
                effects.append({
                    'name': 'color_temperature',
                    'intensity': intensity,
                    'params': {}
                })
            else:
                effects.append({
                    'name': 'color_adjust',
                    'intensity': intensity,
                    'params': {}
                })
        
        if 'ノイズ' in action or 'noise' in action_lower:
            effects.append({
                'name': 'add_noise',
                'intensity': intensity,
                'params': {'noise_type': 'gaussian'}
            })
        
        if 'エッジ' in action or 'edge' in action_lower:
            effects.append({
                'name': 'edge_enhance',
                'intensity': intensity,
                'params': {}
            })
        
        if 'グリッチ' in action or 'glitch' in action_lower:
            effects.append({
                'name': 'glitch_effect',
                'intensity': intensity,
                'params': {}
            })
        
        # RGB色彩編集の検出
        if 'rgb' in action_lower or 'チャンネル' in action:
            if '赤' in action or 'red' in action_lower:
                effects.append({
                    'name': 'adjust_rgb_channels',
                    'intensity': intensity,
                    'params': {'r_factor': 1 + intensity * 0.5, 'g_factor': 1.0, 'b_factor': 1.0}
                })
            elif '緑' in action or 'green' in action_lower:
                effects.append({
                    'name': 'adjust_rgb_channels',
                    'intensity': intensity,
                    'params': {'r_factor': 1.0, 'g_factor': 1 + intensity * 0.5, 'b_factor': 1.0}
                })
            elif '青' in action or 'blue' in action_lower:
                effects.append({
                    'name': 'adjust_rgb_channels',
                    'intensity': intensity,
                    'params': {'r_factor': 1.0, 'g_factor': 1.0, 'b_factor': 1 + intensity * 0.5}
                })
        
        if '色相' in action or 'hue' in action_lower:
            effects.append({
                'name': 'hue_shift',
                'intensity': intensity,
                'params': {}
            })
        
        if '彩度' in action or 'saturation' in action_lower:
            effects.append({
                'name': 'saturation_adjust',
                'intensity': intensity,
                'params': {}
            })
        
        if 'セピア' in action or 'sepia' in action_lower:
            effects.append({
                'name': 'sepia_effect',
                'intensity': intensity,
                'params': {}
            })
        
        if 'モノクローム' in action or 'monochrome' in action_lower:
            tint_color = (255, 220, 180) if '暖' in action else (180, 200, 255) if '寒' in action else (255, 255, 255)
            effects.append({
                'name': 'monochrome_tint',
                'intensity': intensity,
                'params': {'tint_color': tint_color}
            })
        
        if '映画' in action or 'cinematic' in action_lower or 'グレーディング' in action:
            style = 'warm' if '暖' in action else 'cool' if '寒' in action else 'vintage' if 'ヴィンテージ' in action else 'warm'
            effects.append({
                'name': 'color_grade_cinematic',
                'intensity': intensity,
                'params': {'style': style}
            })
        
        if '記憶' in action or 'memory' in action_lower:
            # 記憶の色調（セピア調）
            effects.append({
                'name': 'sepia_effect',
                'intensity': intensity * 0.7,
                'params': {}
            })
        
        if '感情' in action or 'emotion' in action_lower:
            # 感情の色彩（暖色系）
            effects.append({
                'name': 'color_grade_cinematic',
                'intensity': intensity,
                'params': {'style': 'warm'}
            })
        
        # 次元ベースの追加エフェクト
        for dim in dimensions:
            if 'temporal' in dim:
                if not any(e['name'] == 'motion_blur' for e in effects):
                    effects.append({
                        'name': 'motion_blur',
                        'intensity': intensity * 0.5,
                        'params': {'angle': 45}
                    })
            elif 'synesthetic' in dim:
                effects.append({
                    'name': 'texture_overlay',
                    'intensity': intensity * 0.3,
                    'params': {'texture_type': 'grain'}
                })
        
        # デフォルトエフェクト
        if not effects:
            effects.append({
                'name': 'gaussian_blur',
                'intensity': intensity * 0.5,
                'params': {}
            })
        
        return effects
    
    def save_edit_history(self, filepath: str):
        """編集履歴の保存"""
        history_data = []
        for entry in self.edit_history:
            # numpy型を通常の型に変換
            clean_entry = {
                'instruction': entry['instruction'],
                'effects': entry['effects'],
                'timestamp': str(entry['timestamp'])
            }
            history_data.append(clean_entry)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
    
    def load_edit_history(self, filepath: str):
        """編集履歴の読み込み"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.edit_history = json.load(f)


# テスト用のメイン関数
if __name__ == "__main__":
    print("Phenomenological Image Editor - Test Mode")
    
    # エディタのインスタンス化
    editor = PhenomenologicalImageEditor()
    
    # サンプル画像の作成（テスト用）
    test_image = Image.new('RGB', (800, 600), color=(100, 150, 200))
    
    # 単一エフェクトのテスト
    print("\n1. Testing single effect: gaussian_blur")
    blurred = editor.apply_effect(test_image, 'gaussian_blur', intensity=0.7)
    
    # 複数エフェクトのテスト
    print("\n2. Testing multiple effects")
    effects = [
        {'name': 'fog_effect', 'intensity': 0.5},
        {'name': 'vignette', 'intensity': 0.3},
        {'name': 'color_temperature', 'intensity': 0.6, 'params': {'temperature': 0.5}}
    ]
    multi_effect = editor.apply_multiple_effects(test_image, effects)
    
    # 現象学的編集指示のテスト
    print("\n3. Testing phenomenological instruction")
    instruction = {
        'action': '霧の密度を高める',
        'location': '画像全体',
        'dimension': ['appearance', 'temporal'],
        'intensity': 0.6
    }
    result = editor.apply_phenomenological_edit(test_image, instruction)
    
    print("\nAll tests completed!")
    print(f"Available effects: {[name for name in dir(EffectLibrary) if not name.startswith('_')]}")