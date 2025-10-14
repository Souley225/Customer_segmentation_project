from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="customer_segmentation_project",
    version="1.0.0",
    author="Souley225",
    description="Projet d'analyse de segmentation client et recommandation produit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Souley225/customer_segmentation_project",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Business/Financial",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "run-segmentation=src.main:main",
        ],
    },
    package_data={
        "customer_segmentation_project": [
            "config/*.yaml",
        ],
    },
    include_package_data=True,
)