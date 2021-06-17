# Behave

## _Web Automation Project With Pythton and Selenium_
- CK-12 Foundation is a non-profit organization dedicated to increasing access to high quality educational materials for K-12 students all over the world
- In this project we write automation test cases for checking www.ck12.org functionality
- We use Selenium Page Object Model with Python

## Project Installation

If you set up SSH (instructions in the section **GitHub** below),
then run:
```sh
git@github.com:arturadamian/selenium_python_behave.git
```
If not, run:
```sh
https://github.com/arturadamian/selenium_python_ck12.git
```
and then enter your GitHub email and password
******************************************************************
For Windows you might need to set up your Personal Access Token:

Login to [GitHub](www.github.com)

Go to:
```
Account settings --> Developer settings --> Personal access tokens --> Generate new token
Write a Note --> Check on repo --> Press Generate token --> Copy token
```
********************************************************************

After cloning the repo, you can open it with any editor, but if you like VSCode ;)

Then run:
```sh
code ck12
```

## Requirements

To make sure you have all the required packages

In your terminal run:
```sh
cd ck12
pip install -r _requirements.txt
```
**Requirements.txt** *file contains*

| Package | Description |
| ------ | ------ |
| selenium | [pypi/selenium](https://pypi.org/project/selenium/) |
| webdriver-manager | [pypi/webdriver-manager](https://pypi.org/project/webdriver-manager/) |
| pytest | [pypi/pytest](https://pypi.org/project/pytest/) |

*****************************************************************

## Project Settings
File **.vscode/settings.json** contains
```js
"terminal.integrated.env.osx": {
    "PYTHONPATH": "${workspaceFolder}/src"
}
```
> Note:
> By default it is set for Mac
> If you are on Windows replace it with
```js
"terminal.integrated.env.windows": {
    "PYTHONPATH": "${workspaceFolder}/src"
}
```
> Note:
> Workspace settings enable you to configure settings in the context 
> of the workspace you have opened and always override global user settings

Please, add this line if you use virtual environment
```js
"python.venvPath": ".venv"
```
> Note:
> `Virtual Environment is not neccessary`
> However, you can install it with the steps below

```sh
python -m venv .venv
```
to activate / deactivate virtual environment for Mac run
```sh
source .venv/bin/activate
deactivate
```
to activate / deactivate virtual environment for Windows run
```sh
.venv\Scripts\activate
deactivate
```
