import psycopg2

def drop_tables():
    connection = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        database="vacancies"
    )
    cursor = connection.cursor()
    try:
        cursor.execute("drop table employers")
        connection.commit()
    except Exception:
        pass
    try:
        cursor.execute("drop table vacancies")
        connection.commit()
    except Exception:
        pass
    if connection:
        cursor.close()
        connection.close()

def create_tables():
    connection = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        database="vacancies"
    )
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE employers("
                   "id SMALLINT PRIMARY KEY, "
                   "hh_id INT NOT NULL, "
                   "name VARCHAR NOT NULL)"
                   )
    cursor.execute("CREATE TABLE vacancies("
                   "id SMALLINT PRIMARY KEY, "
                   "hh_id INT NOT NULL, "
                   "employer_hh_id INT NOT NULL, "
                   "name VARCHAR NOT NULL, "
                   "salary_from INT NOT NULL, "
                   "salary_to INT NOT NULL, "
                   "url VARCHAR NOT NULL)"
                   )
    connection.commit()
    if connection:
        cursor.close()
        connection.close()

def fill_employer_table(record_list):
    connection = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        database="vacancies"
    )
    cursor = connection.cursor()
    id = 1
    for record in record_list:
        hh_id = record["hh_id"]
        name = record["name"]
        cursor.execute(
            f"INSERT INTO employers "
            f"(id, hh_id, name) "
            f"VALUES (%s, %s, %s)",
            (id, hh_id, name)
        )
        id += 1
    connection.commit()

    if connection:
        cursor.close()
        connection.close()

def fill_vacancy_table(record_list, id=None):
    connection = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        database="vacancies"
    )
    cursor = connection.cursor()

    for record in record_list:
        hh_id = record["hh_id"]
        employer_hh_id = record["employer_hh_id"]
        name = record["name"]
        salary_from = record["salary_from"]
        salary_to = record["salary_to"]
        url = record["url"]

        cursor.execute(
            f"INSERT INTO vacancies "
            f"(id, hh_id, employer_hh_id, name, salary_from, salary_to, url) "
            f"VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (id, hh_id, employer_hh_id, name, salary_from, salary_to, url)
        )
        id += 1
    connection.commit()

    if connection:
        cursor.close()
        connection.close()

def print_vacancies(vacancies):
    for vacancy in vacancies:
        employer_name = vacancy["employer_name"]
        vacancy_name = vacancy["vacancy_name"]
        vacancy_salary_from = "от " + \
                              str(vacancy["vacancy_salary_from"]) + \
                              " " if vacancy["vacancy_salary_from"] != 0 else ""
        vacancy_salary_to = "до " + \
                            str(vacancy["vacancy_salary_to"]) + \
                            " " if vacancy["vacancy_salary_to"] != 0 else ""
        vacancy_url = vacancy["vacancy_url"]
        print(f"Компания: {employer_name}.\n"
              f"Вакансия: {vacancy_name}.\n"
              f"Зарплата: {vacancy_salary_from}{vacancy_salary_to}руб.\n"
              f"Ссылка: {vacancy_url}.\n")

def print_employers(employers):
    for employer in employers:
        employer_name = employer["employer_name"]
        vacancies_count = employer["vacancies_count"]
        print(f"Компания: {employer_name}. Количество вакансий в базе данных: {vacancies_count}.")

def print_average_salary(average_salary):
    print(f"Средняя зарплата по всем вакансиям: {average_salary} руб.")
