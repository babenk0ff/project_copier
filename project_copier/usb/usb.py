import json
import logging
import subprocess

log = logging.getLogger()


class FlashDrive:
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


def run_powershell() -> bytes:
    args = [
        'powershell',
        '-noprofile',
        '-file',
        r'.\project_copier\usb\get_usb_drives.ps1',
    ]

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
    try:
        result = run_powershell()
    except subprocess.CalledProcessError as e:
        log.error(e.stderr.decode('cp866'))
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
