import toml
from setuptools import find_packages, setup

from settings import VERSION

# Load the pyproject.toml file
with open("pyproject.toml", "r", encoding="utf-8") as toml_file:
    pyproject = toml.load(toml_file)

# Extract project metadata and dependencies
project_metadata = pyproject.get("tool", {}).get("poetry", {})
dependencies = project_metadata.get("dependencies", {})

setup(
    name=project_metadata.get("name", "covidashit"),
    version=project_metadata.get("version", VERSION),
    description=project_metadata.get("description", ""),
    author=project_metadata.get(
        "authors", ["Fabrizio Miano <fabriziomiano@gmail.com>"]
    )[0],
    packages=find_packages(),
    include_package_data=True,
    install_requires=list(dependencies.keys()),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: MIT License",
    ],
)
