from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PracticeFormPage:
    URL = "https://demoqa.com/automation-practice-form"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def abrir(self):
        self.driver.get(self.URL)
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "firstName"))
        )

    def preencher(self):
        self.driver.find_element(By.ID, "firstName").send_keys("Danilo")
        self.driver.find_element(By.ID, "lastName").send_keys("Teste")
        self.driver.find_element(By.ID, "userEmail").send_keys(
            "qa.automation@example.com"
        )

        self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "label[for='gender-radio-1']")
            )
        ).click()

        self.driver.find_element(By.ID, "userNumber").send_keys(
            "11987654321"
        )

        assunto = self.driver.find_element(
            By.ID, "subjectsInput"
        )
        assunto.send_keys("Maths")

        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "react-select-2-option-0")
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")
            )
        ).click()

        arquivo = (
            Path(__file__).resolve().parents[1]
            / "fixtures"
            / "upload.txt"
        )

        assert arquivo.is_file(), (
            f"Arquivo nao encontrado: {arquivo}"
        )

        self.driver.find_element(
            By.ID, "uploadPicture"
        ).send_keys(str(arquivo))

        self.driver.find_element(
            By.ID, "currentAddress"
        ).send_keys("Sao Paulo - SP")

        estado = self.driver.find_element(By.ID, "state")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            estado
        )
        estado.click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "react-select-3-option-0")
            )
        ).click()

        cidade = self.wait.until(
            EC.element_to_be_clickable((By.ID, "city"))
        )
        cidade.click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "react-select-4-option-0")
            )
        ).click()

    def enviar(self):
        botao = self.wait.until(
            EC.presence_of_element_located((By.ID, "submit"))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            botao
        )

        self.wait.until(
            EC.element_to_be_clickable((By.ID, "submit"))
        ).click()

    def validar_popup(self):
        popup = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "example-modal-sizes-title-lg")
            )
        )

        assert "Thanks for submitting the form" in popup.text, (
            f"Mensagem inesperada: {popup.text}"
        )

    def fechar_popup(self):
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "closeLargeModal"))
        ).click()
