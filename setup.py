import setuptools
from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()


setup(
    name="rpa_cooperativa",
    version="1.0.55",
    license='MIT License',
    author="Edenilson Fernandes dos Santos",
    author_email='santoeen@gmail.com',
    description="Classes referente automação com python para... api fluid, api whatsapp, api sms, sql, acc",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='rpa cooperativa fluid api automação sql sqlalchemy',
    include_package_data=True,
    package_data={'': ['img/*']},
    packages=setuptools.find_packages(),
    zip_safe=False,
    url = "https://github.com/edenilsonsantos/rpa_cooperativa",
    project_urls = {
        "repository": "https://github.com/edenilsonsantos/rpa_cooperativa",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.8',
    install_requires=['wheel', 'pandas', 'openpyxl', 'cryptography', 'xlsxwriter', 'xlrd', 'openpyxl','selenium', 'webdriver_manager', 'easygui', 'pyperclip', 'mysql-connector-python==8.0.28',
                      'pymysql', 'pyodbc', 'sqlalchemy==1.4.37', 'psycopg2', 'psycopg2-binary', 'denodo-sqlalchemy', 'pillow', 'requests>=2.28.1', 'urllib3>=1.26.9', 
                      'certifi>=2022.5.18.1', 'pyopenssl>=22.0.0', 'idna>=3.3', 'charset-normalizer>=2.0.12', 'pyautogui',
                      'pyrect', 'pyscreeze', 'pytz', 'graypy', 'reportlab', 'psutil', 'requests-html', 'paramiko','opencv-python',
                      'pytesseract', 'xmltodict', 'pywin32', 'pywinauto', 'beautifulsoup4', 'mechanize', 'matplotlib', 
                      'Unidecode', 'WMI', 'tabulate', 'python-dateutil>=2.8.2', 'secure-smtplib']
)
