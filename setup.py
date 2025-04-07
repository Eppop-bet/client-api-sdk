from setuptools import setup, find_packages

setup(
    name="client-api-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.7",
)