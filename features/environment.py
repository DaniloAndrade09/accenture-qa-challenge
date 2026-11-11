from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_scenario(context, scenario):
    if "frontend" in scenario.effective_tags:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        context.driver = webdriver.Chrome(options=options)
        context.driver.implicitly_wait(0)


def after_scenario(context, scenario):
    driver = getattr(context, "driver", None)

    if driver is not None:
        driver.quit()
        context.driver = None
