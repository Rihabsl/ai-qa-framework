import pytest
import allure

SITE_URL   = 'https://www.saucedemo.com'
VALID_USER = 'standard_user'
VALID_PASS = 'secret_sauce'

@allure.feature('UI — Saucedemo')
class TestSauceDemo:

    @allure.title('Page de login — chargement correct')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_page_loads(self, page):
        page.goto(SITE_URL)
        assert 'Swag Labs' in page.title()
        assert page.is_visible('#user-name')
        assert page.is_visible('#password')
        assert page.is_visible('#login-button')
        screenshot = page.screenshot()
        allure.attach(screenshot, 'login_page', allure.attachment_type.PNG)

    @allure.title('Login valide — redirection vers inventaire')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, page):
        page.goto(SITE_URL)
        page.fill('#user-name', VALID_USER)
        page.fill('#password', VALID_PASS)
        page.click('#login-button')
        assert '/inventory.html' in page.url

    @allure.title('Login invalide — message erreur affiché')
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_login(self, page):
        page.goto(SITE_URL)
        page.fill('#user-name', 'wrong_user')
        page.fill('#password', 'wrong_pass')
        page.click('#login-button')
        error = page.locator('[data-test="error"]')
        assert error.is_visible()

    @allure.title('Self-healing — sélecteur cassé réparé par IA')
    @allure.severity(allure.severity_level.NORMAL)
    def test_self_healing_demo(self, page, healer):
        page.goto(SITE_URL)
        healer.safe_fill(page, '#broken-username',
                         VALID_USER, 'champ username du formulaire')
        healer.safe_fill(page, '#broken-password',
                         VALID_PASS, 'champ mot de passe du formulaire')
        healer.safe_click(page, '#broken-submit',
                          'bouton de connexion du formulaire')
        assert '/inventory.html' in page.url
        print(healer.get_healing_report())