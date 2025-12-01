from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# ---------- CONFIG ----------
#  Mets ici le chemin COMPLET vers un VRAI fichier qui existe sur ton PC
file_path = r"C:\Users\yesri\OneDrive\Documents\COURS\business intelligence"   # à adapter !
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Fichier introuvable : {file_path}")

# Dossier où Chrome va enregistrer les fichiers téléchargés
download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)

# ---------- DRIVER ----------
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

try:
    # 1) Aller sur la page
    driver.get("https://demoqa.com/upload-download")
    driver.maximize_window()

    # 2) UPLOAD du fichier
    upload_input = driver.find_element(By.ID, "uploadFile")
    upload_input.send_keys(file_path)

    time.sleep(2)  # petite pause pour laisser la page réagir

    # Vérifier que l'upload a bien été pris en compte
    uploaded_text = driver.find_element(By.ID, "uploadedFilePath").text
    assert os.path.basename(file_path) in uploaded_text, "Upload KO"
    print("Upload OK")

    # 3) DOWNLOAD (télécharge l'image de démo du site)
    download_btn = driver.find_element(By.ID, "downloadButton")
    download_btn.click()

    time.sleep(5)  # attendre le téléchargement

    # Vérifier qu'un fichier est bien apparu dans le dossier de téléchargement
    files = os.listdir(download_dir)
    assert len(files) > 0, "Download KO : aucun fichier téléchargé"
    print("Download OK - fichiers téléchargés :", files)

finally:
    time.sleep(2)
    driver.quit()
