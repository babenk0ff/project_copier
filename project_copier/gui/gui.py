import os
import subprocess
import sys
import tkinter
import tkinter as tk
from tkinter import messagebox, ttk

from project_copier.gui.actions import handle_dirs
from project_copier.usb import get_usb_drives
from .exceptions import DirNotExistError


def show_error_message(message, root=None):
    if root:
        root.withdraw()
    messagebox.showerror('Error', message)


class GUI:
    def __init__(self, dir_path):
        self._dir_path = dir_path
        self._root = self._get_root()
        self._dirs = []
        self._dirs_listbox = self._get_listbox()
        self._dirs_label = self._get_label('Select project')
        self._drives = []
        self._drives_listbox = self._get_listbox()
        self._drives_label = self._get_label('Select USB-flash')
        self._button = self._get_button('Copy')
        self._progress_bar = self._get_progress_bar()

    @staticmethod
    def _get_root():
        root = tk.Tk()
        root.title('Transfer project')
        root.resizable(False, False)
        root.maxsize(304, 774)

        return root

    def _get_listbox(self):
        listbox = tk.Listbox(
            self._root,
            selectmode=tk.SINGLE,
            width=50,
            activestyle='none',
            exportselection=False,
        )

        return listbox

    def _get_label(self, text):
        label = tk.Label(self._root, text=text)

        return label

    def _get_button(self, text):
        button = tkinter.Button(self._root, text=text)

        return button

    def _get_progress_bar(self):
        bar = ttk.Progressbar(
            self._root,
            orient='horizontal',
            mode='determinate',
            name='progress_bar',
        )

        return bar

    def _load_dirs_list(self):
        """
        Заполняет _dirs_listbox имеющимися по пути _dir_path директориями
        """
        if os.path.isdir(self._dir_path):
            self._dirs = [
                d for d
                in os.listdir(self._dir_path)
                if os.path.isdir(os.path.join(self._dir_path, d))
            ]

            for d in self._dirs:
                self._dirs_listbox.insert(tk.END, d)

            self._dirs_listbox.config(height=len(self._dirs))
            self._dirs_listbox.selection_set(0)
        else:
            raise DirNotExistError

    def _load_listbox_drives(self):
        """
        Заполняет _drives_listbox имеющимися USB-разделами
        """
        try:
            self._drives = get_usb_drives()
        except subprocess.CalledProcessError:
            sys.exit(1)

        for drive in self._drives:
            drive_record = str(drive)
            self._drives_listbox.insert(tk.END, drive_record)

        self._drives_listbox.config(height=len(self._drives))
        self._drives_listbox.selection_set(0)

    def _pack_elements(self):
        self._dirs_label.pack()
        self._dirs_listbox.pack()

        self._drives_label.pack()
        self._drives_listbox.pack()

        self._button.config(command=lambda: handle_dirs(
            self._root,
            self._dir_path,
            self._dirs_listbox,
            self._drives,
            self._drives_listbox,
        ))
        self._button.pack(fill='both', padx=10, pady=10)

        self._progress_bar.pack(fill='both')

        self._root.eval('tk::PlaceWindow . center')

    def start(self):
        """
        Запуск графического интерфейса
        """
        try:
            self._load_dirs_list()
            self._load_listbox_drives()

            self._pack_elements()

            self._root.mainloop()

        except DirNotExistError:
            msg = f'Dir "{self._dir_path}" not exist!'
            show_error_message(msg, self._root)
            return
