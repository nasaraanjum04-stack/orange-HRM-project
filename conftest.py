import pytest
from selenium import webdriver
from datetime import datetime
import os
import pytest_html

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def get_screenshot_name(test_name, status):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{test_name}_{status}_{timestamp}.png"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        driver = item.funcargs.get("driver", None)

        if driver:
            os.makedirs("reports/screenshots", exist_ok=True)

            status = "PASS" if rep.passed else "FAIL"

            file_name = get_screenshot_name(item.name, status)
            file_path = os.path.join("reports/screenshots", file_name)


            driver.save_screenshot(file_path)


            import base64
            with open(file_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode()

            extra = getattr(rep, "extra", [])
            extra.append(pytest_html.extras.image(image_base64, mime_type='image/png'))
            rep.extra = extra