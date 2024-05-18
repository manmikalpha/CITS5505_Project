import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestWebApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-automation']);
        cls.driver = webdriver.Chrome(options)
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
        cls.driver.get("http://127.0.0.1:5000/login")
        wait = WebDriverWait(cls.driver, 10)  # Use WebDriverWait for explicit wait
        # Locate the username and password fields and fill them with test credentials
        username_input = wait.until(EC.presence_of_element_located((By.ID, "Email")))
        password_input = cls.driver.find_element(By.ID, "Password")
        username_input.send_keys("mihirtayshete@gmail.com")
        password_input.send_keys("meowmeow")
        password_input.send_keys(Keys.RETURN)


    def test_home_page_content(self):
        self.driver.get("http://127.0.0.1:5000/home")

        # Assert that the home page title matches the expected title
        expected_title = "Pawfect"
        actual_title = self.driver.title
        self.assertEqual(actual_title, expected_title, f"Expected title: {expected_title}, but got: {actual_title}")

        # Assert that the home page contains certain expected elements
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, ".navbar").is_displayed())
        nav_links = self.driver.find_elements(By.CLASS_NAME, "nav-link")
        expected_links = ["Home", "Events", "Gallery", "About", "Logout"]
        for link_element, expected_link_text in zip(nav_links, expected_links):
            self.assertEqual(link_element.text, expected_link_text)
        
        welcome_message = self.driver.find_element(By.ID, "nav-name")
        self.assertTrue(welcome_message.is_displayed())

        # Locate the main message element using class name and partial text
        main_message = self.driver.find_element(By.CSS_SELECTOR, "div.text-overlay > div > h1.petfont")
        # Check if the main message element is displayed
        self.assertTrue(main_message.is_displayed())


        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "#homeCarousel").is_displayed())

        # Locate the annual showcase section using class name and tag name
        annual_showcase_section = self.driver.find_element(By.CSS_SELECTOR, "h2 > span.petfont1.bold")
        # Check if the annual showcase section is displayed
        self.assertTrue(annual_showcase_section.is_displayed())


        # Assert that at least one card is present in the "Annual Showcase"
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, ".card").is_displayed())

        cards = self.driver.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len(cards), 6)

        # Assert that the footer is present
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, ".footer").is_displayed())

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()









# Failed attempt to automate test the home page using selenium webdriver
# import unittest
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from app import create_app, db
# from app.config import TestConfig
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from app.models import User,Events,Images
# from threading import Thread
# from os import environ


# class TestWebApp(unittest.TestCase):
#     @classmethod
   

#     def setUp(self):
#         testApp = create_app(TestConfig)
#         self.app_context = testApp.app_context()
#         self.app_context.push()
#         db.create_all()
#         # Create a user in the database
#         user = User(user_fName = "Mr", user_lName = "Cat", user_email = "cat@gmail.com", user_pswd = "easypasswordformeowbrain")
#         db.session.add(user)
#         db.session.commit()

        
#         def run_server():
#             environ["FLASK_ENV"] = "testing"
#             testApp.run(port=5000)

#         server_thread = Thread(target=run_server)
#         server_thread.start()
        
#          # Set up Selenium WebDriver
#         options = webdriver.ChromeOptions()
#         options.add_experimental_option("excludeSwitches", ['enable-automation']);
#         self.driver = webdriver.Chrome(options)
#         self.driver.maximize_window()
#         self.driver.implicitly_wait(10)
#         self.driver.get("http://localhost:5000/login")
#         wait = WebDriverWait(self.driver, 10)  # Use WebDriverWait for explicit wait
#         # Locate the username and password fields and fill them with test credentials
#         username_input = wait.until(EC.presence_of_element_located((By.ID, "Email")))
#         password_input = self.driver.find_element(By.ID, "Password")
#         username_input.send_keys("cat@gmail.com")
#         password_input.send_keys("easypasswordformeowbrain")
#         password_input.send_keys(Keys.RETURN)

#     def test_home_page_content(self):
#         self.driver.get("http://localhost:5000/home")
        
#         # Assert that the home page title matches the expected title
#         expected_title = "Pawfect"
#         actual_title = self.driver.title
#         self.assertEqual(actual_title, expected_title, f"Expected title: {expected_title}, but got: {actual_title}")

#         # Assert that the home page contains certain expected elements
#         self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, ".navbar").is_displayed())
#         nav_links = self.driver.find_elements(By.CLASS_NAME, "nav-link")
#         expected_links = ["Home", "Events", "Gallery", "About", "Logout"]
#         for link_element, expected_link_text in zip(nav_links, expected_links):
#             self.assertEqual(link_element.text, expected_link_text)
        
#         welcome_message = self.driver.find_element(By.ID, "nav-name")
#         self.assertTrue(welcome_message.is_displayed())

#         # Locate the main message element using class name and partial text
#         main_message = self.driver.find_element(By.CSS_SELECTOR, "div.text-overlay > div > h1.petfont")
#         # Check if the main message element is displayed
#         self.assertTrue(main_message.is_displayed())


#         self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "#homeCarousel").is_displayed())

#         # Locate the annual showcase section using class name and tag name
#         annual_showcase_section = self.driver.find_element(By.CSS_SELECTOR, "h2 > span.petfont1.bold")
#         # Check if the annual showcase section is displayed
#         self.assertTrue(annual_showcase_section.is_displayed())


#         # Assert that at least one card is present in the "Annual Showcase"
#         self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, ".card").is_displayed())

#         cards = self.driver.find_elements(By.CLASS_NAME, "card")
#         self.assertEqual(len(cards), 6)

#         # Assert that the footer is present
#         self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, ".footer").is_displayed())






# if __name__ == "__main__":
#     unittest.main()
