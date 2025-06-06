from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import config
import selector
from navigation import navigate_to_moisturizer_shop, navigate_to_sunscreen_shop

def setup_driver():
    chrome_options = Options()
    if config.selenium_config['headless']:
        chrome_options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def find_cheapest_products(driver, shop_type):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, selector.product_card['all_products']))
    )
    time.sleep(1) 
    products = driver.find_elements(By.XPATH, selector.product_card['all_products'])
    if shop_type == 'moisturizer':
        aloe_products = []
        almond_products = []
        for product in products:
            product_name = product.find_element(By.XPATH, selector.product_card['name']).text
            product_price_text = product.find_element(By.XPATH, selector.product_card['price']).text
            price_str = product_price_text.replace('Price: ', '').replace('Rs.', '').strip()
            price = float(price_str)
            if 'aloe' in product_name.lower():
                aloe_products.append({'price': price, 'product': product, 'name': product_name})
            if 'almond' in product_name.lower():
                almond_products.append({'price': price, 'product': product, 'name': product_name})
        time.sleep(1)  
        if aloe_products:
            cheapest_aloe = min(aloe_products, key=lambda x: x['price'])
            time.sleep(1)  
            driver.execute_script("arguments[0].scrollIntoView(true);", cheapest_aloe['product'])
            time.sleep(1)  
            cheapest_aloe['product'].find_element(By.XPATH, selector.product_card['add_button']).click()
            time.sleep(1)  
        if almond_products:
            cheapest_almond = min(almond_products, key=lambda x: x['price'])
            time.sleep(1)  
            driver.execute_script("arguments[0].scrollIntoView(true);", cheapest_almond['product'])
            time.sleep(1)  
            cheapest_almond['product'].find_element(By.XPATH, selector.product_card['add_button']).click()
            time.sleep(1)  
    elif shop_type == 'sunscreen':
        cheapest_spf50_product = None
        cheapest_spf50_price = float('inf')
        cheapest_spf30_product = None
        cheapest_spf30_price = float('inf')
        spf50_products = []
        spf30_products = []
        for product in products:
            product_name = product.find_element(By.XPATH, selector.product_card['name']).text
            product_price_text = product.find_element(By.XPATH, selector.product_card['price']).text
            price_str = product_price_text.replace('Price: ', '').replace('Rs.', '').strip()
            price = float(price_str)
            if 'spf-50' in product_name.lower():
                spf50_products.append({'name': product_name, 'price': price, 'product': product})
                if price < cheapest_spf50_price:
                    cheapest_spf50_product = product
                    cheapest_spf50_price = price
            elif 'spf-30' in product_name.lower():
                spf30_products.append({'name': product_name, 'price': price, 'product': product})
                if price < cheapest_spf30_price:
                    cheapest_spf30_product = product
                    cheapest_spf30_price = price
        time.sleep(1)  
        if cheapest_spf50_product:
            cheapest_spf50_name = next(item['name'] for item in spf50_products if item['price'] == cheapest_spf50_price)
            time.sleep(1)  
            driver.execute_script("arguments[0].scrollIntoView(true);", cheapest_spf50_product)
            time.sleep(1)  
            cheapest_spf50_product.find_element(By.XPATH, selector.product_card['add_button']).click()
            time.sleep(1)  
        if cheapest_spf30_product:
            cheapest_spf30_name = next(item['name'] for item in spf30_products if item['price'] == cheapest_spf30_price)
            time.sleep(1)  
            driver.execute_script("arguments[0].scrollIntoView(true);", cheapest_spf30_product)
            time.sleep(1)  
            cheapest_spf30_product.find_element(By.XPATH, selector.product_card['add_button']).click()
            time.sleep(1) 

def send_keys_with_delay(element, keys):
    for key in keys:
        element.send_keys(key)
        time.sleep(0.1)

def process_payment(driver):
    pay_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, selector.cart['pay_button']))
    )
    time.sleep(1)
    pay_button.click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, selector.cart['stripe_iframe']))
    )
    stripe_frame = driver.find_element(By.XPATH, selector.cart['stripe_iframe'])
    time.sleep(1)
    driver.switch_to.frame(stripe_frame)
    time.sleep(1)
    email_address = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, selector.payment['email']))
    )
    email_address.send_keys('douaa_asmaa@weather.com')
    time.sleep(1)
    card_number = driver.find_element(By.XPATH, selector.payment['card_number'])
    send_keys_with_delay(card_number, '5555555555554444')
    time.sleep(1)
    expiry_date = driver.find_element(By.XPATH, selector.payment['expiry_date'])
    send_keys_with_delay(expiry_date, '07/30')
    time.sleep(1)
    cvc_code = driver.find_element(By.XPATH, selector.payment['cvc_code'])
    cvc_code.send_keys('888')
    time.sleep(1)
    zip_code = driver.find_element(By.XPATH, selector.payment['zip_code'])
    zip_code.send_keys('20300')
    time.sleep(1)
    submit_button = driver.find_element(By.ID, selector.payment['submit_button'])
    time.sleep(1)
    submit_button.click()
    time.sleep(1)
    driver.switch_to.default_content()
    try:
        WebDriverWait(driver, 10).until(
            EC.url_contains('confirmation')
        )
        header = driver.find_element(By.TAG_NAME, selector.confirmation['header'])
        header_text = header.text
        if header_text == "PAYMENT SUCCESS":
            print("Le paiement a réussi.")
        else:
            print("Le paiement a échoué.")
    except Exception as e:
        print(f"Erreur lors de la vérification du paiement: {e}")

def test_automated():
    driver = setup_driver()
    try:
        driver.get(config.selenium_config['url'])
        temperature_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, selector.landing_page['temperature']))
        )
        temperature_text = temperature_element.text
        temperature = float(temperature_text.split()[0])
        shop_type = None
        if temperature < 19:
            navigate_to_moisturizer_shop(driver)
            shop_type = 'moisturizer'
        elif temperature > 34:
            navigate_to_sunscreen_shop(driver)
            shop_type = 'sunscreen'
        else:
            return
        find_cheapest_products(driver, shop_type)
        cart_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, selector.product_card['cart_button']))
        )
        time.sleep(2)
        cart_button.click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, selector.cart['base']))
        )
        time.sleep(1)
        cart_items = driver.find_elements(By.XPATH, "//tbody/tr")
        for item in cart_items:
            print(f"- {item.text}")
            time.sleep(1)
        time.sleep(1)
        process_payment(driver)
    except Exception as e:
        print(f"\nErreur pendant le test: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_complete_test()
