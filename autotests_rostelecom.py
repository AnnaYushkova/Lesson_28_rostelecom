import pytest
import allure

from pages.auth_page import AuthPage
from pages.registration_page import RegPage


@allure.story("Тест-кейс EXP-001: Корректное отображение 'Стандартной страницы авторизации'")
def test_start_page_is_correct(web_browser):
    page = AuthPage(web_browser)
    phone_tab_class = page.phone_tab.get_attribute("class")
    assert phone_tab_class == "rt-tab rt-tab--small rt-tab--active"
    assert page.phone.is_clickable()
    assert page.password.is_clickable()
    assert page.btn_login.is_clickable()
    assert page.registration_link.is_clickable()
    assert page.auth_title.get_text() == "Авторизация"
    assert page.logo_lk.get_text() == "Личный кабинет"


@pytest.mark.xfail(reason="Расположение элементов на странице не соответсвует ТЗ")
@allure.story("Тест-кейс EXP-002 (Bugs-BR-001): Проверка элементов в левом и правом блоках страницы")
def test_location_of_page_blocks(web_browser):
    page = AuthPage(web_browser)
    assert page.auth_form.find(timeout=1)
    assert page.lk_form.find(timeout=1)


@pytest.mark.xfail(reason="Название вкладки 'Номер' не соответствует постановке задачи")
@allure.story("Тест-кейс EXP-003(Bugs-BR-002): Проверка названия вкладки 'Номер'")
def test_phone_tab(web_browser):
    page = AuthPage(web_browser)
    assert page.phone_tab.get_text() == "Номер"


