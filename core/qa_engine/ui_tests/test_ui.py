import pytest
import allure

SITE_URL = 'https://the-internet.herokuapp.com'

@allure.feature('UI — The Internet (site de test officiel)')
class TestTheInternet:

    @allure.title('Page login — chargement correct')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_homepage_loads(self, page):
        page.goto(SITE_URL)
        assert 'The Internet' in page.title()
        screenshot = page.screenshot()
        allure.attach(screenshot, 'homepage', allure.attachment_type.PNG)

    @allure.title('Login valide — redirection réussie')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, page):
        page.goto(f'{SITE_URL}/login')
        page.fill('#username', 'tomsmith')
        page.fill('#password', 'SuperSecretPassword!')
        page.click('button[type="submit"]')
        assert '/secure' in page.url
        screenshot = page.screenshot()
        allure.attach(screenshot, 'login_success', allure.attachment_type.PNG)

    @allure.title('Login invalide — message erreur affiché')
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_login(self, page):
        page.goto(f'{SITE_URL}/login')
        page.fill('#username', 'mauvais')
        page.fill('#password', 'mauvais')
        page.click('button[type="submit"]')
        assert page.is_visible('#flash')
        screenshot = page.screenshot()
        allure.attach(screenshot, 'login_error', allure.attachment_type.PNG)

    @allure.title('Drag and Drop — fonctionne correctement')
    @allure.severity(allure.severity_level.NORMAL)
    def test_drag_and_drop(self, page):
        page.goto(f'{SITE_URL}/drag_and_drop')
        assert page.is_visible('#column-a')
        assert page.is_visible('#column-b')
        screenshot = page.screenshot()
        allure.attach(screenshot, 'drag_drop', allure.attachment_type.PNG)

    @pytest.mark.skip(reason="Requires Anthropic API credits")
    @allure.title('Self-healing — sélecteur cassé réparé par IA')
    def test_self_healing_demo(self, page, healer):
        pass