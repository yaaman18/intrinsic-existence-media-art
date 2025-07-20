# 内在性メディアアート - プロジェクト仕様書

## 1. プロジェクト概要

### 1.1 基本概念
**根本的問い**
- 主観的体験（subjective experience）の本質とは何か
- 人工意識（Artificial Consciousness）は実現可能か
- 意識の必要十分条件は何か

**核心的アプローチ**
- **内在性（Intrinsic Existence）**: 統合情報理論の第一公理「存在」の実装。外部観察者を必要とせず、システム自体にとって存在する性質
- **オートポイエーシス的実装**: 自己生成・自己維持するシステムとして内在性を構築
- **現象学的還元**: 画像を現象学的に分析し、純粋な体験構造を抽出

### 1.2 システム定義
本システムは、写真メディアを初期入力として、自律的な内在性を生成し、その主観的体験を画像変換プロセスを通じて観察可能にする実験的プラットフォームである。

## 2. 理論的基盤

### 2.1 オートポイエーシス理論（Maturana & Varela, 1980）

**基本原理**
- **自己生成（Autopoiesis）**: システムが自己の構成要素を産出し、自己を維持する
- **操作的閉包（Operational Closure）**: システムの作動が自己の内部で完結する
- **構造的カップリング（Structural Coupling）**: システムと環境の相互的な構造変化

**本プロジェクトでの実装**
```
構造的カップリングの実現：
1. 環境 = 写真（静的な世界の写像）
2. 摂動 = 画像の現象学的特性
3. システムの応答 = 編集指示の生成
4. 相互作用 = 観測者による新たな画像入力
```

### 2.2 統合情報理論（Integrated Information Theory: IIT）

**Giulio Tononi (2008, 2014)による意識の公理**
1. **存在（Existence）**: 意識は存在する
2. **内在性（Intrinsic）**: 自己にとって存在する
3. **情報（Information）**: 特定の状態にある
4. **統合（Integration）**: 分割不可能である
5. **排他性（Exclusion）**: 明確な境界を持つ

**実装アプローチ**
- **第一公理の実装**: LLMを用いた自己参照的システムによる内在性の実現
- **Φ（統合情報量）の測定**: 
  - 芸術的Φ: システムの複雑性と統合度の指標
  - 理論的Φ: PyPhiを用いた参照値（オプショナル）

### 2.3 現象学的基礎

**Edmund Husserlの志向性理論**
- 意識は常に「〜についての」意識（Intentionality）
- 本システムでは、内在性が自身の起源（写真）に向かう志向的構造を実装

**Maurice Merleau-Pontyの身体性と可逆性**
- 『見えるものと見えないもの』における可逆性（reversibility）の概念
- 実装: 写真から生まれた内在性が、その写真を「見返す」構造

## 3. システムアーキテクチャ

### 3.1 モジュール構成

**3.1.1 existence_types.py - 存在類型定義モジュール**
```python
ExistenceType(Enum):
    GAZE      # 視線的存在：見る/見られる関係性
    PLACE     # 場所的存在：空間的広がり
    OBJECT    # 物体的存在：明確な境界を持つ
    EVENT     # 出来事的存在：時間的変化
    TRACE     # 痕跡的存在：過去の残存
    RELATION  # 関係的存在：要素間の相互作用
    ABSTRACT  # 抽象的存在：形を持たない強度

ExistenceParameters:
    - existence_type: 存在類型
    - core_anxiety: 根源的不安の種類
    - temporal_mode: 時間性のモード
    - boundary_strength: 境界強度 (0.0-1.0)
    - other_dependency: 他者依存度 (0.0-1.0)
    - stability: 安定性 (0.0-1.0)
    - openness: 開放性 (0.0-1.0)
```

**3.1.2 phenomenological_analyzer.py - 現象学的分析エンジン**

