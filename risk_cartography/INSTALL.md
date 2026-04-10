# Installation Guide

## Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager

## Step-by-Step Installation

### 1. Verify Python Installation

```bash
python3 --version
# Expected: Python 3.8.x or higher
```

If Python is not installed, download from [python.org](https://www.python.org/downloads/).

### 2. Extract the Package

Unzip `risk_cartography.zip` to your desired location:

```bash
unzip risk_cartography.zip -d /path/to/install/
cd /path/to/install/risk_cartography
```

### 3. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify Installation

```bash
python3 lib/main.py --help
```

You should see the help message with available options.

---

## Folder Structure

After installation, your folder should look like:

```
risk_cartography/
├── lib/                    # Python source code
│   ├── __init__.py
│   ├── main.py            # Entry point
│   ├── config_loader.py
│   ├── data_loader.py
│   ├── analyzer.py
│   ├── html_generator.py
│   └── exporters.py
├── configuration/
│   └── analysis_config.json  # Configuration file
├── output/                 # Generated reports (empty on install)
├── requirements.txt
├── INSTALL.md             # This file
├── RUNBOOK.md             # Operational guide
└── README.md              # Quick start
```

---

## Input Files Location

**Place your Excel files in the root folder** (same level as `lib/`):

```
risk_cartography/
├── carto_des_risques_Entity_ABC1.xlsx   ← INPUT FILES HERE
├── carto_des_risques_Entity_ABC2.xlsx
├── carto_des_risques_Entity_XYZ.xlsx
├── lib/
├── configuration/
└── output/
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas openpyxl
```

### "Permission denied"
```bash
chmod +x lib/main.py
```

### "FileNotFoundError: analysis_config.json"
Ensure you run from the `risk_cartography/` directory:
```bash
cd /path/to/risk_cartography
python3 lib/main.py
```

---

## Uninstall

```bash
# Deactivate virtual environment
deactivate

# Remove folder
rm -rf /path/to/risk_cartography
```
