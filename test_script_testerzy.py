from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import pytest
import time
import random


# The objective of this script is to automate the set of manual tests, dedicated to testerzy.pl,
# published previous on my website - this are the same tests, transformed into automated tests


# Below are variables used in this script:
# for test_01:
training = 'ISTQB® Poziom Podstawowy'

# for test_02:
name = ''
surname = ''
upper = range(97, 122)
for i in range(6):
    name += chr(random.choice(upper))
for i in range(6):
    surname += chr(random.choice(upper))
name_and_surname = name + ' ' + surname
email = str(random.randint(1000, 9999)) + 'random' + str(random.randint(1000, 9999)) + '@' + 'gmail.com'
phone_number = random.randint(100000000, 999999999)

# for test_03 and test_05:
search_event_name = 'Selenium Camp'

# for test_04:
partial_filter_search = 'Wymaga'
filter_search = 'Wymaganie'
filter_result_name_polish = 'wymaganie'
filter_result_name_english = 'requirement'

# for test_05:
len_search_event_name = len(search_event_name)
split_words_of_event_name = len(search_event_name.split(" "))


class Tests:

    @pytest.fixture()
    def setup(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(10)
        self.driver.get("https://testerzy.pl/")
        self.driver.maximize_window()
        self.driver.find_element_by_id("cookie-law-close").click()
        yield
        self.driver.quit()

    def test_01_testerzy_training_calendar(self, setup):
        self.driver.find_element_by_link_text("Szkolenia").click()
        self.driver.find_element_by_link_text("Przeglądaj").click()
        Select(self.driver.find_element_by_id("type")).select_by_visible_text("Online")
        Select(self.driver.find_element_by_id("training")).select_by_visible_text(training)
        time.sleep(3)
        for i in self.driver.find_elements_by_xpath("//div[@class='col-12 p-3']"):
            training_type = self.driver.find_element_by_xpath("//div[@class='training-city']").text
            assert training_type == 'online'
        for j in self.driver.find_elements_by_xpath("//div[@class='col-12 p-3']"):
            training_name = self.driver.find_element_by_xpath("//div[@class='caption']").text
            assert training_name == training


    def test_02_testerzy_contact_form(self, setup):
        self.driver.find_element_by_link_text("Kontakt").click()
        Select(self.driver.find_element_by_id("subject")).select_by_visible_text("Pytanie dotyczące szkoleń")
        self.driver.find_element_by_id("name").send_keys(name_and_surname)
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("phoneNumber").send_keys(phone_number)
        self.driver.find_element_by_xpath("//label[@class='custom-control-label']").click()
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        time.sleep(3)

        error_message = 'Pole wymagane.'
        assert error_message == self.driver.find_element_by_xpath("//div[@class='invalid-feedback']").text

    def test_03_testerzy_search(self, setup):
        self.driver.find_element_by_id("sb-search").click()
        self.driver.find_element_by_xpath("//input[@class='sb-search-input']").send_keys(search_event_name)
        self.driver.find_element_by_xpath("//input[@class='sb-search-input']").send_keys(Keys.ENTER)
        self.driver.find_element_by_xpath("//label[@for='areas_events']").click()
        time.sleep(3)

        assert 1 == len(self.driver.find_elements_by_xpath("//span[@class='event-type type-2']"))
        assert search_event_name == self.driver.find_element_by_xpath("//div[@class='caption article-title']/a").text

    def test_04_testerzy_knowledge_base(self, setup):
        self.driver.find_element_by_link_text("Słownik").click()
        self.driver.find_element_by_id("filter-search").send_keys(partial_filter_search)
        time.sleep(1)
        self.driver.find_element_by_id("filter-search").send_keys(Keys.ENTER)
        self.driver.find_element_by_link_text(filter_search).click()
        time.sleep(3)

        assert filter_result_name_polish == self.driver.find_element_by_xpath("//p[1]/strong").text
        assert filter_result_name_english == self.driver.find_element_by_xpath("//p[3]/strong").text

    def test_05_testerzy_character_counter(self, setup):
        self.driver.find_element_by_link_text("Licznik znaków").click()
        self.driver.find_element_by_id("firstInput_js").send_keys(search_event_name)
        self.driver.find_element_by_id("signsNumber").click()
        self.driver.find_element_by_id("wordsNumber").click()
        time.sleep(3)

        temp1 = self.driver.find_element_by_id("ilosc_js").text
        temp2 = temp1[21:]
        temp3 = self.driver.find_element_by_id("words_js").text
        temp4 = temp3[22:]
        assert temp2 == str(len_search_event_name)
        assert temp4 == str(split_words_of_event_name)