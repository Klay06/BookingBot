import booking.constants as const
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver import ActionChains
import re
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException)

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

        # Handle cookie popup
        try:
            accept_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            ))
            accept_button.click()
            time.sleep(1)
        except:
            pass

        # Click and clear search field
        search_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id=":rh:"]'))
        )
        search_field.clear()
        search_field.click()

        # Slowly type the place
        for char in place_to_go:
            search_field.send_keys(char)
            time.sleep(0.3)

        # Wait until the first autocomplete result contains the correct city name
        suggestion_xpath = '//*[@id="autocomplete-result-0"]'
        wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, suggestion_xpath),
                place_to_go
            )
        )

        # Click the first correct result
        first_result = wait.until(EC.element_to_be_clickable((By.XPATH, suggestion_xpath)))
        first_result.click()


        
    def select_dates(self, check_in_date, check_out_date):
        wait = WebDriverWait(self, 20)

        # 1. Scroll down to make sure calendar is visible
        self.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)

        # 2. Open the calendar
        calendar_open_button_xpath = '//*[@data-testid="date-display-field-start"]'
        calendar_open_button = wait.until(EC.element_to_be_clickable((By.XPATH, calendar_open_button_xpath)))
        calendar_open_button.click()
        time.sleep(1)

        # 3. Re-click to ensure it stays open (this helps with flaky behavior)
        calendar_open_button.click()
        time.sleep(2)

        # 4. Select the check-in and check-out dates
        check_in_xpath = f'//span[@data-date="{check_in_date}"]'
        check_out_xpath = f'//span[@data-date="{check_out_date}"]'

        check_in_element = wait.until(EC.element_to_be_clickable((By.XPATH, check_in_xpath)))
        check_in_element.click()

        check_out_element = wait.until(EC.element_to_be_clickable((By.XPATH, check_out_xpath)))
        check_out_element.click()



    

    def select_adults(self, desired_adults=3):

        wait = WebDriverWait(self, 15)
        print("[INFO] Opening guest selection panel...")

        try:
            guests_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]'))
            )
            guests_button.click()
            print("[SUCCESS] Guest panel opened.")
        except Exception as e:
            print(f"[ERROR] Failed to open guest panel: {e}")
            return

        attempt = 0
        while True:
            attempt += 1
            print(f"[DEBUG] Attempt #{attempt}: Checking current number of adults...")

            try:
                adults_input = wait.until(EC.presence_of_element_located((By.ID, 'group_adults')))
                current_adults = int(adults_input.get_attribute("value"))
                print(f"[INFO] Current number of adults: {current_adults}")
            except Exception as e:
                print(f"[ERROR] Could not read adult count: {e}")
                return

            if current_adults == desired_adults:
                print(f"[SUCCESS] Desired number of adults ({desired_adults}) is already set.")
                break

            try:
                if current_adults < desired_adults:
                    button_xpath = '//*[@id="group_adults"]/following-sibling::button[1]'
                else:
                    button_xpath = '//*[@id="group_adults"]/preceding-sibling::button[1]'

                button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                button.click()
                button.click()
                print(f"[ACTION] Adjusted adult count: clicked button.")
                time.sleep(0.4)
            except Exception as e:
                print(f"[ERROR] Failed to click adjustment button: {e}")
                return
