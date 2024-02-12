## GitHub Action for Broken Link Checking on GitHub Pages - broken_link_checker.yml

This GitHub Action is designed to automate the process of checking for broken links within the HTML pages of notebooks deployed to `github.io`. If any broken links are discovered during the check, the workflow will fail and provide a detailed report of the broken links along with the pages that contain them.

## Inputs
- **`website_url`** (optional): The URL of the website to be checked. If this input is not explicitly provided, the default value is constructed using the pattern `https://spacetelescope.github.io/<repository-name>`. It's important to note that relying solely on the default value might not limit the search to the specified page; in such cases, it's advisable to specify the full URL of the starting page of the repository (e.g., `https://spacetelescope.github.io/<repository-name>/intro.html`).

## Trigger
- **`workflow_call`:** This action is designed to be invoked by other workflows, providing a flexible integration point for repositories requiring automated link validation.

## Jobs

### `find_broken_links`
This job is tasked with the detection of broken links on the specified webpage.

#### Environment
- **`runs-on: ubuntu-latest`**: The job is executed on the latest Ubuntu runner provided by GitHub Actions, ensuring a stable and up-to-date environment for link checking.

#### Steps
- **Broken-Links-Crawler**: Utilizes the `ScholliYT/Broken-Links-Crawler-Action@v3.3.1` action to crawl the specified website and identify broken links.
  - **`website_url`:** The URL to check, as provided by the `website_url` input.
  - **`resolve_before_filtering`:** Set to `'true'` to ensure URLs are resolved before any filtering is applied, enhancing the accuracy of the check.
  - **`verbose`:** Configured to `'Error'` to limit the output to error messages, making the output more concise and focused on issues.
  - **`max_retry_time`:** The maximum time (in seconds) to retry a failed link check, set to `30` seconds.
  - **`max_retries`:** The maximum number of retries for each failed link check, set to `5` attempts.
  - **`exclude_url_prefix`:** URLs starting with this prefix (`https://github.com/spacetelescope/hst_notebooks/issues/new?`) are excluded from the check, preventing false positives from issue creation links.

## Summary
This GitHub Action provides an automated solution for monitoring the integrity of links within the HTML pages of notebooks hosted on `github.io`. By systematically checking for and reporting broken links, this workflow aids in maintaining the quality and reliability of the project's online documentation and resources.

## GitHub Action for Notebook Execution and Validation with Security Checks - ci_runner.yml

This GitHub Action is tailored for the execution and validation of Jupyter Notebooks, incorporating security testing using Bandit. It is designed to handle notebooks that have been modified in a pull request or direct push, ensuring they function as expected and adhere to security best practices.

## Secrets
- **`CASJOBS_USERID`** and **`CASJOBS_PW`**: Optional secrets for CASJOBS authentication, not directly used in the notebook execution but available for jobs requiring CASJOBS services.

## Environment Variables
- Environment variables `CASJOBS_PW` and `CASJOBS_USERID` are set using the provided secrets, making them accessible to the notebooks during execution.

## Jobs

### `gather-notebooks`
This job identifies the changed Jupyter Notebook files and constructs a matrix for subsequent execution.

#### Steps:
1. **Checkout**: Checks out the repository's code.
2. **changed-files**: Utilizes `tj-actions/changed-files@v42.0.2` to list modified `.ipynb` files.
3. **set-matrix**: Converts the list of changed files into a JSON array to be used as a matrix for the `notebook-execution` job.

### `notebook-execution`
This job executes the changed notebooks, installs dependencies, performs security testing, and validates the notebook outputs.

#### Strategy:
- **Fail-fast**: Disabled to ensure that the failure of one notebook does not prevent the execution of others.
- **Matrix**: Dynamically generated from the `gather-notebooks` job to target only the changed notebooks.

#### Steps:
1. **Checkout**: Re-checks out the code for accessibility in this job.
2. **Set up Python**: Installs Python and configures pip caching.
3. **Add conda to system path**: Ensures that conda commands are available for dependency management.
4. **Install dependencies**: Installs the necessary Python packages from requirements files located in the same directory as the notebooks or globally within the repository.
5. **Security testing with Bandit**: Runs Bandit to perform static analysis on the notebook files, identifying common security issues in the Python code.
6. **Execute notebooks**: Converts notebooks to HTML for execution, utilizing environment variables for any necessary authentication.
7. **Validate notebooks**: Uses `pytest` with the `nbval` plugin to ensure that all notebook cells execute without errors.

## Summary
This GitHub Action provides a comprehensive approach to maintaining the quality and security of Jupyter Notebooks within a project. By focusing on modified notebooks, it ensures efficient validation and testing workflows, incorporating security analysis with Bandit to highlight potential vulnerabilities. This process aids in keeping the project's notebooks reliable, secure, and up-to-date.


