"""This module is for the package setup."""

from setuptools import setup, find_packages

setup(
    name="m1wengine",
    version="1.0.0",
    description="A game engine built on top of pygame",
    url="https://github.com/Sean-Nishi/M1Wengine",
    packages=find_packages(),
    install_requires=["pygame-menu==4.4.3", "pygame==2.5.2"],
    extra_requires={
        "dev": ["black==23.1.0", "flake8==4.0.1", "pydocstyle==6.3.0", "twine>=4.0.2"]
    },
    python_requires=">=3.11",
)
