from common import *


def status_zamowienia(driver):
    driver.get("https://localhost:8443/historia-zamowien")

    mail = driver.find_element(By.CSS_SELECTOR, "input#field-email")
    mail.clear()
    mail.send_keys("pub@prestashop.com")

    password = driver.find_element(By.CSS_SELECTOR, "input#field-password")
    password.clear()
    password.send_keys("123456789")

    driver.find_element(By.CSS_SELECTOR, "button#submit-login").click()
    sleep(1)

    details = driver.find_element(
        By.CSS_SELECTOR, "a[data-link-action='view-order-details']"
    )
    details.click()
    sleep(3)
