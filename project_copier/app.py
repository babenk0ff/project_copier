import sys
from project_copier.gui import GUI, show_error_message


def get_path():
    if len(sys.argv) == 1:
        show_error_message('The project path was not specified')
        sys.exit()

    return sys.argv[1]


def main():
    dir_path = get_path()
    app = GUI(dir_path)
    app.start()


if __name__ == '__main__':

    main()
