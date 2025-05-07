import booking.constants as const
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"D:\KLAY\carrer testing\projects\New folder\booking\chromedriver.exe",teardown=False):
        self.driver_path = driver_path
        self.teardown =teardown
        os.environ['PATH']+=self.driver_path
        super(Booking,self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self,exc_type,exc_val,exc_tb):
        
        if self.teardown:
          self.quit()
    
    def land_first_page(self):
        self.get(const.BASE_URL)


    def change_currency(self, currency):
        # 1. Click the currency dropdown
        currency_element = self.find_element(By.XPATH, '//*[@data-testid="header-currency-picker-trigger"]')
        currency_element.click()

        # 2. Wait for the currency option to appear using a dynamic XPath
        wait = WebDriverWait(self, 10)
        currency_option_xpath = f'//*[@data-testid="selection-item" and .//div[contains(text(), "{currency}")]]'
        
        currency_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, currency_option_xpath))
        )

        # 3. Click the currency
        currency_button.click()
    
    def select_place_to_go(self, place_to_go):
        wait = WebDriverWait(self, 10)

        # Wait until the search input is visible and enabled
        search_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id=":rh:"]'))
        )

        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="autocomplete-result-1"]')))
        first_result.click()
        


