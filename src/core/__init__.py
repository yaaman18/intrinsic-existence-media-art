"""
内在性の基本コアモジュール
"""

from .existence_types import ExistenceType, ExistenceParameters
from .intrinsic_birth import IntrinsicBirth
from .autonomous_existence import AutonomousIntrinsicExistence
from .intrinsic_artist_dialogue import IntrinsicArtistDialogue
from .phenomenological_analyzer import PhenomenologicalImageAnalyzer, PhenomenologicalParameters
from .direct_intrinsic_birth import DirectIntrinsicBirth
from .phenomenological_oracle_v5 import PhenomenologicalOracleSystem, EditingOracle

__all__ = [
    'ExistenceType',
    'ExistenceParameters',
    'IntrinsicBirth',
    'AutonomousIntrinsicExistence',
    'IntrinsicArtistDialogue',
    'PhenomenologicalImageAnalyzer',
    'PhenomenologicalParameters',
    'DirectIntrinsicBirth',
    'PhenomenologicalOracleSystem',
    'EditingOracle'
]
