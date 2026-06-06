"""
Standalone scraper script — called by Django via subprocess.
Usage: python run_scraper.py <email> <password> <keyword> <location> <pages> <output_path> <chromedriver_path>
"""
import sys, os, json

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linkedin_scraper.settings")

def main():
    if len(sys.argv) < 8:
        print(json.dumps({"error": "Missing arguments"}))
        sys.exit(1)

    email           = sys.argv[1]
    password        = sys.argv[2]
    keyword         = sys.argv[3]
    location        = sys.argv[4]
    pages           = int(sys.argv[5])
    output_path     = sys.argv[6]
    chromedriver    = sys.argv[7]

    try:
        from scraper_app.scraper import run_scraper
        from scraper_app.report_generator import generate_report

        rows = run_scraper(
            email=email,
            password=password,
            keyword=keyword,
            location=location,
            pages=pages,
            chromedriver_path=chromedriver,
        )

        if not rows:
            print(json.dumps({"error": "No jobs scraped. LinkedIn may have changed its layout or detected automation."}))
            sys.exit(1)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        generate_report(rows, keyword, output_path)
        print(json.dumps({"status": "done", "count": len(rows)}))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
