import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPageTest(unittest.TestCase):
    def setUp(self):
        # Setup Chrome web driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def test_login_success(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Email"))).send_keys("Pavanpotukuchik@gmail.com")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Password"))).send_keys("123456")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "loginButton"))).click()

        try:
            # Validate headline text
            headline_text = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h1"))
            )
            self.assertIn("the charm of your cherished companions!", headline_text.text)

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
            print("Timeout Exception:", e.msg)
            driver.save_screenshot('test_failure.png')
            raise

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
