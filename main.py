from modules import DBManager, HHParcer
from utils import utils


def main():
    vacancy_primary_key = 1
    #счетчик primary_key для таблицы с вакансиями

    utils.drop_tables()
    utils.create_tables()

    # employers_quantity = 10

    while True:
        print(f"Введите количество интересующих компаний для загрузки резюме (не более 10).")
        employers_quantity = (input(">>> "))

        if employers_quantity.isdigit():
            employers_quantity = int(employers_quantity)
            if employers_quantity in range(1, 11):
                break
        print("Введенное значение неверно!")
    print()

    employers_list = []

    for i in range(employers_quantity):
        print(f'Введите ключевое слово для поиска {i + 1}-й компании.')
        keyword = input(">>> ")

        hh = HHParcer.Employer(keyword)
        employer_id = hh.select_employer_id()
        if employer_id == None:
            continue

        employers_list.append(employer_id)
    utils.fill_employer_table(employers_list)

    print('Загрузка вакансий...')

    for employer in employers_list:
        employer_hh_id = employer["hh_id"]
        employer_name = employer["name"]
        pages_count = 2
        hh = HHParcer.Vacancy(employer_hh_id, employer_name)
        vacancies = hh.get_vacancies(pages_count)

        utils.fill_vacancy_table(vacancies, vacancy_primary_key)
        vacancy_primary_key += len(vacancies)

    print()
    print(f"Всего по выбранным компаниям загружено {vacancy_primary_key - 1} вакансий.")
    print()

    while True:
        print("Введите номер команды:\n"
              "1 - вывести cписок всех компаний c количеством вакансий в каждой компании.\n"
              "2 - вывести список всех вакансий.\n"
              "3 - вывести среднюю зарплату по всем вакансиям.\n"
              "4 - вывести список вакансий, у которых зарплата выше средней.\n"
              "5 - выполнить поиск вакансий по ключевому слову.\n"
              "0 - выход")
        command = input(">>> ")
        print()

        dbm = DBManager.DBManager()

        if command == "0":
            break
        elif command == "1":
            employers = dbm.get_companies_and_vacancies_count()
            utils.print_employers(employers)
        elif command == "2":
            vacancies = dbm.get_all_vacancies()
            utils.print_vacancies(vacancies)
        elif command == "3":
            average_salary = dbm.get_avg_salary()
            utils.print_average_salary(average_salary)
        elif command == "4":
            vacancies = dbm.get_vacancies_with_higher_salary()
            utils.print_vacancies(vacancies)
        elif command == "5":
            print("Введите ключевое слово.")
            keyword = input(">>> ")
            vacancies = dbm.get_vacancies_with_keyword(keyword)
            utils.print_vacancies(vacancies)

        print()


if __name__ == '__main__':
    main()
