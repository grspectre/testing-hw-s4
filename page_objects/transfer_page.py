from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class TransferPage:
    """Page Object для страницы переводов"""
    
    # Локаторы
    RUBLES_BLOCK = (By.XPATH, "(//div[@role='button'])[1]")
    DOLLARS_BLOCK = (By.XPATH, "(//div[@role='button'])[2]")
    EUROS_BLOCK = (By.XPATH, "(//div[@role='button'])[3]")
    
    CARD_NUMBER_FIELD = (By.XPATH, "//h3[contains(text(),'Номер карты')]/following-sibling::input[@type='text']")
    TRANSFER_AMOUNT_FIELD = (By.XPATH, "//h3[contains(text(),'Сумма перевода')]/following-sibling::input[@type='text']")
    
    TRANSFER_BUTTON = (By.XPATH, "//button[.//span[text()='Перевести']]")
    
    COMMISSION_TEXT = (By.ID, "comission")
    ERROR_MESSAGE = (By.XPATH, "//span[@style='font-size: 15px; color: red;']")
    INSUFFICIENT_FUNDS_MESSAGE = (By.XPATH, "//*[contains(text(), 'Недостаточно средств')]")
    
    BALANCE_TEXT = (By.ID, "rub-sum")
    RESERVED_TEXT = (By.ID, "rub-reserved")
    
    CONFIRM_DIALOG = (By.CLASS_NAME, "confirm-dialog")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    # Проверка появления alert и работа с ним
    def handle_alert(self, timeout=10):
        try:
            # Ожидание появления alert
            wait = WebDriverWait(self.driver, timeout)
            alert = wait.until(EC.alert_is_present())
            
            # Получение текста alert (если нужно)
            alert_text = alert.text
            print(f"Alert появился с текстом: {alert_text}")
            
            # Принятие alert (нажатие OK)
            alert.accept()
            
            return True
        except TimeoutException:
            print("Alert не появился в течение указанного времени")
            return False

    # Или более простой вариант без ожидания
    def check_and_accept_alert(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            print(f"Alert обнаружен: {alert_text}")
            alert.accept()  # Для принятия (OK)
            # alert.dismiss()  # Для отмены (Cancel)
            return True
        except:
            print("Alert не обнаружен")
            return False

    def open_page(self, balance=30000, reserved=20000):
        """Открытие страницы с заданными параметрами баланса"""
        url = f"http://localhost:8000/?balance={balance}&reserved={reserved}"
        self.driver.get(url)
        return self
    
    def click_rubles_block(self):
        """Клик по блоку 'Рубли'"""
        rubles_block = self.wait.until(EC.element_to_be_clickable(self.RUBLES_BLOCK))
        rubles_block.click()
        return self
    
    def click_dollars_block(self):
        """Клик по блоку 'Доллары'"""
        dollars_block = self.wait.until(EC.element_to_be_clickable(self.DOLLARS_BLOCK))
        dollars_block.click()
        return self
    
    def click_euros_block(self):
        """Клик по блоку 'Евро'"""
        euros_block = self.wait.until(EC.element_to_be_clickable(self.EUROS_BLOCK))
        euros_block.click()
        return self
    
    def enter_card_number(self, card_number):
        """Ввод номера карты"""
        card_field = self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_FIELD))
        card_field.clear()
        card_field.send_keys(card_number)
        return self
    
    def enter_transfer_amount(self, amount):
        """Ввод суммы перевода"""
        amount_field = self.wait.until(EC.presence_of_element_located(self.TRANSFER_AMOUNT_FIELD))
        amount_field.clear()
        amount_field.send_keys(str(amount))
        return self
    
    def click_transfer_button(self):
        """Клик по кнопке 'Перевести'"""
        transfer_btn = self.wait.until(EC.element_to_be_clickable(self.TRANSFER_BUTTON))
        transfer_btn.click()
        return self
    
    def is_card_number_field_visible(self):
        """Проверка видимости поля номера карты"""
        try:
            self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_FIELD))
            return True
        except TimeoutException:
            return False
    
    def is_transfer_amount_field_visible(self):
        """Проверка видимости поля суммы перевода"""
        try:
            self.wait.until(EC.presence_of_element_located(self.TRANSFER_AMOUNT_FIELD))
            return True
        except TimeoutException:
            return False
    
    def is_transfer_button_enabled(self):
        """Проверка активности кнопки перевода"""
        try:
            button = self.driver.find_element(*self.TRANSFER_BUTTON)
            return button.is_enabled()
        except NoSuchElementException:
            return False
    
    def is_transfer_button_visible(self):
        """Проверка видимости кнопки перевода"""
        try:
            self.driver.find_element(*self.TRANSFER_BUTTON)
            return True
        except NoSuchElementException:
            return False
    
    def get_commission_text(self):
        """Получение текста комиссии"""
        try:
            commission_element = self.driver.find_element(*self.COMMISSION_TEXT)
            return commission_element.text
        except NoSuchElementException:
            return ""
    
    def get_error_message(self):
        """Получение текста ошибки"""
        try:
            error_element = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_element.text
        except NoSuchElementException:
            return ""
    
    def is_insufficient_funds_message_visible(self):
        """Проверка видимости сообщения о недостатке средств"""
        try:
            self.driver.find_element(*self.INSUFFICIENT_FUNDS_MESSAGE)
            return True
        except NoSuchElementException:
            return False
    
    def is_confirm_dialog_visible(self):
        """Проверка видимости диалога подтверждения"""
        try:
            self.wait.until(EC.presence_of_element_located(self.CONFIRM_DIALOG))
            return True
        except TimeoutException:
            return False
    
    def get_card_number_field_value(self):
        """Получение значения поля номера карты"""
        try:
            field = self.driver.find_element(*self.CARD_NUMBER_FIELD)
            return field.get_attribute("value")
        except NoSuchElementException:
            return ""
    
    def get_transfer_amount_field_value(self):
        """Получение значения поля суммы перевода"""
        try:
            field = self.driver.find_element(*self.TRANSFER_AMOUNT_FIELD)
            return field.get_attribute("value")
        except NoSuchElementException:
            return ""
    
    def is_card_number_field_focused(self):
        """Проверка фокуса на поле номера карты"""
        try:
            field = self.driver.find_element(*self.CARD_NUMBER_FIELD)
            return field == self.driver.switch_to.active_element
        except NoSuchElementException:
            return False
    
    def get_balance_text(self):
        """Получение текста баланса"""
        try:
            balance_element = self.driver.find_element(*self.BALANCE_TEXT)
            return balance_element.text
        except NoSuchElementException:
            return ""
    
    def get_reserved_text(self):
        """Получение текста резерва"""
        try:
            reserved_element = self.driver.find_element(*self.RESERVED_TEXT)
            return reserved_element.text
        except NoSuchElementException:
            return ""
