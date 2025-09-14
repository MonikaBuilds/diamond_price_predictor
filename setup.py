from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    with open(file_path) as f:
        requirements = [req.strip() for req in f if req.strip()]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name="mlbootcamp",
    version="0.0.1",
    author="monika",
    author_email="monikabhati2005@gmail.com",
    install_requires=get_requirements("requirements.txt"),
    packages=find_packages(where="src"),
    package_dir={"": "src"}
)
