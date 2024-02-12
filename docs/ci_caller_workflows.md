# Scheduled Notebook Execution GitHub Action Documentation

The "Scheduled Notebook Execution" GitHub Action is designed to automate the regular execution of Jupyter Notebooks within a repository. This scheduled execution ensures that notebooks remain functional over time and that their outputs are up-to-date.

## Trigger
- **Schedule:**
  - The workflow is configured to trigger automatically at midnight UTC every Sunday (`0 0 * * 0`). This scheduling allows for weekly checks of the notebooks, providing a balance between frequent testing and resource utilization.

## Jobs

### Scheduled
This job is tasked with the execution of Jupyter Notebooks according to the specified schedule.

#### Details:
- **Operation:** The job incorporates an external workflow, `ci_scheduled.yml` from the `spacetelescope/notebook-ci-actions` repository, at its `v3` iteration. This external workflow is optimized for the execution of Jupyter Notebooks, handling the setup, execution, and any post-execution steps required to validate notebook functionality.
- **Purpose:** Automating the execution of notebooks on a weekly basis helps identify and rectify any issues that may arise due to changes in dependencies, data, or the notebooks themselves. This proactive approach ensures the integrity and reliability of the notebooks over time.

#### Parameters:
- **`python-version`:** The job utilizes the `${{ vars.PYTHON_VERSION }}` variable to specify the Python environment for notebook execution. This allows for the notebooks to be run in an environment that matches their requirements, ensuring compatibility and reducing the likelihood of execution errors.

## Summary
The "Scheduled Notebook Execution" GitHub Action facilitates the ongoing validation and maintenance of Jupyter Notebooks by scheduling their automatic execution on a weekly basis. By leveraging an external, specialized workflow, this action ensures that notebooks remain functional and their content relevant, contributing to the overall quality and usability of the repository's resources.


# Manual Execute All Notebooks GitHub Action Documentation

The "Manual Execute All Notebooks" GitHub Action is designed for on-demand execution of Jupyter Notebooks within the repository. Below is an overview of its configuration and operational details.

## Trigger
- **Type:** `workflow_dispatch`
- **Description:** This action is triggered manually, either through the GitHub UI or via the GitHub API, allowing for flexible execution timing.

## Jobs

### ExecuteNotebooks
This single job is responsible for the execution of all Jupyter Notebooks.

#### Details:
- **Operation:** The job delegates its execution to an external workflow from the `spacetelescope/notebook-ci-actions` repository. It specifically invokes the `.github/workflows/ci_scheduled.yml` workflow at its `v3` version.
- **Purpose:** This approach encapsulates the execution logic, including environment setup, dependency installation, and notebook execution, within an external, reusable workflow.

#### Parameters:
- **`python-version`:** Utilizes a variable `${{ vars.PYTHON_VERSION }}` to determine the Python version used for notebook execution. This setup allows for the use of different Python versions as needed by the notebooks, enhancing compatibility.

## Summary
This GitHub Action facilitates the manual execution of Jupyter Notebooks by leveraging an external workflow. This strategy simplifies the current workflow to a single job that references a comprehensive and potentially complex execution process defined elsewhere. It offers an efficient way to maintain and update the execution process across multiple workflows and projects.



# Manual Full Archive Execute-Store-Generate HTML GitHub Action Documentation

The GitHub Action named "Manual Full Archive Execute-Store-Generate HTML" is configured for manual activation to execute Jupyter Notebooks, store the results, and generate HTML versions of the notebooks. This document provides a detailed overview of its configuration and functionality.

## Trigger
- **Type:** `workflow_dispatch`
- **Description:** This action is manually triggered, providing flexibility for users to execute the workflow at their convenience through the GitHub UI or API.

## Jobs

### GenerateHTML
This job orchestrates the execution of notebooks, storage of execution results, and generation of HTML outputs.

#### Details:
- **Operation:** The job uses an external workflow from the `spacetelescope/notebook-ci-actions` repository, specifically the `ci_build_merge_manual.yml` workflow at its `v3` version. This external workflow is responsible for the detailed steps involved in executing the notebooks, storing results, and generating HTML.
- **Purpose:** By referencing an external workflow, this job abstracts the complexities involved in notebook execution and HTML generation, facilitating reuse and maintainability.

#### Parameters:
- **`python-version`:** The job specifies the Python version through the `${{ vars.PYTHON_VERSION }}` variable. This approach allows for the selection of an appropriate Python environment tailored to the notebooks' requirements.

