from config.config import USERNAME, PASSWORD
from pages.dashboard_page import DashboardPage
from pages.leave_page import LeavePage
from pages.login_page import LoginPage
from pages.pim_page import PIMPage
from utils.logger import get_logger
from utils.screenshot_utils import capture_step

logger = get_logger()

def test_full_e2e(driver):

    logger.info("Step 1: Login")
    LoginPage(driver).load()
    LoginPage(driver).login(USERNAME, PASSWORD)
    capture_step(driver, "login_success")

    logger.info("Step 2: Dashboard validation")
    assert DashboardPage(driver).is_loaded()

    logger.info("Step 3: Add Employee")
    pim = PIMPage(driver)
    pim.go()
    pim.add("Auto", "User")
    capture_step(driver, "employee_created")

    assert pim.verify()

    logger.info("Step 4: Assign Leave")
    leave = LeavePage(driver)
    leave.go()
    leave.assign("Auto User")
    capture_step(driver, "leave_assigned")

    logger.info("Step 5: Filter Scheduled Leave")
    assert leave.filter_scheduled_and_validate("Auto User")
    capture_step(driver, "leave_verified")