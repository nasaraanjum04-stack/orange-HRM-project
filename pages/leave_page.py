import time

from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.waits import wait_click, wait_visible, wait_for_loader_to_disappear
from utils.date_utils import get_future_dates


class LeavePage:

    def __init__(self, driver):
        self.driver = driver


    def go(self):
        wait_click(self.driver, (By.XPATH, "//span[normalize-space()='Leave']")).click()


    def assign(self, name):

        wait_click(self.driver, (By.XPATH, "//a[normalize-space()='Assign Leave']")).click()

        # Enter employee name
        emp = wait_click(self.driver, (By.XPATH, "//input[@placeholder='Type for hints...']"))
        emp.send_keys(name)

        # Select from dropdown
        wait_click(self.driver, (By.XPATH, "//div[@role='listbox']//span")).click()

        # Select Leave Type
        wait_click(self.driver, (By.XPATH, "(//div[contains(@class,'oxd-select-text')])[1]")).click()
        wait_click(self.driver, (By.XPATH, "//span[contains(text(),'Vacation')]")).click()

        # Dynamic Dates
        from_date, to_date = get_future_dates()

        # FROM DATE
        fd = wait_click(self.driver, (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[1]"))
        fd.send_keys(Keys.CONTROL + "a")
        fd.send_keys(Keys.BACKSPACE)
        fd.send_keys(from_date)

        # TO DATE
        td = wait_click(self.driver, (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[2]"))
        td.send_keys(Keys.CONTROL + "a")
        td.send_keys(Keys.BACKSPACE)
        td.send_keys(to_date)

        # Wait loader before submit
        wait_for_loader_to_disappear(self.driver)

        # Click Assign
        wait_click(self.driver, (By.XPATH, "//button[@type='submit']")).click()

        try:
            # Wait for popup
            wait_visible(self.driver, (By.XPATH, "//div[contains(@class,'oxd-dialog-container')]"))

            # Click OK button
            wait_click(self.driver, (By.XPATH, "//button[normalize-space()='Ok']")).click()

        except:
            print("No popup appeared")

        # Wait loader after submit
        wait_for_loader_to_disappear(self.driver)


    def list(self):
        wait_click(self.driver, (By.XPATH, "//a[normalize-space()='Leave List']")).click()


    def verify(self):
        return wait_visible(
            self.driver,
            (By.XPATH, "//div[contains(@class,'oxd-table')]")
        ).is_displayed()

    def filter_scheduled_and_validate(self, employee_name):

        wait_for_loader_to_disappear(self.driver)

        # Go to Leave List
        wait_click(self.driver, (By.XPATH, "//a[normalize-space()='Leave List']")).click()
        # self.driver(By.XPATH, "//div[contains(@class,'oxd-table')]").is_displayed()

        wait_for_loader_to_disappear(self.driver)
        wait = WebDriverWait(self.driver, 10)
        # 🔹 Remove "Pending Approval" chip if present
        try:
            wait = WebDriverWait(self.driver, 10)

            remove_btn = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(.,'Pending Approval')]//i[contains(@class,'bi-x')]"
                ))
            )

            self.driver.execute_script("arguments[0].click();", remove_btn)

        except TimeoutException:
            print("Pending Approval not present or not clickable")

        time.sleep(5)
        status_dropdown = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//label[normalize-space()='Show Leave with Status']/following::div[contains(@class,'oxd-select-text-input')][1]"
            ))
        )

        actions = ActionChains(self.driver)
        actions.move_to_element(status_dropdown).click().perform()
        # wait_click(self.driver, status_dropdown)


        # scheduled_option = (
        #     By.XPATH,
        #     "//div[@role='listbox']//span[normalize-space()='Scheduled']"
        # )
        #
        # wait_click(self.driver, scheduled_option)
        #
        # wait_visible(
        #     self.driver,
        #     (By.XPATH, "//span[normalize-space()='Scheduled']")
        # )
        # Step 2: Wait for dropdown (listbox) to be visible
        wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//div[@role='listbox']"
        )))

        # Step 3: Select "Scheduled"
        scheduled_option = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[@role='listbox']//span[normalize-space()='Scheduled']"
        )))
        scheduled_option.click()


        searchButtonClick= wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[normalize-space()='Search']"
        )))
        searchButtonClick.click()


        wait_for_loader_to_disappear(self.driver)

        table = wait_visible(
            self.driver,
            (By.XPATH, "//div[contains(@class,'oxd-table-body')]")
        )


        self.driver.execute_script("arguments[0].scrollIntoView(true);", table)


        elements = self.driver.find_elements(
            By.XPATH,
            "//div[@role='row']//div[@role='cell'][3]"
        )

        names = [el.text.strip() for el in elements if el.text.strip()]

        print("Filtered Employees:", names)

        time.sleep(20)
        return employee_name in names