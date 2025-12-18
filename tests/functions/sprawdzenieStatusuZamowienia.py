from common import *


def status_zamowienia(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://localhost:8443/historia-zamowien")

    mail = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#field-email"))
    )
    mail.clear()
    mail.send_keys("pub@prestashop.com")

    password = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#field-password"))
    )
    password.clear()
    password.send_keys("123456789")

    submit_login = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button#submit-login"))
    )
    submit_login.click()

    details = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a[data-link-action='view-order-details']")
        )
    )
    details.click()

    wait.until(EC.visibility_of_element_located((By.ID, "order-infos")))

    sleep(5)
