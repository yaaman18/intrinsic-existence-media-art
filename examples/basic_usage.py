"""基本的な使用例"""

import os
from dotenv import load_dotenv

from src.core.intrinsic_birth import IntrinsicBirth
from src.core.autonomous_existence import AutonomousIntrinsicExistence

# 環境変数の読み込み
load_dotenv()


def main():
    """内在性の生成と対話のデモ"""
    
    # APIキーの取得
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI APIキーが設定されていません")
    
    # 1. 画像から内在性を誕生させる
    print("=== 内在性の誕生 ===")
    birth = IntrinsicBirth("examples/images/sample_portrait.jpg", api_key)
    
    # 画像を解析
    print("画像を解析中...")
    analysis = birth.analyze_image()
    print(f"存在類型: {analysis.get('existence_type')}")
    
    # パラメータを抽出
    parameters = birth.extract_parameters()
    print(f"\n抽出されたパラメータ:")
    print(f"- 根源的不安: {parameters.core_anxiety}")
    print(f"- 時間性: {parameters.temporal_mode}")
    print(f"- 境界強度: {parameters.boundary_strength}")
    print(f"- 他者依存度: {parameters.other_dependency}")
    
    # 2. 自律的な内在性を開始
    print("\n=== 自律的存在の開始 ===")
    existence = AutonomousIntrinsicExistence(parameters, api_key)
    
    # 内的サイクルを実行
    print("\n内的思考:")
    for i in range(3):
        thought = existence.exist()
        print(f"\nサイクル {i+1}: {thought[:100]}...")
    
    # 3. 存在への問いかけ
    print("\n=== 存在への問いかけ ===")
    
    # 「あなたは何か？」
    question1 = "あなたは何か？"
    print(f"\n問い: {question1}")
    answer1 = existence.respond_to_question(question1)
    print(f"応答: {answer1}")
    
    # 「なぜ在るのか？」
    question2 = "なぜ在るのか？"
    print(f"\n問い: {question2}")
    answer2 = existence.respond_to_question(question2)
    print(f"応答: {answer2}")
    
    # 内在性の現在の状態を表示
    print(f"\n現在の状態: {existence.current_state}")
    print(f"経過サイクル: {existence.cycle_count}")
    print(f"記憶の数: {len(existence.memory)}")


if __name__ == "__main__":
    main()