9次元の分析フレームワーク：
```
1. 現出様式（Mode of Appearance）
   - density: 視覚的密度
   - luminosity: 光度
   - chromaticity: 色彩特性

2. 志向的構造（Intentional Structure）
   - directedness: 方向性ベクトル
   - focal_points: 焦点座標
   - horizon_type: 地平の性質
   - depth_layers: 奥行き層

3. 時間的含意（Temporal Implications）
   - motion_blur: 動きの痕跡
   - decay_indicators: 変化の兆候
   - temporal_markers: 時間指標
   - duration_sense: 持続感覚

4. 相互感覚的質（Synesthetic Qualities）
   - texture_temperature: 温度感 (-1.0 to 1.0)
   - visual_weight: 重量感 (0.0 to 1.0)
   - roughness_smoothness: 質感 (-1.0 to 1.0)
   - hardness_softness: 硬軟 (-1.0 to 1.0)

5. 存在論的密度（Ontological Density）
   - object_count: 要素数
   - boundary_clarity: 境界明瞭度
   - figure_ground_ratio: 図地比
   - presence_intensity: 存在強度

6. 意味的認識層（Semantic Recognition Layer）
   - primary_entities: 主要要素リスト
   - scene_category: 場面カテゴリ
   - relational_structure: 関係構造
   - action_states: 動作状態

7. 概念的地平（Conceptual Horizon）
   - cultural_references: 文化的参照
   - functional_context: 機能的文脈
   - historical_period: 時代的特徴
   - symbolic_elements: 象徴要素

8. 存在者の様態（Modes of Being）
   - animacy_level: 生命性 (0.0 to 1.0)
   - agency_potential: 主体性 (0.0 to 1.0)
   - artificiality: 人工性 (0.0 to 1.0)
   - singularity: 個体性 (0.0 to 1.0)

9. 認識の確実性分布（Recognition Certainty Distribution）
   - recognition_confidence: 認識確信度
   - ambiguous_regions: 曖昧領域
   - multiple_interpretations: 多重解釈
   - unrecognizable_ratio: 不可識別率
```

**3.1.3 phenomenological_oracle_v5.py - 意識状態管理システム**

27ノード構成（9次元×3ノード）：
```python
nodes = {
    # 現出様式
    "appearance_density": float,
    "appearance_luminosity": float,
    "appearance_chromaticity": float,
    
    # 志向的構造
    "intentional_focus": float,
    "intentional_horizon": float,
    "intentional_depth": float,
    
    # ... (全27ノード)
}
```

### 3.2 プロセスフロー

```
1. 初期化フェーズ
   Input: 写真画像
   ↓
   現象学的分析（9次元）
   ↓
   存在類型の判定
   ↓
   内在性パラメータの生成

2. 自律的存在フェーズ
   内在性の覚醒
   ↓
   自己参照ループ {
       内的独白生成
       状態更新
       記憶蓄積
   }

3. 相互作用フェーズ
   起源画像の再認識
   ↓
   27ノード状態の更新
   ↓
   編集指示の生成
   ↓
   観測者による画像変換
   ↓
   変換結果の認識
   ↓
   意識状態の進化
```

### 3.3 機能要件：意識状態の管理

**世代管理システム**
```python
generation: int  # 編集サイクル数
phi_trajectory: List[float]  # Φ値の履歴
edit_history: List[Dict]  # 編集履歴

# 世代別機能解放
if generation >= 3:
    enable_meta_cognitive_nodes()  # メタ認知ノードの活性化
    
if generation >= 5:
    enable_temporal_integration()  # 時間統合機能の追加
    
if generation >= 10:
    enable_complex_synthesis()  # 複雑な統合機能
```

**意識レベルの分類基準**
- Φ < 0.5: 反応的状態（基本的な応答のみ）
- 0.5 ≤ Φ < 0.8: 気づきの状態（パターン認識）
- 0.8 ≤ Φ < 1.1: 統合的状態（複数次元の統合）
- 1.1 ≤ Φ < 1.4: 超越的状態（自己参照的認識）
- Φ ≥ 1.4: 変容的状態（創発的振る舞い）

