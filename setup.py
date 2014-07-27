import os
from setuptools import setup

install_requires = ["Django", "requests"]

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name = "mobilem-api",
    version = "0.0.2a",
    description = "A library for sending SMS via mobilem.cz gateway.",
    url = "https://github.com/netman92/mobilem_cz",
    author = "Stanislav Komanec",
    author_email = "stanislav@komanec.eu",
    packages = ["mobilem_api"],
    zip_safe = False,
    license = 'MIT',
    install_requires = install_requires,
    test_suite = "tests.get_tests",
)