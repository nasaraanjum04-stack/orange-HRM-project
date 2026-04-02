
from selenium.webdriver.common.by import By
from utils.waits import wait_click, wait_for_loader_to_disappear, wait_visible


class PIMPage:
    def __init__(self,driver): self.driver=driver
    def go(self): wait_click(self.driver,(By.XPATH,"//span[text()='PIM']")).click()

    def add(self, f, l):
        wait_click(self.driver, (By.XPATH, "//button[contains(.,'Add')]")).click()

        wait_click(self.driver, (By.NAME, "firstName")).send_keys(f)
        wait_click(self.driver, (By.NAME, "lastName")).send_keys(l)

        # 🔥 wait for any loader before clicking
        wait_for_loader_to_disappear(self.driver)

        wait_click(self.driver, (By.XPATH, "//button[@type='submit']")).click()

        # 🔥 wait after submit (VERY IMPORTANT)
        wait_for_loader_to_disappear(self.driver)

    def verify(self):
        # wait for loader to disappear after save
        wait_for_loader_to_disappear(self.driver)

        # wait for Personal Details page
        return wait_visible(
            self.driver,
            (By.XPATH, "//h6[normalize-space()='Personal Details']")
        ).is_displayed()