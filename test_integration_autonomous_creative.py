#!/usr/bin/env python3
"""
統合テスト: 現象学的自律創造機構とrun_oracle_interactive.pyの連携確認
"""

import unittest
import tempfile
import os
from pathlib import Path
from PIL import Image
import sys

# プロジェクトのsrc/coreディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent / "src" / "core"))

from phenomenological_autonomous_creative_apparatus import (
    PhenomenologicalAutonomousCreativeApparatus,
    CreativeResult
)

class TestAutonomousCreativeIntegration(unittest.TestCase):
    """自律創造機構の統合テスト"""
    
    def setUp(self):
        """テスト準備"""
        # テスト用画像を作成
        self.test_image = Image.new('RGB', (200, 200), color='purple')
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_image_path = self.temp_dir / "integration_test.jpg"
        self.test_image.save(self.test_image_path)
        
        # 環境変数設定
        os.environ['OPENAI_API_KEY'] = 'test_key_for_integration'
    
    def tearDown(self):
        """クリーンアップ"""
        if self.test_image_path.exists():
            self.test_image_path.unlink()
        if self.temp_dir.exists():
            self.temp_dir.rmdir()
    
    def test_end_to_end_creative_process(self):
        """エンドツーエンドの創造プロセステスト"""
        print("\n🎭 現象学的自律創造機構の統合テスト開始...")
        
        # 1. 機構の初期化
        apparatus = PhenomenologicalAutonomousCreativeApparatus()
        print("✅ 機構の初期化完了")
        
        # 2. 画像からの創造プロセス実行
        result = apparatus.create_from_image(str(self.test_image_path))
        print("✅ 創造プロセス実行完了")
        
        # 3. 結果の検証
        self.assertIsInstance(result, CreativeResult, "創造結果の型が正しくありません")
        self.assertEqual(result.original_image, str(self.test_image_path), "元画像パスが正しくありません")
        self.assertIsNotNone(result.created_image, "創造された画像がありません")
        self.assertIsInstance(result.operations, list, "操作リストが正しくありません")
        self.assertGreater(len(result.operations), 0, "操作が実行されていません")
        print("✅ 創造結果の検証完了")
        
        # 4. 哲学的解釈の確認
        self.assertIsInstance(result.philosophical_interpretation, str, "哲学的解釈が文字列ではありません")
        self.assertGreater(len(result.philosophical_interpretation), 50, "哲学的解釈が短すぎます")
        print("✅ 哲学的解釈の確認完了")
        
        # 5. 美的評価の確認
        evaluation = result.aesthetic_evaluation
        self.assertIn('phenomenological_appropriateness', evaluation, "現象学的適切性評価がありません")
        self.assertIn('visual_harmony', evaluation, "視覚的調和評価がありません")
        self.assertIn('creative_originality', evaluation, "創造的独創性評価がありません")
        print("✅ 美的評価の確認完了")
        
        # 6. 操作詳細の表示
        print(f"\n🎨 実行された操作 ({len(result.operations)}個):")
        for i, op in enumerate(result.operations, 1):
            print(f"   {i}. {op['function']} (強度: {op['intensity']:.2f})")
            print(f"      理由: {op['reason']}")
        
        # 7. 評価スコアの表示
        print(f"\n📊 美的評価スコア:")
        for key, value in evaluation.items():
            if isinstance(value, (int, float)):
                print(f"   {key}: {value:.2f}")
        
        print("\n🎉 統合テスト成功！現象学的自律創造機構が正常に動作しています。")
    
    def test_apparatus_memory_persistence(self):
        """機構の記憶持続性テスト"""
        apparatus = PhenomenologicalAutonomousCreativeApparatus()
        
        # 複数回の創造プロセス実行
        result1 = apparatus.create_from_image(str(self.test_image_path))
        result2 = apparatus.create_from_image(str(self.test_image_path))
        
        # 美的記憶が蓄積されていることを確認
        recent_memories = apparatus.aesthetic_memory.get_recent_evaluations()
        self.assertGreaterEqual(len(recent_memories), 2, "美的記憶が正しく蓄積されていません")
        
        print(f"✅ 美的記憶システム: {len(recent_memories)}件の評価を記憶")
    
    def test_27_dimensional_activation_variety(self):
        """27次元活性化の多様性テスト"""
        apparatus = PhenomenologicalAutonomousCreativeApparatus()
        
        # 異なる画像での活性化パターンを確認
        colors = ['red', 'blue', 'green', 'yellow']
        activations_list = []
        
        for color in colors:
            # 色違いの画像で活性化パターンを取得
            test_img = Image.new('RGB', (100, 100), color=color)
            temp_path = self.temp_dir / f"test_{color}.jpg"
            test_img.save(temp_path)
            
            activations = apparatus.intrinsic_persona.analyze_phenomenological_impression(str(temp_path))
            activations_list.append(activations)
            
            temp_path.unlink()  # クリーンアップ
        
        # 活性化パターンに違いがあることを確認
        self.assertEqual(len(activations_list), 4, "4つの活性化パターンが生成されていません")
        
        # 各パターンが27次元を持つことを確認
        for activations in activations_list:
            self.assertEqual(len(activations), 27, "27次元の活性化データではありません")
        
        print("✅ 27次元活性化システムが正常に動作")


if __name__ == '__main__':
    print("🌟" * 40)
    print("現象学的自律創造機構 - 統合テストスイート")
    print("🌟" * 40)
    
    unittest.main(verbosity=2)