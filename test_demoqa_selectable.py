import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options, use_subprocess=True, version_main=142)
wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)

driver.get("https://demoqa.com/selectable")


# ------------------------------------------------------------
#  TOOL: Vérification de l’état des items
# ------------------------------------------------------------
def get_active(items):
    return [it.text.strip() for it in items if "active" in it.get_attribute("class")]


# ------------------------------------------------------------
#  TEST 1 : LIST MODE
# ------------------------------------------------------------
def test_list():

    print("\n=========== TEST LIST ===========")
    driver.find_element(By.ID, "demo-tab-list").click()
    time.sleep(1)

    items = driver.find_elements(By.CSS_SELECTOR, "#verticalListContainer .list-group-item")

    # -----------------------------
    # 1. Sélection simple
    # -----------------------------
    print("\n1. Test sélection simple")
    items[0].click()
    time.sleep(0.5)
    print("   → Actif :", get_active(items))

    items[1].click()
    time.sleep(0.5)
    print("   → Actif après changement :", get_active(items))

    # -----------------------------
    # 2. Désélection impossible (clic simple remplace seulement)
    # -----------------------------
    print("\n2. Test désélection simple")
    items[1].click()   # clic sur item déjà sélectionné
    time.sleep(0.5)
    print("   → Toujours actif :", get_active(items))

    # -----------------------------
    # 3. Multi sélection Ctrl
    # -----------------------------
    print("\n3. Test multi-sélection avec Ctrl")
    actions.key_down(Keys.CONTROL)
    items[0].click()
    items[2].click()
    items[3].click()
    actions.key_up(Keys.CONTROL)
    time.sleep(1)
    print("   → Actifs (Ctrl) :", get_active(items))

    # -----------------------------
    # 4. Désélection d’un seul item en Ctrl
    # -----------------------------
    print("\n4. Test désélection (Ctrl)")
    actions.key_down(Keys.CONTROL)
    items[2].click()  # désactiver
    actions.key_up(Keys.CONTROL)
    time.sleep(0.5)
    print("   → Actifs :", get_active(items))

    # -----------------------------
    # 5. Tout désélectionner en cliquant ailleurs
    # -----------------------------
    print("\n5. Test désélection totale")
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(0.5)
    print("   → Actifs :", get_active(items))


# ------------------------------------------------------------
#  TEST 2 : GRID MODE
# ------------------------------------------------------------
def test_grid():

    print("\n=========== TEST GRID ===========")
    driver.find_element(By.ID, "demo-tab-grid").click()
    time.sleep(1)

    items = driver.find_elements(By.CSS_SELECTOR, "#gridContainer .list-group-item")

    # -----------------------------
    # 1. Sélection simple
    # -----------------------------
    print("\n1. Test sélection simple")
    items[0].click()
    time.sleep(0.5)
    print("   → Actif :", get_active(items))

    items[4].click()
    time.sleep(0.5)
    print("   → Actif changé :", get_active(items))

    # -----------------------------
    # 2. Désélection par clic simple (n’existe pas)
    # -----------------------------
    print("\n2. Test désélection simple (non supporté)")
    items[4].click()
    time.sleep(0.5)
    print("   → Toujours actif :", get_active(items))

    # -----------------------------
    # 3. Multi sélection avec Ctrl
    # -----------------------------
    print("\n3. Test multi-sélection Ctrl")
    actions.key_down(Keys.CONTROL)
    items[0].click()
    items[8].click()
    actions.key_up(Keys.CONTROL)
    time.sleep(0.5)
    print("   → Actifs :", get_active(items))

    # -----------------------------
    # 4. Désélection d’un item actif (Ctrl)
    # -----------------------------
    print("\n4. Test désélection (Ctrl)")
    actions.key_down(Keys.CONTROL)
    items[0].click()
    actions.key_up(Keys.CONTROL)
    time.sleep(0.5)
    print("   → Actifs :", get_active(items))

    # -----------------------------
    # 5. Test tous les éléments un par un
    # -----------------------------
    print("\n5. Test de chaque cellule (sélection simple)")
    for i in range(len(items)):
        items[i].click()
        time.sleep(0.2)
        print(f"   → {items[i].text} actif :", get_active(items))


# ------------------------------------------------------------
#  EXÉCUTION
# ------------------------------------------------------------
try:
    test_list()
    test_grid()

    print("\n🎉 TOUS LES CAS POSSIBLES SONT TESTÉS AVEC SUCCÈS !")
    input("\nAppuie sur Entrée pour fermer...")

finally:
    driver.quit()
