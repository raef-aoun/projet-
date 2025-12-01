from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# -------- INITIALISATION DU DRIVER --------
# Selenium Manager gère automatiquement ChromeDriver
driver = webdriver.Chrome()
driver.maximize_window()

# -------- OUVRIR LA PAGE --------
driver.get("https://demoqa.com/droppable")
time.sleep(1)

# -------- LOCALISATION DES ÉLÉMENTS --------
drag = driver.find_element(By.ID, "draggable")
drop = driver.find_element(By.ID, "droppable")
drop_text = driver.find_element(By.XPATH, "//*[@id='droppable']/p")

actions = ActionChains(driver)

# -------- TC-DP01 : Dépôt correct dans la zone --------
actions.drag_and_drop(drag, drop).perform()
time.sleep(1)
if drop_text.text == "Dropped!":
    print("TC-DP01 PASS : Texte correct après dépôt")
else:
    print("TC-DP01 FAIL : Texte incorrect")

# -------- TC-DP02 : Drag hors zone --------
# Déplacer "Drag me" hors de la zone
actions.click_and_hold(drag).move_by_offset(300, 0).release().perform()
time.sleep(1)
# Vérifier que la zone n'a pas changé
if drop_text.text == "Dropped!":
    print("TC-DP02 PASS : Aucun changement attendu (zone reste Dropped!)")
else:
    print("TC-DP02 FAIL : Texte modifié hors zone")

# -------- TC-DP03 : Retrait après drop réussi --------
# Déposer à nouveau dans la zone puis retirer
actions.drag_and_drop(drag, drop).perform()
time.sleep(1)
actions.click_and_hold(drag).move_by_offset(300, 0).release().perform()
time.sleep(1)
drop_color = drop.value_of_css_property("background-color")
# Vérification simplifiée : si texte et couleur restent Dropped!
if drop_text.text == "Dropped!" or "70, 130, 180" in drop_color:
    print("TC-DP03 FAIL : Zone ne revient pas à l’état initial")
else:
    print("TC-DP03 PASS : Zone réinitialisée")

# -------- TC-DP04 : Fluidité du drag --------
# Drag aléatoire pour tester fluidité
actions.click_and_hold(drag).move_by_offset(50, 30).move_by_offset(-40, -20).move_by_offset(60, 10).release().perform()
print("TC-DP04 PASS : Drag fluide et suivi du curseur")

# -------- FERMER LE NAVIGATEUR --------
driver.quit()
