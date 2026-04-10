"""
Exporters module for Risk Cartography Analysis.

Handles:
- CSV export for PowerBI
- JSON export for analysis results
- Excel export (optional)
"""

import pandas as pd
import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass

# Handle both package and direct imports
try:
    from .analyzer import RiskAnalysis
except ImportError:
    from analyzer import RiskAnalysis

logger = logging.getLogger(__name__)


# Default output filenames
@dataclass
class DefaultOutputFilenames:
    """Default filenames for exports."""
    risk_data_csv: str = "powerbi_risk_data.csv"
    entity_summary_csv: str = "powerbi_entity_summary.csv"
    category_summary_csv: str = "powerbi_category_summary.csv"
    risk_matrix_csv: str = "powerbi_risk_matrix.csv"
    analysis_json: str = "powerbi_analysis.json"


DEFAULT_OUTPUT_FILENAMES = DefaultOutputFilenames()


class DataExporter:
    """
    Exports analysis results to various formats.
    
    Usage:
        exporter = DataExporter(output_dir='/path/to/output')
        exporter.export_all(df, analysis)
    """
    
    def __init__(self, output_dir: str, config: Optional[Dict] = None):
        """
        Initialize exporter.
        
        Args:
            output_dir: Directory for output files
            config: Optional configuration overrides
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config = config or {}
        self.exported_files = []
    
    def export_risk_data_csv(
        self, 
        df: pd.DataFrame, 
        filename: Optional[str] = None
    ) -> str:
        """
        Export raw risk data to CSV.
        
        Args:
            df: DataFrame with risk data
            filename: Output filename (default from config)
            
        Returns:
            Path to exported file
        """
        filename = filename or DEFAULT_OUTPUT_FILENAMES.risk_data_csv
        filepath = self.output_dir / filename
        
        # Clean up level columns for PowerBI
        export_df = df.copy()
        
        if 'level_gross' in export_df.columns:
            export_df['level_gross_clean'] = export_df['level_gross'].str.replace(
                r'^[^\s]+\s', '', regex=True
            )
        
        if 'level_residual' in export_df.columns:
            export_df['level_residual_clean'] = export_df['level_residual'].str.replace(
                r'^[^\s]+\s', '', regex=True
            )
        
        export_df.to_csv(filepath, index=False, encoding='utf-8-sig')
        self.exported_files.append(str(filepath))
        logger.info(f"Exported risk data: {filepath}")
        
        return str(filepath)
    
    def export_entity_summary_csv(
        self, 
        analysis: RiskAnalysis, 
        filename: Optional[str] = None
    ) -> str:
        """
        Export entity summary to CSV.
        
        Args:
            analysis: RiskAnalysis object
            filename: Output filename
            
        Returns:
            Path to exported file
        """
        filename = filename or DEFAULT_OUTPUT_FILENAMES.entity_summary_csv
        filepath = self.output_dir / filename
        
        # Convert entity stats to DataFrame
        data = []
        for entity_name, stats in analysis.by_entity.items():
            data.append({
                'entity': entity_name,
                'total_risks': stats.total_risks,
                'avg_gross_score': stats.avg_gross_score,
                'avg_residual_score': stats.avg_residual_score,
                'critical_count': stats.critical_count,
                'high_count': stats.high_count,
                'moderate_count': stats.moderate_count,
                'low_count': stats.low_count,
                'risk_reduction_pct': stats.risk_reduction_pct
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        self.exported_files.append(str(filepath))
        logger.info(f"Exported entity summary: {filepath}")
        
        return str(filepath)
    
    def export_category_summary_csv(
        self, 
        analysis: RiskAnalysis, 
        filename: Optional[str] = None
    ) -> str:
        """
        Export category summary to CSV.
        
        Args:
            analysis: RiskAnalysis object
            filename: Output filename
            
        Returns:
            Path to exported file
        """
        filename = filename or DEFAULT_OUTPUT_FILENAMES.category_summary_csv
        filepath = self.output_dir / filename
        
        # Convert category stats to DataFrame
        data = []
        for cat_code, stats in analysis.by_category.items():
            data.append({
                'category_code': cat_code,
                'category_name': stats.category_name,
                'color': stats.color,
                'count': stats.count,
                'avg_gross_score': stats.avg_gross_score,
                'avg_residual_score': stats.avg_residual_score
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        self.exported_files.append(str(filepath))
        logger.info(f"Exported category summary: {filepath}")
        
        return str(filepath)
    
    def export_analysis_json(
        self, 
        analysis: RiskAnalysis, 
        filename: Optional[str] = None
    ) -> str:
        """
        Export full analysis to JSON.
        
        Args:
            analysis: RiskAnalysis object
            filename: Output filename
            
        Returns:
            Path to exported file
        """
        filename = filename or DEFAULT_OUTPUT_FILENAMES.analysis_json
        filepath = self.output_dir / filename
        
        analysis_dict = analysis.to_dict()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis_dict, f, indent=2, ensure_ascii=False, default=str)
        
        self.exported_files.append(str(filepath))
        logger.info(f"Exported analysis JSON: {filepath}")
        
        return str(filepath)
    
    def export_risk_matrix_csv(
        self, 
        analysis: RiskAnalysis, 
        filename: str = 'powerbi_risk_matrix.csv'
    ) -> str:
        """
        Export risk matrix to CSV for PowerBI heatmap.
        
        Args:
            analysis: RiskAnalysis object
            filename: Output filename
            
        Returns:
            Path to exported file
        """
        filepath = self.output_dir / filename
        
        data = []
        for key, count in analysis.risk_matrix_residual.items():
            prob, impact = key.split('x')
            score = int(prob) * int(impact)
            
            # Determine level
            if score <= 2:
                level = 'Low'
            elif score <= 6:
                level = 'Moderate'
            elif score <= 9:
                level = 'High'
            else:
                level = 'Critical'
            
            data.append({
                'probability': int(prob),
                'impact': int(impact),
                'score': score,
                'level': level,
                'count_residual': count,
                'count_gross': analysis.risk_matrix_gross.get(key, 0)
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        self.exported_files.append(str(filepath))
        logger.info(f"Exported risk matrix: {filepath}")
        
        return str(filepath)
    
    def export_all(
        self, 
        df: pd.DataFrame, 
        analysis: RiskAnalysis,
        include_matrix: bool = True
    ) -> Dict[str, str]:
        """
        Export all data files.
        
        Args:
            df: DataFrame with risk data
            analysis: RiskAnalysis object
            include_matrix: Whether to export risk matrix CSV
            
        Returns:
            Dictionary of exported file paths
        """
        exports = {
            'risk_data': self.export_risk_data_csv(df),
            'entity_summary': self.export_entity_summary_csv(analysis),
            'category_summary': self.export_category_summary_csv(analysis),
            'analysis_json': self.export_analysis_json(analysis)
        }
        
        if include_matrix:
            exports['risk_matrix'] = self.export_risk_matrix_csv(analysis)
        
        logger.info(f"\nExported {len(exports)} files to {self.output_dir}")
        
        return exports
    
    def get_exported_files(self) -> list:
        """Get list of all exported file paths."""
        return self.exported_files.copy()


def export_to_powerbi(
    df: pd.DataFrame, 
    analysis: RiskAnalysis, 
    output_dir: str
) -> Dict[str, str]:
    """
    Convenience function to export all PowerBI files.
    
    Args:
        df: DataFrame with risk data
        analysis: RiskAnalysis object
        output_dir: Output directory
        
    Returns:
        Dictionary of exported file paths
    """
    exporter = DataExporter(output_dir)
    return exporter.export_all(df, analysis)


if __name__ == "__main__":
    # Test exports
    import sys
    sys.path.insert(0, '.')
    from data_loader import load_risk_data
    from analyzer import analyze_risks
    import os
    
    test_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lib_dir = os.path.join(test_dir, 'lib')
    
    df, _ = load_risk_data(test_dir)
    analysis = analyze_risks(df)
    
    exports = export_to_powerbi(df, analysis, lib_dir)
    
    print("\n=== EXPORTED FILES ===")
    for name, path in exports.items():
        print(f"  {name}: {path}")
