"""内在性の存在類型と基本パラメータの定義"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ExistenceType(Enum):
    """存在類型の定義"""
    GAZE = "視線的存在"          # 見る/見られる関係を持つ
    PLACE = "場所的存在"         # 空間として広がる
    OBJECT = "物体的存在"        # 明確な輪郭を持つ個物
    EVENT = "出来事的存在"       # 動きや変化の瞬間
    TRACE = "痕跡的存在"         # かつて在ったものの残存
    RELATION = "関係的存在"      # 複数の要素の相互作用
    ABSTRACT = "抽象的存在"      # 形を持たない強度


@dataclass
class ExistenceParameters:
    """内在性の基本パラメータ"""
    
    # 基本属性
    existence_type: ExistenceType
    core_anxiety: str                   # 根源的不安の種類
    temporal_mode: str                  # 時間性のモード
    
    # 数値パラメータ（0.0-1.0）
    boundary_strength: float = 0.5      # 境界の強さ
    other_dependency: float = 0.5       # 他者依存度
    stability: float = 0.5              # 安定性
    openness: float = 0.5               # 開放性
    
    # 状態
    initial_state: str = "nascent"     # 初期状態
    core_anxiety_level: float = 0.5     # 不安レベル
    
    # オプショナル属性
    special_traits: Optional[list] = None
    birth_image_traits: Optional[dict] = None
    
    def __post_init__(self):
        """初期化後の処理"""
        # 存在類型に応じたデフォルト値の設定
        if self.existence_type == ExistenceType.GAZE:
            self.other_dependency = max(0.7, self.other_dependency)
            self.core_anxiety = self.core_anxiety or "being_unseen"
        elif self.existence_type == ExistenceType.PLACE:
            self.boundary_strength = max(0.3, self.boundary_strength)
            self.core_anxiety = self.core_anxiety or "emptiness"
        elif self.existence_type == ExistenceType.TRACE:
            self.stability = min(0.3, self.stability)
            self.core_anxiety = self.core_anxiety or "complete_disappearance"
            
    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            "existence_type": self.existence_type.value,
            "core_anxiety": self.core_anxiety,
            "temporal_mode": self.temporal_mode,
            "boundary_strength": self.boundary_strength,
            "other_dependency": self.other_dependency,
            "stability": self.stability,
            "openness": self.openness,
            "initial_state": self.initial_state,
            "core_anxiety_level": self.core_anxiety_level,
            "special_traits": self.special_traits,
            "birth_image_traits": self.birth_image_traits
        }