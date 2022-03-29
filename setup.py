from distutils.core import setup


setup(
    name="remio",
    version="0.2.0",
    description="A library for managing concurrent socketio, cv2, and pyserial processes. Useful for making robots or devices with Arduinos and Raspberry Pi.",
    license = "Apache License 2.0",
    author="Jason Macas",
    author_email="franciscomacas3@gmail.com",
    install_requires=[i.strip() for i in open("./requirements.txt").readlines()],
    keywords=[
        "OpenCV",
        "Serial",
        "SocketIO",
        "multithreading",
        "multiprocessing",
        "IoT",
        "mjpeg",
        "Arduino"
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
