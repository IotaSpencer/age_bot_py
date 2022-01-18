from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
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
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        'asyncclick',
        'py-cord'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'age_bot = age_bot.scripts.main:start'
        ],
    },
)