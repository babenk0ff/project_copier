import os
import tkinter
import tkinter as tk
from tkinter import messagebox, ttk

from project_copier.actions import handle_files
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
        self._make_copy = lambda: handle_files(
            self._root,
            self._dir_path,
            self._dirs_listbox,
            self._drives,
            self._drives_listbox,
        )
        self._button = self._get_button()
        self._progress_bar = self._get_progress_bar()

    @staticmethod
    def _get_root():
        root = tk.Tk()
        root.title('Transfer project')

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

    def _load_dirs_list(self):
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
        self._drives = get_usb_drives()
        for drive in self._drives:
            drive_record = str(drive)
            self._drives_listbox.insert(tk.END, drive_record)
        self._drives_listbox.config(height=len(self._drives))
        self._drives_listbox.selection_set(0)

    def _get_button(self):
        button = tkinter.Button(
            self._root,
            text='Copy',
            command=self._make_copy,
        )

        return button

    def _get_progress_bar(self):
        bar = ttk.Progressbar(
            self._root,
            orient='horizontal',
            mode='determinate',
            name='progress_bar',
        )

        return bar

    def start(self):
        try:
            self._load_dirs_list()
            self._load_listbox_drives()

            self._dirs_label.pack()
            self._dirs_listbox.pack()

            self._drives_label.pack()
            self._drives_listbox.pack()

            self._button.pack(fill='both', padx=10, pady=10)
            self._progress_bar.pack(fill='both')

        except DirNotExistError:
            msg = f'Dir "{self._dir_path}" not exist!'
            show_error_message(msg, self._root)
            return

        self._root.mainloop()
