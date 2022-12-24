from setuptools import setup, find_namespace_packages, _distutils

setup (
    name= 'clean',
    version= '1',
    description= 'code for clean folders',
    url='https://github.com/melser68/task_2/tree/main/clean_folder',
    author= 'Serhii Melnyk',
    author_email= 'melser68@i.ua',
    license= 'MIT',
    packages= find_namespace_packages(),
    entry_points = {'console_scripts': ['cleanfolder = clean.__main__']}
)