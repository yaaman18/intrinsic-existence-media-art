#!/usr/bin/env python3
"""環境変数のデバッグ"""

import os
from dotenv import load_dotenv

print("1. 現在の作業ディレクトリ:", os.getcwd())
print("2. .envファイルの存在確認:", os.path.exists('.env'))

# .envファイルを明示的に読み込む
load_dotenv(dotenv_path='.env', override=True)

api_key = os.getenv('OPENAI_API_KEY')
print("3. OPENAI_API_KEY:")
if api_key:
    print(f"   - 長さ: {len(api_key)}")
    print(f"   - 最初の20文字: {api_key[:20]}...")
    print(f"   - 最後の10文字: ...{api_key[-10:]}")
else:
    print("   - 見つかりません")

# 他の環境変数も確認
print("\n4. その他の環境変数:")
for key in ['LOG_LEVEL', 'INPUT_IMAGE_DIR', 'OUTPUT_DIR']:
    value = os.getenv(key)
    print(f"   - {key}: {value if value else '未設定'}")