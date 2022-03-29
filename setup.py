from distutils.core import setup


setup(
    name="remio",
    version="0.2.0",
    description="Python remIO",
    author="Jason Macas",
    author_email="franciscomacas3@gmail.com",
    install_requires=[i.strip() for i in open("./requirements.txt").readlines()],
    keywords=[
        "OpenCV",
        "Serial",
        "SocketIO" "multithreading",
        "multiprocessing",
        "IoT",
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
