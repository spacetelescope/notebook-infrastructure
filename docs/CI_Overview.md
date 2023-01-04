# Continuous Integration System for Jupyter Notebooks Overview

Welcome to the CI system for Jupyter notebooks! This system is designed to help developers test and validate their notebooks, as well as generate clear documentation for them.

The system is built using GitHub Actions, which are stored in the 'notebooks-actions' repository to allow for global updates. When a user submits a pull request (PR) with a new or updated notebook, the system automatically executes and validates the notebook as a pre-merge check. If the notebook is successfully validated and executed, the executed version of the notebook is pushed to the 'gh-storage' branch to be used in the later weekly validation and execution process.

Jupyterbook is a powerful tool that allows you to customize the appearance and functionality of your documentation. You can configure the table of contents to your liking, add a Google Analytics tracking ID to gather usage statistics, and even customize the CSS and logos to match your brand.

In addition to the testing and documentation actions, the system also includes a security testing action using bandit. This action scans the notebooks for any potential security vulnerabilities and reports any findings in the PR.

## How each action works

- **Jupyter nbconvert**: This action is used to execute the notebooks and ensure that they are free of syntax errors and run correctly. When a PR is submitted, the action will run the notebooks using nbconvert, and check for any errors that may have occurred during execution. If any errors are found, they will be highlighted in the PR so that the user can fix them before merging their changes.

- **Pytest nbval**: This action is used to validate the notebooks and ensure that their output is as expected. When a PR is submitted, the action will run the notebooks using nbval and compare the output to the expected results. If there are any discrepancies, they will be highlighted in the PR so that the user can investigate and fix the issue.

- **Jupyterbook**: This action is used to generate clean, easy-to-read HTML documentation for the notebooks. When a PR is submitted, the action will run the notebooks through jupyterbook, which will generate a HTML version of the notebook with a customizable table of contents, Google Analytics tracking ID (if provided), and customizable CSS and logos. This allows users to easily navigate and read the documentation for the notebooks, and also helps you gather useful usage statistics and tailorthe documentation to match your brand.

- **Bandit**: This action is used to scan the notebooks for potential security vulnerabilities. When a PR is submitted, the action will run the notebooks through bandit and report any findings in the PR. This helps to ensure that the notebooks are secure and do not introduce any security risks.

In addition to running these actions when a PR is submitted, the system also runs weekly execution and validation against the notebooks in the 'gh-storage' branch to ensure that they remain error-free and up-to-date. This helps to ensure that the notebooks are always in good working condition and ready to be used.

If any failures arise during the pre-merge checks or the weekly execution and validation process, they will be reported back and can be accessed through the Actions tab of the repository. This makes it easy to identify and fix any issues that may arise.

To make it easy for developers to get started with the CI system, we've also included a deployable template for new notebook repositories. This template sets up the necessary actions and structure for testing and documentation, so that developers can quickly get their notebooks up and running with the system.

We hope that this CI system helps you easily maintain and improve your notebooks. If you have any questions or suggestions, please don't hesitate to let us know. Happy coding!
