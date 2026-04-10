# Risk Cartography Analysis

**Interactive dashboard for corruption risk analysis**

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Place Excel files in this folder
#    (carto_des_risques_*.xlsx)

# 3. Run analysis
python3 lib/main.py

# 4. Open output/risk_dashboard.html in browser
```

## Input Files

Place your Excel files here:
```
risk_cartography/
├── carto_des_risques_Entity_A.xlsx   ← YOUR FILES
├── carto_des_risques_Entity_B.xlsx
├── lib/
└── ...
```

**Expected format:**
- Sheet name: `All`
- Skip first 3 rows (headers)
- Columns: Risk ID, Scenario, Description, Factors, P/I/Score (Gross), Measures, P/I/Score (Residual), Actions

## Output

| File | Description |
|------|-------------|
| `output/risk_dashboard.html` | Interactive dashboard |
| `output/powerbi_*.csv` | PowerBI exports |

## Documentation

- [INSTALL.md](INSTALL.md) - Installation guide
- [RUNBOOK.md](RUNBOOK.md) - Operations & configuration

## Requirements

- Python 3.8+
- pandas
- openpyxl
