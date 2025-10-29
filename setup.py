import setuptools

from gpuview import __version__


def read_readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setuptools.setup(
    name="gpuview",
    version=__version__,
    license="MIT",
    description="A lightweight web dashboard for monitoring GPU usage",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/fgaim/gpuview",
    author="Fitsum Gaim",
    author_email="fitsum@geezlab.com",
    keywords="gpu web-monitoring",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Hardware",
    ],
    packages=["gpuview"],
    python_requires=">=3.9",
    install_requires=["gpustat>=1.1.1", "bottle>=0.12.25", "requests>=2.25.0"],
    extras_require={
        "dev": ["pytest", "pytest-cov", "flake8"],
        "test": ["pytest", "pytest-cov"],
    },
    entry_points={
        "console_scripts": [
            "gpuview=gpuview.app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
