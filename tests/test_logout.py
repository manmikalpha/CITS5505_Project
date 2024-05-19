import unittest
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class LoginAndLogoutPageTest(unittest.TestCase):
    def setUp(self):
        # Setup Chrome web driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def test_login_and_logout(self):
        driver = self.driver

        # Step 1: Navigate to the login page
        driver.get("http://127.0.0.1:5000/login")

        # Step 2: Fill out and submit the login form
        registered_email = "testregister@gmail.com"
        password = "123456"

        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Email")))
        email_field.clear()
        email_field.send_keys(registered_email)

        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Password")))
        password_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "loginButton")))
        driver.execute_script("arguments[0].scrollIntoView();", login_button)  # Scroll the button into view

        # Debugging: Check if the button is displayed and enabled
        print("Login button displayed:", login_button.is_displayed())
        print("Login button enabled:", login_button.is_enabled())

        try:
            # Use ActionChains to click the login button
            actions = ActionChains(driver)
            actions.move_to_element(login_button).click().perform()
        except ElementClickInterceptedException:
            print("Element Click Intercepted Exception: Retrying after adjusting view")
            driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            time.sleep(1)  # Adding slight delay to ensure the element is interactable
            actions.move_to_element(login_button).click().perform()

        # Step 3: Verify successful login and validate elements on the homepage
        try:
            # Validate headline text
            headline_text = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.text-overlay h1"))
            )
            self.assertIn("Capture", headline_text.text)

            # Validate carousel image visibility
            carousel_image = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".carousel-item.active img"))
            )
            self.assertTrue(carousel_image.is_displayed())

            # Validate navigation link 'Gallery'
            gallery_link = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, "Gallery"))
            )
            self.assertTrue(gallery_link.is_displayed())

        except TimeoutException as e:
            print("Login failed or homepage elements not found:", e.msg)
            driver.save_screenshot('login_failure.png')
            raise

        # Step 4: Click on the "Logout" link
        try:
            logout_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
            driver.execute_script("arguments[0].scrollIntoView();", logout_link)  # Scroll the link into view

            actions.move_to_element(logout_link).click().perform()
        except TimeoutException as e:
            print("Logout link not found or clickable:", e.msg)
            driver.save_screenshot('logout_failure.png')
            raise

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
