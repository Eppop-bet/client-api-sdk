from setuptools import setup, find_packages
import os


def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_reqs = parse_requirements('requirements.txt')

setup(
    name="esource-client-api-sdk",
    version="0.1.1",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=install_reqs,
    python_requires=">=3.7",
    author="Esource.gg",
    description="Python SDK for the Esource.gg Client API",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Eppop-bet/client-api-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
