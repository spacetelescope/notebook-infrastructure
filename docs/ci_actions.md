# Functional descriptions of actions located in spacetelescope/notebook-ci-action

## GitHub Action for Notebook Execution with Python Version Control and CASJOBS Authentication - ci_runner.yml

This GitHub Action, named "Scheduled Notebook Execution," is tailored for projects that require automated execution and validation of Jupyter Notebooks, with the added capability to specify the Python version and utilize CASJOBS authentication for notebooks that require external data access.

## Trigger
- **`workflow_call`**: Allows for modular integration into CI/CD pipelines, with customizable inputs for Python version and optional CASJOBS credentials.

## Inputs
- **`python-version`**: Specifies the Python version for the runtime environment, ensuring compatibility with notebook requirements.

## Secrets
- **`CASJOBS_USERID`** and **`CASJOBS_PW`**: Provide optional CASJOBS credentials for notebooks that interact with CASJOBS services, ensuring secure and authenticated data access.

## Jobs

### `gather-notebooks`
Identifies changed Jupyter Notebooks to optimize workflow execution by focusing only on modified content.

#### Steps:
1. **Checkout**: Retrieves the full repository history to accurately determine changed files.
2. **changed-files**: Lists modified `.ipynb` files using the `tj-actions/changed-files@v42` action, optimizing the workflow for relevant changes.
3. **set-matrix**: Converts the list of changed notebooks into a JSON array for dynamic job processing.

### `notebook-execution`
Executes and validates the identified notebooks, ensuring they function correctly and adhere to best practices.

#### Permissions:
- **`contents: write`**: Allows the workflow to commit and push changes, such as executed notebooks or fixed issues, back to the repository.

#### Strategy:
- **Fail-fast**: Disabled to ensure isolated handling of notebook execution results, allowing the workflow to proceed despite individual failures.

#### Steps:
1. **Checkout**: Prepares the repository content, including the full history for accurate file tracking and modification.
2. **Set up Python**: Configures the specified Python version, enhancing consistency and compatibility across execution environments.
3. **Add conda to system path**: Ensures access to conda for environment management and package installations.
4. **Install dependencies**: Installs required packages from local and global `requirements.txt` files, along with pre-installation scripts to prepare the environment.
5. **Security testing with Bandit**: Conducts static analysis on notebook files to identify potential security issues, promoting best coding practices.
6. **Validate notebooks**: Clears notebook outputs and validates execution using `nbval`, ensuring that notebooks are error-free and ready for execution.
7. **Execute notebooks**: Executes notebooks in-place, capturing and processing execution results. Failed executions trigger a script to insert a failure message, aiding in debugging and transparency.
8. **Commit modifications**: Commits executed or modified notebooks back to the current branch, ensuring that changes are tracked within the repository.
9. **Manage storage branch**: Handles the checkout and update of a dedicated storage branch (`gh-storage`), facilitating isolated storage of executed notebooks and supporting version control of computational results.

## Summary
The "Scheduled Notebook Execution" GitHub Action provides a comprehensive solution for maintaining, executing, and validating Jupyter Notebooks within a project. By incorporating dynamic Python version control, optional CASJOBS authentication, and focused execution on modified notebooks, this workflow ensures high-quality, functional, and secure notebook content, fostering reliability and reproducibility in computational projects.


## Scheduled Notebook Execution with Custom Python Version GitHub Action Documentation - ci_scheduled.yml

This GitHub Action, "Scheduled Notebook Execution," is designed for automated execution and validation of Jupyter Notebooks, with the flexibility to specify the Python version. It supports CASJOBS authentication for notebooks that require it, ensuring comprehensive testing and validation of notebook functionality.

## Trigger
- **`workflow_call`**: This action is triggered through workflow calls from other workflows, allowing for modular integration. It includes inputs for Python version customization and optional CASJOBS credentials.

## Inputs
- **`python-version`**: A required input specifying the Python version to be used for executing the notebooks. This allows for compatibility with various Python environments and requirements.

## Secrets
- **`CASJOBS_USERID`** and **`CASJOBS_PW`**: Optional secrets for CASJOBS authentication, enabling notebooks that interact with CASJOBS services to authenticate as needed.

## Jobs

### `gather-notebooks`
This job locates all Jupyter Notebook files within the `notebooks/` directory, preparing them for subsequent execution and validation.

#### Steps:
1. **Checkout**: Retrieves the repository code to access the notebook files.
2. **set-matrix**: Generates a matrix of notebook file paths using the `find` command and `jq` to create a JSON array for dynamic job processing.

### `tests`
This job orchestrates the execution and validation of the notebooks identified in the `gather-notebooks` job, using the specified Python version.

#### Strategy:
- **Fail-fast**: Disabled to ensure that issues in one notebook do not prevent the execution of others.
- **Matrix**: Constructed dynamically from the `gather-notebooks` job output, targeting only the identified notebooks for execution.

#### Steps:
1. **Checkout**: Ensures access to the repository's notebooks and any associated files.
2. **Set up Python**: Configures the specified Python version for the job, optimizing dependency installations with pip caching.
3. **Add conda to system path**: Makes conda commands accessible, aiding in environment and package management.
4. **Install dependencies**: Installs necessary packages from requirements files associated with the notebooks or the repository. Adjustments and pre-install scripts are executed as required to prepare the environment.
5. **Execute notebooks**: Converts notebooks to HTML and executes them, using CASJOBS credentials if provided. This step ensures that notebooks are not only syntactically correct but also functionally valid.
6. **Validate notebooks**: Employs `pytest` with `nbval` to verify that all notebook cells execute without errors, confirming the integrity and reliability of the notebook content.

