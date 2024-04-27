## This file will be used to find + install whatever packages we need

from setuptools import find_packages, setup

setup(
    name = 'mcqgenerator',
    version = '0.0.1',
    author = 'Nisha Kaushal',
    author_email = 'nishaka@umich.edu',
    install_requires = ['openai', 'langchain',
                        'streamlit', 'python-dotenv', 'PyPDF2'], #list of packages. like openai, langchain, etc
    packages = find_packages() #finds the packages from local directory; ie the folders that contain __init__.py files
)


##to utilize this, at the end of our requirements.txt, write "-e ." (no quotes)
### Then, in the terminal, run pip install -r requirements.txt