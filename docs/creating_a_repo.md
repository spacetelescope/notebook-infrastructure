# Creating a Notebook Repository

There are two ways to stand up a new notebook repository wired to this CI. Pick the one that matches you.

| You are | Use |
| --- | --- |
| **STScI staff** (institute repos) | The Slack bot (below) |
| **Anyone else** (external) | The GitHub template (steps below) |

## Internal (STScI): use the Slack bot

Institute repositories are created with the Slack bot in the `github_administration` channel. Send it:

```
!CreateRepoFromTemplate spacetelescope <your-repo-name> notebook-ci-template
```

| Argument | Value | Meaning |
| --- | --- | --- |
| Organization | `spacetelescope` | Where the new repo is created |
| Repository name | `<your-repo-name>` | Your new repo's name, no spaces |
| Template | `notebook-ci-template` | The CI-ready template to copy from |

The bot creates the repo from the template with the workflows already in place. Once it confirms, follow the customization and publishing steps below (branches, `_toc.yml`/`_config.yml`, the `PYTHON_VERSION` variable, and Pages).

## External: use the GitHub template

If you are outside STScI, create the repo yourself from the template, then follow the steps below. (The "Use this template" button is intended for non-institute repositories; institute repos use the Slack bot above.)

## Step 1: Using the GitHub Template

- Navigate to the GitHub template repository: [Notebook CI Template](https://github.com/spacetelescope/notebook-ci-template).
- Click on the green **"Use this template"** button located in the top-right corner of the page.
- Select **"Create a new repository"** from the dropdown menu. Ensure the option **"Include all branches"** is checked to copy all necessary branches.

## Step 2: Configuring Your New Repository

- Provide a clear and descriptive name for your repository. It’s helpful to include "notebook" in the repository name to clearly indicate its purpose.
- Select the visibility of your repository (**public** or **private**), depending on your project's requirements.
- Click **"Create repository from template"** to finalize the creation.

## Step 3: Customizing Repository Contents

Your new repository includes an `example.ipynb` notebook already listed in the `_toc.yml` file. This notebook serves as a helpful template to get you started.

- Edit `_toc.yml` in your repository:
  - Keep or modify the existing `example.ipynb` notebook entry based on your needs.
  - Add new notebook entries by listing their paths and filenames, ensuring all your notebooks are included in the published documentation.

- Update `_config.yml`:
  - Personalize the author information, project title, mission name, and the URL pointing to your repository.
  - Optionally, add a GitHub Analytics ID to collect usage data and understand the documentation’s reach.

## Step 4: Managing Branches

Ensure the following essential branches from the template repository are included in your new repository:

- `main` branch: This is where you'll make updates, edits, and push your notebook changes.
- `gh-pages` branch: Used by GitHub Pages to host your published documentation.
- `gh-storage` branch: Required for storing executed notebooks. This branch is used in generating notebook HTML and serves as a baseline for scheduled validation checks.

## Step 5: Setting Repository Variables

Your repository requires a GitHub Actions variable for Python version management:

- Manually set a repository-level Actions variable named `PYTHON_VERSION`:
  - Navigate to your repository on GitHub.
  - Go to **Settings > Secrets and variables > Actions**.
  - Click on **New repository variable**.
  - Enter `PYTHON_VERSION` as the variable name and `3.11` (or your desired Python version) as the value.
  - Click **"Add variable"**.

## Step 6: Publishing Your Documentation

- Enable GitHub Pages to publish your documentation:
  - Navigate to your repository settings (**Settings > Pages**).
  - Select the `gh-pages` branch as the publishing source.
  - Click **"Save"** to confirm the changes.

## Step 7: Testing the GitHub Actions

Ensure the CI system is working correctly by testing the actions:

- Make a small modification to the existing `example.ipynb` notebook.
- Commit the changes and submit a pull request (PR) to your repository.
- After creating the PR, GitHub Actions should automatically start running checks.
- Verify the "Checks" tab within your PR to confirm actions for notebook validation, execution, and security are running successfully.

## What success looks like

When everything is wired up correctly:

- Your pull requests show green checks for **validation**, **execution**, and **security** in the PR's Checks tab.
- After merging to `main`, your notebooks publish to your repository's GitHub Pages site (`https://<owner>.github.io/<your-repo>/`).
- The weekly [scheduled run](scheduled-runs.md) stays green, confirming your notebooks still execute as dependencies and data change over time.

If a check is red, open it from the Checks/Actions tab and read the logs. See [Diagnosing CI Failures](ci_best_practices.md) and [Troubleshooting](troubleshooting-unified.md).

## Next Steps

Your repository setup is complete. Regularly update your notebooks and push the changes to your repository; the notebook CI system will automatically test and publish updates to your documentation, providing a seamless and efficient workflow.
