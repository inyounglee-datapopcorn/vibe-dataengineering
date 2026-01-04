# Seoul-Live Implementation Plan

## Goal
Build a real-time dashboard for Seoul City public data (Subway) using Supabase and Streamlit.

## User Review Required
- **Supabase Setup**: You need to create a project on Supabase and provide the `SUPABASE_URL` and `SUPABASE_KEY` (anon key) and the `SEOUL_API_KEY`.
- **Environment Variables**: You will need to fill in the `.env` file.

## Proposed Changes

### Project Structure (New Directory: `seoul-live/`)

#### [NEW] [requirements.txt](file:///Users/nathan/Documents/Github/vibe-dataengineering/seoul-live/requirements.txt)
- List of dependencies: `requests`, `supabase`, `streamlit`, `python-dotenv`, `plotly`, `pandas`.

#### [NEW] [.gitignore](file:///Users/nathan/Documents/Github/vibe-dataengineering/seoul-live/.gitignore)
- Ignore `venv/`, `.env`, `__pycache__/`, etc.

#### [NEW] [.env](file:///Users/nathan/Documents/Github/vibe-dataengineering/seoul-live/.env)
- Template for API keys.

#### [NEW] [collector.py](file:///Users/nathan/Documents/Github/vibe-dataengineering/seoul-live/collector.py)
- Script to fetch real-time subway data from Seoul API and save to Supabase.

#### [NEW] [app.py](file:///Users/nathan/Documents/Github/vibe-dataengineering/seoul-live/app.py)
- Streamlit dashboard to visualize the data.

#### [NEW] [database.py](file:///Users/nathan/Documents/Github/vibe-dataengineering/seoul-live/database.py)
- Placeholder for Supabase helper functions (as per prompt structure).

#### [NEW] [config.py](file:///Users/nathan/Documents/Github/vibe-dataengineering/seoul-live/config.py)
- Configuration file.

## Verification Plan

### Manual Verification
1.  **Install dependencies**: `pip install -r requirements.txt`.
2.  **Supabase Setup**: User creates table in Supabase SQL Editor.
3.  **Run Collector**: `python collector.py` (needs API keys).
4.  **Run Streamlit**: `streamlit run app.py`.
