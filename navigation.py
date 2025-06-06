from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selector

def navigate_to_moisturizer_shop(driver):
    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, selector.landing_page['moisturizer_button']))
    )
    button.click()
    print("Navigation vers la boutique d'hydratants")

def navigate_to_sunscreen_shop(driver):
    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, selector.landing_page['sunscreen_button']))
    )
    button.click()
    print("Navigation vers la boutique de crèmes solaires")