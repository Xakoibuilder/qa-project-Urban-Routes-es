from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


class UrbanRoutesPage:
    FROM_FIELD = (By.ID, 'from')
    TO_FIELD = (By.ID, 'to')
    ORDER_TAXI_BUTTON = (By.CLASS_NAME, 'button.round')
    TARIFF_CARDS = (By.CLASS_NAME, 'tcard')
    COMFORT_TARIFF = (By.XPATH, "//div[contains(@class, 'tcard') and contains(., 'Comfort')]")
    PHONE_BUTTON = (By.CLASS_NAME, 'np-button')
    PHONE_INPUT = (By.ID, 'phone')
    PHONE_NEXT_BUTTON = (By.XPATH, "//button[text()='Siguiente']")
    PHONE_CODE_INPUT = (By.ID, 'code')
    PHONE_CONFIRM_BUTTON = (By.XPATH, "//button[text()='Confirmar']")
    PAYMENT_METHOD_SECTION = (By.XPATH, "//div[contains(@class, 'pp-text') and contains(., 'Método de pago')]")
    ADD_CARD_BUTTON = (By.XPATH, "//div[contains(@class, 'pp-title') and contains(., 'Agregar')]")
    PAYMENT_MODAL = (By.CSS_SELECTOR, "div.payment-picker.open")
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "div.card-number-input input")
    CARD_CODE_INPUT = (By.CSS_SELECTOR, "div.card-code input")
    CONFIRM_CARD_BUTTON = (By.CSS_SELECTOR, "div.pp-buttons > button:nth-child(1)")
    CLOSE_PAYMENT_MODAL_BUTTON = (By.CSS_SELECTOR, "div.payment-picker.open > div.modal > div.section.active > button")
    MESSAGE_INPUT = (By.ID, 'comment')
    REQS_HEADER = (By.CSS_SELECTOR, "div.reqs-header div.reqs-head")
    BLANKET_SWITCH = (By.CSS_SELECTOR, "div.reqs.open div.reqs-body div:nth-child(1) div.r-sw div span")
    ICE_CREAM_PLUS_BUTTON = (By.CSS_SELECTOR,
                             "div.reqs.open div.reqs-body div.r.r-type-group div.r-group-items div:nth-child(1) div.r-counter div.counter-plus")
    FINAL_ORDER_BUTTON = (By.CSS_SELECTOR, "div.smart-button-wrapper > button > span.smart-button-secondary")
    TIMER_ELEMENT = (By.CSS_SELECTOR, "div.order-header-time")
    TRIP_DETAILS_BUTTON = (By.CSS_SELECTOR, "div.order-buttons > div:nth-child(3) > button")
    DRIVER_NAME_ELEMENT = (By.CLASS_NAME, "order-header-title")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def set_route(self, from_address, to_address):
        from_el = self.wait.until(EC.element_to_be_clickable(self.FROM_FIELD))
        from_el.clear();
        from_el.send_keys(from_address)
        to_el = self.wait.until(EC.element_to_be_clickable(self.TO_FIELD))
        to_el.clear();
        to_el.send_keys(to_address)
        self.wait.until(EC.element_to_be_clickable(self.ORDER_TAXI_BUTTON)).click()
        time.sleep(1.5)
        self.wait.until(EC.presence_of_all_elements_located(self.TARIFF_CARDS))

    def select_comfort_tariff(self):
        comfort_el = self.wait.until(EC.element_to_be_clickable(self.COMFORT_TARIFF))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", comfort_el)
        time.sleep(0.5)
        comfort_el.click()
        time.sleep(1.5)

    def enter_phone_number(self, phone_number):
        payment_method = self.wait.until(EC.presence_of_element_located(self.PAYMENT_METHOD_SECTION))
        scrollable = self._find_scrollable_container(payment_method)
        for _ in range(15):
            try:
                phone_btn = self.driver.find_element(*self.PHONE_BUTTON)
                if phone_btn.is_displayed():
                    phone_btn.click()
                    break
            except:
                self.driver.execute_script("arguments[0].scrollTop += 150;", scrollable)
                time.sleep(0.3)
        time.sleep(1.5)
        phone_field = self.wait.until(EC.presence_of_element_located(self.PHONE_INPUT))
        phone_field.clear();
        phone_field.send_keys(phone_number)
        self.wait.until(EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON)).click()
        time.sleep(2.5)

    def add_credit_card(self, card_number, card_code):
        payment_section = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_SECTION))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                   payment_section)
        time.sleep(0.5)
        payment_section.click()
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()
        time.sleep(1.5)

        # V6: Número de tarjeta
        self.driver.execute_script(f"""
            var container = document.querySelector('div.card-number-input');
            if (container) {{
                var input = container.querySelector('input');
                if (input) {{
                    input.value = '{card_number}';
                    input.dispatchEvent(new Event('input', {{bubbles: true}}));
                    input.dispatchEvent(new Event('change', {{bubbles: true}}));
                }}
            }}
        """)
        time.sleep(0.5)

        # V6: CVV
        self.driver.execute_script(f"""
            var container = document.querySelector('div.card-code');
            if (container) {{
                var input = container.querySelector('input');
                if (input) {{
                    input.value = '{card_code}';
                    input.dispatchEvent(new Event('input', {{bubbles: true}}));
                    input.dispatchEvent(new Event('change', {{bubbles: true}}));
                }}
            }}
        """)
        time.sleep(0.5)

        # V6: Simular TAB (activa validación)
        self.driver.execute_script("""
            var cvvContainer = document.querySelector('div.card-code');
            if (cvvContainer) {
                var input = cvvContainer.querySelector('input');
                if (input) {
                    input.focus();
                    var tabEvent = new KeyboardEvent('keydown', {key: 'Tab', bubbles: true, cancelable: true});
                    input.dispatchEvent(tabEvent);
                    input.blur();
                }
            }
        """)
        time.sleep(1.2)

        # V6: Clic en "Agregar"
        self.driver.execute_script("""
            var confirmBtn = document.querySelector('div.pp-buttons > button:nth-child(1)');
            if (confirmBtn) {
                if (confirmBtn.disabled) confirmBtn.disabled = false;
                confirmBtn.click();
            }
        """)
        time.sleep(1.5)

        # V6: Cerrar modal
        self.driver.execute_script("""
            var closeBtn = document.querySelector('div.payment-picker.open > div.modal > div.section.active > button');
            if (closeBtn && closeBtn.offsetParent !== null) {
                closeBtn.click();
            }
        """)
        time.sleep(1)
        self.wait.until(EC.invisibility_of_element_located(self.PAYMENT_MODAL))

    def send_message_to_driver(self, message):
        message_field = self.wait.until(EC.presence_of_element_located(self.MESSAGE_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", message_field)
        time.sleep(0.5)
        message_field.clear();
        message_field.send_keys(message)

    def request_blanket_and_napkins(self):
        reqs_header = self.wait.until(EC.element_to_be_clickable(self.REQS_HEADER))
        if self._is_section_closed(reqs_header):
            reqs_header.click()
            time.sleep(0.8)
        blanket_switch = self.wait.until(EC.element_to_be_clickable(self.BLANKET_SWITCH))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                   blanket_switch)
        time.sleep(0.5)
        blanket_switch.click()

    def order_two_ice_creams(self):
        plus_button = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", plus_button)
        time.sleep(0.5)
        for _ in range(2):
            plus_button.click()
            time.sleep(0.6)

    def click_order_taxi_button(self):
        taxi_button = self.wait.until(EC.element_to_be_clickable(self.FINAL_ORDER_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", taxi_button)
        time.sleep(0.5)
        taxi_button.click()
        time.sleep(1.5)

    def verify_taxi_search_modal(self):
        timer = self.wait.until(EC.visibility_of_element_located(self.TIMER_ELEMENT))
        initial_time = timer.text.strip()
        assert initial_time != "", "El temporizador no muestra valor"
        assert ":" in initial_time, f"Formato de temporizador inválido: {initial_time}"
        return True

    def _find_scrollable_container(self, element):
        return self.driver.execute_script("""
            var el = arguments[0];
            while (el = el.parentElement) {
                if (el.scrollHeight > el.clientHeight + 50) return el;
            }
            return null;
        """, element)

    def _is_section_closed(self, header_element):
        return self.driver.execute_script("""
            var header = arguments[0];
            var section = header.closest('div.reqs');
            return section && !section.classList.contains('open');
        """, header_element)