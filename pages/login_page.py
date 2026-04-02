
from selenium.webdriver.common.by import By
from utils.waits import wait_click
from config.config import BASE_URL

class LoginPage:
    def __init__(self, driver): self.driver=driver
    def load(self): self.driver.get(BASE_URL)
    def login(self,u,p):
        wait_click(self.driver,(By.NAME,"username")).send_keys(u)
        wait_click(self.driver,(By.NAME,"password")).send_keys(p)
        wait_click(self.driver,(By.XPATH,"//button[@type='submit']")).click()
