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


# GitHub Action for Deploying Jupyter Book to GitHub Pages - ci_builder.yml

This GitHub Action is designed to automatically deploy a Jupyter Book to GitHub Pages upon the successful merge of a pull request. It includes steps for setting up the environment, installing necessary dependencies, building the Jupyter Book, and publishing the content to GitHub Pages.

## Trigger
- **`workflow_call`**: This action is intended to be called by other workflows, allowing for flexible integration into various CI/CD pipelines.

## Secrets
- **`CASJOBS_USERID`**: An optional secret representing the CASJOBS user ID. It's not required for the deployment process but can be used for jobs that require CASJOBS authentication.
- **`CASJOBS_PW`**: Similar to `CASJOBS_USERID`, this optional secret represents the CASJOBS password.

## Environment Variables
- **`CASJOBS_PW`**: Set from the `CASJOBS_PW` secret.
- **`CASJOBS_USERID`**: Set from the `CASJOBS_USERID` secret.

## Jobs

### `deploy-book`
This job handles the deployment of the Jupyter Book to GitHub Pages.

#### Conditions
- **Execution**: The job is executed only if the associated pull request is merged. This ensures that the deployment process is triggered by confirmed changes only.

#### Environment
- **`runs-on: ubuntu-latest`**: The job is executed on the latest Ubuntu runner, ensuring access to up-to-date tools and libraries.

#### Permissions
- **`contents: write`**: Grants the job write permissions to the repository contents, enabling it to publish the built book to GitHub Pages.

#### Steps
1. **Free up disk space**: Removes unnecessary directories to ensure there is enough disk space for the job's operations.
2. **Checkout**: Checks out the repository's code to access the Jupyter Book source files.
3. **Set up Python**: Installs Python 3.8.12 and sets up caching for pip to speed up dependency installation.
4. **Add conda to system path**: Ensures conda commands are available in the system path, facilitating environment management and package installation.
5. **Install Python dependencies**: Installs the required Python packages for building the Jupyter Book, including `jupyter-book` and its dependencies.
6. **Build book HTML**: Executes the `jupyter-book build .` command to build the HTML version of the Jupyter Book from the source files.
7. **GitHub Pages action**: Utilizes the `peaceiris/actions-gh-pages@v3.6.1` action to publish the built HTML content to GitHub Pages, making the Jupyter Book accessible online.

## Summary
This GitHub Action streamlines the process of deploying Jupyter Books to GitHub Pages, ensuring that the latest version of the book is always available online following the successful merge of changes. By automating environment setup, dependency installation, book building, and publishing, this action facilitates efficient and reliable updates to project documentation or educational materials hosted as Jupyter Books.
