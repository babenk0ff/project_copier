import json
import logging
import subprocess
from pathlib import Path

log = logging.getLogger()


class FlashDrive:
    """
    Класс для USB-разделов
    """

    def __init__(self, letter, size):
        self.letter = letter
        self.size = size

    def __str__(self):
        return f'{self.letter} ({self.get_readable_size()})'

    def get_readable_size(self):
        billion_bytes = 10 ** 9
        million_bytes = 10 ** 6
        if self.size > billion_bytes:
            size = round(self.size / billion_bytes, 1)
            return f'{size}GB'
        size = round(self.size / million_bytes)
        return f'{size}MB'


def get_script():
    """
    Получает содержимое powershell-скрипта
    """
    app_path = Path(__file__).parent.resolve()
    with open(app_path / 'get_usb_drives.ps1', 'r', encoding='utf-8') as f:
        script = f.read()

    return script


def run_powershell() -> bytes:
    """
    Исполняет PowerShell-скрипт и возвращает результат
    """
    script = get_script()
    args = ['powershell', '-noprofile', '-command', script]

    proc_result = subprocess.run(
        args=args,
        capture_output=True,
    )
    if proc_result.stderr:
        raise subprocess.CalledProcessError(
            returncode=proc_result.returncode,
            cmd=args,
            stderr=proc_result.stderr,
        )
    else:
        return proc_result.stdout


def get_usb_drives() -> list[FlashDrive]:
    """
    Возвращает USB-разделы, представленные списком FlashDrive
    """
    try:
        result = run_powershell()
    except subprocess.CalledProcessError as e:
        log.error(e.stderr.decode('cp866'))
        raise
    else:
        drives = json.loads(result)
        usb_drives = [
            FlashDrive(drive['deviceid'], drive['size'])
            for drive in drives
            if drive['drivetype'] == 2 and drive['size'] is not None
        ]

        return usb_drives


if __name__ == '__main__':
    print(get_usb_drives())
