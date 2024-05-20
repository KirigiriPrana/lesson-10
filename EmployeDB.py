import sqlalchemy
import allure
from sqlalchemy import create_engine, text

db = "postgresql://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx"

class EmployerTable:
    scripts = {
        'insert_new': text('insert into company(name) values (:new_name)'),
        'get_max_id_company': text('select MAX(id) from company'),
        'max_id_employer': text('select MAX(id) from employee where company_id=(:id_comp)'),
        'select_employer': text('select * from employee where id =(:id_company)'),
        'delete_by_id': text('delete from company where company_id =(:id_to_delete)'),
        'create_employer': text(
            'insert into employee (id, is_active\, first_name, last_name, phone, company_id) values (DEFAULT, DEFAULT,(:first_name, :last_name, :phone, :company_id)'),
        'clear_table': text('DELETE FROM employee  where company_id =(:id_clear)'),
        'select_by_id': text('select * from employee where id =(:select_id)')
    }

    def __init__(self, connection_string):
        self.db = create_engine(connection_string)

    @allure.step("db.Создать компанию c {name}")
    def create_company(self, name: str):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["insert_new"], {"new_name": name})

            return result

    @allure.step("db.Получить {id} компании")
    def get_max_id_comp(self):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["get_max_id_company"]).fetchall()[0][0]

            return result

    @allure.step("db.Получить {id} работника")
    def get_max_id_emp(self, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["max_id_employer"], {"id_comp": id}).fetchall()[0][0]

            return result

    @allure.step("db.Получить информацию о работниках по {id} компании")
    def select_employers(self, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["select_employer"], {"id_company": id})

            return result

    @allure.step("db.Удалить компанию по {id}")
    def delete_company(self, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["delete_by_id"], {"id_to_delete": id})

            return result

    @allure.step("db.Создать работника по {id} компании с данными{f_name},{l_name},{phone}")
    def create_employer(self, f_name: str, l_name: str, phone: str, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["create_employer"],
                                        {"first_name": f_name, "last_name": l_name, "phone": phone, "id_company": id})
            return result

    @allure.step("db.Удалить работников по {id} компании")
    def clear_table_employers(self, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["clear_table"], {"id_clear": id})

            return result

    @allure.step("db.Получить информацию о работнике по {id}")
    def get_employer_by_id(self, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["select_by_id"], {"select_id": id}).fetchone()

            return result
