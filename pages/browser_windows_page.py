from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BrowserWindowsPage:
    URL = "https://demoqa.com/browser-windows"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.janela_original = None

    def abrir(self):
        self.driver.get(self.URL)
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "windowButton"))
        )
        self.janela_original = self.driver.current_window_handle

    def abrir_nova_janela(self):
        self.driver.find_element(By.ID, "windowButton").click()

        self.wait.until(EC.number_of_windows_to_be(2))

        for janela in self.driver.window_handles:
            if janela != self.janela_original:
                self.driver.switch_to.window(janela)
                return

        raise AssertionError("A nova janela nao foi encontrada.")

    def validar_texto(self):
        elemento = self.wait.until(
            EC.visibility_of_element_located((By.ID, "sampleHeading"))
        )

        assert elemento.text == "This is a sample page", (
            f"Texto inesperado: {elemento.text}"
        )

    def fechar_nova_janela(self):
        self.driver.close()
        self.driver.switch_to.window(self.janela_original)
