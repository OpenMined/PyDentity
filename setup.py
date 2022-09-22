"""Module setup."""

import os
from setuptools import setup, find_packages

PACKAGE_NAME = "aries_cloudcontroller"

with open(os.path.abspath("README.md"), "r") as fh:
    long_description = fh.read()


def parse_requirements(filename: str):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version="0.6.3",
        description="A simple python package for controlling an aries agent through the admin-api interface",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/didx-xyz/aries-cloudcontroller-python/tree/main/aries_cloudcontroller",
        packages=find_packages(),
        include_package_data=True,
        package_data={
            "aries_cloudcontroller": [
                "requirements.txt",
            ]
        },
        tests_require=parse_requirements("requirements.dev.txt"),
        install_requires=parse_requirements("requirements.txt"),
        python_requires=">=3.8",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
        ],
    )
