# mark-calculator

A simple cli tool designed to help calculate the required marks for each of your university modules to reach a target overall grade. It takes into account the credit weighting of each module, allowing you to easily determine what grade you need in each module to achieve your target grade.

## Usage

You can easily start the app using docker, like so

```bash
docker run --rm -v mark-calculator:/app/data mark-calculator
```

If you have python installed, you can also just run

```bash
python3 main.py
```

from within the root directory.

First, you will need to add your modules - add all modules, including ungraded ones.

```bash
docker run --rm -v mark-calculator:/app/data mark-calculator add --name="My module" --credits=20 --grade=65
```

If your module has not received a grade, do not add the `--grade` flag.

If you want to remove a module after adding one, run the following

```bash
docker run --rm -v mark-calculator:/app/data mark-calculator remove --name="My module"
```

Once all modules have been added, you can run the file with no command prefix, like so

```bash
docker run --rm -v mark-calculator:/app/data mark-calculator --target=70
```

where `--target` is the overall target grade you wish to achieve.

For all commands and flags, run `--help`

## Install

If you have python installed, you do not need to install anything, just ensure you are using python 3.13.x otherwise there may be unintended side effects.

To easily get started without python, you can use docker. Firstly, you need to build the image by running the following command in the root directory:

```bash
docker build -t mark-calculator .
```

Once completed, you can simply [get started](#usage).

## Todo

- Add option to store specific test scores for a module, to determine the required % for the remaining test scores
- Add a "confidence" score for each module, so you can apply weighting to each one based on how well you think you can do
