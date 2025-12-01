from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import random

driver = webdriver.Chrome()
driver.get("https://demoqa.com/resizable")
driver.maximize_window()
actions = ActionChains(driver)

# Petite pause pour stabilité
time.sleep(1)


# ================================
#   TEST BLOC 1 – AVEC LIMITES
# ================================
print("\n--- TEST BLOC 1 (CONTRAINTES) ---")
try:
    bloc1 = driver.find_element(By.ID, "resizableBoxWithRestriction")
    handle1 = bloc1.find_element(By.CSS_SELECTOR, ".react-resizable-handle-se")

    # Max
    actions.click_and_hold(handle1).move_by_offset(350, 150).release().perform()
    time.sleep(1)
    max_size = bloc1.size

    # Min
    actions.click_and_hold(handle1).move_by_offset(-350, -150).release().perform()
    time.sleep(1)
    min_size = bloc1.size

    print(f"Max size : {max_size} | Min size : {min_size}")

    if max_size["width"] <= 500 and max_size["height"] <= 300 and \
       min_size["width"] >= 150 and min_size["height"] >= 150:
        print("✔ BLOC 1 OK – limites respectées")
    else:
        print("❌ BLOC 1 NON conforme !")

except Exception as e:
    print(f"❌ Erreur test bloc 1 : {e}")


# ================================
#   TEST BLOC 2 – SANS LIMITES
# ================================
print("\n--- TEST BLOC 2 (SANS LIMITES) ---")

bloc2 = driver.find_element(By.ID, "resizable")
handle2 = bloc2.find_element(By.CSS_SELECTOR, ".react-resizable-handle-se")

# Test simple
try:
    actions.click_and_hold(handle2).move_by_offset(80, 40).release().perform()
    print("✔ Bloc 2 manipulable (test simple)")
except Exception as e:
    print(f"❌ Bloc 2 ne peut pas être manipulé : {e}")


# ================================
#   STRESS TEST – MODE HUMAIN
# ================================
print("\n--- STRESS TEST (SIMULATION HUMAINE) ---")

bug_detected = False

def natural_drag(handle, x, y):
    """Déplacement plus humain (petites variations + lenteur)."""
    steps = 6
    for i in range(steps):
        dx = x / steps + random.randint(-3, 3)
        dy = y / steps + random.randint(-3, 3)

        actions.click_and_hold(handle).move_by_offset(dx, dy).pause(0.05).release().perform()
        time.sleep(0.03)


# --------------------------
# Stress test
# --------------------------
try:
    old_size = bloc2.size

    for i in range(15):  # Beaucoup plus réaliste
        natural_drag(handle2, 50, 25)
        natural_drag(handle2, -40, -20)

    time.sleep(1)
    new_size = bloc2.size

    # Test visuel réel : la taille doit changer !
    if new_size == old_size:
        bug_detected = True
        print("❌ BUG MANUEL reproduit : le bloc ne réagit plus aux glissers !")

    # Test supplémentaire : essayer encore un mouvement
    try:
        natural_drag(handle2, 20, 10)
        print("✔ BLOC 2 réagit toujours après stress test")
    except:
        bug_detected = True
        print("❌ Bloc 2 bloqué (freeze détecté comme en test manuel).")

except Exception as e:
    bug_detected = True
    print(f"⚠ ERREUR pendant le stress test : {e}")


# ================================
#   CONCLUSION FINALE
# ================================
print("\n--- RÉSULTAT FINAL ---")
if bug_detected:
    print("❌ BUG confirmé sur BLOC 2 (même comportement que le test manuel) !")
else:
    print("✔ Aucun blocage détecté automatiquement")
    print("⚠ Mais le bug manuel peut ne PAS être détecté selon les machines.")


driver.quit()
print("\n--- TEST TERMINÉ ---")
