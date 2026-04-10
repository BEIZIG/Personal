"""
Risk Analyzer module for Risk Cartography Analysis.

Handles:
- Statistical analysis of risk data
- Entity-level aggregations
- Category-level aggregations
- Risk matrix calculations
- Mitigation effectiveness analysis

Supports both JSON configuration and standalone usage with defaults.
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# DEFAULT VALUES (used when no JSON config provided)
# =============================================================================

DEFAULT_RISK_LEVELS = {
    '🟢 Faible': {'label': 'Low', 'color': '#28a745', 'order': 1},
    '🟡 Modéré': {'label': 'Moderate', 'color': '#ffc107', 'order': 2},
    '🟠 Élevé': {'label': 'High', 'color': '#fd7e14', 'order': 3},
    '🔴 Critique': {'label': 'Critical', 'color': '#dc3545', 'order': 4}
}

DEFAULT_RISK_CATEGORIES = {
    'A': {'name': 'Procurement (Achats)', 'color': '#3498db'},
    'C': {'name': 'Commercial/Sales', 'color': '#9b59b6'},
    'R': {'name': 'Human Resources (RH)', 'color': '#e74c3c'},
    'F': {'name': 'Finance', 'color': '#2ecc71'},
    'M': {'name': 'M&A / JV', 'color': '#f39c12'},
    'S': {'name': 'Sponsoring', 'color': '#1abc9c'},
    'P': {'name': 'Public Officials', 'color': '#34495e'}
}

DEFAULT_TOP_RISKS_COUNT = 10


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SummaryStats:
    """Overall summary statistics."""
    total_risks: int = 0
    total_entities: int = 0
    avg_gross_score: float = 0.0
    avg_residual_score: float = 0.0
    risk_reduction_pct: float = 0.0
    max_gross_score: float = 0.0
    max_residual_score: float = 0.0


@dataclass
class EntityStats:
    """Statistics for a single entity."""
    entity_name: str
    total_risks: int
    avg_gross_score: float
    avg_residual_score: float
    critical_count: int
    high_count: int
    moderate_count: int
    low_count: int
    risk_reduction_pct: float


@dataclass
class CategoryStats:
    """Statistics for a risk category."""
    category_code: str
    category_name: str
    color: str
    count: int
    avg_gross_score: float
    avg_residual_score: float


@dataclass
class LevelStats:
    """Statistics for a risk level."""
    level_key: str
    label: str
    color: str
    count: int
    percentage: float


@dataclass
class MitigationStats:
    """Mitigation effectiveness statistics."""
    improved: int
    unchanged: int
    worsened: int
    improvement_rate: float


@dataclass
class RiskAnalysis:
    """Complete risk analysis results."""
    generated_at: str
    summary: SummaryStats
    by_entity: Dict[str, EntityStats] = field(default_factory=dict)
    by_category: Dict[str, CategoryStats] = field(default_factory=dict)
    by_level: Dict[str, LevelStats] = field(default_factory=dict)
    risk_matrix_gross: Dict[str, int] = field(default_factory=dict)
    risk_matrix_residual: Dict[str, int] = field(default_factory=dict)
    top_risks: List[Dict] = field(default_factory=list)
    mitigation: MitigationStats = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            'generated_at': self.generated_at,
            'summary': asdict(self.summary),
            'by_entity': {k: asdict(v) for k, v in self.by_entity.items()},
            'by_category': {k: asdict(v) for k, v in self.by_category.items()},
            'by_level': {k: asdict(v) for k, v in self.by_level.items()},
            'risk_matrix_gross': self.risk_matrix_gross,
            'risk_matrix_residual': self.risk_matrix_residual,
            'top_risks': self.top_risks,
            'mitigation': asdict(self.mitigation) if self.mitigation else {}
        }
        return result


# =============================================================================
# RISK ANALYZER
# =============================================================================

class RiskAnalyzer:
    """
    Analyzes risk cartography data.
    
    Supports two modes:
    
    1. With JSON configuration:
        from config_loader import load_config
        config = load_config('analysis_config.json')
        analyzer = RiskAnalyzer.from_config(config)
        analysis = analyzer.analyze(df)
    
    2. Standalone with defaults:
        analyzer = RiskAnalyzer()
        analysis = analyzer.analyze(df)
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize analyzer with optional config overrides.
        
        Args:
            config: Optional dict with 'top_risks_count', 'risk_levels', 'risk_categories'
        """
        self.config = config or {}
        self.top_risks_count = self.config.get('top_risks_count', DEFAULT_TOP_RISKS_COUNT)
        self._risk_levels = self.config.get('risk_levels', DEFAULT_RISK_LEVELS)
        self._risk_categories = self.config.get('risk_categories', DEFAULT_RISK_CATEGORIES)
    
    @classmethod
    def from_config(cls, json_config) -> 'RiskAnalyzer':
        """
        Create analyzer from JSON configuration object.
        
        Args:
            json_config: AnalysisConfiguration from config_loader
            
        Returns:
            Configured RiskAnalyzer
        """
        # Convert JSON config to internal format
        risk_levels = {}
        for level in json_config.risk_levels:
            risk_levels[level.key] = {
                'label': level.label_en,
                'color': level.color,
                'order': level.order
            }
        
        risk_categories = {}
        for cat in json_config.risk_categories:
            risk_categories[cat.prefix] = {
                'name': f"{cat.name_en} ({cat.name_fr})",
                'color': cat.color
            }
        
        config = {
            'top_risks_count': json_config.analysis.top_risks_count,
            'risk_levels': risk_levels,
            'risk_categories': risk_categories
        }
        
        return cls(config)
    
    def analyze(self, df: pd.DataFrame) -> RiskAnalysis:
        """
        Perform comprehensive risk analysis.
        
        Args:
            df: DataFrame with risk data
            
        Returns:
            RiskAnalysis with all computed statistics
        """
        if df.empty:
            logger.warning("Empty DataFrame provided for analysis")
            return RiskAnalysis(
                generated_at=datetime.now().isoformat(),
                summary=SummaryStats()
            )
        
        analysis = RiskAnalysis(
            generated_at=datetime.now().isoformat(),
            summary=self._compute_summary(df),
            by_entity=self._analyze_by_entity(df),
            by_category=self._analyze_by_category(df),
            by_level=self._analyze_by_level(df),
            risk_matrix_gross=self._compute_risk_matrix(df, 'gross'),
            risk_matrix_residual=self._compute_risk_matrix(df, 'residual'),
            top_risks=self._get_top_risks(df),
            mitigation=self._analyze_mitigation(df)
        )
        
        return analysis
    
    def _compute_summary(self, df: pd.DataFrame) -> SummaryStats:
        """Compute overall summary statistics."""
        avg_gross = df['score_gross'].mean() if 'score_gross' in df.columns else 0
        avg_residual = df['score_residual'].mean() if 'score_residual' in df.columns else 0
        
        reduction_pct = 0
        if avg_gross > 0:
            reduction_pct = ((avg_gross - avg_residual) / avg_gross) * 100
        
        return SummaryStats(
            total_risks=len(df),
            total_entities=df['entity'].nunique() if 'entity' in df.columns else 0,
            avg_gross_score=round(avg_gross, 2),
            avg_residual_score=round(avg_residual, 2),
            risk_reduction_pct=round(reduction_pct, 1),
            max_gross_score=float(df['score_gross'].max()) if 'score_gross' in df.columns else 0,
            max_residual_score=float(df['score_residual'].max()) if 'score_residual' in df.columns else 0
        )
    
    def _analyze_by_entity(self, df: pd.DataFrame) -> Dict[str, EntityStats]:
        """Analyze risks grouped by entity."""
        results = {}
        
        if 'entity' not in df.columns:
            return results
        
        for entity in df['entity'].unique():
            entity_df = df[df['entity'] == entity]
            
            avg_gross = entity_df['score_gross'].mean()
            avg_residual = entity_df['score_residual'].mean()
            reduction_pct = ((avg_gross - avg_residual) / avg_gross * 100) if avg_gross > 0 else 0
            
            results[entity] = EntityStats(
                entity_name=entity,
                total_risks=len(entity_df),
                avg_gross_score=round(avg_gross, 2),
                avg_residual_score=round(avg_residual, 2),
                critical_count=len(entity_df[entity_df['level_residual'] == '🔴 Critique']),
                high_count=len(entity_df[entity_df['level_residual'] == '🟠 Élevé']),
                moderate_count=len(entity_df[entity_df['level_residual'] == '🟡 Modéré']),
                low_count=len(entity_df[entity_df['level_residual'] == '🟢 Faible']),
                risk_reduction_pct=round(reduction_pct, 1)
            )
        
        return results
    
    def _analyze_by_category(self, df: pd.DataFrame) -> Dict[str, CategoryStats]:
        """Analyze risks grouped by category."""
        results = {}
        
        if 'category' not in df.columns:
            return results
        
        for cat_code, cat_info in self._risk_categories.items():
            cat_df = df[df['category'] == cat_code]
            
            if len(cat_df) > 0:
                results[cat_code] = CategoryStats(
                    category_code=cat_code,
                    category_name=cat_info['name'],
                    color=cat_info['color'],
                    count=len(cat_df),
                    avg_gross_score=round(cat_df['score_gross'].mean(), 2),
                    avg_residual_score=round(cat_df['score_residual'].mean(), 2)
                )
        
        return results
    
    def _analyze_by_level(self, df: pd.DataFrame) -> Dict[str, LevelStats]:
        """Analyze risks grouped by risk level."""
        results = {}
        total = len(df)
        
        if 'level_residual' not in df.columns or total == 0:
            return results
        
        for level_key, level_info in self._risk_levels.items():
            level_df = df[df['level_residual'] == level_key]
            count = len(level_df)
            
            results[level_key] = LevelStats(
                level_key=level_key,
                label=level_info['label'],
                color=level_info['color'],
                count=count,
                percentage=round(count / total * 100, 1)
            )
        
        return results
    
    def _compute_risk_matrix(self, df: pd.DataFrame, risk_type: str) -> Dict[str, int]:
        """
        Compute risk matrix (probability x impact).
        
        Args:
            df: DataFrame with risk data
            risk_type: 'gross' or 'residual'
            
        Returns:
            Dictionary with matrix cell counts (e.g., '1x2': 5)
        """
        matrix = {}
        prob_col = f'prob_{risk_type}'
        impact_col = f'impact_{risk_type}'
        
        if prob_col not in df.columns or impact_col not in df.columns:
            return matrix
        
        # Standard 4x4 matrix
        for prob in range(1, 5):
            for impact in range(1, 5):
                key = f"{prob}x{impact}"
                count = len(df[(df[prob_col] == prob) & (df[impact_col] == impact)])
                matrix[key] = count
        
        return matrix
    
    def _get_top_risks(self, df: pd.DataFrame) -> List[Dict]:
        """Get top N highest residual risks."""
        if 'score_residual' not in df.columns:
            return []
        
        top_df = df.nlargest(self.top_risks_count, 'score_residual')
        
        columns = ['entity', 'risk_id', 'scenario', 'score_gross', 'score_residual', 'level_residual']
        available_cols = [c for c in columns if c in top_df.columns]
        
        return top_df[available_cols].to_dict('records')
    
    def _analyze_mitigation(self, df: pd.DataFrame) -> MitigationStats:
        """Analyze mitigation effectiveness."""
        if 'score_gross' not in df.columns or 'score_residual' not in df.columns:
            return MitigationStats(0, 0, 0, 0.0)
        
        improved = len(df[df['score_residual'] < df['score_gross']])
        unchanged = len(df[df['score_residual'] == df['score_gross']])
        worsened = len(df[df['score_residual'] > df['score_gross']])
        
        total = len(df)
        improvement_rate = (improved / total * 100) if total > 0 else 0
        
        return MitigationStats(
            improved=improved,
            unchanged=unchanged,
            worsened=worsened,
            improvement_rate=round(improvement_rate, 1)
        )


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def analyze_risks(df: pd.DataFrame, config=None) -> RiskAnalysis:
    """
    Convenience function to analyze risk data.
    
    Args:
        df: DataFrame with risk data
        config: Optional JSON config (AnalysisConfiguration) or dict
        
    Returns:
        RiskAnalysis object
    """
    if config is not None and hasattr(config, 'risk_levels'):
        # JSON configuration object
        analyzer = RiskAnalyzer.from_config(config)
    elif isinstance(config, dict):
        # Dict configuration
        analyzer = RiskAnalyzer(config)
    else:
        # Default
        analyzer = RiskAnalyzer()
    
    return analyzer.analyze(df)


if __name__ == "__main__":
    # Test with sample data
    import sys
    from pathlib import Path
    
    logging.basicConfig(level=logging.INFO)
    
    lib_dir = Path(__file__).parent
    config_path = lib_dir / "analysis_config.json"
    
    if config_path.exists():
        print("=== Testing with JSON Configuration ===")
        from config_loader import load_config
        from data_loader import load_risk_data_from_config
        
        config = load_config(str(config_path))
        df, _ = load_risk_data_from_config(config)
        
        analyzer = RiskAnalyzer.from_config(config)
        analysis = analyzer.analyze(df)
    else:
        print("=== Testing with Default Configuration ===")
        from data_loader import load_risk_data
        
        test_dir = lib_dir.parent
        df, _ = load_risk_data(str(test_dir))
        
        analysis = analyze_risks(df)
    
    print("\n=== ANALYSIS SUMMARY ===")
    print(f"Total Risks: {analysis.summary.total_risks}")
    print(f"Total Entities: {analysis.summary.total_entities}")
    print(f"Avg Gross Score: {analysis.summary.avg_gross_score}")
    print(f"Avg Residual Score: {analysis.summary.avg_residual_score}")
    print(f"Risk Reduction: {analysis.summary.risk_reduction_pct}%")
    
    print("\n=== BY LEVEL ===")
    for level, stats in analysis.by_level.items():
        print(f"  {level}: {stats.count} ({stats.percentage}%)")
