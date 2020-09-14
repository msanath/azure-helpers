# Azure Helpers

This is a simple project which makes use of azure's python SDK to create simple resources in azure. Today, you can use the helpers to perform basic CRUD operations on

* [Virtual Machine Scale Sets](https://docs.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview)


## Using the package

To start using the helpers, run

> `pip install azure-helpers`

Follow examples in the examples directory to use the library.


## Developing the package
To extend the package and customize it further, import it from git and run the following to setup a virtual environment:

> `python3 -m venv`\
> `source bin/activate`\
> `pip install -r requirements.txt`

Before merging to the main branch, make sure you generate the distribution archives.
From the directory containing `setup.py`, run:

> `python3 -m pip install --user --upgrade setuptools wheel`\
> `python3 setup.py sdist bdist_wheel`

For more information, refer [python packaging tutorial](https://packaging.python.org/tutorials/packaging-projects/).

**Note**: The git repository also contains settings file for [Visual Studio Code](https://code.visualstudio.com/).