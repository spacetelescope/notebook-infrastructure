# Comprehensive Contributor Guide for GitHub Users: Jupyter Notebook CI System

## Introduction

This guide is designed for contributors working with the STScI Continuous Integration (CI) system for Jupyter notebooks on GitHub. It provides an overview of the process from creating a pull request to the automated checks and the subsequent steps based on the outcomes of these checks.

## Key Components

1. **Creating and Managing Pull Requests (PRs)**
2. **Automated Validation and Checks on PRs**
3. **Handling of Passed or Failed Checks**
4. **HTML Generation for GitHub Pages**
5. **Scheduled and Manual Executions**

## 1. Creating and Managing Pull Requests (PRs)

### Starting with a PR

As a contributor, you begin by creating a Pull Request for your Jupyter notebook directly in the main repository.
It is important to creat the PR merge to main from a branch on the main repository, due to security issues, you cannot merge to main directly from a fork.

If you are working from a fork, create a new branch on the main repository and merge your forked branch to it.  Then create a PR from this new fork, tests will now run correctly.

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

# Troubleshooting Guide for Jupyter Notebook CI System

When contributing to a GitHub project using a Continuous Integration (CI) system for Jupyter notebooks, encountering issues during the process is common. This troubleshooting guide aims to help you navigate through common problems, especially during pull request (PR) checks and notebook execution.

#### Finding Errors During PR Checks

1. **Check the PR Status and Details**: Whenever you submit a PR, the CI system initiates a series of automated checks. If there's an issue, the status section of the PR will indicate a failure. Click on the "Details" link next to the failed check to view the logs.

2. **Review Automated Feedback**: The CI system provides feedback and error messages directly in the PR conversation or in the checks section. Look for any error messages or warnings that could indicate what went wrong.

#### Handling Transient Data Access Errors

1. **Identify the Error**: Sometimes, notebooks fail due to transient issues like temporary network problems or external resource unavailability. These errors often include messages like "timeout," "connection error," or "resource temporarily unavailable."

2. **Re-Run the Notebook Execution**: If you suspect a transient error, you can re-trigger the CI checks. Typically, you can do this by adding a commit to your PR (even a small change like updating documentation or a comment in your notebook) or by using any re-run functionality provided by the CI system.

#### Addressing Common Notebook Execution Errors

1. **Requirements Issues**: Ensure that all dependencies required by your notebook are correctly listed and available. This includes checking the `requirements.txt` file or any other dependency management system in use. If a dependency is missing or there's a version conflict, your notebook might fail to execute properly.

2. **Syntax or Runtime Errors**: Review the execution logs for any Python syntax errors or exceptions thrown during runtime. These errors are usually well-documented in the logs, indicating the cell that caused the issue and the traceback.

3. **Output Validation Failures**: If your notebook uses output validation (e.g., with `pytest nbval`), ensure that the outputs in your notebook match the expected results. Fluctuations in data or non-deterministic outputs can cause these checks to fail.

4. **Security Issues**: The Bandit security check might flag potentially insecure code. Review the Bandit report linked in the PR checks section and address any highlighted issues.

#### General Tips for Troubleshooting

- **Local Testing**: Before submitting your PR, run your notebook locally from start to finish in a clean environment. This can help catch issues early on.
- **Isolate Changes**: If you're having trouble identifying the cause of a failure, try isolating changes to see if a specific modification is causing the issue.
- **Seek Help**: If you're stuck, don't hesitate to ask for help in the PR comments. The project maintainers or other contributors might offer valuable insights.

Remember, troubleshooting CI issues is often a process of trial and error. Patience and persistence are key to resolving these challenges and successfully contributing to the project.


## Conclusion

This CI system offers a streamlined, automated process for managing and maintaining Jupyter notebooks. Your role as a contributor is vital in upholding the quality and functionality of these notebooks.
