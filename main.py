from modules import DBManager, HHParcer
from utils import utils


def main():
    print("\n*** VACANCY DATABASE ***")
    vacancy_primary_key = 1 # счетчик primary_key для таблицы с вакансиями

    print("\nДля работы программы необходимо подключение к СУБД PostgreSQL.\n\n"
          "Введите данные пользователя для подключения.")
    user = input("Пользователь: ")
    password = input("Пароль: ")
    # user = "postgres"
    # password = "postgres"

    utils.create_db(user, password)

    # employers_quantity = 10

    while True:
        print(f"\nВведите количество интересующих компаний для загрузки вакансий (не более 10).")
        employers_quantity = (input(">>> "))

        if employers_quantity.isdigit():
            employers_quantity = int(employers_quantity)
            if employers_quantity in range(1, 11):
                break
        print("Введенное значение неверно!\n")
    print()

    employers_list = []

    for i in range(employers_quantity):
        print(f'Введите ключевое слово для поиска {i + 1}-й компании.')
        keyword = input(">>> ")

        hh = HHParcer.Employer(keyword)
        employer_id = hh.select_employer_id()
        if employer_id is None:
            continue

        employers_list.append(employer_id)

    if len(employers_list) == 0:
        print("\nРабота программы завершена!")
        exit()

    utils.fill_employers_table(user, password, employers_list)

    print('Загрузка вакансий...')

    for employer in employers_list:
        employer_hh_id = employer["hh_id"]
        employer_name = employer["name"]
        pages_count = 10
        hh = HHParcer.Vacancy(employer_hh_id, employer_name)
        vacancies = hh.get_vacancies(pages_count)

        utils.fill_vacancies_table(user, password, vacancies, vacancy_primary_key)
        vacancy_primary_key += len(vacancies)

    if vacancy_primary_key == 1:
        print("\nПо выбранным компаниям вакансий не найдено.")
        print("\nРабота программы завершена!")
        exit()
    print(f"\nВсего по выбранным компаниям загружено вакансий - {vacancy_primary_key - 1}.")

    while True:
        print("\nВведите номер команды:\n"
              "1 - вывести cписок компаний c количеством вакансий по каждой компании.\n"
              "2 - вывести список всех вакансий.\n"
              "3 - вывести среднюю зарплату по всем вакансиям.\n"
              "4 - вывести список вакансий, у которых зарплата выше средней.\n"
              "5 - выполнить поиск вакансий по ключевым словам.\n"
              "0 - выход")
        command = input(">>> ")

        dbm = DBManager.DBManager(user, password)

        if command == "0":
            print("Работа программы завершена!")
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
            print("\nВведите ключевые слова (фрагменты слов) через запятую.")
            keystring = input(">>> ")
            print()
            keywords = keystring.replace(" ", "").split(",")
            vacancies = dbm.get_vacancies_with_keyword(keywords)
            if len(vacancies) == 0:
                print("Вакансий не найдено.\n")
            else:
                utils.print_vacancies(vacancies)
        else:
            print("\nВведенное значение неверно!")


if __name__ == '__main__':
    main()
