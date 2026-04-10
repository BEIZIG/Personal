"""
Configuration Loader module for Risk Cartography Analysis.

Handles:
- Loading JSON configuration files
- Validating configuration structure
- Converting JSON to Python dataclasses
- Providing default configuration
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# =============================================================================
# DATA CLASSES FOR CONFIGURATION
# =============================================================================

@dataclass
class FileConfig:
    """Configuration for a single Excel file."""
    filename: str
    entity_name: str
    enabled: bool = True
    sheet_name: str = "All"
    skip_rows: int = 3
    # Optional per-file column overrides
    column_mapping: Optional[Dict[str, str]] = None


@dataclass
class InputConfig:
    """Input files configuration."""
    base_directory: str = "../"
    file_pattern: str = "*.xlsx"
    files: List[FileConfig] = field(default_factory=list)
    
    # Extract entity name from filename pattern
    filename_prefix: str = "carto_des_risques_"


@dataclass
class ColumnsConfig:
    """Column mapping configuration."""
    mapping: Dict[int, str] = field(default_factory=dict)
    numeric_fields: List[str] = field(default_factory=list)
    skip_header_values: List[str] = field(default_factory=list)


@dataclass
class RiskLevelConfig:
    """Single risk level definition."""
    key: str
    label_en: str
    label_fr: str
    color: str
    order: int
    score_min: int
    score_max: int


@dataclass
class RiskCategoryConfig:
    """Single risk category definition."""
    prefix: str
    name_en: str
    name_fr: str
    color: str
    icon: str


@dataclass
class AnalysisParams:
    """Analysis parameters."""
    top_risks_count: int = 10
    probability_range: tuple = (1, 4)
    impact_range: tuple = (1, 4)


@dataclass
class OutputConfig:
    """Output configuration."""
    directory: str = "./"
    dashboard_filename: str = "risk_dashboard.html"
    exports: Dict[str, str] = field(default_factory=dict)


@dataclass
class DashboardColors:
    """Dashboard color scheme."""
    background_primary: str = "#1a1d29"
    background_secondary: str = "#252836"
    background_card: str = "#2d3142"
    text_primary: str = "#ffffff"
    text_secondary: str = "#a0a3b1"
    accent: str = "#00d4ff"
    border: str = "#3d4157"
    # Status colors (fixed values for risk levels)
    success: str = "#28a745"
    warning: str = "#ffc107"
    orange: str = "#fd7e14"
    danger: str = "#dc3545"


@dataclass
class DashboardConfig:
    """Dashboard configuration."""
    title: str = "Risk Cartography Dashboard"
    colors: DashboardColors = field(default_factory=DashboardColors)


@dataclass
class AnalysisConfiguration:
    """Complete analysis configuration."""
    version: str = "1.0.0"
    input: InputConfig = field(default_factory=InputConfig)
    columns: ColumnsConfig = field(default_factory=ColumnsConfig)
    risk_levels: List[RiskLevelConfig] = field(default_factory=list)
    risk_categories: List[RiskCategoryConfig] = field(default_factory=list)
    analysis: AnalysisParams = field(default_factory=AnalysisParams)
    output: OutputConfig = field(default_factory=OutputConfig)
    dashboard: DashboardConfig = field(default_factory=DashboardConfig)
    
    # Computed lookup dictionaries
    _risk_levels_dict: Dict[str, RiskLevelConfig] = field(default_factory=dict, repr=False)
    _risk_categories_dict: Dict[str, RiskCategoryConfig] = field(default_factory=dict, repr=False)
    
    def __post_init__(self):
        """Build lookup dictionaries after initialization."""
        self._risk_levels_dict = {level.key: level for level in self.risk_levels}
        self._risk_categories_dict = {cat.prefix: cat for cat in self.risk_categories}
    
    def get_level(self, key: str) -> Optional[RiskLevelConfig]:
        """Get risk level by key."""
        return self._risk_levels_dict.get(key)
    
    def get_level_for_score(self, score: int) -> Optional[RiskLevelConfig]:
        """Get risk level for a given score."""
        for level in self.risk_levels:
            if level.score_min <= score <= level.score_max:
                return level
        return None
    
    def get_category(self, prefix: str) -> Optional[RiskCategoryConfig]:
        """Get category by prefix letter."""
        return self._risk_categories_dict.get(prefix.upper())
    
    def get_enabled_files(self) -> List[FileConfig]:
        """Get list of enabled files only."""
        return [f for f in self.input.files if f.enabled]
    
    def get_column_mapping_int_keys(self) -> Dict[int, str]:
        """Get column mapping with integer keys."""
        return {int(k): v for k, v in self.columns.mapping.items()}


# =============================================================================
# CONFIGURATION LOADER
# =============================================================================

class ConfigLoader:
    """
    Loads and validates configuration from JSON files.
    
    Usage:
        loader = ConfigLoader()
        config = loader.load('analysis_config.json')
    """
    
    DEFAULT_CONFIG_NAME = "analysis_config.json"
    
    def __init__(self):
        """Initialize the config loader."""
        self.config_path: Optional[Path] = None
        self.raw_config: Dict = {}
    
    def load(self, config_path: str) -> AnalysisConfiguration:
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to JSON config file
            
        Returns:
            AnalysisConfiguration object
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If JSON is invalid
            ValueError: If configuration is invalid
        """
        self.config_path = Path(config_path).resolve()
        
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        logger.info(f"Loading configuration from: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.raw_config = json.load(f)
        
        return self._parse_config(self.raw_config)
    
    def _parse_config(self, raw: Dict) -> AnalysisConfiguration:
        """Parse raw JSON into configuration dataclasses."""
        
        # Parse input configuration
        input_raw = raw.get('input', {})
        files = []
        for file_raw in input_raw.get('files', []):
            files.append(FileConfig(
                filename=file_raw.get('filename', ''),
                entity_name=file_raw.get('entity_name', ''),
                enabled=file_raw.get('enabled', True),
                sheet_name=file_raw.get('sheet_name', 'All'),
                skip_rows=file_raw.get('skip_rows', 3),
                column_mapping=file_raw.get('column_mapping')
            ))
        
        input_config = InputConfig(
            base_directory=input_raw.get('base_directory', '../'),
            file_pattern=input_raw.get('file_pattern', '*.xlsx'),
            files=files,
            filename_prefix=input_raw.get('filename_prefix', 'carto_des_risques_')
        )
        
        # Parse columns configuration
        columns_raw = raw.get('columns', {})
        mapping_raw = columns_raw.get('mapping', {})
        columns_config = ColumnsConfig(
            mapping={int(k): v for k, v in mapping_raw.items()},
            numeric_fields=columns_raw.get('numeric_fields', []),
            skip_header_values=columns_raw.get('skip_header_values', [])
        )
        
        # Parse risk levels
        levels_raw = raw.get('risk_levels', {}).get('levels', [])
        risk_levels = []
        for level_raw in levels_raw:
            risk_levels.append(RiskLevelConfig(
                key=level_raw.get('key', ''),
                label_en=level_raw.get('label_en', ''),
                label_fr=level_raw.get('label_fr', ''),
                color=level_raw.get('color', '#6c757d'),
                order=level_raw.get('order', 0),
                score_min=level_raw.get('score_min', 0),
                score_max=level_raw.get('score_max', 16)
            ))
        
        # Parse risk categories
        categories_raw = raw.get('risk_categories', {}).get('categories', [])
        risk_categories = []
        for cat_raw in categories_raw:
            risk_categories.append(RiskCategoryConfig(
                prefix=cat_raw.get('prefix', ''),
                name_en=cat_raw.get('name_en', ''),
                name_fr=cat_raw.get('name_fr', ''),
                color=cat_raw.get('color', '#6c757d'),
                icon=cat_raw.get('icon', '📋')
            ))
        
        # Parse analysis params
        analysis_raw = raw.get('analysis', {})
        prob_range = analysis_raw.get('probability_range', [1, 4])
        impact_range = analysis_raw.get('impact_range', [1, 4])
        analysis_params = AnalysisParams(
            top_risks_count=analysis_raw.get('top_risks_count', 10),
            probability_range=tuple(prob_range),
            impact_range=tuple(impact_range)
        )
        
        # Parse output configuration
        output_raw = raw.get('output', {})
        output_config = OutputConfig(
            directory=output_raw.get('directory', './'),
            dashboard_filename=output_raw.get('dashboard_filename', 'risk_dashboard.html'),
            exports=output_raw.get('exports', {})
        )
        
        # Parse dashboard configuration
        dashboard_raw = raw.get('dashboard', {})
        colors_raw = dashboard_raw.get('colors', {})
        dashboard_colors = DashboardColors(
            background_primary=colors_raw.get('background_primary', '#1a1d29'),
            background_secondary=colors_raw.get('background_secondary', '#252836'),
            background_card=colors_raw.get('background_card', '#2d3142'),
            text_primary=colors_raw.get('text_primary', '#ffffff'),
            text_secondary=colors_raw.get('text_secondary', '#a0a3b1'),
            accent=colors_raw.get('accent', '#00d4ff'),
            border=colors_raw.get('border', '#3d4157'),
            # Status colors (fixed for risk levels, not usually in config)
            success=colors_raw.get('success', '#28a745'),
            warning=colors_raw.get('warning', '#ffc107'),
            orange=colors_raw.get('orange', '#fd7e14'),
            danger=colors_raw.get('danger', '#dc3545')
        )
        dashboard_config = DashboardConfig(
            title=dashboard_raw.get('title', 'Risk Cartography Dashboard'),
            colors=dashboard_colors
        )
        
        # Build complete configuration
        config = AnalysisConfiguration(
            version=raw.get('version', '1.0.0'),
            input=input_config,
            columns=columns_config,
            risk_levels=risk_levels,
            risk_categories=risk_categories,
            analysis=analysis_params,
            output=output_config,
            dashboard=dashboard_config
        )
        
        logger.info(f"Configuration loaded: {len(config.input.files)} files, "
                   f"{len(config.risk_levels)} levels, {len(config.risk_categories)} categories")
        
        return config
    
    def validate(self, config: AnalysisConfiguration) -> List[str]:
        """
        Validate configuration and return list of warnings/errors.
        
        Args:
            config: Configuration to validate
            
        Returns:
            List of validation messages (empty if valid)
        """
        issues = []
        
        # Check for enabled files
        enabled_files = config.get_enabled_files()
        if not enabled_files:
            issues.append("ERROR: No enabled files in configuration")
        
        # Check column mapping
        if not config.columns.mapping:
            issues.append("ERROR: No column mapping defined")
        
        # Check risk levels
        if not config.risk_levels:
            issues.append("WARNING: No risk levels defined")
        
        # Check risk categories
        if not config.risk_categories:
            issues.append("WARNING: No risk categories defined")
        
        # Check for required columns
        required_cols = ['risk_id', 'score_gross', 'score_residual', 'level_residual']
        defined_cols = set(config.columns.mapping.values())
        for col in required_cols:
            if col not in defined_cols:
                issues.append(f"WARNING: Required column '{col}' not in mapping")
        
        return issues


def load_config(config_path: Optional[str] = None) -> AnalysisConfiguration:
    """
    Convenience function to load configuration.
    
    Args:
        config_path: Path to config file. If None, looks for default in current dir.
        
    Returns:
        AnalysisConfiguration object
    """
    loader = ConfigLoader()
    
    if config_path is None:
        # Look for default config file
        lib_dir = Path(__file__).parent
        default_paths = [
            Path.cwd() / ConfigLoader.DEFAULT_CONFIG_NAME,
            lib_dir.parent / "configuration" / ConfigLoader.DEFAULT_CONFIG_NAME,
            lib_dir / ConfigLoader.DEFAULT_CONFIG_NAME  # Legacy fallback
        ]
        for path in default_paths:
            if path.exists():
                config_path = str(path)
                break
        
        if config_path is None:
            raise FileNotFoundError(
                f"No config file specified and default '{ConfigLoader.DEFAULT_CONFIG_NAME}' not found"
            )
    
    config = loader.load(config_path)
    
    # Validate and log warnings
    issues = loader.validate(config)
    for issue in issues:
        if issue.startswith("ERROR"):
            logger.error(issue)
        else:
            logger.warning(issue)
    
    return config


def create_default_config(output_path: str, input_dir: str = "../") -> str:
    """
    Create a default configuration file by scanning for Excel files.
    
    Args:
        output_path: Where to save the config file
        input_dir: Directory to scan for Excel files
        
    Returns:
        Path to created config file
    """
    import glob
    
    input_path = Path(input_dir).resolve()
    excel_files = sorted(glob.glob(str(input_path / "*.xlsx")))
    
    files_config = []
    for filepath in excel_files:
        filename = os.path.basename(filepath)
        entity_name = filename.replace("carto_des_risques_", "").replace(".xlsx", "")
        files_config.append({
            "filename": filename,
            "entity_name": entity_name,
            "enabled": True,
            "sheet_name": "All",
            "skip_rows": 3
        })
    
    config = {
        "version": "1.0.0",
        "input": {
            "base_directory": str(input_path),
            "file_pattern": "*.xlsx",
            "files": files_config
        },
        "columns": {
            "mapping": {
                "0": "risk_id",
                "1": "scenario",
                "2": "description",
                "3": "aggravating_factors",
                "4": "prob_gross",
                "5": "impact_gross",
                "6": "score_gross",
                "7": "level_gross",
                "8": "prevention_measures",
                "9": "prob_residual",
                "10": "impact_residual",
                "11": "score_residual",
                "12": "level_residual",
                "13": "corrective_actions"
            },
            "numeric_fields": [
                "prob_gross", "impact_gross", "score_gross",
                "prob_residual", "impact_residual", "score_residual"
            ],
            "skip_header_values": ["N°", "N"]
        },
        "risk_levels": {
            "levels": [
                {"key": "🟢 Faible", "label_en": "Low", "label_fr": "Faible", 
                 "color": "#28a745", "order": 1, "score_min": 1, "score_max": 2},
                {"key": "🟡 Modéré", "label_en": "Moderate", "label_fr": "Modéré",
                 "color": "#ffc107", "order": 2, "score_min": 3, "score_max": 6},
                {"key": "🟠 Élevé", "label_en": "High", "label_fr": "Élevé",
                 "color": "#fd7e14", "order": 3, "score_min": 7, "score_max": 9},
                {"key": "🔴 Critique", "label_en": "Critical", "label_fr": "Critique",
                 "color": "#dc3545", "order": 4, "score_min": 10, "score_max": 16}
            ]
        },
        "risk_categories": {
            "categories": [
                {"prefix": "A", "name_en": "Procurement", "name_fr": "Achats", "color": "#3498db", "icon": "🛒"},
                {"prefix": "C", "name_en": "Commercial/Sales", "name_fr": "Commercial", "color": "#9b59b6", "icon": "💼"},
                {"prefix": "R", "name_en": "Human Resources", "name_fr": "Ressources Humaines", "color": "#e74c3c", "icon": "👥"},
                {"prefix": "F", "name_en": "Finance", "name_fr": "Finance", "color": "#2ecc71", "icon": "💰"},
                {"prefix": "M", "name_en": "M&A / Joint Ventures", "name_fr": "M&A / JV", "color": "#f39c12", "icon": "🤝"},
                {"prefix": "S", "name_en": "Sponsoring", "name_fr": "Sponsoring", "color": "#1abc9c", "icon": "🎯"},
                {"prefix": "P", "name_en": "Public Officials", "name_fr": "Agents Publics", "color": "#34495e", "icon": "🏛️"}
            ]
        },
        "analysis": {
            "top_risks_count": 10,
            "probability_range": [1, 4],
            "impact_range": [1, 4]
        },
        "output": {
            "directory": "./",
            "dashboard_filename": "risk_dashboard.html",
            "exports": {
                "risk_data_csv": "powerbi_risk_data.csv",
                "entity_summary_csv": "powerbi_entity_summary.csv",
                "category_summary_csv": "powerbi_category_summary.csv",
                "risk_matrix_csv": "powerbi_risk_matrix.csv",
                "analysis_json": "powerbi_analysis.json"
            }
        },
        "dashboard": {
            "title": "Risk Cartography Dashboard",
            "colors": {
                "background_primary": "#1a1d29",
                "background_secondary": "#252836",
                "background_card": "#2d3142",
                "text_primary": "#ffffff",
                "text_secondary": "#a0a3b1",
                "accent": "#00d4ff",
                "border": "#3d4157"
            }
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Created default config with {len(files_config)} files: {output_path}")
    return output_path


if __name__ == "__main__":
    # Test configuration loading
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = str(Path(__file__).parent / "analysis_config.json")
    
    try:
        config = load_config(config_path)
        
        print("\n=== CONFIGURATION LOADED ===")
        print(f"Version: {config.version}")
        print(f"Files: {len(config.input.files)} ({len(config.get_enabled_files())} enabled)")
        print(f"Columns: {len(config.columns.mapping)}")
        print(f"Risk Levels: {len(config.risk_levels)}")
        print(f"Categories: {len(config.risk_categories)}")
        print(f"Dashboard Title: {config.dashboard.title}")
        
        print("\n=== ENABLED FILES ===")
        for f in config.get_enabled_files():
            print(f"  - {f.filename} (entity: {f.entity_name}, sheet: {f.sheet_name})")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
