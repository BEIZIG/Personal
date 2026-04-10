#!/usr/bin/env python3
"""
Risk Cartography Analysis - Main Entry Point

This is the main script that orchestrates the entire analysis pipeline:
1. Load configuration (JSON or legacy mode)
2. Load Excel files
3. Perform risk analysis
4. Generate HTML dashboard
5. Export PowerBI-compatible files

Usage:
    python main.py                          # Use analysis_config.json
    python main.py --config my_config.json  # Use custom config
    python main.py /path/to/excel/dir       # Legacy: scan directory
    python main.py --init                   # Create default config file
    python main.py --help                   # Show help

Extensibility:
- Edit analysis_config.json to add/modify files, columns, levels
- Each module can be imported and used independently
- Supports per-file configuration overrides
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add lib directory to path for imports
lib_dir = Path(__file__).parent
sys.path.insert(0, str(lib_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Risk Cartography Analysis - Generate dashboards and reports from Excel files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    # Using JSON configuration (recommended):
    python main.py                              # Use analysis_config.json
    python main.py --config custom_config.json  # Use custom config file
    
    # Legacy mode (directory scanning):
    python main.py /path/to/excel/files
    python main.py /path/to/files --sheet "Data" --skip-rows 2
    
    # Utilities:
    python main.py --init                       # Create default config from Excel files
    python main.py --init --input /path/to/files
        '''
    )
    
    parser.add_argument(
        'input_dir',
        nargs='?',
        default=None,
        help='Directory containing Excel files (legacy mode)'
    )
    
    parser.add_argument(
        '-c', '--config',
        default=None,
        help='Path to JSON configuration file (default: analysis_config.json)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output directory (default: from config or lib/)'
    )
    
    parser.add_argument(
        '-s', '--sheet',
        default='All',
        help='Sheet name for legacy mode (default: All)'
    )
    
    parser.add_argument(
        '--skip-rows',
        type=int,
        default=3,
        help='Rows to skip for legacy mode (default: 3)'
    )
    
    parser.add_argument(
        '--no-dashboard',
        action='store_true',
        help='Skip HTML dashboard generation'
    )
    
    parser.add_argument(
        '--no-exports',
        action='store_true',
        help='Skip PowerBI export files'
    )
    
    parser.add_argument(
        '--init',
        action='store_true',
        help='Create default analysis_config.json from existing Excel files'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def print_banner():
    """Print application banner."""
    print()
    print("=" * 70)
    print("   🛡️  RISK CARTOGRAPHY ANALYSIS")
    print("   Corruption Risk Dashboard Generator")
    print("=" * 70)
    print()


def print_summary(analysis):
    """Print analysis summary to console."""
    s = analysis.summary
    
    print("\n" + "-" * 50)
    print("📊 ANALYSIS SUMMARY")
    print("-" * 50)
    print(f"   Total Risks Analyzed:    {s.total_risks}")
    print(f"   Total Entities:          {s.total_entities}")
    print(f"   Average Gross Score:     {s.avg_gross_score:.2f}")
    print(f"   Average Residual Score:  {s.avg_residual_score:.2f}")
    print(f"   Risk Reduction:          {s.risk_reduction_pct:+.1f}%")
    
    print("\n📈 Risk Level Distribution:")
    for level_key, stats in analysis.by_level.items():
        bar = "█" * int(stats.percentage / 5) + "░" * (20 - int(stats.percentage / 5))
        print(f"   {level_key}: {stats.count:3d} ({stats.percentage:5.1f}%) {bar}")
    
    if analysis.mitigation:
        m = analysis.mitigation
        print(f"\n🔧 Mitigation Status:")
        print(f"   Improved:  {m.improved} ({m.improvement_rate:.1f}%)")
        print(f"   Unchanged: {m.unchanged}")
        print(f"   Worsened:  {m.worsened}")


def run_init_mode(args):
    """Create default configuration file from Excel files."""
    from config_loader import create_default_config
    
    input_dir = args.input_dir or str(lib_dir.parent)
    config_dir = lib_dir.parent / "configuration"
    config_dir.mkdir(parents=True, exist_ok=True)
    output_path = config_dir / "analysis_config.json"
    
    logger.info(f"Scanning for Excel files in: {input_dir}")
    create_default_config(str(output_path), input_dir)
    
    print(f"\n✓ Created configuration file: {output_path}")
    print(f"\nEdit this file to:")
    print("  - Enable/disable specific files")
    print("  - Customize sheet names per file")
    print("  - Modify column mappings")
    print("  - Add new risk categories or levels")
    
    return 0


def run_with_config(args, config):
    """Run analysis using JSON configuration."""
    from data_loader import RiskDataLoader
    from analyzer import RiskAnalyzer
    from html_generator import EnhancedDashboardGenerator
    from exporters import DataExporter
    
    # Determine output directory: CLI arg > config > default (output/)
    if args.output:
        output_dir = Path(args.output).resolve()
    elif config.output.directory:
        # Resolve relative to config file location (configuration folder)
        config_dir = lib_dir.parent / "configuration"
        output_dir = (config_dir / config.output.directory).resolve()
    else:
        output_dir = lib_dir.parent / "output"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # =========================================================================
    # STEP 1: Load Data
    # =========================================================================
    logger.info("\n📂 STEP 1: Loading Excel files from configuration...")
    
    loader = RiskDataLoader.from_config(config)
    df = loader.load_all()
    
    if df.empty:
        logger.error("No data loaded. Please check your configuration and Excel files.")
        return 1
    
    load_summary = loader.get_load_summary()
    logger.info(f"✓ Loaded {load_summary['total_rows']} records from {load_summary['successful']} files")
    
    if load_summary['failed'] > 0:
        logger.warning(f"⚠ {load_summary['failed']} files failed to load")
        for entity, error in load_summary['errors'].items():
            logger.warning(f"  - {entity}: {error}")
    
    # =========================================================================
    # STEP 2: Analyze Data
    # =========================================================================
    logger.info("\n📊 STEP 2: Analyzing risk data...")
    
    analyzer = RiskAnalyzer(config={
        'top_risks_count': config.analysis.top_risks_count
    })
    analysis = analyzer.analyze(df)
    
    print_summary(analysis)
    
    # =========================================================================
    # STEP 3: Generate Dashboard
    # =========================================================================
    if not args.no_dashboard:
        logger.info("\n🎨 STEP 3: Generating enhanced interactive dashboard...")
        
        generator = EnhancedDashboardGenerator(title=config.dashboard.title)
        html = generator.generate(df, analysis)
        
        dashboard_path = output_dir / config.output.dashboard_filename
        generator.save(html, str(dashboard_path))
        
        logger.info(f"✓ Dashboard: {dashboard_path}")
    
    # =========================================================================
    # STEP 4: Export PowerBI Files
    # =========================================================================
    if not args.no_exports:
        logger.info("\n📁 STEP 4: Exporting PowerBI files...")
        
        exporter = DataExporter(str(output_dir))
        exports = exporter.export_all(df, analysis)
        
        for name, path in exports.items():
            logger.info(f"✓ {name}: {Path(path).name}")
    
    return 0


def run_legacy_mode(args):
    """Run analysis using directory scanning (legacy mode)."""
    from data_loader import RiskDataLoader
    from analyzer import RiskAnalyzer
    from html_generator import EnhancedDashboardGenerator
    from exporters import DataExporter
    
    # Determine directories
    input_dir = Path(args.input_dir).resolve() if args.input_dir else lib_dir.parent.resolve()
    output_dir = Path(args.output).resolve() if args.output else lib_dir.resolve()
    
    logger.info(f"Input directory:  {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    
    # Verify input directory exists
    if not input_dir.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        return 1
    
    # Create output directory if needed
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # =========================================================================
    # STEP 1: Load Data
    # =========================================================================
    logger.info("\n📂 STEP 1: Loading Excel files (legacy mode)...")
    
    loader = RiskDataLoader()
    df = loader.load_directory(
        str(input_dir),
        sheet_name=args.sheet,
        skip_rows=args.skip_rows
    )
    
    if df.empty:
        logger.error("No data loaded. Please check your Excel files.")
        return 1
    
    load_summary = loader.get_load_summary()
    logger.info(f"✓ Loaded {load_summary['total_rows']} records from {load_summary['successful']} files")
    
    # =========================================================================
    # STEP 2: Analyze Data
    # =========================================================================
    logger.info("\n📊 STEP 2: Analyzing risk data...")
    
    analyzer = RiskAnalyzer()
    analysis = analyzer.analyze(df)
    
    print_summary(analysis)
    
    # =========================================================================
    # STEP 3: Generate Dashboard
    # =========================================================================
    if not args.no_dashboard:
        logger.info("\n🎨 STEP 3: Generating enhanced interactive dashboard...")
        
        generator = EnhancedDashboardGenerator()
        html = generator.generate(df, analysis)
        
        dashboard_path = output_dir / "risk_dashboard.html"
        generator.save(html, str(dashboard_path))
        
        logger.info(f"✓ Dashboard: {dashboard_path}")
    
    # =========================================================================
    # STEP 4: Export PowerBI Files
    # =========================================================================
    if not args.no_exports:
        logger.info("\n📁 STEP 4: Exporting PowerBI files...")
        
        exporter = DataExporter(str(output_dir))
        exports = exporter.export_all(df, analysis)
        
        for name, path in exports.items():
            logger.info(f"✓ {name}: {Path(path).name}")
    
    return 0


def main():
    """Main execution function."""
    args = parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print_banner()
    
    # Handle --init mode
    if args.init:
        return run_init_mode(args)
    
    # Determine mode: config-based or legacy
    config_path = args.config
    
    # If no config specified, look for default in configuration folder
    if config_path is None and args.input_dir is None:
        default_config = lib_dir.parent / "configuration" / "analysis_config.json"
        if default_config.exists():
            config_path = str(default_config)
            logger.info(f"Using configuration: {config_path}")
    
    # Run with appropriate mode
    if config_path:
        # Config-based mode
        from config_loader import load_config
        
        try:
            config = load_config(config_path)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            logger.info("Run 'python main.py --init' to create a default config file")
            return 1
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return 1
        
        result = run_with_config(args, config)
    else:
        # Legacy directory mode
        logger.info("Running in legacy mode (directory scanning)")
        result = run_legacy_mode(args)
    
    # =========================================================================
    # COMPLETE
    # =========================================================================
    if result == 0:
        print("\n" + "=" * 70)
        print("   ✅ ANALYSIS COMPLETE")
        print("=" * 70)
        print(f"\n   Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    return result


if __name__ == "__main__":
    sys.exit(main())
