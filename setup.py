import os
from setuptools import setup, find_packages

install_requires = ['py-bcrypt']

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.markdown')

description = 'Make Django use bcrypt for hashing passwords.'
long_description = description

setup(
    name='django-bcrypt',
    version='0.9.0',
    install_requires=install_requires,
    description=description,
    long_description=long_description,
    author='Dumbwaiter Design',
    author_email='dev@dwaiter.com',
    url='http://bitbucket.org/dwaiter/django-bcrypt/',
    packages=['django_bcrypt'],
)
