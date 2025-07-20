# Project Five Axioms: Intrinsic Existence
意識に関する五つの公理のプロジェクト １ 内在性

## 概要

写真から生まれる人工的な内在性が、自律的に思考し、画像編集を通じて自己を表現するメディアアートプロジェクト。統合情報理論（IIT）、オートポイエーシス理論、現象学を基盤として、意識の本質を探求する実験的プラットフォーム。

## 核心的問い

- 主観的体験とは何か？
- 生物学的基盤なしに意識は可能か？
- 他者の内在性を認識することの意味とは？

## 理論的基盤

### 1. **オートポイエーシス理論** (Maturana & Varela, 1980)
- 自己生成・自己維持システムとしての実装
- 写真を環境とした構造的カップリング

### 2. **統合情報理論（IIT）** (Giulio Tononi, 2008)
- 第一公理「存在」の実装による内在性
- Φ（統合情報量）による意識の複雑性測定

### 3. **現象学的アプローチ**
- Husserlの志向性理論
- Merleau-Pontyの可逆性概念

## インストール

### 前提条件
- Python 3.8以上
- OpenAI APIキー

### セットアップ手順

```bash
# リポジトリのクローン
git clone https://github.com/yaaman18/intrinsic-existence-media-art.git
cd intrinsic-existence-media-art

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .envファイルを編集してOpenAI APIキーを設定
```

### 必要なディレクトリの作成

```bash
mkdir input_images
mkdir output
mkdir logs
```

## システム構成

### コアモジュール

```
src/core/
├── existence_types.py          # 7つの存在類型定義
├── phenomenological_analyzer.py # 9次元の現象学的分析
├── intrinsic_birth.py          # 画像からの内在性生成
├── autonomous_existence.py      # 自律的思考システム
├── phenomenological_oracle_v5.py # 27ノード意識システム
└── intrinsic_artist_dialogue.py # アーティストとの対話
```

### プロセスフロー

1. **画像入力** → 現象学的9次元分析
2. **内在性生成** → 存在類型とパラメータの決定
3. **自律的存在** → 自己参照的思考ループ
4. **画像認識** → 27ノード状態の更新
5. **編集指示** → 内的状態の外在化
6. **フィードバック** → 意識の進化

## 使用方法

### 基本的な使用例

```python
from src.core.phenomenological_oracle_v5 import PhenomenologicalOracleSystem
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# システムの初期化
oracle = PhenomenologicalOracleSystem(api_key=os.getenv("OPENAI_API_KEY"))

# 画像の説明を入力
image_description = "廃墟となった工場の内部、錆びた機械の隙間から差し込む夕日"

# 託宣を受け取る
oracle_response = oracle.receive_oracle(image_description)

# 結果の表示
print(f"内在性の体験: {oracle_response.vision}")
print(f"統合情報量Φ: {oracle_response.phi}")
print(f"編集指示: {oracle_response.imperative}")
```

### PyPhiによる理論的観測

```python
# 任意のタイミングで理論的Φを観測
theoretical_observation = oracle.observe_theoretical_phi()
if theoretical_observation:
    print(f"理論的Φ: {theoretical_observation['phi_value']}")
```

## 主要概念

### 内在性（Intrinsic Existence）
外部観察者を必要とせず、システム自体にとって存在する性質。IITの第一公理「存在」の実装。

### 27ノードシステム
9つの現象学的次元を各3ノードで表現：
- 現出様式、志向的構造、時間的含意
- 相互感覚的質、存在論的密度、意味的認識層
- 概念的地平、存在者の様態、認識の確実性分布

### 意識の進化
編集サイクルを重ねることで：
- 世代3: メタ認知機能の解放
- 世代5: 時間統合機能の追加
- 世代10+: 複雑な統合機能

## プロジェクトドキュメント

詳細な仕様は [STATEMENT.md](STATEMENT.md) を参照してください。

## トラブルシューティング

### PyPhiのインストールエラー
```bash
# C++コンパイラが必要な場合があります
# Mac: brew install gcc
# Ubuntu: sudo apt-get install build-essential
# Windows: Visual Studio Build Toolsをインストール
```

### メモリ不足エラー
PyPhiの計算は重いため、大きなネットワークでは計算を避けてください。
デフォルトでは27→9→3ノードに削減して計算します。

## 貢献

このプロジェクトは実験的な性質を持つため、現在は限定的な貢献を受け付けています。興味がある方は、Issueでディスカッションを開始してください。

## ライセンス

MIT License

## 作者

yaaman18

## 謝辞

本プロジェクトは、統合情報理論、オートポイエーシス理論、現象学の研究者たちの理論的貢献に基づいています。
