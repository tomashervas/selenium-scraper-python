from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def extract_product(url):
    service = ChromeService(executable_path="/usr/bin/chromedriver")
    options = webdriver.ChromeOptions()

    options.headless = True

    driver = webdriver.Chrome(service=service,options=options)
    driver.set_window_size(1920, 1080)

    try:

        driver.get(url)
        driver.maximize_window()
        time.sleep(2)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "sp-cc-accept"))).click()

        title_element = driver.find_element(By.ID, "productTitle")
        title = title_element.text
        time.sleep(2)
        price_element = driver.find_element(By.CSS_SELECTOR, "span.a-offscreen")
        price = price_element.get_attribute("innerHTML")
        price_validated = validate_price(price)
        if price_validated is None:
            price_whole = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div/div[1]/div[3]/div[1]/span[3]/span[2]/span[1]").text
            price_fraction = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div/div[1]/div[3]/div[1]/span[3]/span[2]/span[2]").text
            price_validated = price_whole + "." + price_fraction

        img_element = driver.find_element(By.ID, "landingImage")
        img = img_element.get_attribute("src")

        return {"title": title, "price": price_validated, "img": img}
    
    except Exception as e:
        print("Error capturado:", e)
    finally:
        # Cerrar el navegador
        driver.quit()

def validate_price(precio_str):
    try:
        precio = float(precio_str.replace('€', '').replace(',', '.').strip())
        return precio
    except ValueError:
        return None