import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="openapi-specgen",
    version="0.0.4",
    description="Generate OpenApi json specification",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/GabrielCappelli/openapi-specgen",
    author="Gabriel Cappelli",
    author_email="6148081+GabrielCappelli@users.noreply.github.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["openapi_specgen"],
    include_package_data=True,
    install_requires=[],
    entry_points={}
)
