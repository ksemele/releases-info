from setuptools import setup, find_packages

REQUIRED = [
    "kubernetes>=29.0.0",
    "prometheus_client>=0.19.0",
    "prometheus-api-client>=0.5.5",
    "requests>=2.31.0",
    "PyYAML>=6.0.1",
    "icecream>=2.1.3",
    "urllib3>=2.2.0",
]

EXTRAS = {
    "test": [
        "pytest>=8.0.0",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.12.0",
        "pytest-asyncio>=0.23.5",
    ],
    "dev": [
        "pytest>=8.0.0",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.12.0",
        "pytest-asyncio>=0.23.5",
        "black>=24.2.0",
        "ruff>=0.2.0",
        "mypy>=1.8.0",
        "pre-commit>=3.6.0",
    ],
}

setup(
    name="releases_info",
    version="0.1.0",
    description="Docker image releases information collector",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(exclude=["tests*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Typing :: Typed",
    ],
    project_urls={
        "Source": "https://github.com/ksemele/releases-info",
        "Bug Reports": "https://github.com/ksemele/releases-info/issues",
    },
)
