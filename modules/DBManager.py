from typing import Any
import psycopg2


class DBManager:
    """
    Класс для работы с данными в таблицах базы данных.
    """

    def __init__(self):
        self.connection = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            database="vacancies"
        )
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self) -> list[Any]:
        """
        Получает список компаний и количество вакансий у каждой.
        Возвращает список словарей в формате:
        {
        "employer_name": "название компании",
        "vacancies_count": "количество вакансий"
        }
        """

        record = []
        self.cursor.execute("SELECT * FROM employers")
        employers = self.cursor.fetchall()

        for row in employers:
            employer_hh_id = row[1]
            employer_name = row[2]
            self.cursor.execute(f"SELECT count(*) FROM vacancies WHERE employer_hh_id = {employer_hh_id}")
            vacancies_count = self.cursor.fetchall()[0][0]
            record.append({"employer_name": employer_name, "vacancies_count": vacancies_count})

        return record

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        Возвращает список словарей в формате:
        {
        "employer_name": "название компании",
        "vacancy_name": "название вакансии",
        "vacancy_salary_from": "зарплата от",
        "vacancy_salary_to": "зарплата до",
        "vacancy_url": "url-адрес",
        }
        """

        record = []
        self.cursor.execute("SELECT * FROM vacancies")
        vacancies = self.cursor.fetchall()
        for row in vacancies:
            employer_hh_id = row[2]
            self.cursor.execute(f"SELECT name FROM employers WHERE hh_id = {employer_hh_id}")
            employer_name = self.cursor.fetchone()[0]
            vacancy_name = row[3]
            vacancy_salary_from = row[4]
            vacancy_salary_to = row[5]
            vacancy_url = row[6]

            record.append(
                {
                    "employer_name": employer_name,
                    "vacancy_name": vacancy_name,
                    "vacancy_salary_from": vacancy_salary_from,
                    "vacancy_salary_to": vacancy_salary_to,
                    "vacancy_url": vacancy_url,
                }
            )

        return record

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        Возвращает число.
        """

        self.cursor.execute("SELECT round(AVG(salary_from)) FROM vacancies WHERE salary_from > 0")
        average_salary_from = self.cursor.fetchall()[0][0]
        if average_salary_from is None:
            average_salary_from = 0

        self.cursor.execute("SELECT round(AVG(salary_to)) FROM vacancies where salary_to > 0")
        average_salary_to = self.cursor.fetchall()[0][0]
        if average_salary_to is None:
            average_salary_to = 0
        average_salary = (int(average_salary_from) + int(average_salary_to)) / 2

        return average_salary

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        Возвращает список словарей аналогично функции get_all_vacancies.
        """

        result_vacancies = []
        all_vacancies = DBManager.get_all_vacancies(self)
        average_salary = DBManager.get_avg_salary(self)
        for vacancy in all_vacancies:
            if vacancy["vacancy_salary_from"] > average_salary or vacancy["vacancy_salary_to"] > average_salary:
                result_vacancies.append(vacancy)

        return result_vacancies

    def get_vacancies_with_keyword(self, keywords: list):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        Возвращает список словарей аналогично функции get_all_vacancies.
        ”"""

        result_vacancies = []
        vacancies = DBManager.get_all_vacancies(self)

        for vacancy in vacancies:
            for word in keywords:
                if word.lower() in vacancy["vacancy_name"].lower():
                    result_vacancies.append(vacancy)

        return result_vacancies
