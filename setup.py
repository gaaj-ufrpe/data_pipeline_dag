from setuptools import find_packages, setup

setup(
    name="dagster_prj",
    packages=find_packages(exclude=["dagster_prj_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)