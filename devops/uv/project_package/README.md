# Replicate .toml file


[project]
name = "project-package"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "git-username", email = "git-email" }
]
requires-python = ">=3.13"
dependencies = []

[project.scripts]
# project-package is the name of the package
# to rn `uv run name-of-the-package` i.e `uv run project-package`
# it will run main function in the project_package/__init__.py file
# file to run can be changed
project-package = "project_package:main"

# custom cli commands can be added
# custom-key = "project_package:file-name:function-name"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
