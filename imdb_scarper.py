from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # ✅ ADD THESE TWO LINES HERE
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def scrape_imdb():
    driver = setup_driver()

    # ✅ Use stable version of page
    driver.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")

    wait = WebDriverWait(driver, 15)

    # ✅ Wait until all movie rows load
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")))

    movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

    print(f"Total movies found: {len(movies)}")  # Should be 250

    data = []

    for i, movie in enumerate(movies, start=1):
        try:
            title = movie.find_element(By.CSS_SELECTOR, "h3").text
            full_text = movie.text

            year_match = re.search(r"\b(19|20)\d{2}\b", full_text)
            year = year_match.group() if year_match else "N/A"

            try:
                rating = movie.find_element(By.CSS_SELECTOR, ".ipc-rating-star--rating").text
            except:
                rating = "N/A"

            data.append({
                "Rank": i,
                "Title": title,
                "Year": year,
                "Rating": rating
            })

        except Exception as e:
            print(f"Error scraping movie {i}: {e}")

    driver.quit()
    return data


def save_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("imdb_top_250.csv", index=False)
    print("✅ CSV file created successfully!")


if __name__ == "__main__":
    print("Scraping started...")
    movies = scrape_imdb()
    save_csv(movies)