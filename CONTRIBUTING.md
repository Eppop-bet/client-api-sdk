# Contributing to Esource.gg Python SDK

We welcome contributions from the community to help improve the library.

This document provides guidelines for contributing to this project. Please feel free to propose changes to this document in a pull request.

## How Can I Contribute?

There are several ways you can contribute:

*   **Reporting Bugs:** If you find a bug, please report it by opening an issue.
*   **Suggesting Enhancements:** Have an idea for a new feature or an improvement? Open an issue to discuss it.
*   **Submitting Pull Requests:** If you've fixed a bug or implemented an enhancement, you can submit a Pull Request.

## Reporting Bugs

Before submitting a bug report, please check the existing [issues](https://github.com/Eppop-bet/client-api-sdk/issues) to see if the problem has already been reported. If it hasn't, please open a new issue and include the following:

*   A clear and descriptive title.
*   A detailed description of the problem, including steps to reproduce it.
*   The version of `esource-client-api` you are using (`pip show esource-client-api`).
*   Your Python version.
*   Any relevant error messages or stack traces.

## Suggesting Enhancements

If you have an idea for an enhancement:

1.  Check the [issues](https://github.com/Eppop-bet/client-api-sdk/issues) to see if a similar enhancement has already been suggested.
2.  If not, open a new issue describing the enhancement:
    *   Use a clear and descriptive title.
    *   Explain why this enhancement would be useful.
    *   Provide as much detail as possible about the proposed changes or functionality.

## Pull Request Process

We welcome pull requests! Here's the general process for submitting code changes:

1.  **Fork the Repository:** Click the "Fork" button on the [repository page](https://github.com/Eppop-bet/client-api-sdk). This creates your own copy of the project.
2.  **Clone Your Fork:** Clone your forked repository to your local machine:
    ```bash
    git clone https://github.com/YOUR_USERNAME/client-api-sdk.git
    cd client-api-sdk
    ```
3.  **Create a Branch:** Create a new branch for your changes, based off the `main` branch:
    ```bash
    git checkout main
    git pull origin main  # Ensure you have the latest changes from the upstream main
    git checkout -b feature/your-descriptive-feature-name
    # Or for bug fixes:
    # git checkout -b fix/short-description-of-fix
    ```
4.  **Set Up Development Environment:** Install the necessary dependencies, including development tools:
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    # Consider using a virtual environment
    ```
5.  **Make Your Changes:** Implement your bug fix or enhancement.
6.  **Add Tests:** If you're adding new functionality or fixing a bug, please add corresponding tests in the `tests/` directory.
7.  **Run Checks:** Ensure your code passes linting and tests locally before pushing:
    ```bash
    # Run linter
    flake8 .
    # Run tests
    pytest
    ```
8.  **Commit Your Changes:** Use clear and concise commit messages. Reference related issues if applicable (e.g., `Fix #123: Correct handling of XYZ parameter`).
    ```bash
    git add .
    git commit -m "feat: Add support for new endpoint XYZ"
    # Or: git commit -m "fix: Correct handling of None values in ABC (#123)"
    ```
9.  **Push to Your Fork:** Push your feature branch to your forked repository on GitHub:
    ```bash
    git push origin feature/your-descriptive-feature-name
    ```
10. **Open a Pull Request:**
    *   Go to the original [repository](https://github.com/Eppop-bet/client-api-sdk) page on GitHub.
    *   You should see a prompt to create a Pull Request from your recently pushed branch. Click it. If not, navigate to the "Pull requests" tab and click "New pull request".
    *   Ensure the base repository is `Eppop-bet/client-api-sdk` and the base branch is `main`.
    *   Ensure the head repository is your fork and the compare branch is your feature branch.
    *   Provide a clear title and description for your Pull Request, explaining the changes and referencing any related issues (e.g., `Closes #45`).
11. **Address Feedback:**
    *   Wait for the automated checks (GitHub Actions) to complete and ensure they pass.
    *   Project maintainers will review your PR. Be prepared to respond to comments and make necessary adjustments.
    *   Once approved and all checks pass, a maintainer will merge your Pull Request.

## Code Style

This project uses `flake8` for linting. Please ensure your code conforms to the style guidelines enforced by the configuration in the `.flake8` file by running `flake8 .` before committing.

## Licensing

By contributing to this project, you agree that your contributions will be licensed under the MIT License that covers the project.
