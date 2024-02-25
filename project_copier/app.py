import sys
from project_copier.gui import GUI, show_error_message


def get_path():
    """
    Получение директории с проектами из переданного аргумента.
    Если аргумент не был передан, то будет выведена ошибка.
    """
    if len(sys.argv) == 1:
        show_error_message('The project path was not specified')
        sys.exit()

    return sys.argv[1]


def main():
    """
    Точка входа в приложение
    """

    dir_path = get_path()
    app = GUI(dir_path)
    app.start()


if __name__ == '__main__':
    main()
