import setuptools

with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="openholdings",
    version="0.0.1",
    author="Miles Henrichs",
    author_email="mileshenrichs21@gmail.com",
    description="Web scraping utilities for ETF holdings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mileshenrichs/openholdings",
    project_urls={
        "Bug Tracker": "https://github.com/mileshenrichs/openholdings/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)