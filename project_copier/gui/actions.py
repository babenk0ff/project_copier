import datetime
import os.path
import shutil
import subprocess
from tkinter import Listbox, messagebox, Tk

from project_copier.usb import FlashDrive

EXCLUDE = ['venv', '.idea', '__pycache__']


def get_src_dst(src_root, dirs_listbox, drives_listbox, drives):
    """
    Формирует и возвращает абсолютные пути для директории проекта и
    целевой директории
    """
    src_dir_name = dirs_listbox.get(dirs_listbox.curselection())
    drive = drives[drives_listbox.curselection()[0]]
    src_full_path = os.path.join(src_root, src_dir_name)

    today = datetime.date.today()
    dst_dir_name = f'{src_dir_name}_{today.strftime("%Y.%m.%d")}'
    dst_path = os.path.join(drive.letter, os.sep, dst_dir_name)

    return src_full_path, dst_path


def prepare_dst_dir(path):
    """
    Удаляет целевую директорию при её существовании
    """
    if os.path.exists(path):
        os.system(f'RMDIR /S /Q {path}')


def get_files_count(path):
    """
    Возвращает число файлов в директории, исключая игнорированные поддиректории
    """
    def get_dirs():
        for _, dirs, files in os.walk(path, topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDE]
            yield files

    return sum(len(files) for files in get_dirs())


def progress_file(root):
    files_copied = 0

    def copy_file(src_path, dst_path):
        """
        Копирует файл из src_path в dst_path, обновляет прогресс бар
        """
        nonlocal files_copied
        shutil.copy2(src_path, dst_path)
        files_copied += 1

        # Обновление значения прогресс бара
        root.children['progress_bar']['value'] = files_copied
        root.update()

    return copy_file


def handle_dirs(
        root: Tk,
        src_root: str,
        dirs_listbox: Listbox,
        drives: list[FlashDrive],
        drives_listbox: Listbox,
):
    """
    Запускает обработку выбранных директорий
    """
    if not drives:
        messagebox.showerror('Error', 'There are no USB flash drives!')
        return

    src, dst = get_src_dst(src_root, dirs_listbox, drives_listbox, drives)
    prepare_dst_dir(dst)

    # Задание максимального значения прогресс бара
    root.children['progress_bar']['maximum'] = get_files_count(src)

    copy_function = progress_file(root)
    shutil.copytree(
        src,
        dst,
        copy_function=copy_function,
        ignore=shutil.ignore_patterns(*EXCLUDE),
    )
