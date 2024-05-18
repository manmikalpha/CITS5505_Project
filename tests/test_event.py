import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EventsPageUITest(unittest.TestCase):
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
        cls.driver.implicitly_wait(10)
        cls.driver.get("http://127.0.0.1:5000/events")

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

    def test_event_filter_buttons(self):
        past_events_button = self.driver.find_element(By.ID, "past-events-btn")
        current_events_button = self.driver.find_element(By.ID, "current-events-btn")
        my_events_button = self.driver.find_element(By.ID, "my-events-btn")
        self.assertTrue(past_events_button.is_displayed())
        self.assertTrue(current_events_button.is_displayed())
        self.assertTrue(my_events_button.is_displayed())

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()