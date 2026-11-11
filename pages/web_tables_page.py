from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebTablesPage:
    URL = "https://demoqa.com/webtables"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def abrir(self):
        self.driver.get(self.URL)
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "addNewRecordButton"))
        )
        self.configurar_paginacao(20)

    def configurar_paginacao(self, quantidade=20):
        seletor = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "select")
            )
        )

        Select(seletor).select_by_value(str(quantidade))

        self.wait.until(
            lambda driver: (
                Select(
                    driver.find_element(By.CSS_SELECTOR, "select")
                ).first_selected_option.get_attribute("value")
                == str(quantidade)
            )
        )
    def cadastrar(self, nome, sobrenome, email, idade, salario, departamento):
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "addNewRecordButton"))
        )
        self.driver.find_element(By.ID, "addNewRecordButton").click()

        campos = {
            "firstName": nome,
            "lastName": sobrenome,
            "userEmail": email,
            "age": str(idade),
            "salary": str(salario),
            "department": departamento,
        }

        for campo, valor in campos.items():
            self.wait.until(
                EC.visibility_of_element_located((By.ID, campo))
            ).send_keys(valor)

        self.driver.find_element(By.ID, "submit").click()

    def localizar_linha(self, email):
        linhas = self.driver.find_elements(
            By.CSS_SELECTOR, "tbody tr"
        )

        for linha in linhas:
            if email in linha.text:
                return linha

        return None

    def validar_registro(self, email):
        self.wait.until(
            lambda driver: self.localizar_linha(email) is not None
        )

        assert self.localizar_linha(email) is not None, (
            f"Registro nao encontrado: {email}"
        )

    def editar(self, email, novo_salario):
        linha = self.localizar_linha(email)
        assert linha is not None, f"Registro nao encontrado: {email}"

        linha.find_element(
            By.CSS_SELECTOR, "[id^='edit-record-']"
        ).click()

        campo = self.wait.until(
            EC.visibility_of_element_located((By.ID, "salary"))
        )
        campo.clear()
        campo.send_keys(str(novo_salario))

        self.driver.find_element(By.ID, "submit").click()

    def validar_salario(self, email, salario):
        self.wait.until(
            lambda driver: (
                (linha := self.localizar_linha(email)) is not None
                and str(salario) in linha.text
            )
        )

    def excluir(self, email):
        busca = self.wait.until(
            EC.visibility_of_element_located((By.ID, "searchBox"))
        )
        busca.clear()
        busca.send_keys(email)

        def encontrar(driver):
            for linha in driver.find_elements(By.CSS_SELECTOR, "tbody tr"):
                celulas = linha.find_elements(By.TAG_NAME, "td")
                if any(c.text.strip() == email for c in celulas):
                    return linha
            return False

        try:
            linha = self.wait.until(encontrar)
        except Exception as erro:
            visiveis = [
                linha.text
                for linha in self.driver.find_elements(
                    By.CSS_SELECTOR, "tbody tr"
                )
            ]
            raise AssertionError(
                f"Email nao encontrado: {email}; "
                f"Filtro: {busca.get_attribute('value')}; "
                f"Linhas: {visiveis}"
            ) from erro

        linha.find_element(
            By.CSS_SELECTOR, "[id^='delete-record-']"
        ).click()

        self.wait.until(lambda driver: not encontrar(driver))

        busca = self.driver.find_element(By.ID, "searchBox")
        busca.clear()

        self.wait.until(
            lambda driver: driver.find_element(
                By.ID, "searchBox"
            ).get_attribute("value") == ""
        )

    def validar_exclusao(self, email):
        self.wait.until(
            lambda driver: self.localizar_linha(email) is None
        )