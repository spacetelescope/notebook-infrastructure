# notebook-ci-template

## Overview

The `notebook-ci-template` repository serves as a foundational template for creating Jupyter Notebook projects equipped with a continuous integration (CI) system. This setup ensures that notebooks are automatically tested and validated, maintaining high-quality standards and reliability.

## Features

- **Continuous Integration (CI):** Automated workflows that execute and validate notebooks upon changes, ensuring code integrity.
- **Jupyter Book Integration:** Facilitates the generation of interactive, shareable documentation from your notebooks.
- **Pre-configured Structure:** Provides a standardized project layout to streamline development and collaboration.

## Setting Up Your Repository

To set up your own repository using this template, follow these steps:

### 1. Create a New Repository

- Navigate to the [notebook-ci-template repository](https://github.com/spacetelescope/notebook-ci-template).
- Click the **"Use this template"** button to generate a new repository under your GitHub account.

### 2. Clone Your Repository

Clone your newly created repository to your local machine:

git clone https://github.com/your-username/your-repo-name.git

markdown
Copy
Edit

### 3. Customize Configuration Files

- **`_config.yml`**: Update to set your project's title, author information, and Jupyter Book settings.
- **`_toc.yml`**: Define the structure and order of your notebooks in the book.

### 4. Add Your Notebooks

Place your Jupyter Notebook files (`.ipynb`) into the appropriate directory (usually `notebooks/` or similar) in the repository.

### 5. Enable GitHub Pages

- Go to your repository settings on GitHub.
- Under the **"Pages"** section, set the source branch (commonly `main` or `gh-pages`) and folder (usually `/docs`).
- After deployment, GitHub will provide a link to your published Jupyter Book.

### 6. Configure GitHub Actions for CI

Ensure the `.github/workflows` directory includes workflows like:

- Notebook execution and error checking
- Linting and validation
- Broken link detection

These will automatically trigger on pushes and pull requests.

### 7. Commit and Push Your Changes

git add . git commit -m "Initial setup with customized configurations" git push origin main

markdown
Copy
Edit

### 8. Verify the Setup

- Visit the **Actions** tab to verify that workflows are running and passing.
- Check your GitHub Pages URL to confirm that the Jupyter Book site has been generated.

## Additional Resources

- 📘 [Jupyter Book Documentation](https://jupyterbook.org/intro.html)
- 🧪 [Notebook CI Overview](https://spacetelescope.github.io/notebook-infrastructure/ci-overview.html)

## Contributing

Contributions to improve this template are welcome!

1. Fork the repository  
2. Create a feature branch  
3. Make your changes and push  
4. Submit a pull request with a clear description

## License

This project is licensed under the [BSD 3-Clause License](LICENSE).

---

*This template is maintained by the [Space Telescope Science Institute (STScI)](https://www.stsci.edu/) as part of the [not
