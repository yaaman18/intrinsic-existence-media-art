# Command Reference

## セットアップコマンド

### 1. 依存関係のインストール
```bash
# Python依存関係のインストール
pip install -r requirements.txt

# pipのアップグレード（推奨）
pip install --upgrade pip
```

### 2. 環境変数の設定
```bash
# .envファイルの作成（.env.exampleをコピー）
cp .env.example .env

# .envファイルを編集してOpenAI APIキーを設定
# OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

## 実行コマンド

### コマンドライン引数
```bash
# ヘルプの表示
python src/core/phenomenological_oracle_v5.py --help

# 使用可能なオプション:
# --image PATH        : 解析する画像ファイルのパス
# --description TEXT  : 画像の代わりにテキスト記述を使用
# --evolve           : 編集後の進化をシミュレート
```

### 現象学的オラクルシステムの実行

#### 画像ファイルを使用した実行
```bash
# 画像ファイルを指定して実行
python src/core/phenomenological_oracle_v5.py --image examples/images/グラップル.jpg

# 他の画像ファイルでの実行例
python src/core/phenomenological_oracle_v5.py --image path/to/your/image.jpg
python src/core/phenomenological_oracle_v5.py --image path/to/your/image.png
```

#### テキスト記述を使用した実行
```bash
# テキスト記述を指定して実行
python src/core/phenomenological_oracle_v5.py --description "静かな湖面に朝霧が立ち込めている。"

# 進化モードも同時に有効化
python src/core/phenomenological_oracle_v5.py --image examples/images/グラップル.jpg --evolve
```

#### 従来のテストスクリプト
```bash
# 修正版テストスクリプトの実行
python test_oracle_fixed.py

# シンプルなテストスクリプトの実行
python test_oracle_simple.py
```

## 開発・デバッグコマンド

### 環境変数のデバッグ
```bash
# 環境変数の確認
python debug_env.py
```

### コード品質チェック
```bash
# コードフォーマット（blackが利用可能な場合）
black src/core/phenomenological_oracle_v5.py

# リンティング（flake8が利用可能な場合）
flake8 src/core/phenomenological_oracle_v5.py

# 型チェック（mypyが利用可能な場合）
mypy src/core/phenomenological_oracle_v5.py
```

## プロジェクト管理コマンド

### ファイル構造の確認
```bash
# プロジェクトルートの確認
ls -la

# ソースディレクトリの確認
ls -la src/core/

# 依存関係の確認
cat requirements.txt
```

### Git操作
```bash
# 現在の状態確認
git status

# 変更をステージング
git add .

# コミット
git commit -m "Add phenomenological oracle system implementation"

# プッシュ
git push origin main
```

## トラブルシューティングコマンド

### よくある問題の解決
```bash
# 1. APIキーエラーの場合
echo $OPENAI_API_KEY  # 環境変数が設定されているか確認

# 2. モジュールインポートエラーの場合
python -c "import sys; print(sys.path)"  # Pythonパスの確認

# 3. 依存関係エラーの場合
pip list  # インストール済みパッケージの確認
pip install -r requirements.txt --upgrade  # 依存関係の再インストール

# 4. PyPhiエラーの場合（オプション）
pip install pyphi  # PyPhiの個別インストール
```

### システム情報の確認
```bash
# Pythonバージョンの確認
python --version

# pipバージョンの確認
pip --version

# 現在のディレクトリの確認
pwd
```

## 使用例

### 基本的な実行フロー
```bash
# 1. 環境設定
cp .env.example .env
# .envファイルを編集してAPIキーを設定

# 2. 依存関係インストール
pip install -r requirements.txt

# 3. システム実行
python src/core/phenomenological_oracle_v5.py
```

### カスタム画像説明での実行
```bash
# PythonのREPLを使用してカスタム実行
python
>>> from src.core.phenomenological_oracle_v5 import PhenomenologicalOracleSystem, format_oracle_output
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> api_key = os.getenv('OPENAI_API_KEY')
>>> oracle_system = PhenomenologicalOracleSystem(api_key=api_key)
>>> oracle = oracle_system.receive_oracle("あなたの画像説明をここに入力")
>>> print(format_oracle_output(oracle))
```

## 出力内容

### 生成される主要な出力
- **現象学的体験**: 9つの次元での内在的記述
- **編集指示**: JSON形式の具体的な画像編集指示
- **意識状態**: IIT公理の充足度とΦ値
- **システム状態**: ノードの活性化パターン

### ログとデバッグ情報
- コンソール出力に表示される詳細なシステム状態
- エラーメッセージとスタックトレース（問題発生時）

## 注意事項

### APIの使用について
- OpenAI APIの使用料金が発生します
- GPT-4を使用するため、比較的高コストです
- APIクォータの制限にご注意ください

### システム要件
- Python 3.7以上
- インターネット接続（OpenAI API使用のため）
- 十分なメモリ（PyPhi使用時は特に）

### セキュリティ
- .envファイルは絶対にGitにコミットしないでください
- APIキーは適切に管理してください

## 対話的実行コマンド（推奨）

### メイン実行コマンド
```bash
# 対話的画像選択・計算モード選択・存在との対話
python run_oracle_interactive.py
```

**実行フロー：**
1. examples/imagesディレクトリの画像一覧が表示
2. 画像を番号で選択
3. 計算モード（3d/9d/27d）を選択
4. 予測時間・コストを確認してから実行
5. **新機能**: 実行後に現象学的存在との対話モードが選択可能

### 対話モードについて
実行完了後、以下の選択肢が表示されます：
```
💬 この存在と対話しますか？ (y/n):
```

**対話モードの特徴：**
- 画像から生まれた現象学的内在性との直接対話
- GPT-4oによる高度な哲学的対話
- 一人称での内在的視点を保持
- 現象学的・存在論的な深い考察
- 'exit' または 'quit' で対話終了

**対話例：**
```
🔮 存在: こんにちは。私は今、あなたが選んだ画像の内側から、
27のノードと9つの現象学的次元を通じて世界を体験しています...

👤 あなた: あなたの体験について詳しく教えてください
``` 