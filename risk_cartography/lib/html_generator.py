"""
Enhanced Interactive HTML Dashboard Generator for Risk Cartography Analysis.

Features:
- Interactive filters (entity, level, category)
- Search functionality across all risks
- Drill-down modals with full risk details
- Dark/Light theme toggle
- PDF export capability
- Animated transitions and hover effects
- Executive summary with key insights
- Alert panel for critical risks
- Sortable/filterable tables
- Real-time statistics updates
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

import pandas as pd

# Handle both package and direct imports
try:
    from .analyzer import RiskAnalysis
    from .config_loader import DashboardColors
except ImportError:
    from analyzer import RiskAnalysis
    from config_loader import DashboardColors

logger = logging.getLogger(__name__)

DEFAULT_COLORS = DashboardColors()


class EnhancedDashboardGenerator:
    """
    Generates highly interactive HTML dashboard with advanced features.
    """
    
    def __init__(self, title: str = "Risk Cartography Dashboard", config: Dict = None):
        self.title = title
        self.colors = DEFAULT_COLORS
        self.config = config or {}
    
    def generate(self, df: pd.DataFrame, analysis: RiskAnalysis) -> str:
        """Generate complete enhanced HTML dashboard."""
        risks_json = self._prepare_risks_data(df)
        
        return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    {self._generate_enhanced_styles()}
</head>
<body>
    {self._generate_navigation()}
    <main id="main-content">
        {self._generate_header(analysis)}
        {self._generate_filter_bar(df, analysis)}
        {self._generate_alert_panel(analysis)}
        {self._generate_executive_summary(analysis)}
        {self._generate_kpi_cards(analysis)}
        <div id="charts-section">
            {self._generate_charts_section(analysis)}
            {self._generate_risk_matrix_section(df)}
        </div>
        {self._generate_detailed_analysis_section(analysis, df)}
        {self._generate_risk_table_section(df)}
        {self._generate_footer(analysis)}
    </main>
    {self._generate_risk_modal()}
    {self._generate_scripts(analysis, risks_json)}
</body>
</html>'''
    
    def save(self, html: str, filepath: str) -> str:
        """Save HTML to file."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.info(f"Enhanced dashboard saved: {filepath}")
        return str(path)
    
    def _prepare_risks_data(self, df: pd.DataFrame) -> str:
        """Prepare risks data as JSON for JavaScript."""
        risks = []
        for _, row in df.iterrows():
            risk = {
                'entity': str(row.get('entity', '')),
                'risk_id': str(row.get('risk_id', '')),
                'scenario': str(row.get('scenario', '')),
                'description': str(row.get('description', ''))[:500],
                'aggravating_factors': str(row.get('aggravating_factors', '')),
                'prevention_measures': str(row.get('prevention_measures', '')),
                'corrective_actions': str(row.get('corrective_actions', '')),
                'prob_gross': int(row.get('prob_gross', 0)) if pd.notna(row.get('prob_gross')) else 0,
                'impact_gross': int(row.get('impact_gross', 0)) if pd.notna(row.get('impact_gross')) else 0,
                'score_gross': int(row.get('score_gross', 0)) if pd.notna(row.get('score_gross')) else 0,
                'level_gross': str(row.get('level_gross', '')),
                'prob_residual': int(row.get('prob_residual', 0)) if pd.notna(row.get('prob_residual')) else 0,
                'impact_residual': int(row.get('impact_residual', 0)) if pd.notna(row.get('impact_residual')) else 0,
                'score_residual': int(row.get('score_residual', 0)) if pd.notna(row.get('score_residual')) else 0,
                'level_residual': str(row.get('level_residual', '')),
                'category': str(row.get('risk_id', ''))[:1] if row.get('risk_id') else ''
            }
            risks.append(risk)
        return json.dumps(risks, ensure_ascii=False)
    
    def _generate_enhanced_styles(self) -> str:
        """Generate enhanced CSS with theme support."""
        return '''<style>
        /* === CSS Variables === */
        :root {
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            --transition-fast: 0.15s ease;
            --transition-normal: 0.3s ease;
            --transition-slow: 0.5s ease;
            --shadow-sm: 0 2px 8px rgba(0,0,0,0.1);
            --shadow-md: 0 4px 20px rgba(0,0,0,0.15);
            --shadow-lg: 0 8px 40px rgba(0,0,0,0.2);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }
        
        /* Dark theme (default) */
        [data-theme="dark"] {
            --bg-primary: #0f1119;
            --bg-secondary: #1a1d29;
            --bg-card: #252836;
            --bg-hover: #2d3142;
            --text-primary: #ffffff;
            --text-secondary: #9ca3af;
            --text-muted: #6b7280;
            --accent: #00d4ff;
            --accent-glow: rgba(0, 212, 255, 0.3);
            --success: #10b981;
            --success-bg: rgba(16, 185, 129, 0.15);
            --warning: #f59e0b;
            --warning-bg: rgba(245, 158, 11, 0.15);
            --orange: #f97316;
            --orange-bg: rgba(249, 115, 22, 0.15);
            --danger: #ef4444;
            --danger-bg: rgba(239, 68, 68, 0.15);
            --border: rgba(255,255,255,0.08);
            --border-strong: rgba(255,255,255,0.15);
            --chart-grid: rgba(255,255,255,0.05);
        }
        
        /* Light theme */
        [data-theme="light"] {
            --bg-primary: #f8fafc;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --bg-hover: #f1f5f9;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
            --accent: #0284c7;
            --accent-glow: rgba(2, 132, 199, 0.2);
            --success: #059669;
            --success-bg: rgba(5, 150, 105, 0.1);
            --warning: #d97706;
            --warning-bg: rgba(217, 119, 6, 0.1);
            --orange: #ea580c;
            --orange-bg: rgba(234, 88, 12, 0.1);
            --danger: #dc2626;
            --danger-bg: rgba(220, 38, 38, 0.1);
            --border: rgba(0,0,0,0.08);
            --border-strong: rgba(0,0,0,0.15);
            --chart-grid: rgba(0,0,0,0.05);
        }
        
        /* === Reset & Base === */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        html { scroll-behavior: smooth; }
        
        body {
            font-family: var(--font-family);
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }
        
        /* === Navigation === */
        .navbar {
            position: sticky;
            top: 0;
            z-index: 100;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        
        .navbar-inner {
            max-width: 1600px;
            margin: 0 auto;
            padding: 0 24px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .nav-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 600;
            font-size: 1.1rem;
            color: var(--text-primary);
        }
        
        .nav-brand-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, var(--accent), #00ff88);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
        
        .nav-links {
            display: flex;
            gap: 8px;
        }
        
        .nav-link {
            padding: 8px 16px;
            border-radius: var(--radius-sm);
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: var(--transition-fast);
        }
        
        .nav-link:hover, .nav-link.active {
            background: var(--bg-hover);
            color: var(--text-primary);
        }
        
        .nav-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: var(--radius-sm);
            font-size: 0.9rem;
            font-weight: 500;
            border: none;
            cursor: pointer;
            transition: var(--transition-fast);
        }
        
        .btn-ghost {
            background: transparent;
            color: var(--text-secondary);
        }
        
        .btn-ghost:hover {
            background: var(--bg-hover);
            color: var(--text-primary);
        }
        
        .btn-primary {
            background: var(--accent);
            color: #000;
        }
        
        .btn-primary:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }
        
        .theme-toggle {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            background: var(--bg-hover);
            border: 1px solid var(--border);
        }
        
        /* === Main Content === */
        #main-content {
            max-width: 1600px;
            margin: 0 auto;
            padding: 24px;
        }
        
        /* === Header === */
        .dashboard-header {
            text-align: center;
            margin-bottom: 24px;
            padding: 32px;
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-card) 100%);
            border-radius: var(--radius-lg);
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }
        
        .dashboard-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--success), var(--warning), var(--orange), var(--danger));
        }
        
        .dashboard-header h1 {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 8px;
            background: linear-gradient(135deg, var(--accent), #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .dashboard-header .subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
        }
        
        .header-stats {
            display: flex;
            justify-content: center;
            gap: 32px;
            margin-top: 20px;
        }
        
        .header-stat {
            text-align: center;
        }
        
        .header-stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--accent);
        }
        
        .header-stat-label {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* === Filter Bar === */
        .filter-bar {
            background: var(--bg-card);
            border-radius: var(--radius-md);
            padding: 16px 20px;
            margin-bottom: 24px;
            border: 1px solid var(--border);
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: center;
        }
        
        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .filter-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .filter-select, .filter-input {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 8px 12px;
            color: var(--text-primary);
            font-size: 0.9rem;
            min-width: 150px;
            transition: var(--transition-fast);
        }
        
        .filter-select:focus, .filter-input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }
        
        .filter-input {
            min-width: 250px;
        }
        
        .filter-chips {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            flex: 1;
        }
        
        .filter-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            background: var(--accent-glow);
            border: 1px solid var(--accent);
            border-radius: 20px;
            font-size: 0.8rem;
            color: var(--accent);
        }
        
        .filter-chip-remove {
            cursor: pointer;
            opacity: 0.7;
        }
        
        .filter-chip-remove:hover {
            opacity: 1;
        }
        
        .filter-stats {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 12px;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        .filter-count {
            font-weight: 600;
            color: var(--accent);
        }
        
        /* === Alert Panel === */
        .alert-panel {
            background: linear-gradient(135deg, var(--danger-bg), transparent);
            border: 1px solid var(--danger);
            border-radius: var(--radius-md);
            padding: 16px 20px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 16px;
            animation: pulse-border 2s infinite;
        }
        
        @keyframes pulse-border {
            0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
            50% { box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1); }
        }
        
        .alert-icon {
            width: 48px;
            height: 48px;
            background: var(--danger);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            flex-shrink: 0;
        }
        
        .alert-content { flex: 1; }
        
        .alert-title {
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 4px;
        }
        
        .alert-description {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        .alert-action {
            background: var(--danger);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: var(--radius-sm);
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-fast);
        }
        
        .alert-action:hover {
            opacity: 0.9;
        }
        
        .alert-panel.hidden { display: none; }
        
        /* === Executive Summary === */
        .executive-summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        
        .insight-card {
            background: var(--bg-card);
            border-radius: var(--radius-md);
            padding: 20px;
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }
        
        .insight-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
        }
        
        .insight-card.success::before { background: var(--success); }
        .insight-card.warning::before { background: var(--warning); }
        .insight-card.danger::before { background: var(--danger); }
        .insight-card.accent::before { background: var(--accent); }
        
        .insight-icon {
            width: 40px;
            height: 40px;
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            margin-bottom: 12px;
        }
        
        .insight-card.success .insight-icon { background: var(--success-bg); }
        .insight-card.warning .insight-icon { background: var(--warning-bg); }
        .insight-card.danger .insight-icon { background: var(--danger-bg); }
        .insight-card.accent .insight-icon { background: var(--accent-glow); }
        
        .insight-title {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .insight-value {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .insight-card.success .insight-value { color: var(--success); }
        .insight-card.warning .insight-value { color: var(--warning); }
        .insight-card.danger .insight-value { color: var(--danger); }
        .insight-card.accent .insight-value { color: var(--accent); }
        
        .insight-detail {
            font-size: 0.9rem;
            color: var(--text-secondary);
        }
        
        .insight-trend {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .trend-up { background: var(--success-bg); color: var(--success); }
        .trend-down { background: var(--danger-bg); color: var(--danger); }
        .trend-stable { background: var(--warning-bg); color: var(--warning); }
        
        /* === KPI Cards === */
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .kpi-card {
            background: var(--bg-card);
            border-radius: var(--radius-md);
            padding: 20px;
            border: 1px solid var(--border);
            text-align: center;
            transition: var(--transition-normal);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .kpi-card::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            transform: scaleX(0);
            transition: var(--transition-normal);
        }
        
        .kpi-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-md);
            border-color: var(--border-strong);
        }
        
        .kpi-card:hover::after {
            transform: scaleX(1);
        }
        
        .kpi-card.success::after { background: var(--success); }
        .kpi-card.warning::after { background: var(--warning); }
        .kpi-card.danger::after { background: var(--danger); }
        .kpi-card.accent::after { background: var(--accent); }
        
        .kpi-value {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 4px;
            transition: var(--transition-fast);
        }
        
        .kpi-card.success .kpi-value { color: var(--success); }
        .kpi-card.warning .kpi-value { color: var(--warning); }
        .kpi-card.danger .kpi-value { color: var(--danger); }
        .kpi-card.accent .kpi-value { color: var(--accent); }
        
        .kpi-label {
            color: var(--text-muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }
        
        .kpi-change {
            font-size: 0.8rem;
            margin-top: 4px;
        }
        
        /* === Charts === */
        .section-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .section-title::before {
            content: '';
            width: 4px;
            height: 24px;
            background: var(--accent);
            border-radius: 2px;
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        
        .chart-card {
            background: var(--bg-card);
            border-radius: var(--radius-md);
            padding: 20px;
            border: 1px solid var(--border);
            transition: var(--transition-normal);
        }
        
        .chart-card:hover {
            border-color: var(--border-strong);
        }
        
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        
        .chart-title {
            font-size: 1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .chart-actions {
            display: flex;
            gap: 8px;
        }
        
        .chart-btn {
            width: 32px;
            height: 32px;
            border-radius: var(--radius-sm);
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: var(--transition-fast);
        }
        
        .chart-btn:hover {
            background: var(--bg-hover);
            color: var(--text-primary);
        }
        
        .chart-container {
            position: relative;
            height: 300px;
        }
        
        .chart-legend {
            display: flex;
            justify-content: center;
            gap: 16px;
            margin-top: 12px;
            flex-wrap: wrap;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
        
        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 3px;
        }
        
        /* === Risk Matrix === */
        .matrix-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .risk-matrix {
            display: grid;
            grid-template-columns: 35px repeat(4, 1fr);
            grid-template-rows: repeat(4, 55px) 30px;
            gap: 6px;
            margin-top: 12px;
            max-width: 350px;
        }
        
        .matrix-cell {
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius-sm);
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
            transition: var(--transition-fast);
            position: relative;
        }
        
        .matrix-cell:hover {
            transform: scale(1.05);
            z-index: 10;
        }
        
        .matrix-cell .tooltip {
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: var(--bg-secondary);
            padding: 6px 10px;
            border-radius: var(--radius-sm);
            font-size: 0.75rem;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: var(--transition-fast);
            border: 1px solid var(--border);
        }
        
        .matrix-cell:hover .tooltip {
            opacity: 1;
        }
        
        .matrix-header {
            color: var(--text-muted);
            font-size: 0.8rem;
            text-align: center;
            font-weight: 500;
        }
        
        .matrix-y-label {
            writing-mode: vertical-rl;
            transform: rotate(180deg);
            color: var(--text-muted);
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .level-low { background: rgba(16, 185, 129, 0.25); color: var(--success); }
        .level-moderate { background: rgba(245, 158, 11, 0.25); color: var(--warning); }
        .level-high { background: rgba(249, 115, 22, 0.25); color: var(--orange); }
        .level-critical { background: rgba(239, 68, 68, 0.25); color: var(--danger); }
        
        .matrix-axis-label {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 8px;
        }
        
        /* === Tables === */
        .table-card {
            background: var(--bg-card);
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
            overflow: hidden;
            margin-bottom: 24px;
        }
        
        .table-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
        }
        
        .table-title {
            font-size: 1rem;
            font-weight: 600;
        }
        
        .table-search {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 8px 12px;
            color: var(--text-primary);
            font-size: 0.9rem;
            min-width: 200px;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .data-table th, .data-table td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        
        .data-table th {
            background: var(--bg-secondary);
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            user-select: none;
            transition: var(--transition-fast);
        }
        
        .data-table th:hover {
            background: var(--bg-hover);
            color: var(--text-primary);
        }
        
        .data-table th .sort-icon {
            margin-left: 6px;
            opacity: 0.5;
        }
        
        .data-table th.sorted .sort-icon {
            opacity: 1;
            color: var(--accent);
        }
        
        .data-table tbody tr {
            transition: var(--transition-fast);
            cursor: pointer;
        }
        
        .data-table tbody tr:hover {
            background: var(--bg-hover);
        }
        
        .data-table td.entity {
            font-weight: 600;
            color: var(--accent);
        }
        
        .risk-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 10px;
            border-radius: 16px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .badge-low { background: var(--success-bg); color: var(--success); }
        .badge-moderate { background: var(--warning-bg); color: var(--warning); }
        .badge-high { background: var(--orange-bg); color: var(--orange); }
        .badge-critical { background: var(--danger-bg); color: var(--danger); }
        
        .score-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 32px;
            height: 26px;
            border-radius: 13px;
            font-weight: 600;
            font-size: 0.85rem;
        }
        
        .score-change {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .score-gross {
            color: var(--text-muted);
            text-decoration: line-through;
            font-size: 0.9rem;
        }
        
        .score-arrow {
            color: var(--success);
        }
        
        /* === Top Risks === */
        .top-risks-list {
            list-style: none;
        }
        
        .risk-item {
            padding: 14px 16px;
            margin-bottom: 8px;
            background: var(--bg-secondary);
            border-radius: var(--radius-sm);
            border-left: 4px solid;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: var(--transition-fast);
        }
        
        .risk-item:hover {
            background: var(--bg-hover);
            transform: translateX(4px);
        }
        
        .risk-item.critical { border-left-color: var(--danger); }
        .risk-item.high { border-left-color: var(--orange); }
        .risk-item.moderate { border-left-color: var(--warning); }
        .risk-item.low { border-left-color: var(--success); }
        
        .risk-info { flex: 1; }
        
        .risk-entity {
            font-weight: 600;
            color: var(--accent);
            font-size: 0.9rem;
        }
        
        .risk-scenario {
            color: var(--text-secondary);
            font-size: 0.85rem;
            margin-top: 4px;
        }
        
        .risk-score-display {
            text-align: right;
        }
        
        .risk-score-value {
            font-size: 1.4rem;
            font-weight: 700;
        }
        
        .risk-item.critical .risk-score-value { color: var(--danger); }
        .risk-item.high .risk-score-value { color: var(--orange); }
        .risk-item.moderate .risk-score-value { color: var(--warning); }
        .risk-item.low .risk-score-value { color: var(--success); }
        
        /* === Modal === */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(4px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: var(--transition-normal);
        }
        
        .modal-overlay.active {
            opacity: 1;
            visibility: visible;
        }
        
        .modal {
            background: var(--bg-card);
            border-radius: var(--radius-lg);
            max-width: 700px;
            width: 90%;
            max-height: 85vh;
            overflow-y: auto;
            border: 1px solid var(--border);
            transform: scale(0.95) translateY(20px);
            transition: var(--transition-normal);
        }
        
        .modal-overlay.active .modal {
            transform: scale(1) translateY(0);
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            background: var(--bg-card);
            z-index: 10;
        }
        
        .modal-title {
            font-size: 1.2rem;
            font-weight: 600;
        }
        
        .modal-close {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: var(--transition-fast);
        }
        
        .modal-close:hover {
            background: var(--danger-bg);
            color: var(--danger);
            border-color: var(--danger);
        }
        
        .modal-body {
            padding: 20px;
        }
        
        .modal-section {
            margin-bottom: 20px;
        }
        
        .modal-section-title {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .modal-section-content {
            background: var(--bg-secondary);
            padding: 12px 16px;
            border-radius: var(--radius-sm);
            font-size: 0.95rem;
            line-height: 1.6;
        }
        
        .modal-scores {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-bottom: 20px;
        }
        
        .score-block {
            background: var(--bg-secondary);
            padding: 16px;
            border-radius: var(--radius-sm);
            text-align: center;
        }
        
        .score-block-label {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 8px;
        }
        
        .score-block-value {
            font-size: 2rem;
            font-weight: 700;
        }
        
        .score-block-details {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 4px;
        }
        
        .score-block.gross .score-block-value { color: var(--orange); }
        .score-block.residual .score-block-value { color: var(--success); }
        
        /* === Footer === */
        .footer {
            text-align: center;
            padding: 24px;
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 24px;
            border-top: 1px solid var(--border);
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 16px;
            margin-bottom: 12px;
        }
        
        .footer-link {
            color: var(--text-secondary);
            text-decoration: none;
            transition: var(--transition-fast);
        }
        
        .footer-link:hover {
            color: var(--accent);
        }
        
        /* === Animations === */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-in {
            animation: fadeIn 0.4s ease forwards;
        }
        
        @keyframes countUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .count-up {
            animation: countUp 0.6s ease forwards;
        }
        
        /* === Responsive === */
        @media (max-width: 1024px) {
            .charts-grid { grid-template-columns: 1fr; }
            .executive-summary { grid-template-columns: repeat(2, 1fr); }
            .nav-links { display: none; }
        }
        
        @media (max-width: 768px) {
            #main-content { padding: 16px; }
            .dashboard-header h1 { font-size: 1.6rem; }
            .kpi-container { grid-template-columns: repeat(2, 1fr); }
            .filter-bar { flex-direction: column; align-items: stretch; }
            .filter-group { flex: 1; }
            .filter-stats { margin-left: 0; justify-content: center; padding-top: 8px; }
            .executive-summary { grid-template-columns: 1fr; }
            .header-stats { flex-wrap: wrap; gap: 16px; }
            .modal { width: 95%; max-height: 90vh; }
        }
        
        /* === Print styles === */
        @media print {
            .navbar, .filter-bar, .btn, .chart-actions, .modal-overlay { display: none !important; }
            body { background: white; color: black; }
            .kpi-card, .chart-card, .table-card { break-inside: avoid; }
        }
    </style>'''
    
    def _generate_navigation(self) -> str:
        """Generate navigation bar."""
        return '''
    <nav class="navbar">
        <div class="navbar-inner">
            <div class="nav-brand">
                <div class="nav-brand-icon">🛡️</div>
                <span>Risk Control</span>
            </div>
            
            <div class="nav-links">
                <a href="#main-content" class="nav-link active">Dashboard</a>
                <a href="#charts-section" class="nav-link">Analytics</a>
                <a href="#risk-table" class="nav-link">Risk Registry</a>
            </div>
            
            <div class="nav-actions">
                <button class="btn btn-ghost" onclick="exportToPDF()">
                    <span>📥</span> Export
                </button>
                <button class="theme-toggle btn-ghost" onclick="toggleTheme()" title="Toggle theme">
                    <span id="theme-icon">🌙</span>
                </button>
            </div>
        </div>
    </nav>'''
    
    def _generate_header(self, analysis: RiskAnalysis) -> str:
        """Generate dashboard header."""
        s = analysis.summary
        return f'''
    <div class="dashboard-header animate-in">
        <h1>Risk Cartography Dashboard</h1>
        <div class="subtitle">
            Corruption Risk Analysis • {s.total_entities} Entities • {datetime.now().strftime('%B %d, %Y')}
        </div>
        <div class="header-stats">
            <div class="header-stat">
                <div class="header-stat-value">{s.total_risks}</div>
                <div class="header-stat-label">Total Risks</div>
            </div>
            <div class="header-stat">
                <div class="header-stat-value">{s.risk_reduction_pct:+.0f}%</div>
                <div class="header-stat-label">Risk Reduction</div>
            </div>
            <div class="header-stat">
                <div class="header-stat-value">{s.avg_residual_score:.1f}</div>
                <div class="header-stat-label">Avg Score</div>
            </div>
        </div>
    </div>'''
    
    def _generate_filter_bar(self, df: pd.DataFrame, analysis: RiskAnalysis) -> str:
        """Generate interactive filter bar."""
        entities = sorted(df['entity'].unique())
        categories = ['A', 'C', 'R', 'F', 'M', 'S', 'P']
        cat_names = {
            'A': 'Procurement', 'C': 'Commercial', 'R': 'HR',
            'F': 'Finance', 'M': 'M&A', 'S': 'Sponsoring', 'P': 'Public Officials'
        }
        
        entity_options = ''.join(f'<option value="{e}">{e}</option>' for e in entities)
        cat_options = ''.join(f'<option value="{c}">{c} - {cat_names[c]}</option>' for c in categories)
        
        return f'''
    <div class="filter-bar animate-in" style="animation-delay: 0.1s;">
        <div class="filter-group">
            <label class="filter-label">Entity</label>
            <select class="filter-select" id="entity-filter" onchange="applyFilters()">
                <option value="">All Entities</option>
                {entity_options}
            </select>
        </div>
        
        <div class="filter-group">
            <label class="filter-label">Risk Level</label>
            <select class="filter-select" id="level-filter" onchange="applyFilters()">
                <option value="">All Levels</option>
                <option value="🔴 Critique">🔴 Critical</option>
                <option value="🟠 Élevé">🟠 High</option>
                <option value="🟡 Modéré">🟡 Moderate</option>
                <option value="🟢 Faible">🟢 Low</option>
            </select>
        </div>
        
        <div class="filter-group">
            <label class="filter-label">Category</label>
            <select class="filter-select" id="category-filter" onchange="applyFilters()">
                <option value="">All Categories</option>
                {cat_options}
            </select>
        </div>
        
        <div class="filter-group" style="flex: 1;">
            <label class="filter-label">Search</label>
            <input type="text" class="filter-input" id="search-filter" 
                   placeholder="Search scenarios, descriptions..." 
                   oninput="applyFilters()">
        </div>
        
        <div class="filter-chips" id="active-filters"></div>
        
        <div class="filter-stats">
            <span>Showing <span class="filter-count" id="visible-count">{analysis.summary.total_risks}</span> of {analysis.summary.total_risks}</span>
            <button class="btn btn-ghost" onclick="resetFilters()">Reset</button>
        </div>
    </div>'''
    
    def _generate_alert_panel(self, analysis: RiskAnalysis) -> str:
        """Generate critical risk alert panel."""
        critical_count = sum(1 for r in analysis.top_risks if '🔴' in str(r.get('level_residual', '')))
        
        if critical_count == 0:
            return '<div class="alert-panel hidden"></div>'
        
        return f'''
    <div class="alert-panel animate-in" style="animation-delay: 0.15s;">
        <div class="alert-icon">⚠️</div>
        <div class="alert-content">
            <div class="alert-title">Critical Risks Detected</div>
            <div class="alert-description">
                {critical_count} risk(s) require immediate attention with residual scores ≥10
            </div>
        </div>
        <button class="alert-action" onclick="filterCritical()">View Critical Risks</button>
    </div>'''
    
    def _generate_executive_summary(self, analysis: RiskAnalysis) -> str:
        """Generate executive summary insights."""
        s = analysis.summary
        m = analysis.mitigation
        
        # Find highest risk entity
        worst_entity = max(analysis.by_entity.items(), 
                         key=lambda x: x[1].avg_residual_score)
        best_entity = min(analysis.by_entity.items(),
                         key=lambda x: x[1].avg_residual_score)
        
        # Mitigation effectiveness
        mitigation_rate = (m.improved / s.total_risks * 100) if m else 0
        
        return f'''
    <div class="executive-summary animate-in" style="animation-delay: 0.2s;">
        <div class="insight-card success">
            <div class="insight-icon">📉</div>
            <div class="insight-title">Risk Reduction</div>
            <div class="insight-value">{s.risk_reduction_pct:+.1f}%</div>
            <div class="insight-detail">
                Average score reduced from {s.avg_gross_score:.1f} to {s.avg_residual_score:.1f}
                <span class="insight-trend trend-up">✓ Effective</span>
            </div>
        </div>
        
        <div class="insight-card warning">
            <div class="insight-icon">🎯</div>
            <div class="insight-title">Mitigation Rate</div>
            <div class="insight-value">{mitigation_rate:.0f}%</div>
            <div class="insight-detail">
                {m.improved if m else 0} of {s.total_risks} risks successfully mitigated
            </div>
        </div>
        
        <div class="insight-card danger">
            <div class="insight-icon">📍</div>
            <div class="insight-title">Highest Exposure</div>
            <div class="insight-value">{worst_entity[0]}</div>
            <div class="insight-detail">
                Average residual score: {worst_entity[1].avg_residual_score:.1f} 
                ({worst_entity[1].critical_count} critical)
            </div>
        </div>
        
        <div class="insight-card accent">
            <div class="insight-icon">⭐</div>
            <div class="insight-title">Best Performance</div>
            <div class="insight-value">{best_entity[0]}</div>
            <div class="insight-detail">
                Average residual score: {best_entity[1].avg_residual_score:.1f}
                <span class="insight-trend trend-up">★ Benchmark</span>
            </div>
        </div>
    </div>'''
    
    def _generate_kpi_cards(self, analysis: RiskAnalysis) -> str:
        """Generate KPI cards."""
        s = analysis.summary
        m = analysis.mitigation
        
        critical_count = analysis.by_level.get('🔴 Critique', type('', (), {'count': 0})).count
        high_count = analysis.by_level.get('🟠 Élevé', type('', (), {'count': 0})).count
        
        return f'''
    <div class="kpi-container animate-in" style="animation-delay: 0.25s;">
        <div class="kpi-card accent" onclick="filterByLevel('')" title="Click to view all">
            <div class="kpi-value count-up">{s.total_risks}</div>
            <div class="kpi-label">Total Risks</div>
        </div>
        <div class="kpi-card danger" onclick="filterByLevel('🔴 Critique')" title="Click to filter">
            <div class="kpi-value count-up">{critical_count}</div>
            <div class="kpi-label">Critical</div>
        </div>
        <div class="kpi-card warning" onclick="filterByLevel('🟠 Élevé')" title="Click to filter">
            <div class="kpi-value count-up">{high_count}</div>
            <div class="kpi-label">High</div>
        </div>
        <div class="kpi-card success">
            <div class="kpi-value count-up">{m.improved if m else 0}</div>
            <div class="kpi-label">Mitigated</div>
            <div class="kpi-change" style="color: var(--success);">↓ Reduced</div>
        </div>
        <div class="kpi-card {'success' if s.risk_reduction_pct > 0 else 'warning'}">
            <div class="kpi-value count-up">{s.risk_reduction_pct:+.0f}%</div>
            <div class="kpi-label">Reduction</div>
        </div>
        <div class="kpi-card accent">
            <div class="kpi-value count-up">{s.total_entities}</div>
            <div class="kpi-label">Entities</div>
        </div>
    </div>'''
    
    def _generate_charts_section(self, analysis: RiskAnalysis) -> str:
        """Generate charts section."""
        return '''
    <div class="charts-grid animate-in" style="animation-delay: 0.3s;">
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">📊 Risk Level Distribution</h3>
                <div class="chart-actions">
                    <button class="chart-btn" onclick="toggleChartType('riskLevelChart')" title="Toggle chart type">🔄</button>
                </div>
            </div>
            <div class="chart-container">
                <canvas id="riskLevelChart"></canvas>
            </div>
        </div>
        
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">📁 Risks by Category</h3>
            </div>
            <div class="chart-container">
                <canvas id="categoryChart"></canvas>
            </div>
        </div>
        
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">🏢 Entity Risk Breakdown</h3>
            </div>
            <div class="chart-container">
                <canvas id="entityChart"></canvas>
            </div>
        </div>
        
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">📈 Gross vs Residual Comparison</h3>
            </div>
            <div class="chart-container">
                <canvas id="comparisonChart"></canvas>
            </div>
        </div>
    </div>'''
    
    def _generate_risk_matrix_section(self, df: pd.DataFrame) -> str:
        """Generate risk matrix section."""
        return f'''
    <div class="charts-grid animate-in" style="animation-delay: 0.35s;">
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">🔥 Risk Heat Matrix — Gross</h3>
            </div>
            <div class="matrix-container">
                <div class="risk-matrix" id="matrix-gross">
                    <div class="matrix-y-label" style="grid-row: 1 / 5;">Impact</div>
                    {self._generate_matrix_cells(df, 'gross')}
                    <div></div>
                    <div class="matrix-header">1</div>
                    <div class="matrix-header">2</div>
                    <div class="matrix-header">3</div>
                    <div class="matrix-header">4</div>
                </div>
                <div class="matrix-axis-label">Probability</div>
            </div>
        </div>
        
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">✅ Risk Heat Matrix — Residual</h3>
            </div>
            <div class="matrix-container">
                <div class="risk-matrix" id="matrix-residual">
                    <div class="matrix-y-label" style="grid-row: 1 / 5;">Impact</div>
                    {self._generate_matrix_cells(df, 'residual')}
                    <div></div>
                    <div class="matrix-header">1</div>
                    <div class="matrix-header">2</div>
                    <div class="matrix-header">3</div>
                    <div class="matrix-header">4</div>
                </div>
                <div class="matrix-axis-label">Probability</div>
            </div>
        </div>
    </div>'''
    
    def _generate_matrix_cells(self, df: pd.DataFrame, risk_type: str) -> str:
        """Generate matrix cells with tooltips."""
        prob_col = f'prob_{risk_type}'
        impact_col = f'impact_{risk_type}'
        
        cells = []
        for impact in range(4, 0, -1):
            for prob in range(1, 5):
                count = len(df[(df[prob_col] == prob) & (df[impact_col] == impact)])
                score = prob * impact
                
                if score <= 2:
                    level_class = 'level-low'
                elif score <= 6:
                    level_class = 'level-moderate'
                elif score <= 9:
                    level_class = 'level-high'
                else:
                    level_class = 'level-critical'
                
                display = count if count > 0 else ''
                tooltip = f'P={prob}, I={impact}, Score={score}'
                cells.append(f'''<div class="matrix-cell {level_class}" onclick="filterByMatrix({prob}, {impact}, '{risk_type}')">
                    {display}
                    <span class="tooltip">{tooltip}</span>
                </div>''')
        
        return '\n                    '.join(cells)
    
    def _generate_detailed_analysis_section(self, analysis: RiskAnalysis, df: pd.DataFrame) -> str:
        """Generate detailed analysis section."""
        return f'''
    <div class="charts-grid animate-in" style="animation-delay: 0.4s;">
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">⚠️ Top 10 Highest Residual Risks</h3>
            </div>
            <ul class="top-risks-list">
                {self._generate_top_risks_list(analysis.top_risks)}
            </ul>
        </div>
        
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">🏢 Entity Summary</h3>
            </div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Entity</th>
                        <th>Risks</th>
                        <th>Critical</th>
                        <th>High</th>
                        <th>Avg Score</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_entity_rows(analysis.by_entity)}
                </tbody>
            </table>
        </div>
    </div>
    
    <div class="charts-grid animate-in" style="animation-delay: 0.45s;">
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">🎯 Mitigation Effectiveness</h3>
            </div>
            <div class="chart-container">
                <canvas id="mitigationChart"></canvas>
            </div>
        </div>
        
        <div class="chart-card">
            <div class="chart-header">
                <h3 class="chart-title">🕸️ Category Risk Radar</h3>
            </div>
            <div class="chart-container">
                <canvas id="categoryRadarChart"></canvas>
            </div>
        </div>
    </div>'''
    
    def _generate_top_risks_list(self, top_risks: List[Dict]) -> str:
        """Generate top risks list."""
        items = []
        for risk in top_risks:
            level = risk.get('level_residual', '')
            if '🔴' in level:
                level_class = 'critical'
            elif '🟠' in level:
                level_class = 'high'
            elif '🟡' in level:
                level_class = 'moderate'
            else:
                level_class = 'low'
            
            scenario = str(risk.get('scenario', ''))[:60]
            if len(str(risk.get('scenario', ''))) > 60:
                scenario += '...'
            
            risk_id = risk.get('risk_id', '')
            entity = risk.get('entity', '')
            
            items.append(f'''
                <li class="risk-item {level_class}" onclick="showRiskDetail('{entity}', '{risk_id}')">
                    <div class="risk-info">
                        <span class="risk-entity">{entity} • {risk_id}</span>
                        <div class="risk-scenario">{scenario}</div>
                    </div>
                    <div class="risk-score-display">
                        <div class="score-change">
                            <span class="score-gross">{risk.get('score_gross', '')}</span>
                            <span class="score-arrow">→</span>
                            <span class="risk-score-value">{risk.get('score_residual', '')}</span>
                        </div>
                    </div>
                </li>''')
        
        return '\n'.join(items)
    
    def _generate_entity_rows(self, by_entity: Dict) -> str:
        """Generate entity table rows."""
        rows = []
        for entity_name, stats in sorted(by_entity.items()):
            critical_badge = (
                f'<span class="risk-badge badge-critical">{stats.critical_count}</span>'
                if stats.critical_count > 0 
                else '<span style="color: var(--text-muted);">0</span>'
            )
            high_badge = (
                f'<span class="risk-badge badge-high">{stats.high_count}</span>'
                if stats.high_count > 0 
                else '<span style="color: var(--text-muted);">0</span>'
            )
            
            rows.append(f'''
                <tr onclick="filterByEntity('{entity_name}')" style="cursor: pointer;">
                    <td class="entity">{entity_name}</td>
                    <td>{stats.total_risks}</td>
                    <td>{critical_badge}</td>
                    <td>{high_badge}</td>
                    <td>{stats.avg_residual_score:.1f}</td>
                </tr>''')
        
        return '\n'.join(rows)
    
    def _generate_risk_table_section(self, df: pd.DataFrame) -> str:
        """Generate full risk registry table."""
        return '''
    <div class="table-card animate-in" style="animation-delay: 0.5s;" id="risk-table">
        <div class="table-header">
            <h3 class="table-title">📋 Complete Risk Registry</h3>
            <input type="text" class="table-search" placeholder="Search registry..." 
                   id="registry-search" oninput="filterRegistry()">
        </div>
        <div style="overflow-x: auto;">
            <table class="data-table" id="risk-registry">
                <thead>
                    <tr>
                        <th onclick="sortRegistry('entity')">Entity <span class="sort-icon">↕</span></th>
                        <th onclick="sortRegistry('risk_id')">ID <span class="sort-icon">↕</span></th>
                        <th onclick="sortRegistry('scenario')">Scenario <span class="sort-icon">↕</span></th>
                        <th onclick="sortRegistry('score_gross')">Gross <span class="sort-icon">↕</span></th>
                        <th onclick="sortRegistry('score_residual')">Residual <span class="sort-icon">↕</span></th>
                        <th onclick="sortRegistry('level_residual')">Level <span class="sort-icon">↕</span></th>
                    </tr>
                </thead>
                <tbody id="registry-body">
                    <!-- Populated by JavaScript -->
                </tbody>
            </table>
        </div>
        <div style="padding: 16px; color: var(--text-muted); text-align: center;" id="registry-status">
            Loading risk data...
        </div>
    </div>'''
    
    def _generate_risk_modal(self) -> str:
        """Generate risk detail modal."""
        return '''
    <div class="modal-overlay" id="risk-modal" onclick="closeModal(event)">
        <div class="modal" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h2 class="modal-title" id="modal-title">Risk Details</h2>
                <button class="modal-close" onclick="closeModal()">✕</button>
            </div>
            <div class="modal-body">
                <div class="modal-scores">
                    <div class="score-block gross">
                        <div class="score-block-label">Gross Risk</div>
                        <div class="score-block-value" id="modal-gross-score">-</div>
                        <div class="score-block-details" id="modal-gross-details">P:- × I:-</div>
                    </div>
                    <div class="score-block residual">
                        <div class="score-block-label">Residual Risk</div>
                        <div class="score-block-value" id="modal-residual-score">-</div>
                        <div class="score-block-details" id="modal-residual-details">P:- × I:-</div>
                    </div>
                </div>
                
                <div class="modal-section">
                    <div class="modal-section-title">Scenario</div>
                    <div class="modal-section-content" id="modal-scenario">-</div>
                </div>
                
                <div class="modal-section">
                    <div class="modal-section-title">Description</div>
                    <div class="modal-section-content" id="modal-description">-</div>
                </div>
                
                <div class="modal-section">
                    <div class="modal-section-title">Aggravating Factors</div>
                    <div class="modal-section-content" id="modal-factors">-</div>
                </div>
                
                <div class="modal-section">
                    <div class="modal-section-title">Prevention Measures</div>
                    <div class="modal-section-content" id="modal-prevention">-</div>
                </div>
                
                <div class="modal-section">
                    <div class="modal-section-title">Corrective Actions</div>
                    <div class="modal-section-content" id="modal-actions">-</div>
                </div>
            </div>
        </div>
    </div>'''
    
    def _generate_footer(self, analysis: RiskAnalysis) -> str:
        """Generate footer."""
        return f'''
    <div class="footer">
        <div class="footer-links">
            <a href="#" class="footer-link" onclick="exportToPDF(); return false;">Export PDF</a>
            <a href="#" class="footer-link" onclick="exportToCSV(); return false;">Export CSV</a>
            <a href="#" class="footer-link" onclick="printDashboard(); return false;">Print</a>
        </div>
        <p>Risk Cartography Dashboard • {analysis.summary.total_entities} Entities • {analysis.summary.total_risks} Risk Records</p>
        <p style="margin-top: 4px;">Generated {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
    </div>'''
    
    def _generate_scripts(self, analysis: RiskAnalysis, risks_json: str) -> str:
        """Generate JavaScript."""
        # Prepare chart data
        level_data = [
            analysis.by_level.get('🟢 Faible', type('', (), {'count': 0})).count,
            analysis.by_level.get('🟡 Modéré', type('', (), {'count': 0})).count,
            analysis.by_level.get('🟠 Élevé', type('', (), {'count': 0})).count,
            analysis.by_level.get('🔴 Critique', type('', (), {'count': 0})).count
        ]
        
        cat_labels = [s.category_name for s in analysis.by_category.values()]
        cat_counts = [s.count for s in analysis.by_category.values()]
        cat_colors = [s.color for s in analysis.by_category.values()]
        cat_gross = [round(s.avg_gross_score, 1) for s in analysis.by_category.values()]
        cat_residual = [round(s.avg_residual_score, 1) for s in analysis.by_category.values()]
        
        entity_names = list(analysis.by_entity.keys())
        entity_critical = [s.critical_count for s in analysis.by_entity.values()]
        entity_high = [s.high_count for s in analysis.by_entity.values()]
        entity_moderate = [s.moderate_count for s in analysis.by_entity.values()]
        entity_low = [s.low_count for s in analysis.by_entity.values()]
        entity_gross = [round(s.avg_gross_score, 1) for s in analysis.by_entity.values()]
        entity_residual = [round(s.avg_residual_score, 1) for s in analysis.by_entity.values()]
        
        m = analysis.mitigation
        
        return f'''
    <script>
        // === Global Data ===
        const allRisks = {risks_json};
        let filteredRisks = [...allRisks];
        let sortColumn = null;
        let sortDirection = 'asc';
        let charts = {{}};
        
        // === Theme Toggle ===
        function toggleTheme() {{
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            const newTheme = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            document.getElementById('theme-icon').textContent = newTheme === 'dark' ? '🌙' : '☀️';
            localStorage.setItem('theme', newTheme);
            updateChartColors();
        }}
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        document.getElementById('theme-icon').textContent = savedTheme === 'dark' ? '🌙' : '☀️';
        
        // === Chart Configuration ===
        Chart.defaults.color = '#9ca3af';
        Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';
        
        const chartColors = {{
            success: '#10b981',
            warning: '#f59e0b',
            orange: '#f97316',
            danger: '#ef4444',
            accent: '#00d4ff'
        }};
        
        function updateChartColors() {{
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            Chart.defaults.color = isDark ? '#9ca3af' : '#64748b';
            Chart.defaults.borderColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';
            Object.values(charts).forEach(chart => chart.update());
        }}
        
        // === Initialize Charts ===
        document.addEventListener('DOMContentLoaded', function() {{
            // Risk Level Doughnut Chart
            charts.riskLevel = new Chart(document.getElementById('riskLevelChart'), {{
                type: 'doughnut',
                data: {{
                    labels: ['Low', 'Moderate', 'High', 'Critical'],
                    datasets: [{{
                        data: {level_data},
                        backgroundColor: [chartColors.success, chartColors.warning, chartColors.orange, chartColors.danger],
                        borderWidth: 0,
                        hoverOffset: 8
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '65%',
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ padding: 16 }} }},
                        tooltip: {{
                            callbacks: {{
                                label: function(ctx) {{
                                    const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                                    const pct = ((ctx.raw / total) * 100).toFixed(1);
                                    return ctx.label + ': ' + ctx.raw + ' (' + pct + '%)';
                                }}
                            }}
                        }}
                    }},
                    animation: {{ animateRotate: true, animateScale: true }}
                }}
            }});
            
            // Category Bar Chart
            charts.category = new Chart(document.getElementById('categoryChart'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(cat_labels)},
                    datasets: [{{
                        label: 'Risk Count',
                        data: {cat_counts},
                        backgroundColor: {json.dumps(cat_colors)},
                        borderRadius: 6,
                        borderSkipped: false
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                title: function(ctx) {{ return ctx[0].label; }},
                                label: function(ctx) {{ return ctx.raw + ' risks'; }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{ beginAtZero: true, ticks: {{ stepSize: 5 }} }},
                        x: {{ grid: {{ display: false }} }}
                    }},
                    animation: {{ duration: 800, easing: 'easeOutQuart' }}
                }}
            }});
            
            // Entity Stacked Bar Chart
            charts.entity = new Chart(document.getElementById('entityChart'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(entity_names)},
                    datasets: [
                        {{ label: 'Critical', data: {entity_critical}, backgroundColor: chartColors.danger, borderRadius: 3 }},
                        {{ label: 'High', data: {entity_high}, backgroundColor: chartColors.orange, borderRadius: 3 }},
                        {{ label: 'Moderate', data: {entity_moderate}, backgroundColor: chartColors.warning, borderRadius: 3 }},
                        {{ label: 'Low', data: {entity_low}, backgroundColor: chartColors.success, borderRadius: 3 }}
                    ]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom' }} }},
                    scales: {{
                        x: {{ stacked: true }},
                        y: {{ stacked: true, grid: {{ display: false }} }}
                    }},
                    animation: {{ duration: 800 }}
                }}
            }});
            
            // Gross vs Residual Comparison
            charts.comparison = new Chart(document.getElementById('comparisonChart'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(entity_names)},
                    datasets: [
                        {{ label: 'Gross', data: {entity_gross}, backgroundColor: 'rgba(249,115,22,0.7)', borderRadius: 4 }},
                        {{ label: 'Residual', data: {entity_residual}, backgroundColor: 'rgba(16,185,129,0.7)', borderRadius: 4 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom' }} }},
                    scales: {{
                        y: {{ beginAtZero: true, max: 16 }},
                        x: {{ grid: {{ display: false }} }}
                    }},
                    animation: {{ duration: 800 }}
                }}
            }});
            
            // Mitigation Pie Chart
            charts.mitigation = new Chart(document.getElementById('mitigationChart'), {{
                type: 'pie',
                data: {{
                    labels: ['Reduced', 'Unchanged', 'Increased'],
                    datasets: [{{
                        data: [{m.improved if m else 0}, {m.unchanged if m else 0}, {m.worsened if m else 0}],
                        backgroundColor: [chartColors.success, '#6b7280', chartColors.danger],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom' }} }},
                    animation: {{ animateRotate: true }}
                }}
            }});
            
            // Category Radar Chart
            charts.categoryRadar = new Chart(document.getElementById('categoryRadarChart'), {{
                type: 'radar',
                data: {{
                    labels: {json.dumps([l[:12] for l in cat_labels])},
                    datasets: [
                        {{ 
                            label: 'Gross', 
                            data: {cat_gross}, 
                            backgroundColor: 'rgba(249,115,22,0.2)', 
                            borderColor: chartColors.orange, 
                            pointBackgroundColor: chartColors.orange,
                            pointRadius: 4
                        }},
                        {{ 
                            label: 'Residual', 
                            data: {cat_residual}, 
                            backgroundColor: 'rgba(16,185,129,0.2)', 
                            borderColor: chartColors.success, 
                            pointBackgroundColor: chartColors.success,
                            pointRadius: 4
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom' }} }},
                    scales: {{
                        r: {{ 
                            beginAtZero: true, 
                            max: 16,
                            ticks: {{ stepSize: 4 }}
                        }}
                    }}
                }}
            }});
            
            // Populate risk registry
            populateRegistry();
        }});
        
        // === Filter Functions ===
        function applyFilters() {{
            const entityFilter = document.getElementById('entity-filter').value;
            const levelFilter = document.getElementById('level-filter').value;
            const categoryFilter = document.getElementById('category-filter').value;
            const searchFilter = document.getElementById('search-filter').value.toLowerCase();
            
            filteredRisks = allRisks.filter(risk => {{
                if (entityFilter && risk.entity !== entityFilter) return false;
                if (levelFilter && risk.level_residual !== levelFilter) return false;
                if (categoryFilter && risk.category !== categoryFilter) return false;
                if (searchFilter) {{
                    const searchText = (risk.scenario + ' ' + risk.description + ' ' + risk.risk_id).toLowerCase();
                    if (!searchText.includes(searchFilter)) return false;
                }}
                return true;
            }});
            
            updateFilterChips();
            populateRegistry();
            document.getElementById('visible-count').textContent = filteredRisks.length;
        }}
        
        function updateFilterChips() {{
            const container = document.getElementById('active-filters');
            const chips = [];
            
            const entity = document.getElementById('entity-filter').value;
            const level = document.getElementById('level-filter').value;
            const category = document.getElementById('category-filter').value;
            
            if (entity) chips.push(createChip('Entity: ' + entity, 'entity-filter'));
            if (level) chips.push(createChip('Level: ' + level.replace(/[🔴🟠🟡🟢]/g, '').trim(), 'level-filter'));
            if (category) chips.push(createChip('Category: ' + category, 'category-filter'));
            
            container.innerHTML = chips.join('');
        }}
        
        function createChip(text, filterId) {{
            return '<span class="filter-chip">' + text + 
                   '<span class="filter-chip-remove" onclick="clearFilter(\\'' + filterId + '\\')">✕</span></span>';
        }}
        
        function clearFilter(filterId) {{
            document.getElementById(filterId).value = '';
            applyFilters();
        }}
        
        function resetFilters() {{
            document.getElementById('entity-filter').value = '';
            document.getElementById('level-filter').value = '';
            document.getElementById('category-filter').value = '';
            document.getElementById('search-filter').value = '';
            applyFilters();
        }}
        
        function filterByEntity(entity) {{
            document.getElementById('entity-filter').value = entity;
            applyFilters();
            document.getElementById('risk-table').scrollIntoView({{ behavior: 'smooth' }});
        }}
        
        function filterByLevel(level) {{
            document.getElementById('level-filter').value = level;
            applyFilters();
        }}
        
        function filterCritical() {{
            filterByLevel('🔴 Critique');
            document.getElementById('risk-table').scrollIntoView({{ behavior: 'smooth' }});
        }}
        
        function filterByMatrix(prob, impact, type) {{
            const filtered = allRisks.filter(r => 
                r['prob_' + type] === prob && r['impact_' + type] === impact
            );
            if (filtered.length > 0) {{
                filteredRisks = filtered;
                populateRegistry();
                document.getElementById('visible-count').textContent = filtered.length;
                document.getElementById('risk-table').scrollIntoView({{ behavior: 'smooth' }});
            }}
        }}
        
        // === Registry Functions ===
        function populateRegistry() {{
            const tbody = document.getElementById('registry-body');
            const search = document.getElementById('registry-search')?.value.toLowerCase() || '';
            
            let data = [...filteredRisks];
            
            // Apply registry search
            if (search) {{
                data = data.filter(r => 
                    (r.entity + r.risk_id + r.scenario).toLowerCase().includes(search)
                );
            }}
            
            // Apply sorting
            if (sortColumn) {{
                data.sort((a, b) => {{
                    let valA = a[sortColumn];
                    let valB = b[sortColumn];
                    if (typeof valA === 'number') {{
                        return sortDirection === 'asc' ? valA - valB : valB - valA;
                    }}
                    valA = String(valA).toLowerCase();
                    valB = String(valB).toLowerCase();
                    return sortDirection === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
                }});
            }}
            
            // Generate rows
            let html = '';
            data.forEach(risk => {{
                const level = risk.level_residual;
                let badgeClass = 'badge-low';
                if (level.includes('🔴')) badgeClass = 'badge-critical';
                else if (level.includes('🟠')) badgeClass = 'badge-high';
                else if (level.includes('🟡')) badgeClass = 'badge-moderate';
                
                const scenario = risk.scenario.length > 50 ? risk.scenario.substring(0, 50) + '...' : risk.scenario;
                const levelLabel = level.replace(/[🔴🟠🟡🟢]/g, '').trim();
                
                html += '<tr onclick="showRiskDetail(\\'' + risk.entity + '\\', \\'' + risk.risk_id + '\\')">' +
                    '<td class="entity">' + risk.entity + '</td>' +
                    '<td>' + risk.risk_id + '</td>' +
                    '<td>' + scenario + '</td>' +
                    '<td><span class="score-pill" style="background: rgba(249,115,22,0.2); color: #f97316;">' + risk.score_gross + '</span></td>' +
                    '<td><span class="score-pill" style="background: rgba(16,185,129,0.2); color: #10b981;">' + risk.score_residual + '</span></td>' +
                    '<td><span class="risk-badge ' + badgeClass + '">' + levelLabel + '</span></td>' +
                    '</tr>';
            }});
            
            tbody.innerHTML = html;
            document.getElementById('registry-status').textContent = 'Showing ' + data.length + ' of ' + allRisks.length + ' risks';
        }}
        
        function filterRegistry() {{
            populateRegistry();
        }}
        
        function sortRegistry(column) {{
            if (sortColumn === column) {{
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            }} else {{
                sortColumn = column;
                sortDirection = 'asc';
            }}
            populateRegistry();
        }}
        
        // === Modal Functions ===
        function showRiskDetail(entity, riskId) {{
            const risk = allRisks.find(r => r.entity === entity && r.risk_id === riskId);
            if (!risk) return;
            
            document.getElementById('modal-title').textContent = entity + ' — ' + riskId;
            document.getElementById('modal-gross-score').textContent = risk.score_gross;
            document.getElementById('modal-gross-details').textContent = 'P:' + risk.prob_gross + ' × I:' + risk.impact_gross;
            document.getElementById('modal-residual-score').textContent = risk.score_residual;
            document.getElementById('modal-residual-details').textContent = 'P:' + risk.prob_residual + ' × I:' + risk.impact_residual;
            document.getElementById('modal-scenario').textContent = risk.scenario || '-';
            document.getElementById('modal-description').textContent = risk.description || '-';
            document.getElementById('modal-factors').textContent = risk.aggravating_factors || '-';
            document.getElementById('modal-prevention').textContent = risk.prevention_measures || '-';
            document.getElementById('modal-actions').textContent = risk.corrective_actions || '-';
            
            document.getElementById('risk-modal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }}
        
        function closeModal(event) {{
            if (event && event.target !== document.getElementById('risk-modal')) return;
            document.getElementById('risk-modal').classList.remove('active');
            document.body.style.overflow = '';
        }}
        
        // Close on Escape
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') closeModal();
        }});
        
        // === Export Functions ===
        function exportToPDF() {{
            window.print();
        }}
        
        function exportToCSV() {{
            const headers = ['Entity', 'Risk ID', 'Scenario', 'Prob Gross', 'Impact Gross', 'Score Gross', 'Prob Residual', 'Impact Residual', 'Score Residual', 'Level'];
            const rows = filteredRisks.map(r => [
                r.entity, r.risk_id, '"' + r.scenario.replace(/"/g, '""') + '"',
                r.prob_gross, r.impact_gross, r.score_gross,
                r.prob_residual, r.impact_residual, r.score_residual,
                r.level_residual.replace(/[🔴🟠🟡🟢]/g, '').trim()
            ]);
            
            let csv = headers.join(',') + '\\n';
            rows.forEach(row => csv += row.join(',') + '\\n');
            
            const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'risk_registry_' + new Date().toISOString().slice(0,10) + '.csv';
            link.click();
        }}
        
        function printDashboard() {{
            window.print();
        }}
        
        // === Chart Type Toggle ===
        function toggleChartType(chartId) {{
            const chart = charts.riskLevel;
            chart.config.type = chart.config.type === 'doughnut' ? 'bar' : 'doughnut';
            chart.update();
        }}
    </script>'''
    
    def save(self, html: str, filepath: str) -> str:
        """Save HTML to file."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.info(f"Enhanced dashboard saved: {filepath}")
        return str(path)


def generate_enhanced_dashboard(
    df: pd.DataFrame,
    analysis: RiskAnalysis,
    output_path: str,
    config: Dict = None
) -> str:
    """
    Convenience function to generate and save enhanced dashboard.
    
    Args:
        df: DataFrame with risk data
        analysis: RiskAnalysis object
        output_path: Output file path
        config: Optional configuration dict
        
    Returns:
        Path to saved file
    """
    generator = EnhancedDashboardGenerator(config=config)
    html = generator.generate(df, analysis)
    return generator.save(html, output_path)


if __name__ == "__main__":
    # Test enhanced dashboard generation
    import sys
    sys.path.insert(0, '.')
    from data_loader import load_risk_data
    from analyzer import analyze_risks
    import os
    
    test_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    df, _ = load_risk_data(test_dir)
    analysis = analyze_risks(df)
    
    output = os.path.join(test_dir, 'output', 'risk_dashboard_enhanced.html')
    generate_enhanced_dashboard(df, analysis, output)
    
    print(f"\nEnhanced dashboard generated: {output}")
