# M1WEngine
### A game engine built on top of pygame

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
- [Community](#Community)

M1WEngine is an open source game engine that is being added to PyPi for use in creating games.

"M1" is a reference to the first mouse button, while "W" refers to the commonly used key for walking forward in video games. The name can be interpreted as "walk forward and and attack" in the context of a video game.

## Documentation
All documentation for the project can be found [here](./docs/).

## Installation

After the initial release install with the following command:

```
pip install m1wengine
```

M1WEngine has not yet reached the point where it is ready to be added to PIP.
Feel free to use a local build of the library instead.

See the development environment setup to make use of the library before the initial release.

In any project you can now import game engine modules with the following lines of code:
```
from m1wengine.{module name} import {object name}
```

An example of importing the score controller is given below:
```
from m1wengine.score_controller import ScoreController
```

## Development Environment
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

Install the local wheel so that imports can be reference in any project on the local machine
```
./wheel_builder.sh
```

### Libraries and Dependencies
The project utilizes pygame as the main game engine.

To ensure quality code is being committed to this project, the following linters are currently in use:
* Flake8 is used for style guide quality ensurance.
* Black python code formatter is used for formatting code consistently across developers and commits.
* PyDocStyle is used to ensure proper documentation is present throughout the code base.

There is a script "linter.sh" at the base of the repository that will run all of the above linters.
Extension settings have been included to run this script on every save in the .vscode settings file.

The vscode extension to make use of this script is called the "Run on Save" extension by emeraldwalk.

### GitHub Actions
On pull requests, a GitHub action will be run to lint commits being submitted for merging.

The GitHub action will run the flake8 code style check and the black code formatter. If either lint checks fail, the PR will not be approved.

### Pull Request Guidelines
When submitting a pull request ensure all of the following have been completed:
* Break down the commits into code that solely completes the function of what is described in the commit title and commit body.
* The commit title should start with a capital letter and have no ending punctuation.
* The commit body should have complete sentences and fully correct punctuation.
* Ensure all code is consistent in style and format.
* Do not mix in formatting commits into functional commits unless the formatting is done to code that has had its function changed.
* The scope of commits within a single PR should not overlap.
  * Code is not added and than deleted accross commits in a single PR.
  * Code is not modified multiple times in a single PR on multiple commits.
* Do not include merge commits.
* Try your best to not introduce bugs into the main branch.
* Review your code first before requesting a reviewer.

### Recommended IDE
It is recommended to use Visual Studio Code IDE. Please install the following plugins if using VS Code:
* Python
* Pylance
* isort
* autorun
* behave

### Running the Game
An example of a fully functional game utilizing the library will exist within the test/ directory.
To run the game from within Visual Studio Code, navigate to the game.py file and select the run python file button in the top right corner of the IDE.

Alternatively, right click on the game.py file and click 'run python file in terminal'

## Gameplay and Mechanics
The supported gameplay and mechanics are highly focused to support a specific game. This is intended to change as more projects make use of this game engine and submit additional features through pull requests.

The current core features include:
* A state machine for NPC automated movement
* Asset loading
* A camera manager
* A complex movement system for all sprites to make use of
* Complex collision detection logic

## System Design
The system design document was created through the draw.io web UI.
All system modules are created to reflect the design choices defined in the [system design specification](./docs/M1WEngine_System_Design.png)

## Community
There is an active discord server for this project where you can meet the maintaners and ask any questions about features, or just join to hang out! The discord server can be found trough the following link:
```
https://discord.gg/vqdnJBfeT8
```

## License
The license is an MIT open source initiave approved license. You may view it [here](LICENSE.md). Use of, copying, and modifying this project are all welcome and allowed. Please consider contributing to this open source project to show your appreciation for the hard work of the community in developing this software.