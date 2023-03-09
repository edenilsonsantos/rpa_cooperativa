from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name="rpa_cooperativa",
    version="0.0.3",
    license='MIT License',
    author="Edenilson Fernandes dos Santos",
    author_email='santoeen@gmail.com',
    description="Classe com métodos referente automação com python, e api fluid",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='rpa cooperativa fluid api automação sql sqlalchemy',
    packages=["rpa_coop","rpa_coop/img"],
    url = "https://github.com/edenilsonsantos/dias-uteis-brasil",
    project_urls = {
        "repository": "https://github.com/edenilsonsantos/dias-uteis-brasil",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=['requests', 'pandas', 'sqlalchemy']
)