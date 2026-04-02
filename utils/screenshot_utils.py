
from datetime import datetime
import os

def capture_step(driver, name):
    os.makedirs("reports/screenshots", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"reports/screenshots/{name}_{ts}.png"
    driver.save_screenshot(path)
    return path
