import psycopg2


def create_db(user, password):
    """
    Создает базу данных vacancies и таблицы employers и vacancies.
    :return: None.
    """

    print("\nПодключение к СУБД...", end=" ")
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            host="localhost",
        )
    except Exception:
        print(f'\nОшибка при подключении к СУБД.')
        print("\nРабота программы завершена!")
        exit()
    else:
        print("OK!")

    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute("drop database if exists vacancies")
    cursor.execute("create database vacancies")

    connection = psycopg2.connect(
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


def fill_employers_table(user, password, record_list):
    """
    Заполняет таблицу employers данными из списка словарей.
    :param record_list: список словарей.
    :return: None.
    """

    connection = psycopg2.connect(
        user=user,
        password=password,
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


def fill_vacancies_table(user, password, record_list, id=None):
    """
    Заполняет таблицу vacancies данными из списка словарей.
    :param record_list: список словарей.
    :param id: хранит очередной индекс primaty key.
    :return: None.
    """

    connection = psycopg2.connect(
        user=user,
        password=password,
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
    """
    Распечатывает список вакансий в читаемом формате.
    :param vacancies: список словарей с данными вакансий.
    :return: None.
    """
    for vacancy in vacancies:
        employer_name = vacancy["employer_name"]
        vacancy_name = vacancy["vacancy_name"]
        if vacancy["vacancy_salary_from"] == 0 and vacancy["vacancy_salary_to"] == 0:
            vacancy_salary = "не указана."
        else:
            vacancy_salary_from = "от " + \
                                  str(vacancy["vacancy_salary_from"]) + \
                                  " " if vacancy["vacancy_salary_from"] != 0 else ""
            vacancy_salary_to = "до " + \
                                str(vacancy["vacancy_salary_to"]) + \
                                " " if vacancy["vacancy_salary_to"] != 0 else ""
            vacancy_salary = f"{vacancy_salary_from}{vacancy_salary_to}руб."
        vacancy_url = vacancy["vacancy_url"]
        print(f"\nКомпания: {employer_name}.\n"
              f"Вакансия: {vacancy_name}.\n"
              f"Зарплата: {vacancy_salary}\n"
              f"Ссылка: {vacancy_url}.")
    print(f"\nВсего выведено вакансий - {len(vacancies)}.")

def print_employers(employers):
    """
    Распечатывает список компаний в читаемом формате.
    :param employers: список словарей с данными компаний.
    :return: None
    """

    for employer in employers:
        employer_name = employer["employer_name"]
        vacancies_count = employer["vacancies_count"]
        print(f"Компания: {employer_name}. Количество вакансий в базе данных: {vacancies_count}.")


def print_average_salary(average_salary):
    """
    Распечатывает значение средней зарплаты.
    :param average_salary: значение средней зарплаты.
    :return: None
    """
    print(f"Средняя зарплата по всем вакансиям: {average_salary} руб.")
