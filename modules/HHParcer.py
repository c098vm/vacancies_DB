import requests
from modules.error import ParsingError


class Employer:
    """
    Класс для работы с компаниями, полученными через API.
    """

    url = "https://api.hh.ru/employers"
    headers = {
        "User-Agent": "MyAppVac/1.01"
    }

    def __init__(self, keyword: str):
        self.params = {
            "per_page": 100,
            "text": keyword
        }

    def get_request(self):
        """
        Метод запроса json-данных через API.
        """

        response = requests.get(url=self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError('Ошибка полученя данных.')
        return response.json()["items"]

    def select_employer_id(self):
        """
        Метод выбора интересующей компании из полученного списка.
        Возвращает словарь в формате:
        {
        "hh_id": "id компании в HeadHunter",
        "name": "название компании"
        }
        """

        print()
        print("Загрузка...")
        employer_data = self.get_request()

        employers_list = []
        index = 1
        for data in employer_data:
            print(f'{index}.{" " * (3 - len(str(index)))}{data["name"]}.')
            employers_list.append(
                {
                    "hh_id": data["id"],
                    "name": data["name"],
                }
            )
            index += 1

        if len(employer_data) == 0:
            print("По такому ключевому слову компаний не найдено.")
            print()
            return None

        print()
        print(f"Найдено {len(employer_data)} компаний.")

        while True:
            print("Введите порядковый номер интересующей компании.")
            selected_employer_num = int(input(">>> ")) - 1

            if selected_employer_num not in range (0, len(employer_data)):
                print("Введенное значение неверно!\n")
            else:
                break

        selected_employer_dict = employers_list[selected_employer_num]
        selected_employer_name = [value for value in selected_employer_dict.values()][1]

        print(f'Выбрана компания "{selected_employer_name}".')
        print()

        return selected_employer_dict


class Vacancy:
    """
    Класс для получения вакансий через API.
    """

    url = "https://api.hh.ru/vacancies"
    headers = {
        "User-Agent": "MyAppVac/1.01"
    }

    def __init__(self, employer_id: int, employer_name: str):
        self.employer_name = employer_name
        self.salary_to = None
        self.vacancies = None
        self.params = {
            "per_page": 100,
            "text": None,
            "page": None,
            "employer_id": employer_id
        }

    def get_request(self):
        """
        Метод запроса json-данных через API.
        """

        response = requests.get(url=self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError('Ошибка полученя данных.')

        return response.json()["items"]

    def get_vacancies(self, page_count):
        """
        Метод сохранения вакансий в список.
        Незаданные (Null) в HeadHunter значения зарплаты записываются как 0.
        Возвращает список словарей в формате:
        {
        "hh_id": "id вакансии в HeadHunter",
        "employer_hh_id": "id компании в HeadHunter",
        "name": "название компании",
        "salary_from": "зарплата от",
        "salary_to": "зарплата до",
        "url": "url-адрес"
        }
        """


        self.vacancies = []
        salary_from = 0
        salary_to = 0
        for page in range(page_count):
            page_vacancies = []
            self.params["page"] = page
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(f'Ошибка {error} при парсинге.')
            else:
                if len(page_vacancies) == 0:
                    break
                print(f'{self.employer_name}: Cтраница {page + 1}. ', end="")
                self.vacancies.extend(page_vacancies)
                print(f'Загружено вакансий - {len(page_vacancies)}.')

        vacancies_list = []

        for data in self.vacancies:

            if data["salary"]:
                if data["salary"]["from"]:
                    salary_from = data["salary"]["from"]
                else:
                    salary_from = 0
                if data["salary"]["to"]:
                    salary_to = data["salary"]["to"]
                else:
                    salary_to = 0

            vacancies_list.append(
                {
                    "hh_id": data["id"],
                    "employer_hh_id": data["employer"]["id"],
                    "name": data["name"],
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "url": data["alternate_url"],
                }
            )

        return vacancies_list
