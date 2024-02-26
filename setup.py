from setuptools import setup, find_packages

setup(
    name='project_copier',
    version='1.1',
    packages=find_packages(),
    package_data={
        '': ['**/*.ps1'],
    },
    entry_points={
        'gui_scripts': [
            'project-copier = project_copier.app:main',
        ]
    }
)
