"""
Base Effect Library - 基盤エフェクトライブラリ
27ノード専用エフェクトシステムの基盤となる再利用可能な画像処理機能を提供
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
from PIL.ImageFilter import GaussianBlur, UnsharpMask, BLUR, SMOOTH_MORE
import cv2
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
import colorsys
from scipy import ndimage
from scipy.signal import convolve2d


@dataclass
class ProcessingParameters:
    """画像処理パラメータの基底クラス"""
    intensity: float = 0.5
    region_mask: Optional[np.ndarray] = None
    blend_mode: str = "normal"
    
    def __post_init__(self):
        self.intensity = max(0.0, min(1.0, self.intensity))


class ColorSpaceUtils:
    """色空間変換ユーティリティ"""
    
    @staticmethod
    def rgb_to_hsv_array(rgb_array: np.ndarray) -> np.ndarray:
        """RGB配列をHSV配列に変換"""
        return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2HSV)
    
    @staticmethod
    def hsv_to_rgb_array(hsv_array: np.ndarray) -> np.ndarray:
        """HSV配列をRGB配列に変換"""
        return cv2.cvtColor(hsv_array, cv2.COLOR_HSV2RGB)
    
    @staticmethod
    def rgb_to_lab_array(rgb_array: np.ndarray) -> np.ndarray:
        """RGB配列をLAB配列に変換"""
        return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2LAB)
    
    @staticmethod
    def lab_to_rgb_array(lab_array: np.ndarray) -> np.ndarray:
        """LAB配列をRGB配列に変換"""
        return cv2.cvtColor(lab_array, cv2.COLOR_LAB2RGB)


class MaskOperations:
    """マスク操作のユーティリティ"""
    
    @staticmethod
    def create_circular_mask(size: Tuple[int, int], center: Tuple[float, float], 
                           radius: float, feather: float = 0.0) -> np.ndarray:
        """円形マスクの生成"""
        h, w = size
        y, x = np.ogrid[:h, :w]
        center_y, center_x = center[0] * h, center[1] * w
        
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        
        if feather > 0:
            inner_radius = radius * (1 - feather)
            outer_radius = radius
            mask = np.clip((outer_radius - dist) / (outer_radius - inner_radius), 0, 1)
        else:
            mask = (dist <= radius).astype(np.float32)
        
        return mask.astype(np.float32)
    
    @staticmethod
    def create_gradient_mask(size: Tuple[int, int], direction: str = "vertical",
                           start: float = 0.0, end: float = 1.0) -> np.ndarray:
        """グラデーションマスクの生成"""
        h, w = size
        
        if direction == "vertical":
            mask = np.linspace(start, end, h).reshape(-1, 1)
            mask = np.repeat(mask, w, axis=1)
        elif direction == "horizontal":
            mask = np.linspace(start, end, w).reshape(1, -1)
            mask = np.repeat(mask, h, axis=0)
        elif direction == "radial":
            center_y, center_x = h // 2, w // 2
            y, x = np.ogrid[:h, :w]
            dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            max_dist = np.sqrt(center_x**2 + center_y**2)
            mask = np.interp(dist, [0, max_dist], [start, end])
        else:
            raise ValueError(f"Unsupported direction: {direction}")
        
        return mask.astype(np.float32)
    
    @staticmethod
    def apply_mask_to_effect(original: Image.Image, processed: Image.Image, 
                           mask: np.ndarray) -> Image.Image:
        """マスクを適用してエフェクトをブレンド"""
        orig_array = np.array(original).astype(np.float32)
        proc_array = np.array(processed).astype(np.float32)
        
        if len(mask.shape) == 2:
            mask = np.stack([mask] * 3, axis=2)
        
        result = orig_array * (1 - mask) + proc_array * mask
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)


class BaseEffectLibrary:
    """基盤エフェクトライブラリ - 再利用可能な基本処理"""
    
    @staticmethod
    def adjust_rgb_channels(image: Image.Image, r_factor: float = 1.0, 
                          g_factor: float = 1.0, b_factor: float = 1.0,
                          mask: Optional[np.ndarray] = None) -> Image.Image:
        """RGBチャンネル個別調整"""
        img_array = np.array(image).astype(np.float32)
        result = img_array.copy()
        
        result[:, :, 0] *= r_factor  # Red
        result[:, :, 1] *= g_factor  # Green  
        result[:, :, 2] *= b_factor  # Blue
        
        result = np.clip(result, 0, 255).astype(np.uint8)
        processed = Image.fromarray(result)
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def hue_shift(image: Image.Image, shift_degrees: float = 0, 
                 mask: Optional[np.ndarray] = None) -> Image.Image:
        """色相シフト"""
        img_array = np.array(image)
        hsv_array = ColorSpaceUtils.rgb_to_hsv_array(img_array).astype(np.float32)
        
        # 色相値を調整（0-179の範囲で）
        hsv_array[:, :, 0] += shift_degrees / 2  # OpenCVでは色相は0-179
        hsv_array[:, :, 0] = np.mod(hsv_array[:, :, 0], 180)
        
        hsv_array = np.clip(hsv_array, 0, 255).astype(np.uint8)
        result_array = ColorSpaceUtils.hsv_to_rgb_array(hsv_array)
        processed = Image.fromarray(result_array)
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def saturation_adjust(image: Image.Image, factor: float = 1.0,
                         mask: Optional[np.ndarray] = None) -> Image.Image:
        """彩度調整"""
        img_array = np.array(image)
        hsv_array = ColorSpaceUtils.rgb_to_hsv_array(img_array).astype(np.float32)
        
        # 彩度値を調整
        hsv_array[:, :, 1] *= factor
        hsv_array[:, :, 1] = np.clip(hsv_array[:, :, 1], 0, 255)
        
        hsv_array = hsv_array.astype(np.uint8)
        result_array = ColorSpaceUtils.hsv_to_rgb_array(hsv_array)
        processed = Image.fromarray(result_array)
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def luminosity_adjust(image: Image.Image, factor: float = 1.0,
                         mask: Optional[np.ndarray] = None) -> Image.Image:
        """輝度調整（LAB色空間使用）"""
        img_array = np.array(image)
        lab_array = ColorSpaceUtils.rgb_to_lab_array(img_array).astype(np.float32)
        
        # L（輝度）チャンネルを調整
        lab_array[:, :, 0] *= factor
        lab_array[:, :, 0] = np.clip(lab_array[:, :, 0], 0, 255)
        
        lab_array = lab_array.astype(np.uint8)
        result_array = ColorSpaceUtils.lab_to_rgb_array(lab_array)
        processed = Image.fromarray(result_array)
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def gaussian_blur(image: Image.Image, radius: float = 5.0, 
                     mask: Optional[np.ndarray] = None) -> Image.Image:
        """ガウシアンブラー"""
        processed = image.filter(GaussianBlur(radius=radius))
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def unsharp_mask(image: Image.Image, radius: float = 2.0, percent: int = 150,
                    threshold: int = 3, mask: Optional[np.ndarray] = None) -> Image.Image:
        """アンシャープマスク（シャープネス強調）"""
        processed = image.filter(UnsharpMask(radius=radius, percent=percent, threshold=threshold))
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def motion_blur(image: Image.Image, angle: float = 0, distance: int = 15,
                   mask: Optional[np.ndarray] = None) -> Image.Image:
        """モーションブラー"""
        img_array = np.array(image)
        
        # モーションブラーカーネルの作成
        rad = np.deg2rad(angle)
        dx = np.cos(rad) * distance
        dy = np.sin(rad) * distance
        
        kernel = np.zeros((distance, distance))
        cv2.line(kernel, (0, 0), (int(dx), int(dy)), 1, 1)
        
        if kernel.sum() > 0:
            kernel = kernel / kernel.sum()
        else:
            kernel[kernel.shape[0]//2, kernel.shape[1]//2] = 1
        
        # 各チャンネルに適用
        if len(img_array.shape) == 3:
            result = np.zeros_like(img_array)
            for i in range(img_array.shape[2]):
                result[:, :, i] = convolve2d(img_array[:, :, i], kernel, mode='same', boundary='symm')
        else:
            result = convolve2d(img_array, kernel, mode='same', boundary='symm')
        
        processed = Image.fromarray(result.astype(np.uint8))
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def add_noise(image: Image.Image, noise_type: str = "gaussian", amount: float = 0.1,
                 mask: Optional[np.ndarray] = None) -> Image.Image:
        """ノイズ追加"""
        img_array = np.array(image).astype(np.float32)
        
        if noise_type == "gaussian":
            noise = np.random.normal(0, amount * 255, img_array.shape)
        elif noise_type == "uniform":
            noise = np.random.uniform(-amount * 255, amount * 255, img_array.shape)
        elif noise_type == "salt_pepper":
            noise = np.zeros_like(img_array)
            salt_pepper_mask = np.random.random(img_array.shape[:2]) < amount
            # 各チャンネルに同じノイズを適用
            noise_values = 255 * np.random.choice([-1, 1], size=np.sum(salt_pepper_mask))
            for channel in range(img_array.shape[2]):
                noise[salt_pepper_mask, channel] = noise_values
        else:
            raise ValueError(f"Unsupported noise type: {noise_type}")
        
        result = img_array + noise
        result = np.clip(result, 0, 255).astype(np.uint8)
        processed = Image.fromarray(result)
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def edge_enhance(image: Image.Image, factor: float = 1.0,
                    mask: Optional[np.ndarray] = None) -> Image.Image:
        """エッジ強調"""
        enhancer = ImageEnhance.Sharpness(image)
        processed = enhancer.enhance(1.0 + factor)
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def create_vignette(image: Image.Image, intensity: float = 0.5, radius: float = 0.8,
                       mask: Optional[np.ndarray] = None) -> Image.Image:
        """ビネット効果"""
        width, height = image.size
        
        # 楕円形のグラデーションマスクを作成
        center_x, center_y = width / 2, height / 2
        max_dist = min(width, height) * radius / 2
        
        vignette_mask = np.zeros((height, width))
        for y in range(height):
            for x in range(width):
                dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                if dist < max_dist:
                    vignette_mask[y, x] = 1.0
                else:
                    vignette_mask[y, x] = max(0, 1.0 - (dist - max_dist) / (max_dist * 0.5))
        
        # ダークニングを適用
        img_array = np.array(image).astype(np.float32)
        darkening = 1 - intensity * (1 - vignette_mask[:, :, np.newaxis])
        result = img_array * darkening
        result = np.clip(result, 0, 255).astype(np.uint8)
        processed = Image.fromarray(result)
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed


class BlendModes:
    """ブレンドモードの実装"""
    
    @staticmethod
    def normal_blend(base: np.ndarray, overlay: np.ndarray, opacity: float = 1.0) -> np.ndarray:
        """通常ブレンド"""
        return base * (1 - opacity) + overlay * opacity
    
    @staticmethod
    def multiply_blend(base: np.ndarray, overlay: np.ndarray, opacity: float = 1.0) -> np.ndarray:
        """乗算ブレンド"""
        result = (base * overlay) / 255.0
        return base * (1 - opacity) + result * opacity
    
    @staticmethod
    def screen_blend(base: np.ndarray, overlay: np.ndarray, opacity: float = 1.0) -> np.ndarray:
        """スクリーンブレンド"""
        result = 255 - ((255 - base) * (255 - overlay)) / 255.0
        return base * (1 - opacity) + result * opacity
    
    @staticmethod
    def overlay_blend(base: np.ndarray, overlay: np.ndarray, opacity: float = 1.0) -> np.ndarray:
        """オーバーレイブレンド"""
        mask = base < 128
        result = np.where(mask, 
                         2 * base * overlay / 255.0,
                         255 - 2 * (255 - base) * (255 - overlay) / 255.0)
        return base * (1 - opacity) + result * opacity