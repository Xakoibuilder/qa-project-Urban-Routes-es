import pytest
import data
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code


class TestUrbanRoutesScenarios:

    @pytest.fixture(autouse=True)
    def setup(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver = webdriver.Chrome(options=options)
        try:
            self.driver.get(data.urban_routes_url.strip())
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(UrbanRoutesPage.FROM_FIELD)
            )
        except Exception as e:
            self._safe_quit()
            raise
        yield
        self._safe_quit()

    def _safe_quit(self):
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
        except:
            pass

    def test_01_set_route(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        from_value = self.driver.find_element(*UrbanRoutesPage.FROM_FIELD).get_attribute('value')
        to_value = self.driver.find_element(*UrbanRoutesPage.TO_FIELD).get_attribute('value')
        assert from_value == data.address_from
        assert to_value == data.address_to

    def test_02_select_comfort(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_comfort_tariff()
        comfort_el = self.driver.find_element(*UrbanRoutesPage.COMFORT_TARIFF)
        assert "active" in comfort_el.get_attribute("class")

    def test_03_enter_phone(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_comfort_tariff()
        page.enter_phone_number(data.phone_number)
        phone_field = self.driver.find_element(*UrbanRoutesPage.PHONE_INPUT)
        assert phone_field.get_attribute('value') == data.phone_number

    def test_04_add_credit_card(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_comfort_tariff()
        page.enter_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        code_field = self.driver.find_element(*UrbanRoutesPage.PHONE_CODE_INPUT)
        code_field.clear();
        code_field.send_keys(code)
        self.driver.find_element(*UrbanRoutesPage.PHONE_CONFIRM_BUTTON).click()
        time.sleep(1.5)
        WebDriverWait(self.driver, 5).until(
            lambda d: d.find_element(*UrbanRoutesPage.PHONE_BUTTON).text.strip() != "Número de teléfono"
        )
        page.add_credit_card(data.card_number, data.card_code)
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(UrbanRoutesPage.PAYMENT_MODAL)
        )

    def test_05_send_message_to_driver(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_comfort_tariff()
        page.enter_phone_number(data.phone_number)
        self._complete_phone_and_payment(page)
        page.send_message_to_driver(data.message_for_driver)
        message_field = self.driver.find_element(*UrbanRoutesPage.MESSAGE_INPUT)
        assert message_field.get_attribute('value') == data.message_for_driver

    def test_06_request_blanket(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_comfort_tariff()
        page.enter_phone_number(data.phone_number)
        self._complete_phone_and_payment(page)
        page.request_blanket_and_napkins()
        blanket_switch = self.driver.find_element(*UrbanRoutesPage.BLANKET_SWITCH)
        assert blanket_switch.is_displayed()
        assert blanket_switch.is_enabled()

    def test_07_order_two_ice_creams(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_comfort_tariff()
        page.enter_phone_number(data.phone_number)
        self._complete_phone_and_payment(page)
        page.order_two_ice_creams()
        counter_value = self.driver.execute_script("""
            const counter = document.querySelector('div.counter-value');
            return counter ? counter.textContent.trim() : '0';
        """)
        assert counter_value == "2"

    def test_08_click_order_taxi_button(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_comfort_tariff()
        page.enter_phone_number(data.phone_number)
        self._complete_phone_and_payment(page)
        page.send_message_to_driver(data.message_for_driver)
        page.request_blanket_and_napkins()
        page.order_two_ice_creams()
        page.click_order_taxi_button()
        taxi_button = self.driver.find_element(*UrbanRoutesPage.FINAL_ORDER_BUTTON)
        assert taxi_button.is_displayed()

    def test_09_verify_taxi_search_modal(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.select_comfort_tariff()
        page.enter_phone_number(data.phone_number)
        self._complete_phone_and_payment(page)
        page.send_message_to_driver(data.message_for_driver)
        page.request_blanket_and_napkins()
        page.order_two_ice_creams()
        page.click_order_taxi_button()

        # V11: Esperar temporizador
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(UrbanRoutesPage.TIMER_ELEMENT)
        )
        timer_text = self.driver.find_element(*UrbanRoutesPage.TIMER_ELEMENT).text.strip()
        assert timer_text != ""
        assert ":" in timer_text

        # V11: Esperar que se agote
        WebDriverWait(self.driver, 60).until(
            EC.invisibility_of_element_located(UrbanRoutesPage.TIMER_ELEMENT)
        )

        # V11: Verificar cambio de modal
        details_button = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(UrbanRoutesPage.TRIP_DETAILS_BUTTON)
        )

        # V11: Clic en "Detalles del viaje"
        details_button.click()
        time.sleep(1)

        assert True

    def _complete_phone_and_payment(self, page):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(UrbanRoutesPage.PHONE_CODE_INPUT)
        )
        code = retrieve_phone_code(self.driver)
        code_field = self.driver.find_element(*UrbanRoutesPage.PHONE_CODE_INPUT)
        code_field.clear();
        code_field.send_keys(code)
        self.driver.find_element(*UrbanRoutesPage.PHONE_CONFIRM_BUTTON).click()
        time.sleep(1.5)
        WebDriverWait(self.driver, 5).until(
            lambda d: d.find_element(*UrbanRoutesPage.PHONE_BUTTON).text.strip() != "Número de teléfono"
        )
        page.add_credit_card(data.card_number, data.card_code)
        time.sleep(1)