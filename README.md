# 🔍 LinkedIn Job Scraper

A **Python-based LinkedIn job scraper** that automatically collects job listings from LinkedIn using Selenium and BeautifulSoup, with bot-detection avoidance and lazy-load scrolling support.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-4.x-orange)
![pandas](https://img.shields.io/badge/pandas-2.x-red)
![ChromeDriver](https://img.shields.io/badge/ChromeDriver-Latest-yellow)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔎 **Job Listing Scraper** | Scrapes job title, company, location, date posted, job URL |
| 📜 **Lazy-Load Scrolling** | Automatically scrolls to load all jobs on the page |
| 🤖 **Bot Detection Avoidance** | Uses random delays and browser headers to avoid blocks |
| 💾 **CSV Export** | Saves all scraped jobs to a clean CSV file using pandas |
| 🔄 **Updated CSS Selectors** | Fixed and up-to-date selectors for current LinkedIn layout |
| 🌐 **Keyword + Location Search** | Search any job role in any location |

---

## 🗂 Project Structure

```
linkedin_scraper/
├── scraper.py          ← Main scraper script
├── requirements.txt    ← Python dependencies
├── output/
│   └── jobs.csv        ← Scraped job listings saved here
└── README.md
```

---

## 🚀 Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/linkedin-job-scraper.git
cd linkedin-job-scraper
```

### 2. Install dependencies
```bash
pip install selenium beautifulsoup4 pandas
```

### 3. Download ChromeDriver
- Check your Chrome version: `chrome://settings/help`
- Download matching ChromeDriver from: https://chromedriver.chromium.org/downloads
- Place `chromedriver.exe` in the project folder

### 4. Set your search keyword and location
```python
# In scraper.py — edit these values:
KEYWORD  = "Python Developer"   # Job role to search
LOCATION = "India"              # Location to filter
```

### 5. Run the scraper
```bash
python scraper.py
```

### 6. Output
Jobs are saved to `output/jobs.csv` with columns:
- Job Title
- Company Name
- Location
- Date Posted
- Job URL

---

## 📊 Sample Output

| Job Title | Company | Location | Date Posted | Job URL |
|---|---|---|---|---|
| Python Developer | TCS | Pune, India | 2 days ago | linkedin.com/jobs/... |
| Django Developer | Infosys | Mumbai, India | 1 week ago | linkedin.com/jobs/... |
| Backend Engineer | Wipro | Bengaluru, India | 3 days ago | linkedin.com/jobs/... |

---

## 🛠 Tech Stack

- **Language:** Python 3.11
- **Browser Automation:** Selenium 4.x + ChromeDriver
- **HTML Parsing:** BeautifulSoup4
- **Data Handling:** pandas
- **Output Format:** CSV

---

## ⚠️ Common Issues & Fixes

| Issue | Fix |
|---|---|
| `ChromeDriver version mismatch` | Download ChromeDriver matching your Chrome version |
| `No jobs found` | LinkedIn updated CSS selectors — update class names in scraper.py |
| `Bot detection / CAPTCHA` | Increase random delay between scrolls |
| `Login required` | Add LinkedIn login credentials in scraper.py |
| `Lazy load not working` | Increase scroll count and sleep time |

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.  
Scraping LinkedIn may violate their [Terms of Service](https://www.linkedin.com/legal/user-agreement).  
Use responsibly and do not scrape personal data without consent.

---

## 👨‍💻 Developer

**Sudarshan Laxman Pulgamwar** (25771)
BCA T.Y | Dayanand College of Commerce, Latur | 2025-26

---

## 📄 License

MIT License — free to use, modify, and distribute.
