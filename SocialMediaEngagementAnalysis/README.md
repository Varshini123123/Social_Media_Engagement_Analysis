# Social Media Engagement Analysis

Project title: Social Media Engagement Analysis
Student name: Student Name
Project ID: Social Media Engagement Analysis
Domain: Marketing

## Problem Statement
This project answers: Which social media posts and posting times generate the highest engagement, and what actions can marketers take to improve social media performance?

## Objectives
- Measure overall social media engagement
- Identify top-performing and low-performing posts
- Compare performance across platforms
- Analyze posting date, day of week, and hour patterns
- Compare content types and campaigns
- Calculate engagement rate using impressions when available
- Create evidence-based recommendations for marketing decisions

## Technology Stack
- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Plotly
- Streamlit
- SQLite
- Jupyter Notebook

## Dataset Source and Verification
The project is built to work with a real Kaggle dataset in CSV or Excel format under `data/raw/`.

Current local validation uses the sample file:
- `data/sample/social_media_engagement_sample.csv`

This sample is clearly labeled as a development dataset and must not be treated as a production or business dataset.

## Project Structure
```text
social-media-engagement-analysis/
app.py
requirements.txt
README.md
config.py
.gitignore
data/
    raw/
    processed/
    sample/
notebooks/
    social_media_eda.ipynb
src/
    data_loader.py
    data_cleaning.py
    feature_engineering.py
    metrics.py
    visualizations.py
    database.py
    insights.py
sql/
    schema.sql
    data_quality_checks.sql
    business_analysis_queries.sql
reports/
    problem_statement.md
    data_dictionary.md
    data_quality_report.md
    insights_and_recommendations.md
    presentation_outline.md
outputs/
    charts/
    cleaned_data/
    reports/
```

## Environment Setup
```powershell
cd d:\SocialMediaEngagementAnalysis
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Project
```powershell
cd d:\SocialMediaEngagementAnalysis
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

## Sample Data and Current Evidence
The working example currently contains 30 posts and yields the following KPI snapshot:
- Total posts: 30
- Total engagements: 16,013
- Average engagements per post: 533.77
- Engagement rate: 2.28%
- Best platform: YouTube
- Best content type: Story
- Best posting day: Tuesday
- Best posting hour: 17:00

These values are calculated from the loaded sample dataset and update automatically when a real dataset is inserted in `data/raw/`.

## Data Cleaning and Output Files
The cleaning workflow:
- loads CSV or Excel files
- validates required columns
- normalizes platform and content labels
- removes duplicates
- converts dates and times
- validates numeric metrics
- creates derived engagement features
- exports the cleaned dataset to `data/processed/social_media_cleaned.csv`

## SQL Analysis
The SQL scripts are stored in `sql/` and include schema creation, quality checks, and business-analysis queries.

## Jupyter Notebook
Run the EDA notebook from `notebooks/social_media_eda.ipynb`.

## Troubleshooting
- If no dataset is found in `data/raw/`, the app automatically uses the sample dataset.
- If required columns are missing, update the alias mapping in `config.py`.
- If the port is busy, rerun the app on a different port such as `8502`.

## Known Limitations
- The current report is based on a sample dataset, not a live Kaggle dataset.
- Observed performance reflects correlation rather than proven causation.
- Real-world datasets may include more or fewer fields than the sample file.