## Summary
The "Manual Full Archive Execute-Store-Generate HTML" GitHub Action is designed for manual initiation, allowing users to execute a comprehensive workflow that includes notebook execution, result storage, and HTML generation. Leveraging an external workflow for these tasks promotes efficiency and reusability while maintaining a simplified and focused configuration in the current repository.


# Build HTML on Merge GitHub Action Documentation

The "Build HTML on Merge" GitHub Action is designed to automatically generate HTML versions of Jupyter Notebooks upon the successful merge of pull requests into the main branch. This documentation details the action's trigger conditions, job configuration, and operational specifics.

## Triggers
- **Pull Request:** 
  - **Branches:** The action is triggered by pull requests targeted at the `main` branch.
  - **Types:** It specifically responds to the `closed` event type, meaning it runs after a pull request is closed.
- **Workflow Dispatch:** 
  - The action can also be manually triggered, providing additional flexibility for execution outside of pull request merges.

## Jobs

### Generate_HTML
This job is responsible for the generation of HTML from Jupyter Notebooks following a merge event.

#### Conditions:
- **Execution Condition:** The job only executes if the closing of the pull request corresponds to a merge (`github.event.pull_request.merged == true`). This ensures the action runs solely in response to successful merges, rather than all closed pull requests.

#### Details:
- **Operation:** The job utilizes an external workflow defined in the `spacetelescope/notebook-ci-actions` repository, specifically the `ci_builder.yml` workflow at its `v3` version. This external workflow encompasses the steps necessary for converting Jupyter Notebooks into HTML format.
- **Purpose:** Leveraging an external workflow centralizes the logic for HTML generation, promoting reusability and maintainability across different projects and workflows.

#### Parameters:
- **`python-version`:** The Python version is specified dynamically using the `${{ vars.PYTHON_VERSION }}` variable, allowing for the selection of an environment that meets the notebooks' requirements.

## Summary
The "Build HTML on Merge" action automates the conversion of Jupyter Notebooks to HTML following the successful merge of pull requests into the main branch. By employing an external workflow for the conversion process, this action ensures a consistent and maintainable approach to generating HTML representations of notebooks, facilitating easier review and sharing of the notebook content.


# Manual HTML Deploy GitHub Action Documentation

The GitHub Action named "Manual HTML Deploy" is specifically crafted for manual invocation to generate HTML versions of Jupyter Notebooks. This document outlines its configuration and operational framework.

## Trigger
- **Type:** `workflow_dispatch`
- **Description:** This action is configured for manual triggering, allowing users to initiate the workflow as needed from the GitHub UI or through the GitHub API. This provides flexibility in generating HTML from notebooks on demand.

## Jobs

### GenerateHTML
This job is centered around the conversion of Jupyter Notebooks into HTML format.

#### Details:
- **Operation:** The job employs an external workflow from the `spacetelescope/notebook-ci-actions` repository, utilizing `ci_builder_manual.yml` at its `v3` iteration. This external workflow encapsulates the steps required for notebook processing and HTML generation.
- **Purpose:** Utilizing an external workflow for HTML generation abstracts the complexity of the process, promoting reusability and simplifying maintenance. It ensures that the HTML generation process is standardized across different projects that utilize the same workflow.

#### Parameters:
- **`python-version`:** Through the use of the `${{ vars.PYTHON_VERSION }}` variable, this job allows for the specification of the Python environment. This flexibility ensures compatibility with the varying requirements of different Jupyter Notebooks, enhancing the robustness of the HTML generation process.

## Summary
The "Manual HTML Deploy" GitHub Action provides a convenient mechanism for manually triggering the generation of HTML from Jupyter Notebooks. By leveraging an external, reusable workflow, it ensures a consistent approach to notebook processing while offering the flexibility to accommodate different Python environments and notebook specifications.


# Notebook Execution and Validation GitHub Action Documentation

This GitHub Action, named "Notebook Execution and Validation," is designed to automate the execution and validation of Jupyter Notebooks within a repository, particularly upon direct pushes to the main branch or when pull requests are submitted. It is structured to sequentially run three distinct phases: Validation, Execution, and HTML Deployment, with each subsequent phase contingent on the successful completion of the preceding one.

## Trigger Conditions
- **Pull Request:** 
  - **Branches:** The workflow is activated by pull requests targeting the `main` branch.
  - **Paths:** It specifically responds to changes within the `notebooks/` directory that affect `.ipynb` files or any `.yml` files, ensuring that the workflow runs only when relevant content is modified.

