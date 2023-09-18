from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

count = 0
def extract_product(url):
    global count
    url = url
    # Configurar opciones de Chrome (puedes personalizarlas según tus necesidades)
    options = webdriver.ChromeOptions()

    #chrome_options.add_argument("--headless")
    # options.headless = True

    # Crear una instancia del controlador de Chrome
    driver = webdriver.Chrome(options)
    driver.set_window_size(1920, 1080)

    try:
        # Navegar a la URL
        driver.get(url)
        # driver.maximize_window()
        # time.sleep(2)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "sp-cc-accept"))).click()
 
        # time.sleep(3)
        title_element = driver.find_element(By.ID, "productTitle")
        title = title_element.text
        product_id_element = driver.find_element(By.ID, "corePrice_feature_div")
        product_id = product_id_element.get_attribute("data-csa-c-asin")
        price_element = driver.find_element(By.CSS_SELECTOR, "span.a-offscreen")
        price = price_element.get_attribute("innerHTML")
        price_validated = validate_price(price)
        if price_validated is None:
            price_whole = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div/div[1]/div[3]/div[1]/span[3]/span[2]/span[1]").text
            price_fraction = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div/div[1]/div[3]/div[1]/span[3]/span[2]/span[2]").text
            price_validated = float(price_whole + "." + price_fraction)

        img_element = driver.find_element(By.ID, "landingImage")
        img = img_element.get_attribute("src")

        count = 0

        return {"title": title, "price": price_validated, "img": img, "product_id": product_id}
    
    except Exception as e:
        print(f"Error en el inteno {count}")

        if count < 3:
            count += 1
            return extract_product(url)
    finally:
        # Cerrar el navegador
        driver.quit()

def validate_price(precio_str):
    try:
        precio = float(precio_str.replace('€', '').replace(',', '.').strip())
        return precio
    except ValueError:
        return None