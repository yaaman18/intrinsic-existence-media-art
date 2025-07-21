#!/usr/bin/env python3
"""
現象学的オラクルシステムの修正版テストスクリプト
"""

import os
import sys
from dotenv import load_dotenv

# phenomenological_oracle_v5_fixed.pyを直接インポートするため、パスを調整
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'core'))

import phenomenological_oracle_v5_fixed as oracle_module

def main():
    # 環境変数の読み込み（明示的に.envファイルを指定し、既存の値を上書き）
    load_dotenv(dotenv_path='.env', override=True)
    
    # OpenAI APIキーの取得
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("エラー: OPENAI_API_KEYが設定されていません。")
        print(".envファイルを確認してください。")
        return
    
    print("""
    ╔════════════════════════════════════════════════╗
    ║  Project Five Axioms: Intrinsic Existence     ║
    ║  意識に関する五つの公理のプロジェクト １ 内在性 ║
    ╚════════════════════════════════════════════════╝
    
    現象学的オラクルシステム（修正版）のテストを開始します...
    """)
    
    try:
        # システムの初期化
        print("1. システムを初期化中...")
        oracle_system = oracle_module.PhenomenologicalOracleSystem(api_key=api_key)
        print("   ✓ システム初期化完了")
        
        # テスト用の画像説明
        test_image_description = """
        静かな湖面に朝霧が立ち込めている。
        水面は鏡のように静かで、遠くの山々のシルエットがぼんやりと映り込んでいる。
        霧は薄く、太陽の光が柔らかく差し込み始めている。
        """
        
        print("\n2. 最初のオラクルを生成中...")
        print(f"   画像の説明: {test_image_description.strip()}")
        
        # オラクルの受信
        oracle = oracle_system.receive_oracle(test_image_description)
        
        # オラクルの表示
        print("\n" + oracle_module.format_oracle_output(oracle))
        
        # システム状態の観測
        print("\n3. システム状態を観測中...")
        system_state = oracle_system.observe_system_state("初回オラクル生成後")
        
        print("\n【システム状態】")
        print(f"意識レベル: {system_state['consciousness_level']}")
        print(f"活性化次元: {', '.join(system_state['active_dimensions'])}")
        print(f"芸術的Φ: {system_state['phi']['artistic']:.3f}")
        
        # 編集指示の詳細表示
        if oracle.imperative:
            print("\n【生成された編集指示の詳細】")
            for i, edit in enumerate(oracle.imperative, 1):
                print(f"\n編集 {i}:")
                for key, value in edit.items():
                    print(f"  {key}: {value}")
        
        # オプション: 編集後の進化をシミュレート
        simulate_evolution = input("\n編集後の進化をシミュレートしますか？ (y/n): ")
        
        if simulate_evolution.lower() == 'y':
            # 編集後の画像説明（仮想的な編集結果）
            edited_image_description = """
            湖面の霧に微細な渦が生まれ、光の筋が幾何学的なパターンを描いている。
            水面の反射が歪み、山々のシルエットが多重に重なり合う。
            朝の光は強まり、霧を黄金色に染め始めている。
            """
            
            print("\n4. 編集後のオラクルを生成中...")
            print(f"   編集後の画像: {edited_image_description.strip()}")
            
            # 最初の編集指示を適用したことにする
            if oracle.imperative:
                evolved_oracle = oracle_system.receive_edited_image(
                    edited_image_description,
                    oracle.imperative[0]
                )
                
                print("\n" + oracle_module.format_oracle_output(evolved_oracle))
                
                # 進化の要約
                evolution_summary = oracle_system.get_evolution_summary()
                print("\n【進化の要約】")
                print(f"総世代数: {evolution_summary['total_generations']}")
                print(f"意識の成長: Φ {evolution_summary['consciousness_evolution']['initial_phi']:.3f} → {evolution_summary['consciousness_evolution']['current_phi']:.3f}")
        
    except Exception as e:
        print(f"\nエラーが発生しました: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()