import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    order_taxi_button = (By.CLASS_NAME, 'button.round')
    tariff_cards = (By.CLASS_NAME, 'tcard')
    comfort_tariff = (By.XPATH, "//div[contains(@class, 'tcard') and contains(., 'Comfort')]")
    phone_input = (By.ID, 'phone')
    phone_modal = (By.XPATH, "//div[contains(@class, 'modal')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def set_from(self, from_address):
        element = self.wait.until(EC.element_to_be_clickable(self.from_field))
        element.clear()
        element.send_keys(from_address)

    def set_to(self, to_address):
        element = self.wait.until(EC.element_to_be_clickable(self.to_field))
        element.clear()
        element.send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        print("✓ Direcciones ingresadas")

        time.sleep(1.5)
        button = self.wait.until(EC.element_to_be_clickable(self.order_taxi_button))
        button.click()
        print("✓ Botón 'Pedir un taxi' clickeado")

        time.sleep(2)
        tariffs = self.wait.until(EC.presence_of_all_elements_located(self.tariff_cards))
        print(f"✓ Tarifas encontradas: {len(tariffs)}")

    def select_comfort_tariff(self):
        time.sleep(1)
        comfort_element = self.wait.until(EC.element_to_be_clickable(self.comfort_tariff))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                   comfort_element)
        time.sleep(0.5)
        comfort_element.click()
        print("✓ Tarifa Comfort seleccionada")
        time.sleep(3)

    def scroll_panel_down_until_phone_visible(self):
        """Hacer scroll hacia ABAJO en el panel izquierdo hasta que el teléfono sea visible"""
        print("\nHaciendo scroll hacia ABAJO en el panel izquierdo...")

        # 🔑 Encontrar el campo de teléfono primero (existe en DOM aunque no sea visible)
        phone_field = self.wait.until(EC.presence_of_element_located(self.phone_input))
        print("✓ Campo de teléfono encontrado en DOM")

        # 🔑 Encontrar su contenedor scrollable padre
        scrollable_panel = self.driver.execute_script("""
            var phone = arguments[0];
            var parent = phone.parentElement;

            // Buscar hacia arriba el primer ancestro con scroll hacia abajo
            while (parent) {
                if (parent.scrollHeight > parent.clientHeight + 50) {
                    return parent;
                }
                parent = parent.parentElement;
            }
            return null;
        """, phone_field)

        if not scrollable_panel:
            print("❌ No se encontró contenedor scrollable")
            return False

        print("✓ Contenedor scrollable padre encontrado")

        # 🔑 Hacer scroll hacia ABAJO en incrementos de 100px (equivalente a clics en flecha inferior)
        print("Realizando scroll hacia ABAJO en incrementos de 100px...")

        max_attempts = 10
        for attempt in range(max_attempts):
            # Verificar si el campo es visible
            is_visible = phone_field.is_displayed()

            if is_visible:
                print(f"✓ Campo de teléfono visible después de {attempt} incrementos")
                return True

            # Hacer scroll hacia abajo
            self.driver.execute_script("""
                var panel = arguments[0];
                panel.scrollTop += 100;
            """, scrollable_panel)

            print(f"  Scroll {attempt + 1}/{max_attempts} (+100px)")
            time.sleep(0.4)  # Pausa para ver el movimiento

        print("⚠️ Campo de teléfono no visible después de máximo scroll")
        return False

    def open_phone_modal(self):
        print("\nAbriendo modal de teléfono...")

        # 🔑 Hacer scroll hacia ABAJO hasta que el teléfono sea visible
        phone_visible = self.scroll_panel_down_until_phone_visible()

        if not phone_visible:
            print("⚠️ Intentando scroll alternativo...")
            # Fallback: scroll general hacia abajo
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)

        # Encontrar el campo de teléfono
        phone_field = self.driver.find_element(*self.phone_input)

        # Verificar visibilidad
        is_visible = phone_field.is_displayed()
        print(f"✓ Campo visible final: {is_visible}")

        # Hacer clic en el campo
        print("Haciendo clic en el campo de teléfono...")
        try:
            phone_field.click()
            print("✓ Clic realizado")
        except:
            print("⚠️ Usando JavaScript para hacer clic")
            self.driver.execute_script("arguments[0].click();", phone_field)
            print("✓ Clic realizado con JavaScript")

        # Esperar modal
        time.sleep(2.5)

        # Verificar modal
        try:
            modal = self.wait.until(EC.presence_of_element_located(self.phone_modal))
            print("✓ Modal de teléfono abierto")
            return True
        except:
            print("❌ Modal no apareció")
            self.driver.save_screenshot("modal_error.png")
            print("📸 Captura guardada: modal_error.png")
            return False


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        print("✓ Navegador iniciado y maximizado")

    def test_v4_final_phone_modal(self):
        url = data.urban_routes_url.strip()
        print(f"✓ Cargando URL: {url}")
        self.driver.get(url)

        routes_page = UrbanRoutesPage(self.driver)

        # Configurar ruta
        routes_page.set_route(data.address_from, data.address_to)

        # Seleccionar Comfort
        routes_page.select_comfort_tariff()

        # Abrir modal de teléfono
        modal_opened = routes_page.open_phone_modal()

        assert modal_opened, "El modal de teléfono no se abrió"

        print("\n==========================================")
        print("✅ VERSIÓN 4 FINAL: PRUEBA EXITOSA")
        print("==========================================")
        print("Pasos completados:")
        print("  ✓ Ventana maximizada")
        print("  ✓ Direcciones ingresadas")
        print("  ✓ Botón 'Pedir un taxi' clickeado")
        print("  ✓ Tarifas aparecieron")
        print("  ✓ Tarifa Comfort seleccionada")
        print("  ✓ Campo de teléfono encontrado en DOM")
        print("  ✓ Scroll hacia ABAJO realizado en panel izquierdo")
        print("  ✓ Campo de teléfono visible")
        print("  ✓ Clic en campo de teléfono")
        print("  ✓ Modal de teléfono abierto")
        print("\nPróximo paso: Ingresar número en el modal")

    @classmethod
    def teardown_class(cls):
        if cls.driver:
            time.sleep(5)
            cls.driver.quit()
            print("✓ Navegador cerrado")


if __name__ == "__main__":
    test = TestUrbanRoutes()
    test.setup_class()
    try:
        test.test_v4_final_phone_modal()
    finally:
        test.teardown_class()