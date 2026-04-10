# Risk Cartography Analysis - Runbook

## Quick Reference

| Action | Command |
|--------|---------|
| Run analysis | `python3 lib/main.py` |
| Show help | `python3 lib/main.py --help` |
| Use custom config | `python3 lib/main.py --config my_config.json` |
| Skip dashboard | `python3 lib/main.py --no-dashboard` |
| Skip exports | `python3 lib/main.py --no-exports` |

---

## Standard Operation

### 1. Place Input Files

Copy your Excel files to the root folder:
```
risk_cartography/
├── carto_des_risques_Entity_ABC1.xlsx   ← Your files
├── carto_des_risques_Entity_ABC2.xlsx
└── ...
```

### 2. Update Configuration (if needed)

Edit `configuration/analysis_config.json` to list your files:

```json
"files": [
  {
    "filename": "carto_des_risques_Entity_ABC1.xlsx",
    "entity_name": "Entity_ABC1",
    "enabled": true,
    "sheet_name": "All",
    "skip_rows": 3
  },
  {
    "filename": "your_new_file.xlsx",
    "entity_name": "Your Entity Name",
    "enabled": true,
    "sheet_name": "All",
    "skip_rows": 3
  }
]
```

### 3. Run Analysis

```bash
cd /path/to/risk_cartography
python3 lib/main.py
```

### 4. View Results

Open `output/risk_dashboard.html` in your browser.

---

## Output Files

After running, the `output/` folder contains:

| File | Description |
|------|-------------|
| `risk_dashboard.html` | Interactive HTML dashboard |
| `powerbi_risk_data.csv` | All risks (for PowerBI) |
| `powerbi_entity_summary.csv` | Summary by entity |
| `powerbi_category_summary.csv` | Summary by category |
| `powerbi_risk_matrix.csv` | Probability × Impact matrix |
| `powerbi_analysis.json` | Full analysis in JSON |

---

## Configuration Reference

### Adding New Entities

1. Add Excel file to root folder
2. Add entry to `configuration/analysis_config.json`:

```json
{
  "filename": "carto_des_risques_NewEntity.xlsx",
  "entity_name": "New Entity",
  "enabled": true,
  "sheet_name": "All",
  "skip_rows": 3
}
```

### Disabling an Entity

Set `"enabled": false` to temporarily exclude:

```json
{
  "filename": "carto_des_risques_Entity_ABC1.xlsx",
  "enabled": false  // Will be skipped
}
```

### Custom Sheet Name

If your data is in a different sheet:

```json
{
  "filename": "my_file.xlsx",
  "sheet_name": "Risk Data",  // Custom sheet name
  "skip_rows": 2              // Adjust header rows
}
```

---

## Column Mapping

If your Excel columns are in different positions, update the mapping:

```json
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
  }
}
```

**Required columns**: risk_id, prob_gross, impact_gross, score_gross, level_gross, prob_residual, impact_residual, score_residual, level_residual

---

## Dashboard Features

### Interactive Filters
- Filter by Entity, Risk Level, Category
- Full-text search across scenarios

### Click Interactions
- KPI cards → Filter by level
- Risk matrix cells → Filter by P×I
- Table rows → Show risk details

### Export Options
- **Export PDF**: Print to PDF
- **Export CSV**: Download filtered data
- **Theme Toggle**: Dark/Light mode

---

## Troubleshooting

### "No data loaded"
- Check Excel files exist in root folder
- Verify filenames match config
- Ensure sheet "All" exists

### "Column not found"
- Check column mapping indexes
- Columns are 0-indexed (first column = 0)

### "Invalid risk level"
- Verify level values match expected: 🟢 Faible, 🟡 Modéré, 🟠 Élevé, 🔴 Critique

### Dashboard shows wrong data
- Clear browser cache
- Re-run analysis
- Check `output/` folder timestamp

---

## Maintenance

### Re-run After Data Changes
```bash
python3 lib/main.py
# Refresh browser to see updates
```

### Backup Configuration
```bash
cp configuration/analysis_config.json configuration/analysis_config.backup.json
```

### Reset to Defaults
```bash
python3 lib/main.py --init
# Creates fresh analysis_config.json
```
