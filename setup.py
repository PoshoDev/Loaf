from setuptools import setup, find_packages

VERSION = "0.2.21"
DESCRIPTION = "Effortlessly access your SQL servers and procedures, plus " \
              "some other utilities!"
with open('README.md', encoding="utf8") as f:
    LONG_DESCRIPTION = f.read()

# Setting up
# install_requires excludes the following since they come with Python itself: socket, sqlite3
setup(
    name="loaf",
    version=VERSION,
    author="Posho (Rodrigo Gómez Maitret)",
    author_email="<rodrigo.g.maitret@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "pymysql",
        "datetime",
        "configparser",
        "cryptography",
        "psycopg2-binary",
    ],
    keywords=['python', 'SQL', 'MySQL', 'MariaDB', 'PostgreSQL', 'database',
              'db', 'easy', 'loaf', 'bread'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
