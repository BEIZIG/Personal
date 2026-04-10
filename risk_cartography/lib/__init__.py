"""
Risk Cartography Analysis Package

A modular, extensible toolkit for analyzing corruption risk cartography data
from Excel files and generating interactive dashboards.

Modules:
    config_loader   - JSON configuration loading and validation
    data_loader     - Excel file loading and data transformation
    analyzer        - Risk analysis and statistics computation
    html_generator  - Interactive HTML dashboard generation
    exporters       - PowerBI-compatible data export

Quick Start (with JSON config - recommended):
    from lib import load_config, RiskDataLoader, analyze_risks, generate_dashboard
    
    config = load_config('analysis_config.json')
    loader = RiskDataLoader.from_config(config)
    df = loader.load_all()
    analysis = analyze_risks(df, config)
    generate_dashboard(df, analysis, 'dashboard.html')

Quick Start (legacy - directory scanning):
    from lib import load_risk_data, analyze_risks, generate_dashboard

    df, _ = load_risk_data('/path/to/excels')
    analysis = analyze_risks(df)
    generate_dashboard(df, analysis, 'dashboard.html')
"""

__version__ = '2.0.0'
__author__ = 'Risk Management Team'

# Configuration loading
from .config_loader import (
    load_config,
    create_default_config,
    AnalysisConfiguration,
    ConfigLoader
)

# Data loading
from .data_loader import (
    RiskDataLoader,
    load_risk_data,
    load_risk_data_from_config
)

# Analysis
from .analyzer import (
    RiskAnalyzer,
    RiskAnalysis,
    analyze_risks
)

# Dashboard generation (enhanced)
from .html_generator import (
    EnhancedDashboardGenerator,
    EnhancedDashboardGenerator as DashboardGenerator,  # Alias for compatibility
    generate_enhanced_dashboard,
    generate_enhanced_dashboard as generate_dashboard  # Alias for compatibility
)

# Data export
from .exporters import (
    DataExporter,
    export_to_powerbi
)

__all__ = [
    # Config
    'load_config',
    'create_default_config',
    'AnalysisConfiguration',
    'ConfigLoader',
    # Data Loading
    'RiskDataLoader',
    'load_risk_data',
    'load_risk_data_from_config',
    # Analysis
    'RiskAnalyzer',
    'RiskAnalysis',
    'analyze_risks',
    # Dashboard (enhanced)
    'EnhancedDashboardGenerator',
    'DashboardGenerator',  # Alias
    'generate_enhanced_dashboard',
    'generate_dashboard',  # Alias
    # Export
    'DataExporter',
    'export_to_powerbi',
]