## Permissions
The workflow is granted comprehensive permissions to interact with repository contents, issue tokens, manage issues, and handle pull requests, facilitating a wide range of operations that may be required during the execution and validation process.

## Jobs

### NotebookExecutionValidation
This job encapsulates the core functionality of executing and validating the Jupyter Notebooks.

#### Details:
- **Operation:** The job integrates an external workflow from the `spacetelescope/notebook-ci-actions` repository, specifically `ci_runner.yml` at its `v3` version. This external workflow is designed to handle the intricacies of notebook execution and validation in a standardized manner.
- **Sequential Phases:** The workflow is structured to ensure a logical progression through the validation, execution, and HTML Deployment phases. If the validation phase fails, subsequent phases (execution and HTML Deployment) are aborted to prevent the propagation of errors.
- **Environment:** Each phase of the workflow operates on its own dedicated runner with an independent environment setup, except for the HTML generation phase, which utilizes a single runner and leverages the global environment settings.

#### Parameters:
- **`python-version`:** By employing the `${{ vars.PYTHON_VERSION }}` variable, the job allows for the dynamic selection of the Python environment, accommodating the diverse requirements of different notebooks.

#### Permissions:
- **Contents:** The job specifically requests `write` permissions for repository contents, enabling it to make changes or updates as necessary during the notebook execution and validation process.

## Summary
The "Notebook Execution and Validation" GitHub Action is a comprehensive solution for ensuring the integrity and functionality of Jupyter Notebooks within a project. By leveraging an external, reusable workflow and enforcing a strict sequential operation of validation, execution, and HTML deployment phases, it maintains high standards of quality and reliability for notebook-based projects.


# PEP8 Notebook Style Check Execution GitHub Action Documentation

The "PEP8 Notebook Style Check Execution" GitHub Action is specifically designed to enforce PEP8 style guidelines within the Python code contained in Jupyter Notebook cells. This action ensures that the code adheres to the widely accepted PEP8 standards for Python coding style, enhancing readability and maintainability.

## Trigger Conditions
- **Pull Request:**
  - **Branches:** Activated by pull requests targeting the `main` branch, ensuring that code style checks are performed prior to merging.
  - **Paths:** The action is specifically triggered by changes in the `notebooks/` directory affecting `.ipynb` files or any `.yml` files, making it focused on relevant modifications that could impact code style.

## Jobs

### Notebook_PEP8_Check
This job is the core of the workflow, performing the PEP8 style checks on Python code within the notebook cells.

#### Details:
- **Operation:** Utilizes an external workflow from the `spacetelescope/notebook-ci-actions` repository, `notebook_pep8check.yml` at version `v3`. This external workflow is tailored to perform PEP8 checks, ensuring that the code in notebooks adheres to these styling guidelines.
- **Purpose:** The inclusion of this style check in the CI pipeline helps maintain a consistent coding style throughout the project's notebooks, contributing to the overall quality and readability of the code.

#### Parameters:
- **`python-version`:** The action allows specification of the Python environment via the `${{ vars.PYTHON_VERSION }}` variable. This flexibility ensures that the style checks are compatible with the Python version used in the notebooks, preventing any discrepancies due to version differences.

## Summary
The "PEP8 Notebook Style Check Execution" GitHub Action is an essential tool for maintaining high coding standards within Jupyter Notebooks. By automatically enforcing PEP8 compliance on every pull request to the main branch, it helps ensure that all notebook code remains clean, well-structured, and in line with best practices for Python development.

# PEP8 Script Style Check Execution GitHub Action Documentation

The "PEP8 Script Style Check Execution" GitHub Action is designed to enforce PEP8 style guidelines on Python scripts, particularly those located within a project's `notebooks/` directory. This workflow ensures that Python code complies with the PEP8 standards, promoting readability, consistency, and maintainability across the codebase.

## Trigger Conditions
- **Pull Request:**
  - **Branches:** The action is triggered by pull requests aimed at the `main` branch. This setup ensures that code style checks are a prerequisite for merging changes, thereby maintaining code quality.
  - **Paths:** It specifically targets changes to Python scripts (`**.py`) within the `notebooks/` directory and any `.yml` files, focusing the checks on relevant modifications.

## Jobs

### Script_PEP8_Check
This job is dedicated to performing the PEP8 style checks on the targeted Python scripts.

