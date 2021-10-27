from setuptools import setup, find_packages

VERSION = '0.1.10'
DESCRIPTION = 'Effortlessly access your MySQL server and procedures, plus some other utilities!'
with open('README.md', encoding="utf8") as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="loaf",
    version=VERSION,
    author="Posho (Rodrigo Gómez Maitret)",
    author_email="<rodrigo.g.maitret@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pymysql", "datetime"], # Excludes "socket"
    keywords=['python', 'MySQL', 'database', 'db', 'easy', 'loaf', 'bread'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
