import setuptools
from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name="rpa_cooperativa",
    version="1.0.1",
    license='MIT License',
    author="Edenilson Fernandes dos Santos",
    author_email='santoeen@gmail.com',
    description="Classes referente automação com python para... api fluid, api whatsapp, api sms, sql, ACClient",
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
    install_requires=['requests', 'pandas', 'sqlalchemy', 'pyautogui']
)
