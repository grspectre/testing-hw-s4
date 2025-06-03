import pytest
from page_objects.transfer_page import TransferPage

class TestCurrencySelection:
    """Тесты выбора валют"""
    
    @pytest.mark.smoke
    def test_focus_on_card_field_when_selecting_rubles(self, driver):
        """Тест: Фокусировка на поле ввода карты при выборе счёта перевода"""
        page = TransferPage(driver)
        page.open_page(balance=10000, reserved=1)
        page.click_rubles_block()
        
        # Проверяем, что фокус установлен на поле номера карты
        assert page.is_card_number_field_focused()
    
    @pytest.mark.regression
    def test_default_amount_for_small_balance(self, driver):
        """Тест: Сумма по умолчанию равна доступной сумме, если она меньше тысячи"""
        page = TransferPage(driver)
        page.open_page(balance=2, reserved=1)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        
        # Проверяем, что в поле суммы перевода отображается доступная сумма
        default_amount = page.get_transfer_amount_field_value()
        assert default_amount == "1" or default_amount == ""
    
    @pytest.mark.regression
    def test_boundary_condition_transfer(self, driver):
        """Тест: Граничное условие для перевода"""
        page = TransferPage(driver)
        page.open_page(balance=2, reserved=1)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        
        # Доступная сумма = 2 - 1 = 1 рубль
        # Проверяем, что можно перевести доступную сумму
        page.enter_transfer_amount(1)
        assert page.is_transfer_button_visible()
    
    @pytest.mark.regression
    def test_sequential_transfers(self, driver):
        """Тест: Два последовательных перевода"""
        page = TransferPage(driver)
        page.open_page(balance=10000, reserved=1)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        page.enter_transfer_amount(10000)
        
        # Проверяем, что отображается ошибка недостатка средств
        assert page.is_insufficient_funds_message_visible()
        
        # Меняем последний символ номера карты
        page.enter_card_number("1212 2323 5666 5556")
        
        # Проверяем, что сумма сбросилась и кнопка активна
        default_amount = page.get_transfer_amount_field_value()
        commission_amount = page.get_commission_text()
        assert default_amount == "1000" and page.is_transfer_button_enabled() and commission_amount == "100"
    
    @pytest.mark.critical
    def test_dollar_transfer_not_working(self, driver):
        """Тест: Не должен работать перевод в долларах"""
        page = TransferPage(driver)
        page.open_page(balance=10000, reserved=1)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        page.enter_transfer_amount(1000)
        
        # Убеждаемся, что кнопка перевода доступна для рублей
        assert page.is_transfer_button_enabled()
        
        # Переключаемся на доллары
        page.click_dollars_block()
        
        # Проверяем, что кнопка перевода НЕ доступна
        assert not page.is_transfer_button_visible()
    
    @pytest.mark.critical
    def test_euro_transfer_not_working(self, driver):
        """Тест: Не должен работать перевод в евро"""
        page = TransferPage(driver)
        page.open_page(balance=10000, reserved=1)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        page.enter_transfer_amount(1000)
        
        # Убеждаемся, что кнопка перевода доступна для рублей
        assert page.is_transfer_button_enabled()
        
        # Переключаемся на евро
        page.click_euros_block()
        
        # Проверяем, что кнопка перевода НЕ доступна
        assert not page.is_transfer_button_visible()
