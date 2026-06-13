import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def test_frontend_sentiment():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(options=options)
    try:
        driver.get("http://localhost:5000/")

        text_input = driver.find_element(By.ID, "text-input")
        text_input.send_keys("This product is great and amazing")

        submit_btn = driver.find_element(By.ID, "submit-btn")
        submit_btn.click()

        time.sleep(3)

        result = driver.find_element(By.ID, "result-output")
        text = result.text
        assert text != ""
        assert any(word in text for word in ["POSITIVE", "NEGATIVE", "Confidence"])
    finally:
        driver.quit()