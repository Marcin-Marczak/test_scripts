from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pytest
from faker import Faker
import time

# This script is dedicated to sign up to newsletter of NH Hotels.
# t_01 is a positive test - with valid data (user is able to sign up to newsletter),
# t_02 - t_10 are negative tests - with invalid data (user is not able to sign up to newsletter)

# Locators used in this script:
locator_name = "name"
locator_lastname = "lastname"
locator_email = "email"
locator_confirm_email = "confmail"
locator_country_language = "//div[@class='col-sm-6 col-md-4']"
locator_select_country = "//li[@data-original-index='171']"
locator_select_language = "//li[@data-original-index='4']"
locator_private_policy = "//label[@for='GDPR_flag_6']"
locator_send = "//input[@value='Send']"
locator_error = "//ul[@role='alert']/li"

# Variables used in asserts:
confirmation_text = 'THANK YOU FOR SUBSCRIBING TO OUR NEWSLETTER!'
error_message = 'This is required'
error_message_emails_not_match = 'The e-mails entered must match'
error_message_invalid_email = 'Not a valid email address'


class Tests:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.nh-hotels.com/")
        self.driver.maximize_window()
        self.driver.find_element_by_id("consent-prompt-submit").click()
        self.driver.find_element_by_link_text("Newsletter").click()
        yield
        self.driver.quit()

    def test_01_positive_all_data_valid(self):
        fake = Faker("ru")
        self.driver.find_element_by_id(locator_name).send_keys(fake.first_name_male())
        self.driver.find_element_by_id(locator_lastname).send_keys(fake.last_name_male())
        temp1 = fake.email()
        self.driver.find_element_by_id(locator_email).send_keys(temp1)
        self.driver.find_element_by_id(locator_confirm_email).send_keys(temp1)
        self.driver.find_elements_by_xpath(locator_country_language)[0].click()
        self.driver.find_element_by_xpath(locator_select_country).click()
        self.driver.find_elements_by_xpath(locator_country_language)[1].click()
        self.driver.find_elements_by_xpath(locator_select_language)[1].click()
        self.driver.find_element_by_xpath(locator_private_policy).click()
        self.driver.save_screenshot("screenshots/test_01_1_positive_all_data_valid.png")
        self.driver.find_element_by_xpath(locator_send).click()
        time.sleep(2)
        self.driver.save_screenshot("screenshots/test_01_2_positive_all_data_valid.png")
        assert confirmation_text == self.driver.find_element_by_xpath("//h2[@class='h3']").text

    def test_02_blank_name(self):
        fake = Faker("cz")
        self.driver.find_element_by_id(locator_lastname).send_keys(fake.last_name_female())
        temp2 = fake.email()
        self.driver.find_element_by_id(locator_email).send_keys(temp2)
        self.driver.find_element_by_id(locator_confirm_email).send_keys(temp2)
        self.driver.find_elements_by_xpath(locator_country_language)[0].click()
        self.driver.find_element_by_xpath(locator_select_country).click()
        self.driver.find_elements_by_xpath(locator_country_language)[1].click()
        self.driver.find_elements_by_xpath(locator_select_language)[1].click()
        self.driver.find_element_by_xpath(locator_private_policy).click()
        self.driver.find_element_by_xpath(locator_send).click()
        self.driver.save_screenshot("screenshots/test_02_blank_name.png")
        assert error_message == self.driver.find_element_by_xpath(locator_error).text

    def test_03_blank_last_name(self):
        fake = Faker("pl")
        self.driver.find_element_by_id(locator_name).send_keys(fake.first_name_male())
        temp3 = fake.email()
        self.driver.find_element_by_id(locator_email).send_keys(temp3)
        self.driver.find_element_by_id(locator_confirm_email).send_keys(temp3)
        self.driver.find_elements_by_xpath(locator_country_language)[0].click()
        self.driver.find_element_by_xpath(locator_select_country).click()
        self.driver.find_elements_by_xpath(locator_country_language)[1].click()
        self.driver.find_elements_by_xpath(locator_select_language)[1].click()
        self.driver.find_element_by_xpath(locator_private_policy).click()
        self.driver.find_element_by_xpath(locator_send).click()
        self.driver.save_screenshot("screenshots/test_03_blank_last_name.png")
        assert error_message == self.driver.find_element_by_xpath(locator_error).text

    def test_04_blank_email_and_confirm_email(self):
        fake = Faker("es")
        self.driver.find_element_by_id(locator_name).send_keys(fake.first_name_female())
        self.driver.find_element_by_id(locator_lastname).send_keys(fake.last_name_female())
        self.driver.find_elements_by_xpath(locator_country_language)[0].click()
        self.driver.find_element_by_xpath(locator_select_country).click()
        self.driver.find_elements_by_xpath(locator_country_language)[1].click()
        self.driver.find_elements_by_xpath(locator_select_language)[1].click()
        self.driver.find_element_by_xpath(locator_private_policy).click()
        self.driver.find_element_by_xpath(locator_send).click()
        self.driver.save_screenshot("screenshots/test_04_blank_email_and_confirm_email.png")
        assert error_message == self.driver.find_element_by_xpath(locator_error).text

    def test_05_blank_email(self):
        fake = Faker("fr")
        self.driver.find_elements_by_xpath(locator_country_language)[0].click()
        self.driver.find_element_by_xpath(locator_select_country).click()
        self.driver.find_elements_by_xpath(locator_country_language)[1].click()
        self.driver.find_elements_by_xpath(locator_select_language)[1].click()
        self.driver.find_element_by_xpath(locator_private_policy).click()
        self.driver.find_element_by_id(locator_name).send_keys(fake.first_name_male())
        self.driver.find_element_by_id(locator_lastname).send_keys(fake.last_name_male())
        self.driver.find_element_by_id(locator_confirm_email).send_keys(fake.email())
        self.driver.find_element_by_id(locator_confirm_email).send_keys(Keys.ENTER)
        self.driver.save_screenshot("screenshots/test_05_blank_email.png")
        assert error_message == self.driver.find_elements_by_xpath(locator_error)[0].text
        assert error_message_emails_not_match == self.driver.find_elements_by_xpath(locator_error)[1].text

    def test_06_blank_confirm_email(self):
        fake = Faker("it")
        self.driver.find_element_by_id(locator_name).send_keys(fake.first_name_female())
        self.driver.find_element_by_id(locator_lastname).send_keys(fake.last_name_female())
        self.driver.find_element_by_id(locator_email).send_keys(fake.email())
        self.driver.find_elements_by_xpath(locator_country_language)[0].click()
        self.driver.find_element_by_xpath(locator_select_country).click()
        self.driver.find_elements_by_xpath(locator_country_language)[1].click()
        self.driver.find_elements_by_xpath(locator_select_language)[1].click()
        self.driver.find_element_by_xpath(locator_private_policy).click()
        self.driver.find_element_by_xpath(locator_send).click()
        self.driver.save_screenshot("screenshots/test_06_blank_confirm_email.png")
        assert error_message_emails_not_match == self.driver.find_element_by_xpath(locator_error).text

    def test_07_invalid_emails(self):
        fake = Faker("de")
        self.driver.find_element_by_id(locator_name).send_keys(fake.first_name_male())
        self.driver.find_element_by_id(locator_lastname).send_keys(fake.last_name_male())
        temp7 = fake.word()
        self.driver.find_element_by_id(locator_email).send_keys(temp7)
        self.driver.find_element_by_id(locator_confirm_email).send_keys(temp7)
        self.driver.find_elements_by_xpath(locator_country_language)[0].click()
        self.driver.find_element_by_xpath(locator_select_country).click()
        self.driver.find_elements_by_xpath(locator_country_language)[1].click()
        self.driver.find_elements_by_xpath(locator_select_language)[1].click()
        self.driver.find_element_by_xpath(locator_private_policy).click()
        self.driver.find_element_by_xpath(locator_send).click()
        self.driver.save_screenshot("screenshots/test_07_invalid_emails.png")
        assert error_message_invalid_email == self.driver.find_element_by_xpath(locator_error).text

    def test_08_emails_not_match(self):
        fake = Faker("ja")
        self.driver.find_elements_by_xpath(locator_country_language)[0].click()
        self.driver.find_element_by_xpath(locator_select_country).click()
        self.driver.find_elements_by_xpath(locator_country_language)[1].click()
        self.driver.find_elements_by_xpath(locator_select_language)[1].click()
        self.driver.find_element_by_xpath(locator_private_policy).click()
        self.driver.find_element_by_id(locator_name).send_keys(fake.first_name_male())
        self.driver.find_element_by_id(locator_lastname).send_keys(fake.last_name_male())
        self.driver.find_element_by_id(locator_email).send_keys(fake.email())
        self.driver.find_element_by_id(locator_confirm_email).send_keys(fake.email())
        self.driver.find_element_by_xpath(locator_send).click()
        self.driver.save_screenshot("screenshots/test_08_emails_not_match.png")
        assert error_message_emails_not_match == self.driver.find_element_by_xpath(locator_error).text

    def test_09_without_privacy_policy_agree(self):
        fake = Faker("hu")
        self.driver.find_element_by_id(locator_name).send_keys(fake.first_name_female())
        self.driver.find_element_by_id(locator_lastname).send_keys(fake.last_name_female())
        temp8 = fake.email()
        self.driver.find_element_by_id(locator_email).send_keys(temp8)
        self.driver.find_element_by_id(locator_confirm_email).send_keys(temp8)
        self.driver.find_elements_by_xpath(locator_country_language)[0].click()
        self.driver.find_element_by_xpath(locator_select_country).click()
        self.driver.find_elements_by_xpath(locator_country_language)[1].click()
        self.driver.find_elements_by_xpath(locator_select_language)[1].click()
        self.driver.find_element_by_xpath(locator_send).click()
        self.driver.save_screenshot("screenshots/test_09_without_privacy_policy_agree.png")
        assert error_message == self.driver.find_element_by_xpath(locator_error).text

    def test_10_submit_blank_form(self):
        self.driver.find_element_by_xpath(locator_send).click()
        self.driver.save_screenshot("screenshots/test_10_submit_blank_form.png")
        assert error_message == self.driver.find_elements_by_xpath(locator_error)[0].text
        assert error_message == self.driver.find_elements_by_xpath(locator_error)[1].text
        assert error_message == self.driver.find_elements_by_xpath(locator_error)[2].text
        assert error_message == self.driver.find_elements_by_xpath(locator_error)[3].text
