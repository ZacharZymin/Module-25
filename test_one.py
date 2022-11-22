from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromiumService
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from settings import *
import pytest


@pytest.fixture(autouse=True)
def testing():
    # Download actually version chromedriver.exe
    pytest.driver = webdriver.Chrome(
        service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    pytest.driver.implicitly_wait(5)

    # Open page login
    pytest.driver.get(url_login)

    yield

    pytest.driver.quit()


def test_show_my_pets(testing):
    # Enter email
    pytest.driver.find_element(By.ID, "email").send_keys(valid_email)
    # Enter password
    pytest.driver.find_element(By.ID, "pass").send_keys(valid_password)
    # Push the button "submit"
    # WebDriverWait(pytest.driver, 10).until(EC.element_to_be_selected((By.XPATH, btn_submit)))
    pytest.driver.find_element(By.XPATH, btn_submit).click()
    # Push "burger menu"
    pytest.driver.find_element(By.CLASS_NAME, btn_burgerMenu).click()
    # Push the button "My pets"
    pytest.driver.find_element(By.XPATH, btn_mypets).click()

    ''' Collection of information'''

    # All pets here
    all_pets = pytest.driver.find_elements(By.XPATH, all_pets_path)
    # Half of the pets have a photo
    have_photo = pytest.driver.find_elements(By.XPATH, have_photo_path)
    # All pets have name, age and animal type
    descriptions = pytest.driver.find_elements(By.XPATH, descriptions_path)
    # Unique names
    unique_names = pytest.driver.find_elements(By.XPATH, unique_names_path)

    for i in range(len(all_pets)):
        count_pets = all_pets[i].text.split(": ")
        assert count_pets[1][0] == '5'
        assert have_photo[i].get_attribute('src') > '2'
        assert descriptions[i].text != ''
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        set_unique = set(unique_names)
        assert len(unique_names) == len(set_unique)
