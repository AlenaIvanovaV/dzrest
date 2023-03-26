from tests.conftest import demoshop
from selene import have
import allure




def test_cart(chrome_browser):
    response = demoshop.post('/login', data={'Email': 'angel40995@inbox.ru', 'Password': 'qwerty'},
                             allow_redirects=False)
    response = demoshop.post('/addproducttocart/catalog/31/1/1')
    assert response.status_code == 200
    chrome_browser.open('')
    chrome_browser.element('#topcartlink .cart-qty').click()
    chrome_browser.element('#topcartlink .cart-qty').should(have.text('(1)'))
    with allure.step('Deleting products from cart'):
        chrome_browser.open('')
        chrome_browser.element('.ico-cart .cart-label').click()
        chrome_browser.element('.qty-input').clear().set_value('0')
        chrome_browser.element('.update-cart-button').click()

def test_wishlist(chrome_browser):
    with allure.step('Adding product to Wishlist'):
        response = demoshop.post('/addproducttocart/details/14/2')
        assert response.status_code == 200
        chrome_browser.open('')
        chrome_browser.element('.ico-wishlist .wishlist-qty').should(have.text('(1)')).click()
        chrome_browser.element('.cart-item-row .product').should(have.text('Black & White Diamond Heart'))

    with allure.step('Deleting products from wishlist'):
        chrome_browser.open('')
        chrome_browser.element('.ico-wishlist .wishlist-qty').click()
        chrome_browser.element('[name="removefromcart"]').click()
        chrome_browser.element('.update-wishlist-button').click()
        chrome_browser.element('.wishlist-content').should(have.exact_text('The wishlist is empty!'))
