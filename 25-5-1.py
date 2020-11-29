import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# зайти на главную страницу со всеми петами, всех пользователей

@pytest.mark.usefixtures("testing")
def test_show_my_pets():
    # Неявное ожидание всех элементов на странице
    pytest.driver.implicitly_wait(5)

    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('ren_ish@mail.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('mytestingstarts')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    # Переход на страницу с моими питомцами
    pytest.driver.find_element_by_css_selector('button[class="navbar-toggler"]').click()
    pytest.driver.find_element_by_class_name("nav-link").click()

    # Проверяем, что мы оказались на странице пользователя со списком его питомцев
    assert pytest.driver.find_element_by_tag_name('h2').text == "Renata"

    # Явное ожидание появления элементов на странице
    wait = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located(('id', 'all_my_pets')))

    # Считаем кол-во питомцев на странице, сверяем с количеством в профиле пользователя
    pets = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr')
    leftdiv = pytest.driver.find_element_by_xpath('//div[@class=".col-sm-4 left"]').text
    leftdivstr = str(leftdiv)
    numbers = []
    for s in leftdivstr.split():
        if s.isdigit():
            numbers.append(int(s))
    assert len(pets) == numbers[0]

    # проверка, что у каждой карточки есть фото, имя питомца, его возраст).
    images = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    breed = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    age = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    for i in range(len(pets)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert breed[i].text != ''
        assert age[i].text != ''
