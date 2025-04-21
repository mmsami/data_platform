from setuptools import setup, find_packages
# pip install -e .

setup(
    name="data_platform",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)