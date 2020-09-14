import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="azure_helpers",
    version="0.0.2",
    author="Sanath Manavarte",
    author_email="msanath@gmail.com",
    description="A package which uses azure SDK for creating simple resources and managing them.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msanath/azure-helpers.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'azure-cli-core',
        'azure-mgmt-compute==13.0.0'
    ]
)
