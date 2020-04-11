from setuptools import setup

setup(
    name="hsklcourses",
    version="0.2.1",
    description="Folder structure generator for courses of the University of Applied Sciences Kaiserslautern",
    url="http://github.com/ptrstn/hsklcourses",
    author="Peter Stein",
    license="WTFPL",
    packages=["hsklcourses"],
    install_requires=["requests", "beautifulsoup4"],
)
