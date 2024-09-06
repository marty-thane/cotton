from setuptools import setup, find_packages

setup(
    name="cotton",
    version="1.0",
    description="Music downloader for people who know what they want.",
    url="https://github.com/marty-thane/cotton",
    author="Marty Thane",
    author_email="mzf@tuta.io",
    license="GPLv3",
    packages=find_packages(),
    install_requires=[
        "tabulate",
        "yt-dlp",
        "ytmusicapi",
    ],
    entry_points={
        "console_scripts": [
            "cotton=cotton.frontend:main"
            ]
    },
    python_requires=">=3.12.5",
)
