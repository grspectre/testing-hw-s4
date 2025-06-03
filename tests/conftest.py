import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def pytest_addoption(parser):
    """Добавление опций командной строки для pytest"""
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome",
        help="Browser to run tests (chrome or firefox)"
    )
    parser.addoption(
        "--headless", 
        action="store_true", 
        default=False,
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--base-url", 
        action="store", 
        default="http://localhost:8000",
        help="Base URL for tests"
    )

@pytest.fixture(scope="session")
def browser_name(request):
    """Получение имени браузера из параметров командной строки"""
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def headless(request):
    """Проверка режима headless"""
    return request.config.getoption("--headless")

@pytest.fixture(scope="session")
def base_url(request):
    """Получение базового URL"""
    return request.config.getoption("--base-url")

@pytest.fixture
def driver(browser_name, headless):
    """Создание экземпляра WebDriver"""
    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()
