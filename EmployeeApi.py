import requests
import allure


class EmployeeApi:

    def __init__(self,url):
        self.url = url

    @allure.step("api.Получить токен")
    def get_token(self, user='flora', password='nature-fairy'):
        creds = {
            'username': user,
            'password': password
        }
        resp = requests.post(self.url+'/auth/login',json=creds)
        return resp.json()["userToken"]

    @allure.step("api.Создать компанию")
    def create_company(self, name, description=""):
        company = {
            "name": name,
            "description": description
        }
        my_headers = {}
        my_headers["x-client-token"] = self.get_token()
        resp = requests.post(self.url + '/company',
                             json=company, headers=my_headers)
        return resp.json()

    @allure.step("api.Получить список работников")
    def get_employee_list(self, params_to_add=None):
        resp = requests.get(self.url + '/employee' + params_to_add)
        return resp.json()

    @allure.step("api.Создать работника")
    def create_employee(self, id, firstName, lastName, middleName,  companyId, email, url, phone, birthdate, isActive):
        employer = {
            "id": id,
            "firstName": firstName,
            "lastName": lastName,
            "middleName": middleName,
            "companyId": companyId,
            "email": email,
            "url": url,
            "phone": phone,
            "birthdate": birthdate,
            "isActive": isActive
        }
        my_headers = {}
        my_headers["x-client-token"] = self.get_token()
        resp = requests.post(self.url+'/employee',
                             json=employer, headers=my_headers)
        return resp.json()

    @allure.step("api.Получить информацию о работнике по {id}")
    def get_employer(self, id):
        resp = requests.get(self.url + f'/employee/{id}')
        return resp.json()

    @allure.step("api.Изменить информацию о работнике по {id}")
    def change_data(self, id, lastName, email, url, phone, isActive):
        employer = {
            "lastName": lastName,
            "email": email,
            "url": url,
            "phone": phone,
            "isActive": isActive
        }

        my_headers = {}
        my_headers["x-client-token"] = self.get_token()
        resp = requests.patch(self.url + f'/employee/{id}',
                              json=employer, headers=my_headers)
        return resp.json()
    
    
    @allure.step("api.Получить информацию о компании по {id}")
    def get_company_by_id(self, id):
        resp = requests.get(self.url + f'/company/{id}')
        return resp.json()