## Summary
The "Scheduled Notebook Execution" GitHub Action facilitates the automated testing and validation of Jupyter Notebooks in a customizable Python environment. By incorporating CASJOBS authentication and allowing for Python version specification, this workflow ensures that notebooks are compatible, functional, and secure, maintaining high standards of quality and reliability within the project.


## GitHub Action for Broken Link Checking on GitHub Pages - broken_link_checker.yml

This GitHub Action is designed to automate the process of identifying and reporting broken links within the HTML pages of notebooks deployed to GitHub Pages. It provides an essential quality check to ensure the integrity and reliability of project documentation or educational content.

## Workflow Configuration

### Triggers
- **`workflow_call`**: This action is configured to be invoked by other workflows, allowing for flexible integration into different CI/CD pipelines.

### Inputs
- **`website_url`** (optional): Specifies the URL to be checked for broken links. The default value targets the GitHub Pages site associated with the repository (`https://spacetelescope.github.io/<repository-name>`). For more precise control, it's recommended to specify the full URL to the starting page of the site (e.g., `https://spacetelescope.github.io/<repository-name>/intro.html`).

## Jobs

### `find_broken_links`
This job systematically scans the specified website URL for broken links, employing a dedicated action for thorough link evaluation.

#### Environment
- **`runs-on: ubuntu-latest`**: Executes the job on the latest Ubuntu runner provided by GitHub Actions, ensuring a modern and consistent environment for link checking.

#### Steps
1. **Broken-Links-Crawler**: Utilizes the `ScholliYT/Broken-Links-Crawler-Action@v3.3.1` to crawl the specified website and identify any broken links.
   - **`website_url`**: The target website URL derived from workflow inputs, directing the crawler's focus.
   - **`resolve_before_filtering`**: Ensures URLs are resolved before any filtering is applied, enhancing the accuracy of the link check.
   - **`verbose`**: Set to 'Error' to streamline the output, focusing on critical issues.
   - **`max_retry_time`** and **`max_retries`**: Configures retry logic to address transient network issues, improving the robustness of the check.
   - **`exclude_url_prefix`**: Excludes specific URL prefixes from the check, such as 'mailto:' links and GitHub issue creation URLs, to prevent false positives.

## Summary
This GitHub Action offers a proactive approach to maintaining the quality and user experience of documentation hosted on GitHub Pages. By regularly checking for and addressing broken links, projects can ensure their online content remains accessible, relevant, and user-friendly.

## PEP8 Notebook Style Check Execution GitHub Action Documentation - notebook_pep8check.yml

This GitHub Action is designed to enforce PEP8 style guidelines within Python code contained in Jupyter Notebook cells. By integrating this workflow, projects can ensure their notebook code adheres to standard Python coding conventions, promoting readability and maintainability.

## Workflow Configuration

### Triggers
- **`workflow_call`**: Enables this action to be invoked by other workflows, allowing for flexible integration into various CI/CD pipelines.

### Inputs
- **`python-version`**: Specifies the Python version to be used for setting up the environment, ensuring compatibility with the project's requirements.

## Jobs

### `gather-notebooks`
Identifies modified Jupyter Notebooks for PEP8 checks, optimizing the workflow to focus on relevant changes.

#### Conditional Execution
- The job only triggers for open pull requests, ensuring that style checks are performed in the context of ongoing changes rather than on merged or closed content.

#### Steps:
1. **Checkout**: Retrieves the repository's code to access the Jupyter Notebook files.
2. **changed-files**: Lists modified `.ipynb` files using `tj-actions/changed-files@v41.0.1`, targeting only the notebooks that have been changed.
3. **set-matrix**: Converts the list of changed notebooks into a JSON array, facilitating dynamic job processing based on modified content.

### `notebook-style-checks`
Executes PEP8 style checks on the identified notebooks, utilizing a custom script for detailed evaluation.

#### Environment
- **`ci_env`**: Specifies the environment in which the job runs, potentially including specific configurations or secrets relevant to CI processes.

#### Strategy
- **Fail-fast**: Disabled to allow individual notebook checks to proceed independently, ensuring comprehensive style evaluation across all modified notebooks.

#### Steps:
1. **Checkout**: Prepares the repository's content for access to the notebooks and associated resources.
2. **Set up Python**: Configures the specified Python environment, optimizing dependency installations with pip caching.
3. **Add conda to system path**: Ensures that conda commands are accessible for managing environments and dependencies.
4. **Install dependencies**: Installs `flake8` for PEP8 compliance checking, along with other dependencies like `numpy` and `pytz` that might be required for notebook execution.
5. **Check-out notebook-ci-actions repository**: Retrieves a helper script for PEP8 checks from a dedicated repository, ensuring access to up-to-date and maintained tools for style evaluation.
6. **Run PEP8 style check**: Executes the PEP8 checker script on the modified notebooks, identifying any deviations from the PEP8 guidelines and reporting them for review and correction.

## Summary
The "PEP8 Notebook Style Check Execution" GitHub Action facilitates the automated enforcement of PEP8 coding standards within Jupyter Notebooks. By focusing on modified notebooks and employing a dedicated style checking script, this workflow contributes to the maintenance of high-quality, readable, and consistent Python code across notebook-based projects.