@pytest.mark.xfail(reason="Кнопка должна иметь текст 'Продолжить'")
@allure.story("Тест-кейс EXP-004(Bugs-BR-003): Проверка названия кнопки 'Продолжить' в форме 'Регистрация'")
def test_registration_page_and_continue_button(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    assert reg_page.name_field_text.get_text() == "Имя"
    assert reg_page.last_name_field_text.get_text() == "Фамилия"
    assert reg_page.region_field_text.get_text() == "Регион"
    assert reg_page.email_or_mobile_phone_field_text.get_text() == "E-mail или мобильный телефон"
    assert reg_page.password_field_text.get_text() == "Пароль"
    assert reg_page.password_confirmation_field_text.get_text() == "Подтверждение пароля"
    assert reg_page.continue_button.get_text() == "Продолжить"


@allure.story("Тест-кейс EXP-005: Регистрация пользователя с пустым полем 'Имя'")
def test_registration_page_with_empty_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('')
    reg_page.last_name_field.send_keys("Тестова")
    reg_page.email_or_mobile_phone_field.send_keys("testtest@mail.ru")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


@allure.story("Тест-кейс EXP-006: Регистрация пользователя со значением в поле 'Имя' меньше 2 символов")
def test_registration_with_name_less_than_2_symbols(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('Т')
    reg_page.last_name_field.send_keys("Тестова")
    reg_page.email_or_mobile_phone_field.send_keys("testtest@mail.ru")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


@allure.story("Тест-кейс EXP-007: Регистрация пользователя со значением в поле 'Имя' превышающим 30 символов")
def test_registration_with_name_more_than_30_symbols(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('абвгдеёжзийклмнопрстуфхцчшщъьэю')
    reg_page.last_name_field.send_keys("Тестова")
    reg_page.email_or_mobile_phone_field.send_keys("testetst@mail.ru")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


@allure.story("Тест-кейс EXP-008: Регистрация пользователя с цифрами в поле 'Фамилия'")
def test_registration_with_numeric_last_name(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Тест")
    reg_page.last_name_field.send_keys("123456789")
    reg_page.email_or_mobile_phone_field.send_keys("testtest@mail.ru")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


@allure.story("Тест-кейс EXP-009: Регистрация пользователя с цифрами в поле 'Имя'")
def test_registration_with_numeric_name(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("123456789")
    reg_page.last_name_field.send_keys("Тестова")
    reg_page.email_or_mobile_phone_field.send_keys("testtest@mail.ru")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


@allure.story("Тест-кейс EXP-010: Регистрация пользователя с именем на латинице")
def test_registration_with_latin_name(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Test")
    reg_page.last_name_field.send_keys("Тестова")
    reg_page.email_or_mobile_phone_field.send_keys("testtest@mail.ru")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


@allure.story("Тест-кейс EXP-011: Регистрация пользователя с фамилией на латинице")
def test_registration_with_latin_last_name(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Тест")
    reg_page.last_name_field.send_keys("Testova")
    reg_page.email_or_mobile_phone_field.send_keys("testtest@mail.ru")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


@allure.story("Тест-кейс EXP-012: Регистрация пользователя с уже зарегистрированным номером")
def test_registration_of_an_already_registered_user(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Тест")
    reg_page.last_name_field.send_keys("Тестова")
    reg_page.email_or_mobile_phone_field.send_keys("+77777777777")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible


@allure.story("Тест-кейс EXP-013(Bugs-BR-004): Проверка значка 'х' - закрыть всплывающее окно оповещения")
@pytest.mark.xfail(reason="Должен быть значок закрыть 'х'")
def test_close_button_in_notification_form(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Тест")
    reg_page.last_name_field.send_keys("Тестова")
    reg_page.email_or_mobile_phone_field.send_keys("+77777777777")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    assert reg_page.login_button.get_text() == 'Войти'
    assert reg_page.recover_password_button.get_text() == 'Восстановить пароль'
    assert reg_page.close_button.get_text() == 'x'


@allure.story("Тест-кейс EXP-014: При регистрации пользователя введен пароль содержащий менее 8 символов")
def test_short_password_during_registration(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Тест")
    reg_page.last_name_field.send_keys("Тестова")
    reg_page.email_or_mobile_phone_field.send_keys("testtest@mail.ru")
    reg_page.password_field.send_keys("Test123")
    reg_page.password_confirmation_field.send_keys("Test123")
    reg_page.continue_button.click()
    assert reg_page.error_message_password.get_text() == "Длина пароля должна быть не менее 8 символов"


@allure.story("Тест-кейс EXP-015: При регистрация пользователя в поле 'Фамилия' введено значение, "
              "содержащее недопустимые символы вместо кириллицы")
def test_instead_of_cyrillic_invalid_characters(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Тест")
    reg_page.last_name_field.send_keys("!!!@@@")
    reg_page.email_or_mobile_phone_field.send_keys("testtest@mail.ru")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    assert reg_page.message_must_be_filled_in_cyrillic.get_text() == \
           "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


@allure.story("Тест-кейс EXP-016: Значения в поле ввода 'Пароль' и поле ввода 'Подтверждение пароля' "
              "в форме 'Регистрация' не совпадают")
def test_password_and_password_confirmation_do_not_match(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Тест")
    reg_page.last_name_field.send_keys("Тестова")
    reg_page.email_or_mobile_phone_field.send_keys("testest@mail.ru")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123456")
    reg_page.continue_button.click()
    assert reg_page.message_passwords_dont_match.get_text() == "Пароли не совпадают"


@allure.story("Тест-кейс EXP-017: Не валидный email в поле ввода 'Email или мобильный телефон' в форме регистрация")
def test_invalid_email_or_mobile_phone(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Тест")
    reg_page.last_name_field.send_keys("Тестова")
    reg_page.email_or_mobile_phone_field.send_keys("test.test.ru")
    reg_page.password_field.send_keys("Qwerty123")
    reg_page.password_confirmation_field.send_keys("Qwerty123")
    reg_page.continue_button.click()
    assert reg_page.message_enter_the_phone_in_the_format.get_text() == "Введите телефон в формате +7ХХХХХХХХХХ или" \
                                                                        " +375XXXXXXXXX, или email " \
                                                                        "в формате example@email.ru"


@allure.story("Тест-кейс EXP-018: Вход по неправильному паролю в форме 'Авторизация' уже зарегистрированного "
              "пользователя, надпись 'Забыл пароль' перекрашивается в оранжевый цвет")
def test_authorization_for_user_with_invalid_password(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+77777777777')
    page.password.send_keys("Test")
    page.btn_login.click()
    assert page.message_invalid_username_or_password.get_text() == "Неверный логин или пароль"
    assert "rt-link--orange" in page.the_element_forgot_the_password.get_attribute('class')


@allure.story("Тест-кейс EXP-019: Ааутентификация зарегестрированного пользователя")
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys("+79651683318")
    page.password.send_keys("142536-Hn")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()
