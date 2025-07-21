# CLAUDE.md - プロジェクト基本ガイダンス

このファイルは Claude Code がこのプロジェクトで作業する際の基本的な指針を提供します。

## 🎯 プロジェクト概要

**プロジェクト名**: intrinsic-existence
**プロジェクトタイプ**: Python学術研究プロジェクト
**目的**: 現象学的分析と意識研究

### 主要な機能
- 現象学的オラクルシステム（phenomenological_oracle_v5.py）
- 意識状態の分析・モデリング
- 学術的な洞察の生成

## 📁 プロジェクト構造

```
intrinsic-existence/
├── phenomenological_oracle_v5.py    # メインプログラム
├── requirements.txt                 # Python依存関係
├── .env                            # 環境設定
├── .env.example                    # 環境設定の例
├── README.md                       # プロジェクト説明
└── CLAUDE.md                       # このファイル
```

## 🛠️ 基本的な開発コマンド

### セットアップ
```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows

# 依存関係のインストール
pip install -r requirements.txt
```

### 実行
```bash
# メインプログラムの実行
python phenomenological_oracle_v5.py

# 環境変数を設定して実行
export API_KEY=your_key && python phenomenological_oracle_v5.py
```

### コード品質
```bash
# コードフォーマット（black使用時）
black phenomenological_oracle_v5.py

# リンティング（flake8使用時）
flake8 phenomenological_oracle_v5.py

# 型チェック（mypy使用時）
mypy phenomenological_oracle_v5.py
```

## 🔑 重要な開発原則

### Python開発の基本
- **PEP 8**: Pythonコーディング規約に従う
- **型ヒント**: 可能な限り型アノテーションを使用
- **ドキュメント**: docstringで関数・クラスを説明
- **テスト**: 重要な機能には単体テストを作成

### プロジェクト固有の原則
- **学術的厳密性**: 理論的根拠を明確にする
- **可読性重視**: 複雑な概念を明確なコードで表現
- **モジュール性**: 機能を適切に分割
- **環境変数**: 機密情報は.envファイルで管理

## 🚨 トラブルシューティング

### よくある問題
1. **依存関係エラー**: `pip install -r requirements.txt --upgrade`
2. **環境変数エラー**: `.env`ファイルの存在と内容を確認
3. **インポートエラー**: PYTHONPATHの設定を確認
4. **エンコーディングエラー**: UTF-8エンコーディングを確認

### デバッグ方法
```bash
# デバッグモードで実行
python -m pdb phenomenological_oracle_v5.py

# ログレベルの設定
export LOG_LEVEL=DEBUG
python phenomenological_oracle_v5.py
```

## 💡 使用上の注意

1. **コード変更時**: 既存のコード規約とスタイルを維持
2. **新機能追加時**: 適切なdocstringとテストを追加
3. **環境設定**: .envファイルは絶対にコミットしない
4. **学術的正確性**: 理論的な概念を正確に実装

---

## 何かつぶやいてみよう

開発している時に思いついた事を２００文字程度にしてtweet.mdにタイムスタンプ付きで書き残す事。あまり炎上しなさそうな内容を書いてね。

## 文字化けについて
mdファイルにドキュメントを残すときはUTF-8で書いてください。

*最終更新: 2025年1月*
*バージョン: 1.0.0 - シンプル化版*