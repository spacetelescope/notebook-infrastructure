# Comprehensive Contributor Guide for GitHub Users: Jupyter Notebook CI System

## Introduction

This detailed guide is designed for contributors working with the STScI Continuous Integration (CI) system for Jupyter notebooks on GitHub. It provides an overview of the process from creating a pull request to the automated checks and the subsequent steps based on the outcomes of these checks.

## Key Components

1. **Creating and Managing Pull Requests (PRs)**
2. **Automated Validation and Checks on PRs**
3. **Handling of Passed or Failed Checks**
4. **HTML Generation for GitHub Pages**
5. **Scheduled and Manual Executions**

## 1. Creating and Managing Pull Requests (PRs)

### Starting with a PR

As a contributor, you begin by creating a Pull Request for your Jupyter notebook directly in the main repository.

#### How to Create a PR

- **Prepare Your Notebook**: Make sure your Jupyter notebook is complete and aligns with the repository's guidelines.
- **Create a New Branch**: In the repository, create a new branch for your notebook. This helps in isolating your changes.
- **Add Your Notebook**: Add your notebook to the appropriate directory within your branch.
- **Commit and Push**: Commit your changes with a descriptive message and push the branch to the repository.
- **Open a PR**: On GitHub, navigate to the main repository, click on 'New Pull Request', and select your branch. Provide a detailed description of your changes in the PR template.

### What the Contributor Should Expect

- **Automated Feedback**: Automated checks will start as soon as the PR is opened. Progress can be tracked on the PR page.
- **Communication**: Be proactive in responding to comments or suggestions from reviewers or maintainers within the PR.

## 2. Automated Validation and Checks on PRs

### Upon PR Creation

#### Bandit Security Check

- **Execution**: Bandit runs automatically to scan your notebook for security issues.
- **Review**: Check the Bandit report for any potential security flaws and address them if necessary.

#### Notebook Execution via `nbconvert`

- **Process**: The notebook is fully executed, ensuring all code cells function as intended.
- **Observation**: Keep an eye out for any execution errors and be prepared to make corrections.

#### Validation with `pytest nbval`

- **Validation**: This step checks for the accuracy and consistency of the notebook's output.
- **Results**: Monitor the validation results. Resolve any discrepancies that arise.

## 3. Handling of Passed or Failed Checks

### If Checks Pass

- **Merging**: If all checks are successful, the notebook is ready to be merged into the main branch.
- **Storage**: The merged notebook is then stored in the 'gh-storage' branch.

### If Checks Fail

- **Notification**: Failure notifications will appear directly on the PR page.
- **Diagnosis**: Use the detailed reports and tracebacks to identify and fix the issues.
- **Resolution**: Update your PR with the necessary changes. This reinitiates the automated checks.

## 4. HTML Generation for GitHub Pages

### After PR Merge

- **Conversion to HTML**: Following the merge, your notebook is automatically converted to an HTML page.
- **Publishing**: This HTML version is then published on the project’s GitHub Pages.

### Access and Distribution

- **Viewing**: You can view the published notebooks on the GitHub Pages site.
- **Sharing**: Share the GitHub Pages link to increase the visibility of your work.

## 5. Scheduled and Manual Executions

### Regular Automated Updates

- **Scheduled Runs**: The system executes all notebooks in the repository periodically to ensure they are up-to-date and functional.

### Manual Utility Actions

- **Manual Execution**: You can manually trigger the execution of all notebooks for immediate validation.
- **Complete Overhaul**: A comprehensive action is available for a full re-execution and HTML regeneration, to be used selectively.

## Conclusion

This CI system offers a streamlined, automated process for managing and maintaining Jupyter notebooks. Your role as a contributor is vital in upholding the quality and functionality of these notebooks.
