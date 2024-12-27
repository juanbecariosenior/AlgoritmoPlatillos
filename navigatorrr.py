from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Configurar las opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--incognito")  # Activar el modo incógnito

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

# Abrir una URL en modo incógnito
driver.get("http://10.123.1.92/comandera/comandera/kirest.html")

time.sleep(30)

iniciar_button = WebDriverWait(driver,30).until(
    EC.visibility_of_element_located((By.XPATH, '//input[@type="button" and @value="Iniciar"]')) 
)

iniciar_button.click()

# Mantener la ventana abierta por un tiempo
input("Presiona Enter para cerrar el navegador...")

# Cerrar el navegador
driver.quit()