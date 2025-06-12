from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="zentix-clean",
    version="0.1.0",
    author="Zentix Team",
    author_email="contact@zentix.ai",
    description="نظام التعلم الذاتي المتقدم",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zentix/zentix-clean",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "zentix=zentix.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "zentix": ["config/*.yaml", "templates/*.html"],
    },
) 