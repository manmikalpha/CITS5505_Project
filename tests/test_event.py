import unittest
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class EventsPageUITest(unittest.TestCase):
    @classmethod
    def setUp(self):
        # Setup Chrome web driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver = self.driver

        # Step 1: Navigate to the login page
        driver.get("http://127.0.0.1:5000/login")

        # Step 2: Click on the "Sign Up" link to go to the registration page
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up"))).click()

        # Step 3: Fill out and submit the registration form
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "FirstName"))).send_keys("test")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "LastName"))).send_keys("test")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Email"))).send_keys("testregister@gmail.com")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Password"))).send_keys("123456")

        # Submit the registration form
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "registerButton")))
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)  # Scroll the button into view

        try:
            submit_button.click()
        except ElementClickInterceptedException:
            print("Element Click Intercepted Exception: Retrying after adjusting view")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)  # Adding slight delay to ensure the element is interactable
            submit_button.click()

        # Step 4: Fill out and submit the login form
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Email")))
        current_email_value = email_field.get_attribute("value")
        registered_email = "testregister@gmail.com"
        password = "123456"
        if current_email_value != registered_email:
            email_field.clear()
            email_field.send_keys(registered_email)

        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Password")))
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/events")

        
        

    def test_create_new_event_button(self):
        
        create_event_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create New Event')]")
        self.assertTrue(create_event_button.is_displayed())
        create_event_button.click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "createEventModal")))
        create_event_modal = self.driver.find_element(By.ID, "createEventModal")
        self.assertTrue(create_event_modal.is_displayed())
        title_input = self.driver.find_element(By.ID, "title")
        date_input = self.driver.find_element(By.ID, "date")
        description_input = self.driver.find_element(By.ID, "description")
        image_input = self.driver.find_element(By.NAME, "image")
        self.assertTrue(title_input.is_displayed())
        self.assertTrue(date_input.is_displayed())
        self.assertTrue(description_input.is_displayed())
        self.assertTrue(image_input.is_displayed())
        close_button = self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-secondary[data-bs-dismiss='modal']")
        close_button.click()
        wait = WebDriverWait(self.driver, 10)
        past_events_button = wait.until(EC.visibility_of_element_located((By.ID, "past-events-btn")))
        current_events_button = self.driver.find_element(By.ID, "current-events-btn")
        my_events_button = self.driver.find_element(By.ID, "my-events-btn")
        self.assertTrue(past_events_button.is_displayed())
        self.assertTrue(current_events_button.is_displayed())
        self.assertTrue(my_events_button.is_displayed())
        

    @classmethod
    def tearDownClass(self):
        user = User.query.filter_by(user_email="testregister@gmail.com").first()
        if user:
            db.session.delete(user)
            db.session.commit()
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()