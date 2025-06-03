import pytest
from page_objects.transfer_page import TransferPage

class TestBalanceValidation:
    """Тесты валидации баланса и резерва"""
    
    @pytest.mark.smoke
    def test_reserve_not_greater_than_balance(self, driver):
        """Тест: Сумма резерва НЕ больше суммы на счету"""
        page = TransferPage(driver)
        page.open_page(balance=50000, reserved=30000)
        
        # Проверяем отображение корректных значений
        balance_text = page.get_balance_text()
        reserved_text = page.get_reserved_text()
        
        assert "50" in balance_text or "50'000" in balance_text
        assert "30" in reserved_text or "30'000" in reserved_text
    
    @pytest.mark.critical
    def test_reserve_greater_than_balance(self, driver):
        """Тест: Сумма резерва больше суммы на счету"""
        page = TransferPage(driver)
        page.open_page(balance=50000, reserved=60000)
        
        # Проверяем, что появилось сообщение об ошибке
        error_message = page.get_error_message()
        assert "Резерв" in error_message and "больше" in error_message
    
    @pytest.mark.regression
    @pytest.mark.parametrize("balance", [0, -10000])
    def test_zero_negative_balance(self, driver, balance):
        """Тест: Нулевая и отрицательная сумма 'На счету'"""
        page = TransferPage(driver)
        page.open_page(balance=balance, reserved=20000)
        
        # Проверяем, что появилось сообщение об ошибке
        error_message = page.get_error_message()
        assert "На счету" in error_message or "баланс" in error_message.lower()
    
    @pytest.mark.regression
    @pytest.mark.parametrize("reserved", [0, -10000])
    def test_zero_negative_reserved(self, driver, reserved):
        """Тест: Нулевая и отрицательная сумма 'Резерв'"""
        page = TransferPage(driver)
        page.open_page(balance=20000, reserved=reserved)
        
        # Проверяем, что появилось сообщение об ошибке для отрицательных значений
        if reserved < 0:
            error_message = page.get_error_message()
            assert "Резерв" in error_message or "резерв" in error_message.lower()
    
    @pytest.mark.regression
    @pytest.mark.parametrize("balance,reserved", [
        (0, 0),
        (-10000, -10000),
    ])
    def test_zero_negative_both_values(self, driver, balance, reserved):
        """Тест: Нулевое и отрицательное значение 'На счету' и 'Резерв'"""
        page = TransferPage(driver)
        page.open_page(balance=balance, reserved=reserved)
        
        # Проверяем, что появилось сообщение об ошибке для отрицательных значений
        if balance < 0 or reserved < 0:
            error_message = page.get_error_message()
            assert len(error_message) > 0
