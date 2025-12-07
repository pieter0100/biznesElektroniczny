from common import *


def pobierz_fakture(driver):
    driver.get("https://localhost:8443/historia-zamowien")

    mail = driver.find_element(By.CSS_SELECTOR, "input#field-email")
    mail.clear()
    mail.send_keys("pub@prestashop.com")

    password = driver.find_element(By.CSS_SELECTOR, "input#field-password")
    password.clear()
    password.send_keys("123456789")

    driver.find_element(By.CSS_SELECTOR, "button#submit-login").click()
    sleep(1)

    table = driver.find_element(By.CSS_SELECTOR, "tbody")
    rows = table.find_elements(By.CSS_SELECTOR, "tr")

    for row in rows:
        cols = row.find_elements(By.CSS_SELECTOR, "td")

        try:
            cols[4].find_element(By.CSS_SELECTOR, "a").click()
            print("pobrano fakture")
        except:
            print("brak faktury")

    sleep(1)
