import os, time, random, tempfile
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


# ── Exact XPaths from LinkedIn login page ──
XPATH_EMAIL  = "/html/body/div[1]/div[2]/div/div/div/main/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div[2]/div/div[3]/div[1]/div/div/div/input"
XPATH_PASS   = "/html/body/div[1]/div[2]/div/div/div/main/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div[2]/div/div[3]/div[2]/div/div/input"
XPATH_BUTTON = "/html/body/div[1]/div[2]/div/div/div/main/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div[2]/div/div[3]/button"


def random_sleep(a=1.0, b=2.5):
    time.sleep(random.uniform(a, b))


def init_driver(chromedriver_path):
    # Fresh temp profile every run — avoids conflicts with open Chrome windows
    user_data_dir = os.path.join(tempfile.gettempdir(), f"li_scraper_{os.getpid()}")
    os.makedirs(user_data_dir, exist_ok=True)

    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--password-store=basic")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })

    driver = uc.Chrome(
        driver_executable_path=chromedriver_path,
        options=options,
        version_main=149,        # match your Chrome 149
        headless=False,
        use_subprocess=True,     # key flag — spawns Chrome as subprocess, not child process
    )

    driver.set_page_load_timeout(120)
    driver.set_script_timeout(60)
    driver.implicitly_wait(0)
    return driver


def _js_type(driver, element, text):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(0.4)
    driver.execute_script("arguments[0].value = '';", element)
    time.sleep(0.2)
    for ch in text:
        element.send_keys(ch)
        time.sleep(random.uniform(0.05, 0.14))


def linkedin_login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 40)

    # ── Email ──
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_EMAIL)))
    wait.until(EC.visibility_of(email_field))
    time.sleep(1.5)
    _js_type(driver, email_field, email)
    random_sleep(0.8, 1.4)

    # ── Password ──
    pwd_field = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_PASS)))
    wait.until(EC.visibility_of(pwd_field))
    _js_type(driver, pwd_field, password)
    random_sleep(0.6, 1.2)

    # ── Submit ──
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BUTTON)))
    driver.execute_script("arguments[0].click();", btn)

    # ── Wait for feed ──
    try:
        WebDriverWait(driver, 40).until(EC.any_of(
            EC.url_contains("/feed"),
            EC.url_contains("/mynetwork"),
            EC.url_contains("/jobs"),
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.global-nav__nav")),
            EC.presence_of_element_located((By.ID, "global-nav-search")),
        ))
    except TimeoutException:
        # CAPTCHA/2FA — wait for manual solve
        WebDriverWait(driver, 120).until(EC.any_of(
            EC.url_contains("/feed"),
            EC.url_contains("/mynetwork"),
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.global-nav__nav")),
        ))

    random_sleep(2.0, 3.0)


def build_search_url(keyword, location="", start=0):
    kw  = keyword.replace(" ", "%20")
    url = f"https://www.linkedin.com/jobs/search/?keywords={kw}&start={start}"
    if location:
        url += f"&location={location.replace(' ', '%20')}"
    return url


def slow_scroll(driver, steps=6, delay=0.6):
    try:
        height = driver.execute_script("return document.body.scrollHeight")
        for i in range(1, steps + 1):
            driver.execute_script(f"window.scrollTo(0, {int(height * i / steps)});")
            time.sleep(delay)
    except Exception:
        pass


def extract_jobs_from_soup(soup):
    rows = []
    cards = (
        soup.select("ul.scaffold-layout__list-container > li") or
        soup.select("ul.jobs-search__results-list > li") or
        soup.select("li.occludable-update") or
        soup.select("div.job-card-container")
    )

    for card in cards:
        try:
            title_el = (
                card.select_one("a.job-card-list__title") or
                card.select_one("a.job-card-container__link") or
                card.select_one("h3.base-search-card__title") or
                card.select_one("h3")
            )
            title = title_el.get_text(strip=True) if title_el else ""

            link_el = (
                card.select_one("a.job-card-list__title") or
                card.select_one("a.job-card-container__link") or
                card.select_one("a.base-card__full-link") or
                card.select_one("a[href*='/jobs/view/']")
            )
            job_link = ""
            if link_el and link_el.has_attr("href"):
                job_link = link_el["href"].split("?")[0]

            company_el = (
                card.select_one(".job-card-container__primary-description") or
                card.select_one("h4.base-search-card__subtitle") or
                card.select_one(".artdeco-entity-lockup__subtitle span")
            )
            company = company_el.get_text(strip=True) if company_el else ""

            loc_el = (
                card.select_one(".job-card-container__metadata-item") or
                card.select_one("span.job-search-card__location") or
                card.select_one(".artdeco-entity-lockup__caption span")
            )
            location = loc_el.get_text(strip=True) if loc_el else ""

            time_el = card.select_one("time")
            date_posted = ""
            if time_el:
                date_posted = time_el.get("datetime") or time_el.get_text(strip=True)

            if not title and not company:
                continue

            rows.append({
                "title":       title,
                "company":     company,
                "location":    location,
                "date_posted": date_posted,
                "job_link":    job_link,
                "scraped_at":  datetime.utcnow().isoformat(),
            })
        except Exception:
            pass

    return rows


def run_scraper(email, password, keyword, location="", pages=2, chromedriver_path="chromedriver.exe"):
    driver = init_driver(chromedriver_path)
    results = []
    try:
        linkedin_login(driver, email, password)
        for p in range(pages):
            url = build_search_url(keyword, location, start=p * 25)
            driver.get(url)
            random_sleep(2.5, 4.0)
            slow_scroll(driver)
            random_sleep(1.5, 2.5)
            rows = extract_jobs_from_soup(BeautifulSoup(driver.page_source, "html.parser"))
            results.extend(rows)
            random_sleep(2.0, 3.5)
    finally:
        try:
            driver.quit()
        except Exception:
            pass
    return results
