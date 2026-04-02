
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_click(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def wait_for_loader_to_disappear(driver, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located(
                ("xpath", "//div[contains(@class,'oxd-form-loader')]")
            )
        )
    except:
        pass

def wait_visible(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )