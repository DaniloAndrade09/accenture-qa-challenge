from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SortablePage:
    URL = "https://demoqa.com/sortable"

    ITENS = (By.CSS_SELECTOR, "#demo-tabpane-list .list-group-item")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def abrir(self):
        self.driver.get(self.URL)
        self.wait.until(
            EC.visibility_of_element_located(self.ITENS)
        )

    def obter_ordem(self):
        return [
            item.text.strip()
            for item in self.driver.find_elements(*self.ITENS)
            if item.is_displayed()
        ]

    def validar_ordem_inicial(self):
        esperado = [
            "One", "Two", "Three",
            "Four", "Five", "Six"
        ]

        atual = self.obter_ordem()

        assert atual == esperado, (
            f"Ordem inicial incorreta: {atual}"
        )

    def mover_ultimo_para_primeiro(self):
        esperado = [
            "Six", "One", "Two",
            "Three", "Four", "Five"
        ]

        for tentativa in range(1, 4):
            if self.obter_ordem() == esperado:
                return

            itens = self.driver.find_elements(*self.ITENS)
            assert len(itens) == 6, (
                f"Esperados 6 elementos, encontrados {len(itens)}"
            )

            origem = itens[-1]
            destino = itens[0]

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                destino
            )

            deslocamento = (
                destino.rect["y"] - origem.rect["y"]
            )

            passos = 12
            incremento = deslocamento / passos

            acoes = ActionChains(self.driver)
            acoes.move_to_element(origem)
            acoes.click_and_hold()
            acoes.pause(0.3)

            anterior = 0

            for passo in range(1, passos + 1):
                atual = round(incremento * passo)
                delta = atual - anterior
                acoes.move_by_offset(0, delta)
                acoes.pause(0.08)
                anterior = atual

            acoes.pause(0.3)
            acoes.release()
            acoes.perform()

            try:
                WebDriverWait(self.driver, 2).until(
                    lambda driver: self.obter_ordem() == esperado
                )
                print(
                    f"Drag and Drop confirmado "
                    f"na tentativa {tentativa}"
                )
                return
            except Exception:
                print(
                    f"Tentativa {tentativa}: "
                    f"{self.obter_ordem()}"
                )

        raise AssertionError(
            "Drag and Drop nao alterou a lista "
            f"apos 3 tentativas. Ordem: {self.obter_ordem()}"
        )

    def validar_nova_ordem(self):
        esperado = [
            "Six", "One", "Two",
            "Three", "Four", "Five"
        ]

        try:
            self.wait.until(
                lambda driver: self.obter_ordem() == esperado
            )
        except Exception as erro:
            atual = self.obter_ordem()

            print("DIAGNOSTICO SORTABLE")
            print("Ordem esperada:", esperado)
            print("Ordem encontrada:", atual)

            destino = Path("reports/diagnostico_sortable")
            destino.mkdir(parents=True, exist_ok=True)

            self.driver.save_screenshot(
                str(destino / "tela.png")
            )

            (destino / "pagina.html").write_text(
                self.driver.page_source,
                encoding="utf-8"
            )

            raise AssertionError(
                f"Drag and Drop nao produziu a ordem esperada. "
                f"Ordem encontrada: {atual}"
            ) from erro

        atual = self.obter_ordem()
        assert atual == esperado
