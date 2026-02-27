from setuptools import (
    setup,
    find_packages,
)

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    # Library name and version
    name="lylac",
    version="2.3.19.0",

    # Dependencies
    install_requires=[
        "bcrypt>=4.3.0",
        "pandas>=2.2.3",
        "passlib>=1.7.4",
        "psycopg2>=2.9.10",
        "pydantic>=2.11.5",
        "PyJWT>=2.10.1",
        "SQLAlchemy>=2.0.41",
    ],

    # Author info
    author="Pável Hernández Reza",
    author_email="onnymm@outlook.com",

    # Description
    description="Gestor de conexión a bases de datos en PostgreSQL altamente personalizable.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/onnymm/lylac",

    # Metadata
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "orm",
        "postgresql",
        "sqlalchemy",
    ],
    python_requires='>=3.11',
    packages=find_packages(),
)
