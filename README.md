# Trend Trackers — Sales Trend Analysis

A beginner-friendly, editable analytics project using Python, SQL, and an interactive dashboard.

## Important note about the data
`data/sales_data.csv` is a **synthetic demonstration dataset** generated for this starter project. It is not real company data. Use it to learn and test the project. For an assessed submission that requires a public/real dataset, replace it with an approved dataset and update the report and findings accordingly.

## Project contents
- `data/sales_data.csv` — editable sample data
- `src/analysis.py` — data cleaning, KPIs, summaries, charts
- `src/load_database.py` — creates `data/sales_database.db` from CSV
- `src/dashboard.py` — interactive Streamlit dashboard with filters and downloadable filtered rows
- `sql/analysis_queries.sql` — SQL queries
- `docs/PROJECT_REPORT.md` — report template
- `docs/PRESENTATION_GUIDE.md` — slide plan, speaking notes, and viva prompts
- `docs/POWER_BI_GUIDE.md` — instructions to build the Power BI dashboard
- `outputs/` — generated charts and summaries after running analysis

## 1. Requirements
Install Python 3.10+ and a code editor such as VS Code. Internet is needed once to install Python packages.

## 2. Set up
Open a terminal in the `Trend_Trackers_Project` folder.

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 3. Run the Python analysis
```bash
python src/analysis.py
```
Charts and summary CSVs will be saved in `outputs/`.

## 4. Create / refresh the SQLite database
```bash
python src/load_database.py
```
This creates `data/sales_database.db`. Open it with a SQLite browser or use Python to run the queries in `sql/analysis_queries.sql`.

## 5. Run the interactive dashboard
```bash
streamlit run src/dashboard.py
```
Streamlit will print a local URL, usually `http://localhost:8501`. Open that URL in your browser. Use the sidebar filters and the CSV download button.

## 6. Modify the project
- Edit `data/sales_data.csv` in Excel or a spreadsheet editor.
- Keep required column names consistent, especially `Order ID`, `Order Date`, `Region`, `Category`, `Product Name`, `Quantity`, `Sales`, and `Profit`.
- Edit chart titles and calculations in `src/analysis.py`.
- Edit the dashboard layout in `src/dashboard.py`.
- Edit and run SQL statements in `sql/analysis_queries.sql`.
- Re-run the Python analysis after replacing data.

## 7. Build the Power BI version
Follow `docs/POWER_BI_GUIDE.md`. Import `data/sales_data.csv`, create measures, add visuals and slicers, then save a `.pbix` file.

## 8. Troubleshooting
- `python` not found: try `py` on Windows or `python3` on macOS/Linux; install Python and enable PATH if needed.
- `No module named ...`: activate `.venv` and run `python -m pip install -r requirements.txt`.
- Dashboard doesn't start: run the command from the project root, not from `src`.
- Column error: check the exact spelling of the CSV headers.
- Power BI Desktop is Windows-focused; if you're on macOS/Linux, you can still run the Python/Streamlit dashboard and use Power BI through a supported Windows environment if available.

## Responsible interpretation
A sales association does not prove causation. Mention limitations, date coverage, missing values, and whether data is synthetic or real in your presentation.
