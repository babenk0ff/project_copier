from setuptools import setup, find_packages

setup(
    name='project_copier',
    version='1.0',
    packages=find_packages(),
    package_dir={
        'gui': 'project_copier/gui',
        'usb': 'project_copier/usb',
    },
    package_data={
        '': ['**/*.ps1'],
    },
    entry_points={
        'console_scripts': [
            'project-copier = project_copier.app:main',
        ]
    }
)
