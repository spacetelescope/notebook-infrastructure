# Best Practices for Diagnosing CI Failures

This guide provides best practices to diagnose and resolve issues when Continuous Integration (CI) systems report failures on your Jupyter notebooks. The CI system leverages the following tools:

- **nbconvert**: Executes notebooks and generates outputs.
- **pytest nbval**: Validates notebook outputs to ensure consistency and reproducibility.
- **Bandit**: Scans notebooks for security issues.

## Step 1: Identify the Failed Checks

When a CI run fails:

- Navigate to the pull request (PR) or commit where the CI failed.
- Go to the **Checks** tab to identify which specific check failed (execution, validation, or security).

## Step 2: Diagnosing Notebook Execution Failures (`nbconvert`)

If the failure occurred during notebook execution:

- Review the log output from `nbconvert` under the **Checks** tab for details on the error.
- Common reasons include:
  - Syntax or runtime errors within notebook cells.
  - External data or dependencies not accessible by CI.

- **Resolution Steps:**
  - Replicate the notebook execution locally using a clean Python environment.
  - Ensure all required dependencies are listed in your `requirements.txt` or environment file.
  - Ensure external resources (datasets, APIs) are reachable from the CI environment.

## Step 3: Diagnosing Validation Failures (`pytest nbval`)

Validation failures typically mean the notebook outputs have changed unexpectedly:

- Examine the logs provided by `pytest nbval` under the **Checks** tab.
- Common causes include:
  - Changes in notebook outputs due to code modifications.
  - Non-deterministic code (e.g., random number generation, timestamps).

- **Resolution Steps:**
  - Run `pytest --nbval notebook.ipynb` locally to replicate the issue.
  - Make outputs deterministic (use fixed seeds or consistent data inputs).
  - Update notebook outputs intentionally and commit the notebook if the changes are valid.

## Step 4: Diagnosing Security Failures (`Bandit`)

Security-related failures indicate potential vulnerabilities detected by Bandit:

- Check the Bandit report under the **Checks** tab for details on identified issues.
- Common issues include:
  - Hard-coded passwords or API keys.
  - Use of insecure or deprecated functions.

- **Resolution Steps:**
  - Remove or securely manage any hard-coded sensitive information.
  - Replace insecure code patterns with recommended secure alternatives.
  - Rerun Bandit locally (`bandit notebook.ipynb`) to confirm the issue is resolved.

## Step 5: Re-run CI Checks

After applying fixes:

- Push the updated notebook to your branch.
- Verify that all checks pass in the PR.

## Best Practices

- Regularly test notebooks locally before pushing.
- Keep your notebook dependencies explicitly listed and updated.
- Avoid non-deterministic outputs or include clear instructions if unavoidable.
- Maintain good security practices by scanning notebooks periodically with Bandit.

