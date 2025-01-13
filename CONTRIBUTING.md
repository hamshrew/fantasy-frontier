
# Contributing to Fantasy Frontier

Thank you for considering contributing to Fantasy Frontier! This document outlines the guidelines for contributing to the project to ensure consistency and maintain quality.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
    - [Reporting Issues](#reporting-issues)
    - [Submitting Code Changes](#submitting-code-changes)
    - [Suggesting Features](#suggesting-features)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Setting Up the Project](#setting-up-the-project)

---

## Code of Conduct

By contributing, you agree to uphold a respectful and collaborative environment. Be kind and constructive in your interactions. Harassment or offensive behavior will not be tolerated.

---

## How to Contribute

### Reporting Issues

- Check the [issue tracker](https://github.com/hamshrew/fantasy-frontier/issues) to see if your problem or idea has already been reported.
- If not, create a [new issue](https://github.com/hamshrew/fantasy-frontier/issues/new). Be as detailed as possible:
  - Describe the issue or feature request.
  - Include steps to reproduce (if it's a bug).
  - Mention relevant versions or configurations.

### Submitting Code Changes

1. **Fork the Repository**: Create your own copy of the project.
2. **Create a New Branch**: Use descriptive branch names (e.g., `feature/building-placement` or `bugfix/resource-calculation`).
3. **Make Changes**: Ensure your code adheres to the [Coding Standards](#coding-standards).
4. **Write Tests**: Add or update unit tests in the `tests/` directory to cover your changes.
5. **Submit a Pull Request**:
    - Provide a clear description of the changes.
    - Reference any relevant issue numbers.
    - Request a review when ready.

### Suggesting Features

- Create a detailed feature request in the [issue tracker](https://github.com/hamshrew/fantasy-frontier/issues/new).
- Include:
  - The problem the feature addresses.
  - How the feature improves the game.
  - Possible implementation ideas (optional).

---

## Development Workflow

1. Clone the repository:

    ```bash
    git clone https://github.com/hamshrew/fantasy-frontier.git
    cd fantasy-frontier
    ```

2. Create a virtual environment and install dependencies:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Run tests to confirm everything is working:

    ```bash
    pytest
    ```

### Running the Game

Use the following command to start the game (if applicable):

```bash
python -m ffrontier.main
```

---

## Coding Standards

Follow these guidelines to ensure consistency across the codebase:

### General Style

- Adhere to **PEP 8** standards (enforced with `flake8`).
- Use a maximum line length of **100 characters**.
- Write clear, descriptive function and variable names.

### Comments and Docstrings

- Use **docstrings** for all public classes and functions.
- Focus comments on the *why*, not the *what* (e.g., explain decisions rather than restating code).

Example:

```python
def hex_distance(a: Hex, b: Hex) -> int:
    """
    Calculate the distance between two hexes in the grid.

    Args:
        a (Hex): The first hex.
        b (Hex): The second hex.

    Returns:
        int: The Manhattan distance between the two hexes.
    """
    return max(abs(a.q - b.q), abs(a.r - b.r), abs(a.s - b.s))
```

### Testing

- Add tests for every new feature or bugfix in the `tests/` directory.
- Use `pytest` to ensure all tests pass before submitting changes.

### Commit Messages

- Write clear, descriptive commit messages.
- Format:

    ```text
    [Type]: Brief summary

    [Optional] More detailed explanation if necessary.
    ```

    Example:

    ```text
    Feature: Add building placement functionality

    Users can now place and remove buildings on the hex grid using the UI.
    ```

---

## Setting Up the Project

1. Clone the repository and set up the virtual environment (as described in the [Development Workflow](#development-workflow)).
2. Install additional tools for linting and type checking:

    ```bash
    pip install flake8 mypy
    ```

3. Run `flake8` to check code style:

    ```bash
    flake8 ffrontier
    ```

4. Run `mypy` to check type hints:

    ```bash
    mypy ffrontier
    ```

---

Thank you for contributing to Fantasy Frontier!
