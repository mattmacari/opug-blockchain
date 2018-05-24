import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opug_blockchain",
    version="0.0.0",
    author="Matthew Leick Macari",
    author_email="matthew.f.macari@gmail.com",
    description="A small example/toy project for Blockchain data structures.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattmacari/opug-blockchain",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
