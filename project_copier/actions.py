import datetime
import os.path
import shutil
from tkinter import Listbox, messagebox, Tk

from project_copier.usb import FlashDrive

EXCLUDE = ['venv', '.idea', '__pycache__']


def get_src_dst(src_root, dirs_listbox, drives_listbox, drives):
    src_dir_name = dirs_listbox.get(dirs_listbox.curselection())
    drive = drives[drives_listbox.curselection()[0]]
    src_full_path = os.path.join(src_root, src_dir_name)

    today = datetime.date.today()
    dst_dir_name = f'{src_dir_name}_{today.strftime("%Y.%m.%d")}'
    dst_path = os.path.join(drive.letter, os.sep, dst_dir_name)

    if os.path.exists(dst_path):
        os.system(f'RMDIR /S /Q {dst_path}')

    return src_full_path, dst_path


def get_files_count(path):
    def get_dirs():
        for _, dirs, files in os.walk(path, topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDE]
            yield files

    return sum(len(files) for files in get_dirs())


def handle_files(
        root: Tk,
        src_root: str,
        dirs_listbox: Listbox,
        drives: list[FlashDrive],
        drives_listbox: Listbox,
):
    if not drives:
        messagebox.showerror('Error', 'There are no USB flash drives!')
        return

    src, dst = get_src_dst(src_root, dirs_listbox, drives_listbox, drives)

    root.children['progress_bar']['maximum'] = get_files_count(src)
    files_copied = 0

    def progress_files(src_path, dst_path):
        nonlocal files_copied
        shutil.copy2(src_path, dst_path)
        files_copied += 1
        root.children['progress_bar']['value'] = files_copied
        root.update()

    shutil.copytree(
        src,
        dst,
        copy_function=progress_files,
        ignore=shutil.ignore_patterns(*EXCLUDE),
    )
