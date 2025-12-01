from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------
# CONFIGURATION SELENIUM
# -------------------------------
driver = webdriver.Chrome()   # Selenium Manager gère automatiquement ChromeDriver
driver.maximize_window()

# -------------------------------
# TEST 1 – Accès aux détails d’un livre
# -------------------------------
def test_access_book_details():
    driver.get("https://demoqa.com/books")

    try:
        # cliquer sur le premier livre
        first_book = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".rt-tr-group:nth-child(1) .rt-td a")
            )
        )
        book_name = first_book.text
        first_book.click()

        # vérifier que la page des détails s'affiche
        title = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, "title-wrapper")
            )
        )

        print("TC-BK01 : PASS – Détails du livre affichés.")
        return True, book_name

    except:
        print("TC-BK01 : FAIL – Page blanche détectée, aucun contenu.")
        return False, None


# -------------------------------
# TEST 2 – Vérifier l’URL du livre
# -------------------------------
def test_url(book_name):
    try:
        current_url = driver.current_url

        if "book=" in current_url:
            print("TC-BK02 : PASS – URL correcte :", current_url)
            return True
        else:
            print("TC-BK02 : FAIL – URL incorrecte :", current_url)
            return False

    except:
        print("TC-BK02 : FAIL – Impossible de vérifier l’URL.")
        return False


# -------------------------------
# TEST 3 – Vérifier les erreurs JS
# -------------------------------
def test_console_errors():
    logs = driver.get_log("browser")

    errors = [log for log in logs if log["level"] == "SEVERE"]

    if errors:
        print("TC-BK03 : FAIL – Erreurs JavaScript détectées.")
        for e in errors:
            print("Erreur JS :", e["message"])
        return False
    else:
        print("TC-BK03 : PASS – Aucune erreur JS.")
        return True


# -------------------------------
# TEST 4 – Bouton “Back to Book Store”
# -------------------------------
def test_back_button():
    try:
        back_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "addNewRecordButton"))
        )
        back_btn.click()

        # vérifier retour à la liste
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".rt-table")
            )
        )

        print("TC-BK04 : PASS – Retour à la liste OK.")
        return True

    except:
        print("TC-BK04 : FAIL – Bouton retour inaccessible → page blanche.")
        return False


# -------------------------------
# EXÉCUTION DES TESTS
# -------------------------------
results = []

r1, book_name = test_access_book_details()
results.append(r1)

if book_name:
    results.append(test_url(book_name))
else:
    results.append(False)

results.append(test_console_errors())
results.append(test_back_button())

print("\n----------------------")
print("Résumé du Test Automatisé")
print("----------------------")
print("PASS :", results.count(True))
print("FAIL :", results.count(False))

driver.quit()
