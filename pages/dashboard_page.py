
from selenium.webdriver.common.by import By
from utils.waits import wait_click

class DashboardPage:
    def __init__(self,driver): self.driver=driver
    def is_loaded(self):
        return wait_click(self.driver,(By.XPATH,"//h6[text()='Dashboard']")).is_displayed()
