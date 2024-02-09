# Third Party Library
from setuptools import find_packages, setup

setup(
    name="project",
    version="0.1.0",
    description="",
    author="None",
    author_email="shaheer2511@outlook.com",
    keywords="project",
    license="",
    url="",
    python_requires="~=3.8",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=False,
    install_requires=[
        #place required modules to be installed along with the version control
    ],
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
