from distutils.version import LooseVersion
from distutils.util import convert_path
from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    # patch for unicodes
    long_description = long_description.replace("➶", ">>")
    long_description = long_description.replace("©", "(c)")


pkg_version = {}
ver_path = convert_path("remio/version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), pkg_version)


setup(
    name="remio",
    packages=find_packages("remio", exclude=["test", "site", "arduino"]),
    version=pkg_version["__version__"],
    description="A library for managing concurrent socketio, cv2, and pyserial processes. Useful for making robots or devices with Arduinos and Raspberry Pi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    author="Jason Macas",
    author_email="franciscomacas3@gmail.com",
    url="https://github.com/Hikki12/remio",
    install_requires=requirements,
    keywords=[
        "OpenCV",
        "Serial",
        "SocketIO",
        "multithreading",
        "multiprocessing",
        "IoT",
        "mjpeg",
        "Arduino",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