#### Details:
- **Operation:** The job leverages an external workflow, `script_pep8check.yml` from the `spacetelescope/notebook-ci-actions` repository, at its `v3` version. This external workflow is specialized in conducting PEP8 style checks on Python scripts, ensuring adherence to standardized coding conventions.
- **Purpose:** Integrating PEP8 style checks into the continuous integration process helps uphold a consistent and professional coding standard throughout the project's Python scripts, contributing to code quality and developer collaboration.

#### Parameters:
- **`python-version`:** By utilizing the `${{ vars.PYTHON_VERSION }}` variable, the job allows for the specification of the Python environment in which the style checks are conducted. This ensures compatibility with the project's Python version, aligning the checks with the development environment.

## Summary
The "PEP8 Script Style Check Execution" GitHub Action plays a crucial role in maintaining a high standard of code quality within Python scripts. By automatically enforcing PEP8 compliance for every pull request targeting the main branch, it fosters a culture of quality and consistency in coding practices across the project.


# Weekly Broken Link Check GitHub Action Documentation

The "Weekly Broken Link Check" GitHub Action is designed to automatically scan for and identify broken links within the project's documentation or web pages. This scheduled action helps maintain the integrity and reliability of the project's external references.

## Trigger
- **Schedule:**
  - **Cron:** Scheduled to run at 0400 UTC every Sunday (`0 4 * * 0`). This regular, weekly schedule ensures that broken links are identified and can be addressed promptly, minimizing the duration that incorrect or outdated links remain in the project documentation.

## Jobs

### Scheduled
This job focuses on the detection and reporting of broken links within the project's assets.

#### Details:
- **Operation:** The job utilizes an external workflow, specifically `broken_link_checker.yml` from the `spacetelescope/notebook-ci-actions` repository, at its `v3` version. This workflow is designed to methodically check each link in the project's documentation or web pages to ensure they are functional and lead to the intended content.
- **Purpose:** Regularly checking for broken links is essential for maintaining the quality and user experience of the project's documentation. It helps ensure that users and contributors can reliably access referenced resources, contributing to the project's overall credibility and usability.

## Summary
The "Weekly Broken Link Check" GitHub Action is a critical maintenance tool for any project reliant on external links in its documentation or web pages. By automating the process of identifying broken links on a weekly basis, this action supports the project's commitment to quality, reliability, and a positive user experience.

# Weekly PEP8 Style Checks GitHub Action Documentation

The "Weekly PEP8 Style Checks" GitHub Action is configured to enforce PEP8 coding standards across Python scripts and Jupyter notebooks within the `hst_notebooks` repository. This automated workflow ensures consistent code quality and adherence to Python style guidelines on a weekly basis.

## Triggers
- **Schedule:**
  - **Cron:** The workflow is scheduled to run at midnight (00:00) UTC every day (`0 0 * * *`). This frequency ensures regular and consistent checks without overwhelming the development process.
- **Workflow Dispatch:**
  - This trigger allows manual execution of the workflow, providing flexibility to initiate style checks outside the scheduled intervals.

## Jobs

### Notebook_PEP8_Check
This job focuses on enforcing PEP8 standards within the Jupyter notebooks.

#### Details:
- **Operation:** Utilizes the `all_notebooks_pep8check.yml` workflow from the `spacetelescope/notebook-ci-actions` repository at its `v3` version. This workflow is specifically designed to scan Jupyter notebooks for PEP8 compliance, including the Python code within notebook cells.
- **Purpose:** Regular PEP8 checks on notebooks help maintain clean, readable, and standardized code, enhancing maintainability and collaboration within the project.

### Script_PEP8_Check
This job is responsible for applying PEP8 checks to Python scripts within the repository.

#### Details:
- **Operation:** Employs the `all_scripts_pep8check.yml` workflow from the `spacetelescope/notebook-ci-actions` repository, also at version `v3`. This workflow is tailored to assess PEP8 compliance in standalone Python scripts, ensuring they meet the established coding standards.
- **Purpose:** By enforcing PEP8 standards on Python scripts, this job contributes to a cohesive and professional codebase, facilitating code review and integration processes.

#### Parameters for Both Jobs:
- **`python-version`:** Both jobs allow for the specification of the Python environment via the `${{ vars.PYTHON_VERSION }}` variable. This ensures that style checks are performed in a context that matches the project's development environment, accounting for potential differences in style guidelines across Python versions.

## Summary
The "Weekly PEP8 Style Checks" GitHub Action plays a crucial role in upholding code quality within the `hst_notebooks` repository. By conducting automated PEP8 compliance checks on both Python scripts and Jupyter notebooks, this workflow supports the development of a clean, consistent, and professional codebase.

