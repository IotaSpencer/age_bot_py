import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="age_bot",
    version="0.0.1",
    author="IotaSpencer",
    author_email="me@iotaspencer.me",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IotaSpencer/age_bot_py",
    project_urls={
        "Bug Tracker": "https://github.com/IotaSpencer/age_bot_py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "lib"},
    packages=setuptools.find_packages(where="lib"),
    python_requires=">=3.7",
)