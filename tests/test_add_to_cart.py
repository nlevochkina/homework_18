import allure
import requests
from allure_commons.types import AttachmentType
from selene import browser, have


@allure.title('Автотест на добавление товара в корзину авторизованным пользователем')
def test_add_to_cart_auth_user():
    with allure.step('Авторизовываемся через API'):
        login = requests.post(url='https://demowebshop.tricentis.com/login',
                              data={'email': 'qaguru1@example.com', 'password': '123456', 'RememberMe': False},
                              allow_redirects=False)
        allure.attach(body=login.text,
                      name='response',
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')
        allure.attach(body=str(login.cookies),
                      name='cookie',
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')

    with allure.step('Получаем cookie через API'):
        cookie = login.cookies.get('NOPCOMMERCE.AUTH')
        browser.open('https://demowebshop.tricentis.com/')
        browser.driver.add_cookie({'name': 'NOPCOMMERCE.AUTH', 'value': cookie})
        browser.open('https://demowebshop.tricentis.com/')

    with allure.step('Проверяем, что авторизация произошла'):
        browser.element('.account').should(have.text('qaguru1@example.com'))

    with allure.step('Добавляем товар в корзину через API'):
        requests.post(url='https://demowebshop.tricentis.com/addproducttocart/details/31/1',
                      cookies={'NOPCOMMERCE.AUTH': cookie})
        allure.attach(body=str(login.cookies),
                      name='cookie',
                      attachment_type=AttachmentType.TEXT,
                      extension='txt')

    with allure.step('Провряем, что товар добавлен в корзину'):
        browser.open('https://demowebshop.tricentis.com/cart')
        browser.element('.product-name').should(have.text('14.1-inch Laptop'))


@allure.title('Автотест на добавление товара в корзину неавторизованным пользователем')
def test_add_to_cart_user():
    with allure.step('Добавляем товар в корзину через API'):
        response = requests.post(url='https://demowebshop.tricentis.com/addproducttocart/details/31/1')

    with allure.step('Провряем, что товар добавлен в корзину'):
        assert response.status_code == 200
