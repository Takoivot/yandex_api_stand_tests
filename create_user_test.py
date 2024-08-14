import data
import sender_stand_request


def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_user_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," + user_body["address"] + ",,," + \
               user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_responce = sender_stand_request.post_new_user(user_body)

    assert user_responce.status_code == 400
    assert user_responce.json()["code"] == 400
    assert user_responce.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

def negative_assert_no_first_name(user_body):
    user_responce = sender_stand_request.post_new_user(user_body)

    assert user_responce.status_code == 400
    assert user_responce.json()["code"] == 400
    assert user_responce.json()["message"] == "Не все необходимые параметры были переданы"

# 1 test
def test_create_user_2_letter_in_first_name_get_success_response():
    user_body = get_user_body("Аа")
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_user_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," + user_body["address"] + ",,," + \
               user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

#2 test
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

#3 test
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")

#4 test
def test_create_user_16_letter_in_first_name_get_success_response():
    negative_assert_symbol("Аааааааааааааааа")

#5 test
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

#6 test
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")

#7 test
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и КО")

#8 test
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("#@%")

#9 test
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

#10 test
def test_create_user_no_first_name_get_error_response():
        # Копируется словарь с телом запроса из файла data в переменную user_body
        # Иначе можно потерять данные из исходного словаря
        user_body = data.user_body.copy()
        # Удаление параметра firstName из запроса
        user_body.pop("firstName")
        # Проверка полученного ответа
        negative_assert_no_first_name(user_body)

#11 test
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

#12 test
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    responce = sender_stand_request.post_new_user(user_body)

    assert responce.status_code == 400
