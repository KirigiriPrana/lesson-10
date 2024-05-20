import allure
import pytest
from EmployeeApi import EmployeeApi
from EmployeDB import EmployerTable

api = EmployeeApi("https://x-clients-be.onrender.com")
db = EmployerTable("postgresql://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx")

@allure.title("Получение списка работников в компании")
@allure.description("Получение списка работников в компании")
@allure.feature("READ")
@allure.severity("blocker")
def test_get_list():
    name = "My company"
    db.create_company(name)
    max_id = db.get_max_id_comp()

    api_result = api.get_employee_list(f'?company={max_id}')
         
    db_result = db.select_employers(max_id)
            
    with allure.step("Сравнить результаты длины списков сотрудников полученные через БД и API"):      
         assert len(api_result) == len(db_result)
           
    db.delete_company(max_id)


@allure.title("Добавить работника в компанию")
@allure.description("Добавить работника в компанию")
@allure.feature("CREATE")
@allure.severity("blocker")
def test_add_new_employer():
    name = "My company"
    db.create_company(name)
    max_id_c = db.get_max_id_comp()
             
    api_result_b = api.get_employee_list(f'?company={max_id_c}')
    
    db_result_b = db.select_employers(max_id_c)

    with allure.step("Добавить данные"):
        name_emp = 'Иван'
        la_name = 'Петров'
        phone_num = '+79969598584'
    db.create_employer('Иван', 'Петров', '+79969598584', max_id_c)

    
    api_result_a = api.get_employee_list(f'?company={max_id_c}')
     
    db_result_a = db.select_employers(max_id_c)

    with allure.step("Сравнить списки работников полученных в начале, что они равны"): 
        assert len(api_result_b) == len(db_result_b)
    with allure.step("Сравнить списки работников полученных в конце, что они равны"): 
        assert len(api_result_a) == len(db_result_a)
    with allure.step("Сравнить списки работников, что конечный список больше на 1-ого работника"):     
        assert len(db_result_a) - len(db_result_b) == 1
    with allure.step("Проверить поля. Поля заполнены верны"): 
        for employer in api_result_a:
            if api_result_a == employer["id"]:
                assert employer["first_name"] == name_emp
                assert employer["last_name"] == la_name
                assert employer["phone"] == phone_num
                assert employer["company_id"] == max_id_c

    with allure.step("Удалить работников и компанию через БД"):    
        db.clear_table_employers(max_id_c)
        db.delete_company(max_id_c)


@allure.title("Получение информацию о работнике")
@allure.description("Получение информацию о работнике")
@allure.feature("READ")
@allure.severity("normal")
def test_one_employer():
    name = "My company"
    db.create_company(name)    
    max_id_c = db.get_max_id_comp()

    with allure.step("Добавить данные"):
        name_emp = 'Иван'
        la_name = 'Петров'
        phone_num = '+79969598584'
    db.create_employer('Иван', 'Петров', '+79969598584', max_id_c)
    
    max_id_e = db.get_max_id_emp(max_id_c)
      
    db_result = db.get_employer_by_id(max_id_e)

    with allure.step("Сравнить, что полученные данные верны"):
        assert db_result["firstName"] == name_emp
        assert db_result["lastName"] == la_name
        assert db_result["companyId"] == max_id_c
        assert db_result["phone"] == phone_num

    with allure.step("Удалить работников и компанию через БД"):  
        db.clear_table_employers(max_id_c)
        db.delete_company(max_id_c)


@allure.title("Изменение данных работника")
@allure.description("Изменение данных работника")
@allure.feature("UPDATE")
@allure.severity("critical")
def test_change_data():
    name = "My company"
    db.create_company(name)     
    max_id_c = db.get_max_id_comp()

    db.create_employer('Иван', 'Петров', '+79969598584', max_id_c)
    
    max_id_e = db.get_max_id_emp(max_id_c)

    
    with allure.step("Добавить данные"):
        id = max_id_e
        last_name = 'Белов'
        email = 'test@mail.com'
        url = 'https://my_profile.com'
        phone = '89654789654'
        is_active = True
     
    my_headers = {"x-client-token": api.get_token()}
    api.change_data(id, last_name, email, url, phone, is_active, headers=my_headers)

    employer_body = api.get_employer(max_id_e)

    with allure.step("Проверить, что данные изменились"):
        assert employer_body["id"] == max_id_e
        assert employer_body["isActive"] == is_active
        assert employer_body["email"] == email
        assert employer_body["url"] == url

    with allure.step("Удалить работников и компанию через БД"): 
        db.clear_table_employers(max_id_c)
        db.delete_company(max_id_c)


@allure.title("Удаление работников и компании")
@allure.description("Удаление работников и компании")
@allure.feature("DELETE")
@allure.severity("critical")
def test_delete_company_and_employers():
    name = "My company"
    db.create_company(name)      
    max_id_c = db.get_max_id_comp()

    db.create_employer('Иван', 'Петров', '+79969598584', max_id_c)
           
    db.clear_table_employers(max_id_c)
         
    api_result = api.get_employee_list(f'?company={max_id_c}')
    with allure.step("Проверить, что сотрудник удалился"):
        assert len(api_result) == 0
              
    deleted = db.delete_company(max_id_c)

    with allure.step("Проверить, что компания удалена"): 
         assert len(api_result) != 0
         assert deleted["id"] == max_id_c
         assert deleted["name"] == name
         assert deleted["isActive"] == True

    rows = api.get_company_by_id(max_id_c)
         
    with allure.step("Проверить, что информации нет"):      
        assert len(rows) == 0