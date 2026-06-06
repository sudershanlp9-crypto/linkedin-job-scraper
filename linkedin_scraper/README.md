# LinkedIn Job Scraper — Django Edition

Scrape LinkedIn jobs via a web form and auto-generate a polished Excel report with charts.

## Setup

```bash
pip install -r requirements.txt
```

Place `chromedriver.exe` in the project root (same folder as `manage.py`).
Match the version to your Chrome — download from: https://chromedriver.chromium.org/downloads

## Run

```bash
cd linkedin_scraper
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## What you get

Fill in the form → click **Start Scraping** → download the Excel report.

The `.xlsx` report has 3 sheets:

| Sheet | Contents |
|---|---|
| 📋 Raw Data | All scraped jobs with clickable links |
| 📊 Summary | KPI boxes + Top 10 Companies + Top 10 Locations tables |
| 📈 Charts | Bar chart (companies) + Pie chart (locations) |

## Notes

- Keep Chrome window visible if LinkedIn shows CAPTCHA — solve it manually (2 min timeout).
- Reports are saved in the `reports/` folder inside the project.
- Credentials are never stored or logged.
