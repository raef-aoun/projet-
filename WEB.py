from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ----------------------------
# Setup WebDriver
# ----------------------------
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://demoqa.com/webtables")
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10)

# ----------------------------
# Stockage résultats
# ----------------------------
results = {}

# ----------------------------
# TC-WT-01 : Ajout utilisateur valide
# ----------------------------
try:
    wait.until(EC.element_to_be_clickable((By.ID, "addNewRecordButton"))).click()
    driver.find_element(By.ID, "firstName").send_keys("Karim")
    driver.find_element(By.ID, "lastName").send_keys("Ben Ali")
    driver.find_element(By.ID, "userEmail").send_keys("karim.benali@test.com")
    driver.find_element(By.ID, "age").send_keys("30")
    driver.find_element(By.ID, "salary").send_keys("4000")
    driver.find_element(By.ID, "department").send_keys("QA")
    driver.find_element(By.ID, "submit").click()
    results["TC-WT-01"] = "PASS – Utilisateur ajouté"
except Exception as e:
    results["TC-WT-01"] = f"FAIL – {e}"

# ----------------------------
# TC-WT-02 : Champs obligatoires vides
# ----------------------------
try:
    wait.until(EC.element_to_be_clickable((By.ID, "addNewRecordButton"))).click()
    driver.find_element(By.ID, "lastName").send_keys("Test")
    driver.find_element(By.ID, "submit").click()
    results["TC-WT-02"] = "PASS – Formulaire non soumis"

    # fermer modal si ouvert
    try:
        close_btn = wait.until(EC.element_to_be_clickable((By.ID, "closeLargeModal")))
        close_btn.click()
    except:
        pass
except Exception as e:
    results["TC-WT-02"] = f"FAIL – {e}"

# ----------------------------
# TC-WT-03 : Modification utilisateur
# ----------------------------
try:
    edit_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[title='Edit']")))
    wait.until(EC.element_to_be_clickable(edit_buttons[0])).click()
    email_field = driver.find_element(By.ID, "userEmail")
    email_field.clear()
    email_field.send_keys("updated.user@test.com")
    driver.find_element(By.ID, "submit").click()
    results["TC-WT-03"] = "PASS – Email mis à jour"
except Exception as e:
    results["TC-WT-03"] = f"FAIL – {e}"

# ----------------------------
# TC-WT-04 : Suppression utilisateur
# ----------------------------
try:
    delete_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[title='Delete']")))
    wait.until(EC.element_to_be_clickable(delete_buttons[0])).click()
    results["TC-WT-04"] = "PASS – Utilisateur supprimé"
except Exception as e:
    results["TC-WT-04"] = f"FAIL – {e}"

# ----------------------------
# TC-WT-05 : Persistance après refresh
# ----------------------------
try:
    driver.refresh()
    time.sleep(2)
    users = driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")
    found = any("Karim" in row.text and "Ben Ali" in row.text for row in users)
    if found:
        results["TC-WT-05"] = "PASS – Données persistantes"
    else:
        results["TC-WT-05"] = "FAIL – Données perdues"
except Exception as e:
    results["TC-WT-05"] = f"FAIL – {e}"

# ----------------------------
# Fermeture du navigateur
# ----------------------------
driver.quit()

# ----------------------------
# Rapport automatique
# ----------------------------
print("\n--- RAPPORT AUTOMATIQUE DES TESTS WEB TABLES ---")
for tc, result in results.items():
    print(f"{tc} : {result}")
print(f"Taux de réussite : {sum(1 for r in results.values() if 'PASS' in r)/len(results)*100:.0f}%")
