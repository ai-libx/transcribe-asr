from setuptools import setup, find_packages

setup(
    name="tasr",
    version="0.1.0",
    author="Chiawei Lee",
    author_email="ljw@live.jp",
    description="A simple CLI tool focused on quickly and accurately converting audio files into text.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ai-libx/transcribe-asr",
    packages=find_packages(),
    install_requires=[
        "funasr>=1.2.6",
        "setuptools>=58.1.0",
        "soundfile>=0.13.1",
    ],
    entry_points={
        "console_scripts": [
            "tasr=tasr.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    license="Apache License v2",
)