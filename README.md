# notebook-infrastructure

## Overview

The `notebook-infrastructure` repository provides standards and software infrastructure to support Jupyter notebooks intended for public consumption at the Space Telescope Science Institute (STScI). It includes documentation, templates, and tools to assist with the creation, management, and deployment of high-quality, reviewable notebooks.

## Repository Structure

- **docs/** – Documentation for CI, contributor workflows, and usage.
- **notebook-repo-template/** – A GitHub repository template to create notebook projects that conform to STScI guidelines.
- **tools/** – Additional utilities for managing notebook repositories outside the template.
- **README.md** – This file.

## Documentation

Detailed instructions and documentation are available at:

📘 [notebook-infrastructure.readthedocs.io](https://notebook-infrastructure.readthedocs.io/en/latest/)

This includes:

- CI system overview
- Action descriptions
- Workflow examples
- Contributor and operator guides
- Repository creation instructions

## Getting Started

To create a new repository using this infrastructure:

1. Visit the [Creating a Repo](https://notebook-infrastructure.readthedocs.io/en/latest/creating_a_repo.html) guide.
2. Use the `notebook-repo-template` to initialize your notebook project.
3. Follow the CI setup and customization instructions.
4. Trigger test runs with a sample change (e.g., edit `example.ipynb`) via a pull request.

## Contributing

We welcome contributions that improve this infrastructure! To contribute:

1. **Fork** the repository
2. **Create a feature branch** off `main`
3. **Make your changes**, ensuring consistency with existing styles and standards
4. **Open a pull request** with a clear description

Refer to the [Contributing Guide](https://notebook-infrastructure.readthedocs.io/en/latest/contributing.html) for more detailed guidance.

## License

This project is licensed under the BSD 3-Clause License.  
See the [LICENSE](LICENSE) file for more details.

---

**Maintained by:** [Space Telescope Science Institute (STScI)](https://www.stsci.edu/)

