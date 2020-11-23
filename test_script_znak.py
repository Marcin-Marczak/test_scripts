from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import random


# Below are variables used in this script:
Login = 'testing.marcin@gmail.com'
PasswordLogin = 'Testing2019'

RandomLogin = str(random.randint(1, 1000000)) + "random@gmail.com"

letters = range(97, 122)
digits = random.randint(1, 9)
RandomPassword = ''
for i in range(3):
    RandomPassword += str(digits) + chr(random.choice(letters))

RandomPassword2 = RandomPassword


class Tests:

    @pytest.fixture()
    def setup(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.znak.com.pl/")
        self.driver.maximize_window()
        self.driver.find_element_by_id("onesignal-slidedown-cancel-button").click()
        self.driver.find_element(By.LINK_TEXT, "Logowanie").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("//button[@class='close']").click()
        yield
        self.driver.quit()

# test 01: login and logout using valid data (e-mail and password):
    def test_01_login_and_logout(self, setup):
        self.driver.find_element_by_id("inputUser").send_keys(Login)
        self.driver.find_element_by_id("inputPass").send_keys(PasswordLogin)
        self.driver.find_element_by_xpath("//input[@value='Zaloguj się']").click()
        assert self.driver.find_element_by_link_text("Wyloguj").is_displayed()
        self.driver.find_element_by_link_text("Wyloguj").click()
        self.driver.find_element_by_xpath("//button[@class='btn btn-danger btn-ok']").click()
        assert self.driver.find_element(By.LINK_TEXT, "Logowanie").is_displayed()

# test 02: create a new account using valid random e-mail and password (with login and logout):
    def test_02_create_an_random_account_and_login_logout(self, setup):
        self.driver.find_element_by_link_text("Nie masz konta?").click()
        self.driver.find_element_by_id("registerMail").send_keys(RandomLogin)
        random_login_to_use = RandomLogin
        self.driver.find_element_by_xpath("//input[@placeholder='Ustal hasło']").send_keys(RandomPassword)
        self.driver.find_element_by_xpath("//input[@placeholder='Powtórz hasło']").send_keys(RandomPassword2)
        random_password_to_use = RandomPassword
        self.driver.find_element_by_id("labelZgodaDane").click()
        self.driver.find_element_by_xpath("//button[@title='Zarejestruj się']").click()
        assert self.driver.find_element_by_link_text("strony logowania").is_displayed()
        self.driver.find_element_by_xpath("//button[@type='button']").click()
        self.driver.find_element_by_id("inputUser").send_keys(random_login_to_use)
        self.driver.find_element_by_id("inputPass").send_keys(random_password_to_use)
        self.driver.find_element_by_xpath("//input[@value='Zaloguj się']").click()
        assert self.driver.find_element_by_link_text("Wyloguj").is_displayed()
        self.driver.find_element_by_link_text("Wyloguj").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("//button[@class='btn btn-danger btn-ok']").click()
        assert self.driver.find_element(By.LINK_TEXT, "Logowanie").is_displayed()

# test 03: no possibility to create a new account using an e-mail that already is registered:
    def test_03_create_an_account_with_already_registered_email(self, setup):
        self.driver.find_element_by_link_text("Nie masz konta?").click()
        self.driver.find_element_by_id("registerMail").send_keys(Login)
        self.driver.find_element_by_xpath("//input[@placeholder='Ustal hasło']").send_keys(RandomPassword)
        self.driver.find_element_by_xpath("//input[@placeholder='Powtórz hasło']").send_keys(RandomPassword2)
        self.driver.find_element_by_id("labelZgodaDane").click()
        self.driver.find_element_by_xpath("//button[@title='Zarejestruj się']").click()
        error_message = "Istnieje konto dla adresu:testing.marcin@gmail.com."
        assert error_message in self.driver.find_element_by_id("alert-modal").get_attribute("textContent")

# test 04: no possibility to create a new account without consent to personal data processing:
    def test_04_create_an_account_without_personal_data_consent(self, setup):
        self.driver.find_element_by_link_text("Nie masz konta?").click()
        self.driver.find_element_by_id("registerMail").send_keys(RandomLogin)
        self.driver.find_element_by_xpath("//input[@placeholder='Ustal hasło']").send_keys(RandomPassword)
        self.driver.find_element_by_xpath("//input[@placeholder='Powtórz hasło']").send_keys(RandomPassword2)
        self.driver.find_element_by_xpath("//button[@title='Zarejestruj się']").click()
        data_consent_message = "Aby móc kupować w księgarni internetowej znak.com.pl, musisz potwierdzić, że zapoznałaś(eś) się z treścią regulaminu i akceptujesz jego postanowienia."
        assert data_consent_message in self.driver.find_element_by_xpath("//div[@id='messageZgodaDane']").text

# test 05: no possibility to login using invalid Login:
    def test_05_login_with_invalid_login(self, setup):
        self.driver.find_element_by_id("inputUser").send_keys(RandomLogin)
        self.driver.find_element_by_id("inputPass").send_keys(PasswordLogin)
        self.driver.find_element(By.XPATH, "//input[@value='Zaloguj się']").click()
        error_message = "Niepoprawny użytkownik lub hasło"
        assert error_message in self.driver.find_element_by_id("alert-modal").get_attribute("textContent")

# test 06: no possibility to login using invalid Password:
    def test_06_login_with_invalid_password(self, setup):
        self.driver.find_element_by_id("inputUser").send_keys(Login)
        self.driver.find_element_by_id("inputPass").send_keys(RandomPassword)
        self.driver.find_element(By.XPATH, "//input[@value='Zaloguj się']").click()
        error_message = "Niepoprawny użytkownik lub hasło"
        assert error_message in self.driver.find_element_by_id("alert-modal").get_attribute("textContent")