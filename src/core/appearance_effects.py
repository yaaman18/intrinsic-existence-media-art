"""
Appearance Effects - 現出様式エフェクト
フッサール現象学の「現出」概念に基づく3つのノード専用エフェクト実装

1. density（視覚的密度） - フッサールの「充実」（Erfüllung）概念
2. luminosity（光の強度） - ハイデガーの「明け開け」（Lichtung）概念  
3. chromaticity（色彩の質） - メルロ＝ポンティの「肉」（chair）概念
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import cv2
from typing import Tuple, Optional
from scipy import ndimage
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
import random

try:
    from .base_effect_library import BaseEffectLibrary, ColorSpaceUtils, MaskOperations
except ImportError:
    from base_effect_library import BaseEffectLibrary, ColorSpaceUtils, MaskOperations


class AppearanceEffects:
    """現出様式の3ノード専用エフェクト実装"""
    
    @staticmethod
    def density_effect(image: Image.Image, intensity: float, node_state: float,
                      mask: Optional[np.ndarray] = None) -> Image.Image:
        """
        density（視覚的密度）エフェクト
        
        理論的基盤：フッサールの「充実」（Erfüllung）概念
        現象学的充実の空間的分布を表現し、意識の志向的作用が集中する
        「注意の凝縮点」と「地平的背景」を視覚化
        
        Args:
            image: 入力画像
            intensity: エフェクト強度 (0.0-1.0)
            node_state: ノード状態値 (0.0-1.0)
            mask: 適用マスク
        
        Returns:
            処理された画像
        """
        img_array = np.array(image).astype(np.float32)
        height, width = img_array.shape[:2]
        
        # node_stateに基づく密度分布の計算
        if node_state > 0.5:
            # 高密度状態：クラスタリング効果
            cluster_count = int(3 + (node_state - 0.5) * 10)  # 3-8個のクラスタ
            density_map = AppearanceEffects._create_clustering_density_map(
                img_array, cluster_count, intensity
            )
        else:
            # 低密度状態：散逸効果
            scatter_factor = (0.5 - node_state) * 2.0
            density_map = AppearanceEffects._create_scattering_density_map(
                img_array, scatter_factor, intensity
            )
        
        # 密度マップを画像に適用
        result = AppearanceEffects._apply_density_map(img_array, density_map)
        result = np.clip(result, 0, 255).astype(np.uint8)
        processed = Image.fromarray(result)
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def _create_clustering_density_map(img_array: np.ndarray, cluster_count: int, 
                                     intensity: float) -> np.ndarray:
        """クラスタリング密度マップの生成"""
        height, width = img_array.shape[:2]
        
        # 画像から特徴点を抽出
        gray = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        
        # エッジ検出で特徴点を取得
        edges = cv2.Canny(gray, 50, 150)
        feature_points = np.column_stack(np.where(edges > 0))
        
        if len(feature_points) < cluster_count:
            # 特徴点が少ない場合はランダムポイントを追加
            random_points = np.random.rand(cluster_count - len(feature_points), 2)
            random_points[:, 0] *= height
            random_points[:, 1] *= width
            feature_points = np.vstack([feature_points, random_points])
        
        # K-meansクラスタリング
        if len(feature_points) >= cluster_count:
            kmeans = KMeans(n_clusters=cluster_count, random_state=42, n_init=10)
            labels = kmeans.fit_predict(feature_points)
            centers = kmeans.cluster_centers_
        else:
            centers = feature_points[:cluster_count]
        
        # 密度マップの作成
        y_indices, x_indices = np.mgrid[:height, :width]
        positions = np.stack([y_indices.ravel(), x_indices.ravel()], axis=1)
        
        # 各ピクセルから最近のクラスタ中心への距離を計算
        distances = cdist(positions, centers)
        min_distances = np.min(distances, axis=1).reshape(height, width)
        
        # 距離を密度値に変換（近いほど高密度）
        max_dist = np.max(min_distances)
        density_map = 1.0 - (min_distances / max_dist)
        
        # 強度調整
        density_map = intensity * density_map + (1 - intensity) * 0.5
        
        return density_map
    
    @staticmethod
    def _create_scattering_density_map(img_array: np.ndarray, scatter_factor: float, 
                                     intensity: float) -> np.ndarray:
        """散逸密度マップの生成"""
        height, width = img_array.shape[:2]
        
        # ノイズベースの散逸パターン
        noise = _generate_perlin_noise_2d((height, width), 
                                         frequency=0.1 * (1 + scatter_factor))
        
        # 散逸の強度に応じて密度の変動を調整
        density_variation = scatter_factor * 0.8
        density_map = 0.5 + density_variation * noise
        density_map = np.clip(density_map, 0.1, 0.9)
        
        # 強度調整
        density_map = intensity * density_map + (1 - intensity) * 0.5
        
        return density_map
    
    @staticmethod
    def _apply_density_map(img_array: np.ndarray, density_map: np.ndarray) -> np.ndarray:
        """密度マップを画像に適用"""
        # 密度値に基づいて画素の集約度を調整
        result = img_array.copy()
        
        # 低密度領域では周囲との平均化（散逸効果）
        # 高密度領域では値の増強（集約効果）
        for i in range(3):  # RGB各チャンネル
            channel = img_array[:, :, i]
            
            # ガウシアンフィルタで周囲情報を取得
            blurred = ndimage.gaussian_filter(channel, sigma=2.0)
            
            # 密度に基づく補間
            result[:, :, i] = density_map * channel + (1 - density_map) * blurred
        
        return result
    
    @staticmethod
    def luminosity_effect(image: Image.Image, intensity: float, node_state: float,
                         mask: Optional[np.ndarray] = None) -> Image.Image:
        """
        luminosity（光の強度）エフェクト
        
        理論的基盤：ハイデガーの「明け開け」（Lichtung）概念
        存在論的な「開示性」（Erschlossenheit）の度合いを視覚化し、
        存在者が「明るみの中に立ち現れる」現象を表現
        
        Args:
            image: 入力画像
            intensity: エフェクト強度 (0.0-1.0)
            node_state: ノード状態値 (0.0-1.0)
            mask: 適用マスク
        
        Returns:
            処理された画像
        """
        img_array = np.array(image).astype(np.float32)
        
        # LAB色空間で輝度を精密制御
        lab_array = ColorSpaceUtils.rgb_to_lab_array(img_array.astype(np.uint8))
        lab_float = lab_array.astype(np.float32)
        
        # node_stateに基づく「明け開け」の度合い
        if node_state > 0.5:
            # 高い開示性：存在者が明るみに現れる
            disclosure_factor = 1.0 + (node_state - 0.5) * 2.0 * intensity
            
            # 選択的な輝度増強（重要な領域を優先的に照らす）
            luminance_map = AppearanceEffects._create_disclosure_luminance_map(
                lab_float[:, :, 0], disclosure_factor
            )
        else:
            # 低い開示性：存在の隠れ
            concealment_factor = (0.5 - node_state) * 2.0 * intensity
            
            # 部分的な暗化（存在忘却の表現）
            luminance_map = AppearanceEffects._create_concealment_luminance_map(
                lab_float[:, :, 0], concealment_factor
            )
        
        # 輝度チャンネルを調整
        lab_float[:, :, 0] = luminance_map
        lab_float[:, :, 0] = np.clip(lab_float[:, :, 0], 0, 100)
        
        # RGB色空間に戻す
        lab_result = lab_float.astype(np.uint8)
        result_array = ColorSpaceUtils.lab_to_rgb_array(lab_result)
        processed = Image.fromarray(result_array)
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def _create_disclosure_luminance_map(luminance: np.ndarray, 
                                       disclosure_factor: float) -> np.ndarray:
        """開示的輝度マップの生成"""
        # エッジ検出で「現れ」の境界を特定
        edges = cv2.Canny((luminance * 255 / 100).astype(np.uint8), 30, 100)
        edge_distances = ndimage.distance_transform_edt(edges == 0)
        
        # エッジ近傍ほど強く照らす（存在者の境界の開示）
        max_dist = np.max(edge_distances)
        proximity_factor = 1.0 - (edge_distances / max_dist)
        
        # 既存の輝度値と組み合わせ
        enhancement = 1.0 + disclosure_factor * proximity_factor * 0.3
        result = luminance * enhancement
        
        return result
    
    @staticmethod
    def _create_concealment_luminance_map(luminance: np.ndarray,
                                        concealment_factor: float) -> np.ndarray:
        """隠蔽的輝度マップの生成"""
        # 低輝度領域を優先的に暗化（存在忘却の表現）
        darkness_mask = luminance < np.mean(luminance)
        
        # 暗化の強度を調整
        darkening = 1.0 - concealment_factor * 0.4
        result = luminance * (darkening + 0.6 * darkness_mask * concealment_factor)
        
        return result
    
    @staticmethod
    def chromaticity_effect(image: Image.Image, intensity: float, node_state: float,
                           mask: Optional[np.ndarray] = None) -> Image.Image:
        """
        chromaticity（色彩の質）エフェクト
        
        理論的基盤：メルロ＝ポンティの「肉」（chair）概念
        知覚する身体と世界との「交差配列」（chiasme）における質的差異を表現し、
        知覚的世界の「厚み」を視覚化
        
        Args:
            image: 入力画像
            intensity: エフェクト強度 (0.0-1.0)
            node_state: ノード状態値 (0.0-1.0)
            mask: 適用マスク
        
        Returns:
            処理された画像
        """
        img_array = np.array(image)
        
        # HSV色空間で色彩の質を制御
        hsv_array = ColorSpaceUtils.rgb_to_hsv_array(img_array).astype(np.float32)
        
        # node_stateに基づく「交差配列」の度合い
        if node_state > 0.5:
            # 高い交差配列：色彩の相互浸透
            chiasme_factor = (node_state - 0.5) * 2.0
            result_hsv = AppearanceEffects._create_chiasme_effect(
                hsv_array, chiasme_factor, intensity
            )
        else:
            # 低い交差配列：色彩の分離
            separation_factor = (0.5 - node_state) * 2.0
            result_hsv = AppearanceEffects._create_separation_effect(
                hsv_array, separation_factor, intensity
            )
        
        # RGB色空間に戻す
        result_hsv = np.clip(result_hsv, 0, 255).astype(np.uint8)
        result_array = ColorSpaceUtils.hsv_to_rgb_array(result_hsv)
        processed = Image.fromarray(result_array)
        
        if mask is not None:
            processed = MaskOperations.apply_mask_to_effect(image, processed, mask)
        
        return processed
    
    @staticmethod
    def _create_chiasme_effect(hsv_array: np.ndarray, chiasme_factor: float,
                              intensity: float) -> np.ndarray:
        """交差配列効果の生成"""
        h, w = hsv_array.shape[:2]
        result = hsv_array.copy()
        
        # 色相の相互浸透（近隣色との影響）
        hue_channel = hsv_array[:, :, 0].copy()
        
        # ガウシアンフィルタで色相の拡散効果
        blurred_hue = ndimage.gaussian_filter(hue_channel, 
                                             sigma=2.0 + chiasme_factor * 3.0)
        
        # 元の色相と拡散した色相の混合
        mixing_ratio = intensity * chiasme_factor * 0.4
        result[:, :, 0] = (1 - mixing_ratio) * hue_channel + mixing_ratio * blurred_hue
        
        # 彩度の変調（相互浸透による彩度の豊かさ）
        saturation_enhancement = 1.0 + intensity * chiasme_factor * 0.3
        result[:, :, 1] *= saturation_enhancement
        
        return result
    
    @staticmethod
    def _create_separation_effect(hsv_array: np.ndarray, separation_factor: float,
                                 intensity: float) -> np.ndarray:
        """分離効果の生成"""
        result = hsv_array.copy()
        
        # 色相の鋭利化（境界の明確化）
        hue_channel = hsv_array[:, :, 0]
        
        # エッジ検出による境界強調
        edges = cv2.Canny(hue_channel.astype(np.uint8), 20, 60)
        edge_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpened_hue = cv2.filter2D(hue_channel, -1, edge_kernel)
        
        # 分離度に応じた混合
        sharpening_ratio = intensity * separation_factor * 0.5
        result[:, :, 0] = (1 - sharpening_ratio) * hue_channel + sharpening_ratio * sharpened_hue
        
        # 彩度の純化（分離による色彩の純度向上）
        saturation_purification = 1.0 + intensity * separation_factor * 0.2
        result[:, :, 1] *= saturation_purification
        
        return result


# Perlin noiseの簡易実装（scipyに依存しない）
def _generate_perlin_noise_2d(shape: Tuple[int, int], frequency: float = 0.1) -> np.ndarray:
    """簡易Perlinノイズ生成"""
    h, w = shape
    noise = np.zeros((h, w))
    
    # 複数のオクターブを重ね合わせ
    for octave in range(4):
        freq = frequency * (2 ** octave)
        amp = 1.0 / (2 ** octave)
        
        # グリッドサイズ
        grid_h = int(h * freq) + 1
        grid_w = int(w * freq) + 1
        
        # ランダムグラデーション生成
        gradients = np.random.rand(grid_h, grid_w, 2) * 2 - 1
        
        # 各ピクセルでの補間
        for i in range(h):
            for j in range(w):
                x = j * freq
                y = i * freq
                
                # グリッド座標
                x0, y0 = int(x), int(y)
                x1, y1 = min(x0 + 1, grid_w - 1), min(y0 + 1, grid_h - 1)
                
                # 補間
                sx = x - x0
                sy = y - y0
                
                # 4つの格子点での値を計算
                n00 = np.dot(gradients[y0, x0], [x - x0, y - y0])
                n10 = np.dot(gradients[y0, x1], [x - x1, y - y0])
                n01 = np.dot(gradients[y1, x0], [x - x0, y - y1])
                n11 = np.dot(gradients[y1, x1], [x - x1, y - y1])
                
                # 双線形補間
                nx0 = n00 * (1 - sx) + n10 * sx
                nx1 = n01 * (1 - sx) + n11 * sx
                nxy = nx0 * (1 - sy) + nx1 * sy
                
                noise[i, j] += amp * nxy
    
    return noise

# numpy.random.perlin_noise_2d関数が存在しない場合の代替
if not hasattr(np.random, 'perlin_noise_2d'):
    np.random.perlin_noise_2d = _generate_perlin_noise_2d