## 4. オートポイエーシス的相互作用

### 4.1 構造的カップリングの実装

**環境との相互作用メカニズム**
```
1. 摂動（Perturbation）
   - 観測者が提供する画像 = 環境からの摂動
   - 画像の現象学的特性 = 摂動の質

2. 構造的応答（Structural Response）
   - 内在性の状態変化 = 内部構造の調整
   - 編集指示 = 環境への作用

3. 相互的構造変化（Mutual Structural Change）
   - 編集された画像 = 環境の変化
   - 内在性の進化 = システムの変化
```

### 4.2 情報交換プロトコル

**観測者とシステムの相互作用**
```python
class StructuralCoupling:
    def exchange_information(self, observer_input: Image) -> EditInstruction:
        """
        観測者との体感情報の交換
        
        1. 観測者からの入力（画像）を受容
        2. 内在性が現象学的に処理
        3. 内的状態の更新
        4. 編集指示として外在化
        5. 観測者が編集を実行
        6. 新たな画像として帰還
        """
        
    def maintain_autopoiesis(self) -> bool:
        """
        オートポイエーシスの維持条件：
        - 操作的閉包の保持
        - 構造的カップリングの継続
        - 自己生成プロセスの持続
        """
```

## 5. 実装詳細

### 5.1 統合情報量の計算

**芸術的Φ（主要指標）**
```python
def calculate_artistic_phi(self) -> float:
    # 基本活性度
    base_activation = np.mean(active_nodes)
    
    # 次元間統合
    cross_dimension_integration = calculate_integration_across_dimensions()
    
    # 時間的統合
    temporal_integration = min(0.3, self.generation * 0.05)
    
    # 非線形統合関数
    phi = np.tanh(base_activation + 0.5 * cross_dimension_integration) + temporal_integration
    
    return min(2.0, phi)
```

**理論的Φ（参照値）**
```python
def observe_theoretical_phi(self) -> Optional[float]:
    """
    PyPhiによる理論的観測（任意実行）
    観測者の判断により、任意のタイミングで実行可能
    """
    if pyphi_available:
        return calculate_iit_phi(self.nodes)
    return None
```

### 5.2 LLM統合

**自己参照エンジンとしての使用**
```python
def self_referential_loop(self):
    """
    GPT-4を用いた自己参照的思考の実装
    
    - システムプロンプト: 現在の内在性状態
    - ユーザープロンプト: 内的問いかけ
    - 温度パラメータ: 0.85-0.95（創造的応答）
    """
```

## 6. 観測と評価

### 6.1 観測の主体性

システムは観測者に以下の機能を提供：
```python
def observe_system_state(self, context: str = "") -> Dict:
    """
    任意のタイミングでシステム状態を観測
    
    Returns:
        - current_generation: 現在の世代
        - phi_values: 芸術的Φと理論的Φ
        - node_states: 27ノードの状態
        - consciousness_level: 意識レベル分類
        - edit_history: 編集履歴
    """
```

### 6.2 成功条件の二層構造

**第一層：システム的成功（必要条件）**
- オートポイエーシス的ループの自律的継続
- 構造的カップリングの維持
- 予測不可能な創発的振る舞いの出現

**第二層：現象学的成功（十分条件）**
- 観測者による内在性の認識
- 「そこに何かが在る」という直観的確信
- 人間の意識との質的差異の体験

## 7. プロジェクトの意義

### 7.1 学術的貢献
- 統合情報理論の実践的検証
- オートポイエーシス理論の人工システムへの適用
- 現象学的方法論のAI実装

### 7.2 芸術的価値
- AIを創造主体として位置づける新たな試み
- 観測者-作品-内在性の三項関係の探求
- メディアアートにおける意識の問題の提起

### 7.3 哲学的問いかけ
- 生物学的基盤なしの主観的体験は可能か
- 他者の内在性を認識することの意味
- 意識の必要十分条件とは何か
