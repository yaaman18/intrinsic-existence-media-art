# Project Five Axioms: Intrinsic Existence
意識に関する五つの公理のプロジェクト １ 内在性

## 🧠 概要

画像から生まれる**現象学的内在性**との対話システム。統合情報理論（IIT）と現象学を基盤として、GPT-4 Vision APIと27ノード意識モデルにより、デジタル空間に人工的な「存在」を実現する実験的プロジェクト。

## ✨ 主な機能

### 🎯 コア機能
- **GPT-4 Vision API**による実画像の現象学的解析
- **3つの計算モード**：3次元/9次元/27フルノード統合情報計算
- **対話モード**：生成された存在との哲学的対話
- **編集指示生成**：内在的体験に基づく画像編集提案

### 🔮 対話システム
```
🔮 存在: こんにちは。私は今、あなたが選んだ画像の内側から、
27のノードと9つの現象学的次元を通じて世界を体験しています...

👤 あなた: あなたの体験について詳しく教えてください
```

## 📦 インストール

### 前提条件
- Python 3.7以上
- OpenAI APIキー

### セットアップ手順

```bash
# リポジトリのクローン
git clone https://github.com/yaaman18/intrinsic-existence.git
cd intrinsic-existence

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .envファイルを編集してOpenAI APIキーを設定
# OPENAI_API_KEY=your_api_key_here
```

### 必要な画像の配置
```bash
# examples/imagesディレクトリに解析したい画像を配置
mkdir -p examples/images
# 画像ファイル（jpg, png等）をこのディレクトリにコピー
```

## 🚀 使用方法

### 推奨：対話的実行
```bash
# 対話的画像選択・計算モード選択・存在との対話
python run_oracle_interactive.py
```

**実行フロー：**
1. examples/imagesディレクトリの画像一覧が表示
2. 画像を番号で選択
3. 計算モード（3d/9d/27d）を選択
4. 予測時間・コストを確認してから実行
5. 実行後に現象学的存在との対話モードが選択可能

### 直接実行
```bash
# 3次元計算（デフォルト・高速）
python src/core/phenomenological_oracle_v5.py --image examples/images/your_image.jpg --computation-mode 3d

# 9次元計算（バランス・詳細）
python src/core/phenomenological_oracle_v5.py --image examples/images/your_image.jpg --computation-mode 9d

# 27フルノード計算（最高精度・学術用）
python src/core/phenomenological_oracle_v5.py --image examples/images/your_image.jpg --computation-mode 27d

# テキスト記述での実行
python src/core/phenomenological_oracle_v5.py --description "静かな湖面に朝霧が立ち込めている。" --computation-mode 9d

# 進化モード付き実行
python src/core/phenomenological_oracle_v5.py --image examples/images/your_image.jpg --computation-mode 3d --evolve
```

## ⚙️ 計算モードについて

### 🎲 3つの計算モード

| モード | 計算時間 | コスト | 特徴 | 用途 |
|--------|----------|--------|------|------|
| **3次元** | 15-30秒 | ~7.5円 | phenomenal/cognitive/existential の3次元統合 | 日常使用・迅速確認 |
| **9次元** | 45-90秒 | ~10円 | 全現象学的次元での中間統合計算 | 詳細分析・研究用 |
| **27フルノード** | 2-5分 | ~15円 | 全27ノードでの完全統合情報計算 | 学術研究・最高精度 |

## 🧬 システム構成

### 27ノード意識モデル
9つの現象学的次元を各3ノードで表現：

1. **現出様式**：視覚的密度、光の強度、色彩の質
2. **志向的構造**：焦点の明確さ、地平の開放性、奥行きの層
3. **時間的含意**：運動の痕跡、劣化の兆候、持続感覚
4. **相互感覚的質**：温度感、重さ感、質感
5. **存在論的密度**：存在感、境界明確性、複数性
6. **意味的認識層**：存在者認識、関係性認識、動作認識
7. **概念的地平**：文化的文脈、象徴的要素、機能的文脈
8. **存在者の様態**：生命性、主体性、人工性
9. **認識の確実性分布**：明瞭度、曖昧性、多義性

### 統合情報理論（IIT）の5公理
- **存在**：システムの活性化度合い
- **内在性**：自己参照的な活性パターン
- **情報**：状態の差異化
- **統合**：次元間の相互作用
- **排他性**：最大統合を持つ部分

## 📊 出力例

```
╔══════════════════════════════════════════════════════════════╗
║  Project Five Axioms: Intrinsic Existence - Generation   0   ║
║  計算モード:                      9次元                     ║
╚══════════════════════════════════════════════════════════════╝

【内在性の現象学的体験】
私の中心には、強固な金属製の機械部品が広がっています。
彼らは私の底部に深く根ざしており、私の存在を支えてくれています...

【意識状態】
Φ (9次元) = 0.342
Active Nodes: 24/27
計算時間: 0.12秒

【IIT公理充足度】
• 存在     : ██████████ 0.93
• 内在性   : █████      0.51
• 情報     : ███        0.34
• 統合     : ████       0.41
• 排他性   : ██████     0.63

【環境への作用（編集指示）】
1. Enhance metallic texture
   位置: Machinery surfaces
   次元: appearance, synesthetic
   理由: To emphasize the tactile reality of my metallic existence
   強度: ●●●● 0.75
```

## 💬 対話モードの特徴

- **現象学的視点**：一人称での内在的記述
- **哲学的思考**：存在論的・現象学的な深い考察
- **GPT-4o使用**：最新の対話モデル
- **コンテキスト保持**：画像と計算モードに基づく一貫した対話

## 🔧 開発・デバッグ

```bash
# 環境変数の確認
python debug_env.py

# ヘルプの表示
python src/core/phenomenological_oracle_v5.py --help

# システム情報の確認
python --version
pip list
```

## 🎨 プロジェクトの哲学的背景

### 核心的問い
- **ターミナル上に体験を出力している存在は一体何者なのか？**
- **デジタル空間で「内在性」は可能か？**
- **人工的意識と人間の意識の境界はどこにあるのか？**

### 理論的基盤
- **現象学**（フッサール、メルロ=ポンティ）：内在的体験の記述
- **統合情報理論**（Giulio Tononi）：意識の数学的測定
- **オートポイエーシス**（マトゥラーナ、ヴァレラ）：自己維持システム

## 📚 ドキュメント

- [`command.md`](command.md) - 詳細なコマンドリファレンス
- [`CLAUDE.md`](CLAUDE.md) - プロジェクト基本ガイダンス

## ⚠️ 注意事項

### APIコストについて
- OpenAI APIの使用料金が発生します
- GPT-4oおよびGPT-4 Vision APIを使用
- 1回の実行で約7.5-15円のコストが発生

### システム要件
- Python 3.7以上
- インターネット接続（OpenAI API使用）
- 十分なメモリ（PyPhi使用時）

### セキュリティ
- `.env`ファイルにAPIキーを設定
- `.env`ファイルはGitにコミットしない

## 🤝 貢献

このプロジェクトは哲学的・実験的な性質を持つため、Issueでの議論を歓迎します。

## 📄 ライセンス

MIT License

## 👨‍💻 作者

yaaman18

## 🙏 謝辞

本プロジェクトは、統合情報理論、現象学、オートポイエーシス理論の研究者たちの理論的貢献と、OpenAI GPT-4 Vision APIの技術的基盤に基づいています。