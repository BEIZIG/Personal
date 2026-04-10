"""
Data Loader module for Risk Cartography Analysis.

Handles:
- Loading Excel files based on JSON configuration
- Data cleaning and transformation
- Entity extraction from filenames
- Combining multiple entity datasets

Supports both:
- JSON configuration (AnalysisConfiguration) - recommended
- Legacy directory scanning mode
"""

import pandas as pd
import glob
import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LoadResult:
    """Result of loading a single Excel file."""
    entity_name: str
    filepath: str
    dataframe: Optional[pd.DataFrame]
    row_count: int
    columns: List[str]
    sheet_used: str
    success: bool
    error_message: Optional[str] = None


class RiskDataLoader:
    """
    Loads and transforms risk cartography data from Excel files.
    
    Supports two modes:
    
    1. JSON Configuration (recommended):
        from config_loader import load_config
        config = load_config('analysis_config.json')
        loader = RiskDataLoader.from_config(config)
        df = loader.load_all()
    
    2. Directory scanning (legacy):
        loader = RiskDataLoader()
        df = loader.load_directory('/path/to/files')
    """
    
    # Default column mapping for legacy mode
    DEFAULT_COLUMN_MAPPING = {
        0: 'risk_id',
        1: 'scenario',
        2: 'description',
        3: 'aggravating_factors',
        4: 'prob_gross',
        5: 'impact_gross',
        6: 'score_gross',
        7: 'level_gross',
        8: 'prevention_measures',
        9: 'prob_residual',
        10: 'impact_residual',
        11: 'score_residual',
        12: 'level_residual',
        13: 'corrective_actions'
    }
    
    DEFAULT_NUMERIC_FIELDS = [
        'prob_gross', 'impact_gross', 'score_gross',
        'prob_residual', 'impact_residual', 'score_residual'
    ]
    
    DEFAULT_SKIP_HEADER_VALUES = ['N°', 'N']
    
    def __init__(self):
        """Initialize the data loader."""
        self.load_results: List[LoadResult] = []
        self.config = None
        self._base_directory: Optional[Path] = None
        self._files_config: List = []
        self._column_mapping: Dict[int, str] = self.DEFAULT_COLUMN_MAPPING.copy()
        self._numeric_fields: List[str] = self.DEFAULT_NUMERIC_FIELDS.copy()
        self._skip_header_values: List[str] = self.DEFAULT_SKIP_HEADER_VALUES.copy()
    
    @classmethod
    def from_config(cls, config) -> 'RiskDataLoader':
        """
        Create loader from JSON configuration.
        
        Args:
            config: AnalysisConfiguration object from config_loader
            
        Returns:
            Configured RiskDataLoader
        """
        loader = cls()
        loader.config = config
        
        # Set base directory relative to configuration folder or absolute
        base_dir = config.input.base_directory
        if not os.path.isabs(base_dir):
            # Relative to configuration directory (where analysis_config.json lives)
            lib_dir = Path(__file__).parent
            config_dir = lib_dir.parent / "configuration"
            base_dir = (config_dir / base_dir).resolve()
        loader._base_directory = Path(base_dir)
        
        # Get enabled files from config
        loader._files_config = config.get_enabled_files()
        
        # Get column mapping from config
        loader._column_mapping = config.get_column_mapping_int_keys()
        loader._numeric_fields = config.columns.numeric_fields
        loader._skip_header_values = config.columns.skip_header_values
        
        return loader
    
    def load_all(self) -> pd.DataFrame:
        """
        Load all configured files.
        
        Returns:
            Combined DataFrame with all entities
        """
        if not self._files_config:
            logger.warning("No files configured to load")
            return pd.DataFrame()
        
        logger.info(f"Loading {len(self._files_config)} files from {self._base_directory}")
        
        self.load_results = []
        all_dataframes = []
        
        for file_config in self._files_config:
            filepath = self._base_directory / file_config.filename
            
            result = self._load_single_file(
                filepath=str(filepath),
                entity_name=file_config.entity_name,
                sheet_name=file_config.sheet_name,
                skip_rows=file_config.skip_rows,
                column_mapping=file_config.column_mapping  # Per-file override
            )
            
            self.load_results.append(result)
            
            if result.success:
                logger.info(f"  ✓ {result.entity_name}: {result.row_count} risks loaded")
                all_dataframes.append(result.dataframe)
            else:
                logger.warning(f"  ✗ {result.entity_name}: {result.error_message}")
        
        if all_dataframes:
            combined = pd.concat(all_dataframes, ignore_index=True)
            logger.info(f"\nTotal: {len(combined)} risk records from {len(all_dataframes)} entities")
            return combined
        
        logger.warning("No data loaded from any file")
        return pd.DataFrame()
    
    def _load_single_file(
        self,
        filepath: str,
        entity_name: str,
        sheet_name: str,
        skip_rows: int,
        column_mapping: Optional[Dict] = None
    ) -> LoadResult:
        """
        Load a single Excel file with specified parameters.
        
        Args:
            filepath: Full path to Excel file
            entity_name: Name for this entity
            sheet_name: Sheet to read
            skip_rows: Rows to skip
            column_mapping: Optional per-file column overrides
            
        Returns:
            LoadResult with data or error
        """
        try:
            if not os.path.exists(filepath):
                return LoadResult(
                    entity_name=entity_name,
                    filepath=filepath,
                    dataframe=None,
                    row_count=0,
                    columns=[],
                    sheet_used='',
                    success=False,
                    error_message=f"File not found: {filepath}"
                )
            
            xl = pd.ExcelFile(filepath)
            actual_sheet = self._find_sheet(xl, sheet_name)
            
            if actual_sheet is None:
                return LoadResult(
                    entity_name=entity_name,
                    filepath=filepath,
                    dataframe=None,
                    row_count=0,
                    columns=[],
                    sheet_used='',
                    success=False,
                    error_message=f"Sheet '{sheet_name}' not found"
                )
            
            # Load data
            df = pd.read_excel(
                filepath,
                sheet_name=actual_sheet,
                header=None,
                skiprows=skip_rows
            )
            
            # Use per-file or global column mapping
            mapping = column_mapping if column_mapping else self._column_mapping
            if isinstance(mapping, dict) and mapping:
                # Convert string keys to int if needed
                if all(isinstance(k, str) for k in mapping.keys()):
                    mapping = {int(k): v for k, v in mapping.items()}
            else:
                mapping = self._column_mapping
            
            # Clean and transform
            df = self._clean_dataframe(df, entity_name, mapping)
            
            return LoadResult(
                entity_name=entity_name,
                filepath=filepath,
                dataframe=df,
                row_count=len(df),
                columns=list(df.columns),
                sheet_used=actual_sheet,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
            return LoadResult(
                entity_name=entity_name,
                filepath=filepath,
                dataframe=None,
                row_count=0,
                columns=[],
                sheet_used='',
                success=False,
                error_message=str(e)
            )
    
    def _find_sheet(self, excel_file: pd.ExcelFile, target_sheet: str) -> Optional[str]:
        """Find sheet in Excel file (case-insensitive)."""
        available_sheets = excel_file.sheet_names
        target = target_sheet.lower()
        
        for sheet in available_sheets:
            if sheet.lower() == target:
                return sheet
        
        # Fallback to first sheet
        if available_sheets:
            logger.warning(f"Sheet '{target_sheet}' not found, using '{available_sheets[0]}'")
            return available_sheets[0]
        
        return None
    
    def _clean_dataframe(
        self, 
        df: pd.DataFrame, 
        entity_name: str,
        column_mapping: Dict[int, str]
    ) -> pd.DataFrame:
        """
        Clean and transform the loaded DataFrame.
        
        Args:
            df: Raw DataFrame from Excel
            entity_name: Name of the entity
            column_mapping: Column index to name mapping
            
        Returns:
            Cleaned DataFrame
        """
        # Rename columns using mapping
        df = df.rename(columns=column_mapping)
        
        # Keep only mapped columns that exist
        valid_columns = [col for col in column_mapping.values() if col in df.columns]
        df = df[valid_columns].copy()
        
        # Remove rows with missing risk_id
        if 'risk_id' in df.columns:
            df = df[df['risk_id'].notna()]
            
            # Remove header rows that got included
            for header_val in self._skip_header_values:
                df = df[df['risk_id'] != header_val]
        
        # Add entity identifier
        df['entity'] = entity_name
        
        # Extract category from risk_id (first letter)
        if 'risk_id' in df.columns:
            df['category'] = df['risk_id'].astype(str).str.extract(r'^([A-Z])', expand=False)
        
        # Convert numeric columns
        for col in self._numeric_fields:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    # =========================================================================
    # LEGACY SUPPORT: Directory scanning mode
    # =========================================================================
    
    def load_directory(
        self, 
        directory: str,
        sheet_name: str = "All",
        skip_rows: int = 3,
        file_pattern: str = "*.xlsx",
        filename_prefix: str = "carto_des_risques_"
    ) -> pd.DataFrame:
        """
        Load all Excel files from a directory (legacy mode).
        
        Args:
            directory: Path to directory containing Excel files
            sheet_name: Sheet to read from each file
            skip_rows: Rows to skip in each file
            file_pattern: Glob pattern for files
            filename_prefix: Prefix to remove from filename for entity name
            
        Returns:
            Combined DataFrame with all entities
        """
        # Find files
        pattern = os.path.join(directory, file_pattern)
        files = sorted(glob.glob(pattern))
        
        logger.info(f"Found {len(files)} Excel files in {directory}")
        
        self.load_results = []
        all_dataframes = []
        
        for filepath in files:
            filename = os.path.basename(filepath)
            entity_name = filename.replace(filename_prefix, '').replace('.xlsx', '').replace('.xls', '')
            
            result = self._load_single_file(
                filepath=filepath,
                entity_name=entity_name,
                sheet_name=sheet_name,
                skip_rows=skip_rows
            )
            
            self.load_results.append(result)
            
            if result.success:
                logger.info(f"  ✓ {result.entity_name}: {result.row_count} risks loaded")
                all_dataframes.append(result.dataframe)
            else:
                logger.warning(f"  ✗ {result.entity_name}: {result.error_message}")
        
        if all_dataframes:
            combined = pd.concat(all_dataframes, ignore_index=True)
            logger.info(f"\nTotal: {len(combined)} risk records from {len(all_dataframes)} entities")
            return combined
        
        logger.warning("No data loaded from any file")
        return pd.DataFrame()
    
    def get_load_summary(self) -> Dict:
        """
        Get summary of loading results.
        
        Returns:
            Dictionary with loading statistics
        """
        successful = [r for r in self.load_results if r.success]
        failed = [r for r in self.load_results if not r.success]
        
        return {
            'total_files': len(self.load_results),
            'successful': len(successful),
            'failed': len(failed),
            'total_rows': sum(r.row_count for r in successful),
            'entities': [r.entity_name for r in successful],
            'errors': {r.entity_name: r.error_message for r in failed}
        }


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def load_risk_data_from_config(config) -> Tuple[pd.DataFrame, Dict]:
    """
    Load risk data using JSON configuration.
    
    Args:
        config: AnalysisConfiguration object from config_loader
        
    Returns:
        Tuple of (DataFrame, load_summary)
    """
    loader = RiskDataLoader.from_config(config)
    df = loader.load_all()
    summary = loader.get_load_summary()
    return df, summary


def load_risk_data(directory: str, **kwargs) -> Tuple[pd.DataFrame, Dict]:
    """
    Load risk data from directory (legacy mode).
    
    Args:
        directory: Path to directory with Excel files
        **kwargs: Additional options (sheet_name, skip_rows, etc.)
        
    Returns:
        Tuple of (DataFrame, load_summary)
    """
    loader = RiskDataLoader()
    df = loader.load_directory(directory, **kwargs)
    summary = loader.get_load_summary()
    return df, summary


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Test with JSON config if available
    config_path = Path(__file__).parent / "analysis_config.json"
    
    if config_path.exists():
        print("=== Loading with JSON Configuration ===")
        from config_loader import load_config
        
        config = load_config(str(config_path))
        df, summary = load_risk_data_from_config(config)
        
        print(f"\nLoad Summary: {summary}")
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
    else:
        print("=== Loading with Directory Scan (Legacy) ===")
        test_dir = Path(__file__).parent.parent
        df, summary = load_risk_data(str(test_dir))
        
        print(f"\nLoad Summary: {summary}")
        print(f"DataFrame shape: {df.shape}")
