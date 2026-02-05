from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docgenny",
    version="0.1.0",
    author="Bailey Armitage",
    author_email="bailey.sdev@gmail.com",
    description="Automatically generate comprehensive technical documentation from Python codebases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rexbrandy/docgenny",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses only stdlib!
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "docgenny=docgenny.cli:main",
        ],
    },
    keywords="documentation generator automatic docs markdown python ast",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/docgenny/issues",
        "Source": "https://github.com/yourusername/docgenny",
        "Documentation": "https://github.com/yourusername/docgenny#readme",
    },
)