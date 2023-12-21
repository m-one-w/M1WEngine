# Reluctant Hero
### Inspired by the alter ego of a popular gaming franchise character


## Table of contents
- [Documentation](#documentation)
- [Installation](#installation)
- [Development Environment](#development-environment)
    - [Libraries and Dependencies](#libraries-and-dependencies)
    - [GitHub Actions](#github-actions)
    - [Pull Request Guidelines](#pull-request-guidelines)
    - [Recommended IDE](#recommended-ide)
    - [Running the Game](#running-the-game)
- [Gameplay and Mechanics](#gameplay-and-mechanics)
- [System Design](#system-design)
- [Agile Guidelines](#agile-guidelines)
- [Further References](#further-references)

## Documentation
All documentation for the project can be found [here](./docs/).

## Installation
Installation instructions assume windows 10 is in use.

To run this program, Python 3.11.1 is required.
If Python is not installed or not the correct version download the windows installer from
[Python 3.11.1 Download](https://www.python.org/downloads/release/python-3111/)

To install the project dependencies, pip is required. pip should be included in Python when downloading from python.org.
Upgrade pip with the following command:
```
py -m pip install --upgrade pip
```
Ensure your terminal is navigated to the correct directory where this repository exists locally.

Install all dependencies with the following command:
```
pip install -r /path/to/requirements.txt
```
The requirements.txt is located in the top-level directory of the repository.

## Development Environment
### Libraries and Dependencies
The project utilizes pygame as the main game engine.

To ensure quality code is being committed to this project, the following linters are currently in use:
* Flake8 is used for style guide quality ensurance.
* Black python code formatter is used for formatting code consistently across developers and commits.
* PyDocStyle is used to ensure proper documentation is present throughout the code base.

There is a script "linter.sh" at the base of the repository that will run all of the above linters.
Extension settings have been included to run this script on every save in the .vscode settings file.

### GitHub Actions
On pull requests, a GitHub action will be run to lint commits being submitted for merging.

The GitHub action will run both the flake8 code style check and the black code formatter. If either lint checks fail, the PR will not be approved.

### Pull Request Guidelines
When submitting a pull request ensure all of the following have been completed:
* Break down the commits into code that solely completes the function of what is described in the commit header or commit body.
* Ensure all code is consistent in style and format.
* Do not mix in formatting commits into functional commits unless the formatting is done to code that has had its function changed.
* Review your code first before requesting a reviewer.

### Recommended IDE
It is recommended to use Visual Studio Code IDE. Please install the following plugins if using VS Code:
* Python
* Pylance
* isort
* autorun

### Running the Game
To run the game from within Visual Studio Code, navigate to the game.py file and select the run python file button in the top right corner of the IDE.

Alternatively, right click on the game.py file and click 'run python file in terminal'

## Gameplay and Mechanics
The objective of Reluctant Hero is to maximize your score while traversing the map.
A detailed spec sheet of the mechanics can be found [here](./docs/spec_sheet.md)

## System Design
The system design document was created through the draw.io web UI.
All system modules are created to reflect the design choices defined in the [system design specification](./docs/Reluctant_Hero_System_Design.png)

## Agile Guidelines
The agile story point estimates are defined in the following [documentation](./docs/agile_guide_lines.md)

## Further references
This project was initially based on the following youtube tutorial:
[Create a Zelda-style game in Python](https://www.youtube.com/watch?v=QU1pPzEGrqw)

It is recommended new developers watch this youtube tutorial before submitting any pull requests to come up to speed on the project.