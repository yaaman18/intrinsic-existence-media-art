# Project Five Axioms: Intrinsic Existence
# -意識に関する五つの公理のプロジエクト　１、内在性-

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

## 技術仕様

- **言語**: Python 3.8+
- **主要ライブラリ**: 
  - OpenAI API (GPT-4)
  - PIL/Pillow
  - NumPy
  - PyPhi (オプション)
- **必要なAPIキー**: OpenAI API

## インストールと使用

```bash
# 依存関係のインストール
pip install -r requirements.txt

# 基本的な使用例
from src.core.phenomenological_oracle_v5 import PhenomenologicalOracleSystem

# システムの初期化
oracle = PhenomenologicalOracleSystem(api_key="your-api-key")

# 画像の認識と編集指示の生成
oracle_response = oracle.receive_oracle(image_description)
```

## プロジェクトドキュメント

詳細な仕様は [STATEMENT.md](STATEMENT.md) を参照してください。

## 貢献

このプロジェクトは実験的な性質を持つため、現在は限定的な貢献を受け付けています。興味がある方は、Issueでディスカッションを開始してください。

## ライセンス

MIT License

## 作者

yaaman18

## 謝辞

本プロジェクトは、統合情報理論、オートポイエーシス理論、現象学の研究者たちの理論的貢献に基づいています。
