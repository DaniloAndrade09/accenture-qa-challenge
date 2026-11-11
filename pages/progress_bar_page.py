import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProgressBarPage:
    URL = "https://demoqa.com/progress-bar"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15, poll_frequency=0.05)

    def abrir(self):
        self.driver.get(self.URL)
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "startStopButton"))
        )

    def progresso(self):
        barra = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#progressBar [role='progressbar']")
            )
        )

        valor = barra.get_attribute("aria-valuenow")

        if valor is not None:
            return int(valor)

        texto = barra.text.strip().replace("%", "")

        if texto.isdigit():
            return int(texto)

        raise AssertionError(
            f"Nao foi possivel identificar o progresso. "
            f"HTML: {barra.get_attribute('outerHTML')}"
        )

    def iniciar(self):
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "startStopButton"))
        ).click()

    def parar_antes_de_25(self):
        limite = time.monotonic() + 15

        while time.monotonic() < limite:
            valor = self.progresso()

            if 10 <= valor < 20:
                self.wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, "startStopButton")
                    )
                ).click()

                valor_final = self.progresso()

                assert valor_final <= 25, (
                    f"Progresso ultrapassou 25%: {valor_final}%"
                )

                return valor_final

            if valor > 25:
                raise AssertionError(
                    f"Progresso ultrapassou o limite: {valor}%"
                )

            time.sleep(0.02)

        raise TimeoutError(
            "Nao foi possivel interromper antes de 25%."
        )

    def validar_parado(self):
        valor_inicial = self.progresso()
        time.sleep(0.4)
        valor_final = self.progresso()

        assert valor_inicial == valor_final, (
            f"Barra continuou avancando: "
            f"{valor_inicial}% -> {valor_final}%"
        )

        assert valor_final <= 25
        return valor_final

    def aguardar_100(self):
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "startStopButton"))
        ).click()

        WebDriverWait(self.driver, 30).until(
            lambda driver: self.progresso() == 100
        )

    def resetar(self):
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "resetButton"))
        ).click()

        self.wait.until(
            lambda driver: self.progresso() == 0
        )
