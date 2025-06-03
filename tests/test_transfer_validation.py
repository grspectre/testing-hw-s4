import pytest
from page_objects.transfer_page import TransferPage

class TestTransferValidation:
    """Тесты валидации переводов"""
    
    @pytest.mark.smoke
    def test_card_data_absent(self, driver):
        """Тест: Рублевый перевод. Данные карты отсутствуют"""
        page = TransferPage(driver)
        page.open_page(balance=30000, reserved=20000)
        page.click_rubles_block()
        
        # Проверяем, что поле номера карты пустое
        assert page.get_card_number_field_value() == ""
        
        # Проверяем, что поле суммы перевода отсутствует
        assert not page.is_transfer_amount_field_visible()
    
    @pytest.mark.smoke
    def test_card_data_correct(self, driver):
        """Тест: Рублевый перевод. Данные карты корректны"""
        page = TransferPage(driver)
        page.open_page(balance=30000, reserved=20000)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        
        # Проверяем, что появилось поле суммы перевода
        assert page.is_transfer_amount_field_visible()
        
        page.enter_transfer_amount(2000)
        
        # Проверяем расчет комиссии (10% от суммы)
        commission_text = page.get_commission_text()
        assert "200" in commission_text  # 10% от 2000
        
        # Проверяем, что кнопка перевода активна
        assert page.is_transfer_button_enabled()
        
        page.click_transfer_button()
        
        # Проверяем, что появился диалог подтверждения
        assert page.check_and_accept_alert()
    
    @pytest.mark.regression
    @pytest.mark.parametrize("card_number", [
        "123",  # < 16 цифр
        "12345678901234567",  # > 16 цифр
        "123456789012345",  # 15 цифр
        "abcd efgh ijkl mnop",  # буквы
        "!@#$ %^&* ()_+ ={}|",  # спецсимволы
    ])
    def test_card_data_incorrect(self, driver, card_number):
        """Тест: Рублевый перевод. Данные карты не корректны"""
        page = TransferPage(driver)
        page.open_page(balance=30000, reserved=20000)
        page.click_rubles_block()
        page.enter_card_number(card_number)
        
        # Проверяем, что блок суммы перевода НЕ отображается
        assert not page.is_transfer_amount_field_visible()
    
    @pytest.mark.critical
    def test_sufficient_funds(self, driver):
        """Тест: Рублевый перевод. Достаточно средств на счету"""
        page = TransferPage(driver)
        page.open_page(balance=30000, reserved=20000)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        page.enter_transfer_amount(1000)
        
        # Проверяем, что кнопка перевода доступна
        assert page.is_transfer_button_enabled()
        
        page.click_transfer_button()
        
        # Проверяем, что открыто окно подтверждения
        assert page.is_confirm_dialog_visible()
    
    @pytest.mark.critical
    def test_insufficient_funds(self, driver):
        """Тест: Рублевый перевод. НЕ достаточно средств на счету"""
        page = TransferPage(driver)
        page.open_page(balance=30000, reserved=20000)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        page.enter_transfer_amount(1000000)  # Большая сумма
        
        # Проверяем, что кнопка перевода НЕ доступна
        assert not page.is_transfer_button_enabled()
        
        # Проверяем, что отображается сообщение о недостатке средств
        assert page.is_insufficient_funds_message_visible()
    
    @pytest.mark.regression
    def test_negative_transfer_amount(self, driver):
        """Тест: Рублевый перевод. Отрицательная сумма перевода"""
        page = TransferPage(driver)
        page.open_page(balance=30000, reserved=20000)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        page.enter_transfer_amount(-1000)
        
        # Проверяем, что кнопка перевода НЕ доступна
        assert not page.is_transfer_button_enabled()
    
    @pytest.mark.regression
    def test_zero_transfer_amount(self, driver):
        """Тест: Рублевый перевод. Нулевая сумма перевода"""
        page = TransferPage(driver)
        page.open_page(balance=30000, reserved=20000)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        page.enter_transfer_amount(0)
        
        # Проверяем, что кнопка перевода НЕ доступна
        assert not page.is_transfer_button_enabled()
    
    @pytest.mark.smoke
    @pytest.mark.parametrize("amount,expected_commission", [
        (1000, 100),
        (2000, 200),
        (4500, 450),
        (10000, 1000),
    ])
    def test_commission_calculation(self, driver, amount, expected_commission):
        """Тест: Рублевый перевод. Расчет комиссии"""
        page = TransferPage(driver)
        page.open_page(balance=30000, reserved=20000)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        page.enter_transfer_amount(amount)
        
        # Проверяем, что комиссия равна 10% от введенной суммы
        commission_text = page.get_commission_text()
        assert str(expected_commission) in commission_text
    
    @pytest.mark.regression
    @pytest.mark.parametrize("invalid_amount", [
        "abc",  # буквы
        "!@#",  # спецсимволы
        "12.34.56",  # некорректный формат
        "",  # пустое значение
    ])
    def test_transfer_amount_validation(self, driver, invalid_amount):
        """Тест: Валидация поля 'Сумма перевода'"""
        page = TransferPage(driver)
        page.open_page(balance=30000, reserved=20000)
        page.click_rubles_block()
        page.enter_card_number("1212 2323 5666 5555")
        page.enter_transfer_amount(invalid_amount)
        
        # Проверяем, что кнопка перевода не активна при некорректных данных
        assert not page.is_transfer_button_enabled()
