# setup.py
from setuptools import setup, find_packages

setup(
    name="mt_triad",
    version="0.1.0",
    package_dir={"": "src"},  # Indica que los paquetes están en src/
    packages=find_packages(where="src"),
    install_requires=[],
    python_requires=">=3.8",
)
