#!/usr/bin/env python3
"""
Base Effect Library Unit Tests
基盤エフェクトライブラリの全関数単体テスト
数学的精度・エラーハンドリング・パフォーマンスを包括的に検証
"""

import unittest
import numpy as np
from PIL import Image
import cv2
import sys
from pathlib import Path
import time

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent.parent / "src" / "core"))

from base_effect_library import (
    BaseEffectLibrary, ColorSpaceUtils, MaskOperations, BlendModes
)


class TestColorSpaceUtils(unittest.TestCase):
    """色空間変換ユーティリティのテスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        # テスト用のRGB画像配列を作成
        self.rgb_test = np.array([
            [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
            [[128, 128, 128], [255, 255, 255], [0, 0, 0]],
            [[255, 128, 64], [64, 255, 128], [128, 64, 255]]
        ], dtype=np.uint8)
        
    def test_rgb_to_hsv_conversion(self):
        """RGB→HSV変換の正確性テスト"""
        hsv_result = ColorSpaceUtils.rgb_to_hsv_array(self.rgb_test)
        
        # 形状の検証
        self.assertEqual(hsv_result.shape, self.rgb_test.shape)
        
        # データ型の検証
        self.assertEqual(hsv_result.dtype, np.uint8)
        
        # 値範囲の検証（OpenCV HSV: H=0-179, S=0-255, V=0-255）
        self.assertTrue(np.all(hsv_result[:, :, 0] <= 179))  # Hue
        self.assertTrue(np.all(hsv_result[:, :, 1] <= 255))  # Saturation
        self.assertTrue(np.all(hsv_result[:, :, 2] <= 255))  # Value
        
    def test_hsv_to_rgb_conversion(self):
        """HSV→RGB変換の正確性テスト"""
        # RGB → HSV → RGB の可逆性テスト
        hsv_intermediate = ColorSpaceUtils.rgb_to_hsv_array(self.rgb_test)
        rgb_result = ColorSpaceUtils.hsv_to_rgb_array(hsv_intermediate)
        
        # 形状とデータ型の検証
        self.assertEqual(rgb_result.shape, self.rgb_test.shape)
        self.assertEqual(rgb_result.dtype, np.uint8)
        
        # 可逆性の検証（±2の誤差許容）
        diff = np.abs(rgb_result.astype(int) - self.rgb_test.astype(int))
        self.assertTrue(np.all(diff <= 2), f"Max difference: {np.max(diff)}")
        
    def test_rgb_to_lab_conversion(self):
        """RGB→LAB変換の正確性テスト"""
        lab_result = ColorSpaceUtils.rgb_to_lab_array(self.rgb_test)
        
        # 形状の検証
        self.assertEqual(lab_result.shape, self.rgb_test.shape)
        
        # LAB値範囲の検証（OpenCV LAB: L=0-100, A=0-255, B=0-255の変換後）
        self.assertTrue(np.all(lab_result[:, :, 0] <= 255))  # L channel
        self.assertTrue(np.all(lab_result[:, :, 1] <= 255))  # A channel
        self.assertTrue(np.all(lab_result[:, :, 2] <= 255))  # B channel
        
    def test_lab_to_rgb_conversion(self):
        """LAB→RGB変換の正確性テスト"""
        # RGB → LAB → RGB の可逆性テスト
        lab_intermediate = ColorSpaceUtils.rgb_to_lab_array(self.rgb_test)
        rgb_result = ColorSpaceUtils.lab_to_rgb_array(lab_intermediate)
        
        # 形状とデータ型の検証
        self.assertEqual(rgb_result.shape, self.rgb_test.shape)
        self.assertEqual(rgb_result.dtype, np.uint8)
        
        # 可逆性の検証（LABは非線形なので±10の誤差許容）
        diff = np.abs(rgb_result.astype(int) - self.rgb_test.astype(int))
        self.assertTrue(np.all(diff <= 10), f"Max difference: {np.max(diff)}")


class TestMaskOperations(unittest.TestCase):
    """マスク操作のテスト"""
    
    def test_create_circular_mask(self):
        """円形マスク生成のテスト"""
        size = (100, 100)
        center = (0.5, 0.5)
        radius = 0.3
        feather = 0.1
        
        mask = MaskOperations.create_circular_mask(size, center, radius, feather)
        
        # 形状の検証
        self.assertEqual(mask.shape, size)
        
        # データ型の検証
        self.assertEqual(mask.dtype, np.float32)
        
        # 値範囲の検証（0.0-1.0）
        self.assertTrue(np.all(mask >= 0.0))
        self.assertTrue(np.all(mask <= 1.0))
        
        # 中心部は1.0に近い値
        center_y, center_x = int(size[0] * center[0]), int(size[1] * center[1])
        self.assertGreater(mask[center_y, center_x], 0.8)
        
        # エッジ部は0.0に近い値
        edge_value = mask[0, 0]
        self.assertLess(edge_value, 0.2)
        
    def test_create_gradient_mask_vertical(self):
        """垂直グラデーションマスク生成のテスト"""
        size = (100, 80)
        mask = MaskOperations.create_gradient_mask(size, "vertical")
        
        # 形状の検証
        self.assertEqual(mask.shape, size)
        
        # グラデーションの検証（上から下へ0→1）
        self.assertAlmostEqual(mask[0, 40], 0.0, places=2)
        self.assertAlmostEqual(mask[99, 40], 1.0, places=2)
        self.assertAlmostEqual(mask[50, 40], 0.5, places=1)
        
    def test_create_gradient_mask_horizontal(self):
        """水平グラデーションマスク生成のテスト"""
        size = (80, 100)
        mask = MaskOperations.create_gradient_mask(size, "horizontal")
        
        # グラデーションの検証（左から右へ0→1）
        self.assertAlmostEqual(mask[40, 0], 0.0, places=2)
        self.assertAlmostEqual(mask[40, 99], 1.0, places=2)
        self.assertAlmostEqual(mask[40, 50], 0.5, places=1)
        
    def test_create_gradient_mask_radial(self):
        """放射グラデーションマスク生成のテスト"""
        size = (100, 100)
        mask = MaskOperations.create_gradient_mask(size, "radial")
        
        # 中心は0.0、端は1.0に近い値
        center = mask[50, 50]
        corner = mask[0, 0]
        self.assertLess(center, 0.1)
        self.assertGreater(corner, 0.9)
        
    def test_apply_mask_to_effect(self):
        """マスク適用のテスト"""
        # テスト画像作成
        original = Image.new('RGB', (100, 100), (255, 0, 0))  # 赤
        processed = Image.new('RGB', (100, 100), (0, 255, 0))  # 緑
        
        # 50%のマスク
        mask = np.full((100, 100), 0.5, dtype=np.float32)
        
        result = MaskOperations.apply_mask_to_effect(original, processed, mask)
        
        # 結果の検証
        result_array = np.array(result)
        
        # 50%ブレンドなので中間色になる
        expected_red = 255 * 0.5  # 元の赤の50%
        expected_green = 255 * 0.5  # 処理済みの緑の50%
        
        self.assertAlmostEqual(result_array[50, 50, 0], expected_red, delta=2)
        self.assertAlmostEqual(result_array[50, 50, 1], expected_green, delta=2)
        self.assertAlmostEqual(result_array[50, 50, 2], 0, delta=2)


class TestBaseEffectLibrary(unittest.TestCase):
    """基盤エフェクトライブラリのテスト"""
    
    def setUp(self):
        """テスト用画像の準備"""
        self.test_image = Image.new('RGB', (200, 200), (128, 128, 128))
        
        # カラーテスト用画像
        self.color_image = Image.new('RGB', (100, 100), (200, 100, 50))
        
    def test_adjust_rgb_channels(self):
        """RGBチャンネル調整のテスト"""
        r_factor, g_factor, b_factor = 1.5, 0.8, 1.2
        
        result = BaseEffectLibrary.adjust_rgb_channels(
            self.color_image, r_factor, g_factor, b_factor
        )
        
        result_array = np.array(result)
        
        # チャンネル調整の検証
        expected_r = min(255, int(200 * r_factor))
        expected_g = min(255, int(100 * g_factor))  
        expected_b = min(255, int(50 * b_factor))
        
        self.assertEqual(result_array[50, 50, 0], expected_r)
        self.assertEqual(result_array[50, 50, 1], expected_g)
        self.assertEqual(result_array[50, 50, 2], expected_b)
        
    def test_hue_shift(self):
        """色相シフトのテスト"""
        shift_degrees = 60
        
        result = BaseEffectLibrary.hue_shift(self.color_image, shift_degrees)
        
        # 画像サイズの保持
        self.assertEqual(result.size, self.color_image.size)
        
        # 色相が変化していることの確認（元画像と異なる）
        orig_array = np.array(self.color_image)
        result_array = np.array(result)
        
        # 完全に同一ではないことを確認
        self.assertFalse(np.array_equal(orig_array, result_array))
        
    def test_saturation_adjust(self):
        """彩度調整のテスト"""
        # 彩度を2倍に
        factor = 2.0
        result = BaseEffectLibrary.saturation_adjust(self.color_image, factor)
        
        # 画像サイズの保持
        self.assertEqual(result.size, self.color_image.size)
        
        # 彩度が変化していることの確認
        orig_array = np.array(self.color_image)
        result_array = np.array(result)
        self.assertFalse(np.array_equal(orig_array, result_array))
        
        # 彩度0での無彩色化テスト
        grayscale_result = BaseEffectLibrary.saturation_adjust(self.color_image, 0.0)
        grayscale_array = np.array(grayscale_result)
        
        # グレースケールでは各チャンネルが近似値になる
        r, g, b = grayscale_array[50, 50]
        self.assertLess(abs(r - g), 5)
        self.assertLess(abs(g - b), 5)
        
    def test_luminosity_adjust(self):
        """輝度調整のテスト"""
        factor = 1.5
        result = BaseEffectLibrary.luminosity_adjust(self.color_image, factor)
        
        # 画像サイズの保持
        self.assertEqual(result.size, self.color_image.size)
        
        # 輝度調整で全体的に明るくなることの確認
        orig_array = np.array(self.color_image)
        result_array = np.array(result)
        
        # 平均輝度の増加
        orig_brightness = np.mean(orig_array)
        result_brightness = np.mean(result_array)
        self.assertGreater(result_brightness, orig_brightness)
        
    def test_gaussian_blur(self):
        """ガウシアンブラーのテスト"""
        radius = 5.0
        result = BaseEffectLibrary.gaussian_blur(self.test_image, radius)
        
        # 画像サイズの保持
        self.assertEqual(result.size, self.test_image.size)
        
        # ブラー効果の確認（エッジの検証）
        # 単色画像なので大きな変化はないが、処理が正常実行されることを確認
        self.assertIsInstance(result, Image.Image)
        
    def test_unsharp_mask(self):
        """アンシャープマスクのテスト"""
        result = BaseEffectLibrary.unsharp_mask(self.test_image)
        
        # 画像サイズの保持
        self.assertEqual(result.size, self.test_image.size)
        self.assertIsInstance(result, Image.Image)
        
    def test_motion_blur(self):
        """モーションブラーのテスト"""
        angle = 45
        distance = 10
        
        result = BaseEffectLibrary.motion_blur(self.test_image, angle, distance)
        
        # 画像サイズの保持
        self.assertEqual(result.size, self.test_image.size)
        self.assertIsInstance(result, Image.Image)
        
    def test_add_noise_gaussian(self):
        """ガウシアンノイズ追加のテスト"""
        amount = 0.1
        result = BaseEffectLibrary.add_noise(self.test_image, "gaussian", amount)
        
        # 画像サイズの保持
        self.assertEqual(result.size, self.test_image.size)
        
        # ノイズが追加されていることの確認
        orig_array = np.array(self.test_image)
        result_array = np.array(result)
        
        # 完全に同一ではないことを確認
        self.assertFalse(np.array_equal(orig_array, result_array))
        
    def test_add_noise_uniform(self):
        """一様ノイズ追加のテスト"""
        result = BaseEffectLibrary.add_noise(self.test_image, "uniform", 0.1)
        self.assertEqual(result.size, self.test_image.size)
        
    def test_add_noise_salt_pepper(self):
        """塩胡椒ノイズ追加のテスト"""
        result = BaseEffectLibrary.add_noise(self.test_image, "salt_pepper", 0.05)
        self.assertEqual(result.size, self.test_image.size)
        
    def test_edge_enhance(self):
        """エッジ強調のテスト"""
        factor = 1.0
        result = BaseEffectLibrary.edge_enhance(self.test_image, factor)
        
        # 画像サイズの保持
        self.assertEqual(result.size, self.test_image.size)
        self.assertIsInstance(result, Image.Image)
        
    def test_create_vignette(self):
        """ビネット効果のテスト"""
        intensity = 0.5
        radius = 0.8
        
        result = BaseEffectLibrary.create_vignette(self.test_image, intensity, radius)
        
        # 画像サイズの保持
        self.assertEqual(result.size, self.test_image.size)
        
        # ビネット効果の確認（中央は明るく、端は暗く）
        result_array = np.array(result)
        
        center_brightness = np.mean(result_array[100, 100])  # 中央
        corner_brightness = np.mean(result_array[10, 10])    # 角
        
        self.assertGreaterEqual(center_brightness, corner_brightness)


class TestBlendModes(unittest.TestCase):
    """ブレンドモードのテスト"""
    
    def setUp(self):
        """テスト用配列の準備"""
        self.base = np.array([128, 64, 192], dtype=np.float32)
        self.overlay = np.array([255, 128, 64], dtype=np.float32)
        
    def test_normal_blend(self):
        """通常ブレンドのテスト"""
        opacity = 0.5
        result = BlendModes.normal_blend(self.base, self.overlay, opacity)
        
        # 50%ブレンドの計算検証
        expected = self.base * 0.5 + self.overlay * 0.5
        np.testing.assert_array_almost_equal(result, expected)
        
    def test_multiply_blend(self):
        """乗算ブレンドのテスト"""
        opacity = 1.0
        result = BlendModes.multiply_blend(self.base, self.overlay, opacity)
        
        # 乗算ブレンドの計算検証
        expected_multiply = (self.base * self.overlay) / 255.0
        np.testing.assert_array_almost_equal(result, expected_multiply, decimal=1)
        
    def test_screen_blend(self):
        """スクリーンブレンドのテスト"""
        opacity = 1.0
        result = BlendModes.screen_blend(self.base, self.overlay, opacity)
        
        # スクリーンブレンドは通常より明るくなる
        self.assertTrue(np.all(result >= self.base))
        
    def test_overlay_blend(self):
        """オーバーレイブレンドのテスト"""
        opacity = 1.0
        result = BlendModes.overlay_blend(self.base, self.overlay, opacity)
        
        # 結果の値範囲チェック
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result <= 255))


class TestErrorHandling(unittest.TestCase):
    """エラーハンドリングのテスト"""
    
    def test_invalid_noise_type(self):
        """不正なノイズタイプのテスト"""
        image = Image.new('RGB', (100, 100), (128, 128, 128))
        
        with self.assertRaises(ValueError):
            BaseEffectLibrary.add_noise(image, "invalid_noise_type", 0.1)
            
    def test_invalid_gradient_direction(self):
        """不正なグラデーション方向のテスト"""
        with self.assertRaises(ValueError):
            MaskOperations.create_gradient_mask((100, 100), "invalid_direction")


class TestPerformance(unittest.TestCase):
    """パフォーマンステスト"""
    
    def test_large_image_processing(self):
        """大画像での処理時間テスト"""
        # 2K画像でのテスト
        large_image = Image.new('RGB', (2048, 1536), (128, 128, 128))
        
        # ガウシアンブラーの処理時間測定
        start_time = time.time()
        result = BaseEffectLibrary.gaussian_blur(large_image, 3.0)
        processing_time = time.time() - start_time
        
        # 10秒以内で完了することを確認
        self.assertLess(processing_time, 10.0)
        self.assertEqual(result.size, large_image.size)
        
    def test_color_space_conversion_performance(self):
        """色空間変換のパフォーマンステスト"""
        # 大きな配列でのテスト
        large_array = np.random.randint(0, 256, (1024, 1024, 3), dtype=np.uint8)
        
        # RGB→HSV変換時間測定
        start_time = time.time()
        hsv_result = ColorSpaceUtils.rgb_to_hsv_array(large_array)
        conversion_time = time.time() - start_time
        
        # 1秒以内で完了することを確認
        self.assertLess(conversion_time, 1.0)
        self.assertEqual(hsv_result.shape, large_array.shape)


def run_all_tests():
    """全テストの実行"""
    # テストスイートの作成
    test_suite = unittest.TestSuite()
    
    # 各テストクラスを追加
    test_classes = [
        TestColorSpaceUtils,
        TestMaskOperations,
        TestBaseEffectLibrary,
        TestBlendModes,
        TestErrorHandling,
        TestPerformance
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # テストの実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 結果の表示
    print(f"\n{'='*60}")
    print("🧪 Base Effect Library Unit Tests Results")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors))/result.testsRun*100:.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print(f"\n⚠️  Errors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    if not result.failures and not result.errors:
        print(f"\n🎉 All tests passed successfully!")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()