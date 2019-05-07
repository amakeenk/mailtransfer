from os.path import dirname
from os.path import join
from setuptools import find_packages
from setuptools import setup

setup(
    name='mailtransfer',
    version='1.3',
    author='Alexander Makeenkov',
    author_email='whoami.tut@gmail.com',
    url='https://github.com/amakeenk/mailtransfer',
    description='Simple linux tool for transfer mails from one mailserver to another mailserver',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    entry_points={
        'console_scripts':
            ['mailtransfer = mailtransfer.main:main']
        }
)
