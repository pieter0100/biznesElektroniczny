from common import *


def pobierz_fakture(driver):
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

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button#submit-login"))
    )
    submit_btn.click()

    try:
        table_body = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody"))
        )
    except:
        print("Brak tabeli zamówień lub timeout")
        return

    rows = table_body.find_elements(By.CSS_SELECTOR, "tr")

    for row in rows:
        cols = row.find_elements(By.CSS_SELECTOR, "td")

        if len(cols) > 4:
            try:
                invoice_link = cols[4].find_element(By.TAG_NAME, "a")

                driver.execute_script("arguments[0].click();", invoice_link)
                print("pobrano fakture")

            except Exception:
                print("brak faktury")
