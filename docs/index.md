# Notebook CI/CD Documentation

Automated validation, testing, execution, and documentation for Jupyter
notebook repositories, powered by
[`spacetelescope/notebook-ci-actions`](https://github.com/spacetelescope/notebook-ci-actions).

Pick the path that matches what you're doing.

!!! tip "Setting up a new notebook repository?"
    Start with **[Creating a Repo](creating_a_repo.md)** -- it walks you from an
    empty repo to passing CI, step by step. New to the terms? See the
    [Glossary](glossary.md).

## :material-notebook-edit: I write notebooks

You contribute notebooks to a repo that already uses this CI. You don't set up
or edit the CI itself, you just need your notebooks to pass.

[Start with the Quick Reference :material-arrow-right:](authors/quick-reference.md){ .md-button .md-button--primary }
[Read the Full Guide](authors/guide.md){ .md-button }

## :material-cog: I maintain a notebook repo

You set up the caller workflows, choose which checks run, and manage configuration and updates.

[Configuration Reference :material-arrow-right:](configuration-reference.md){ .md-button .md-button--primary }

## :material-server: I run the infrastructure

You manage the self-hosted runners and the underlying CI infrastructure.

[Custom Runner Configuration :material-arrow-right:](custom-runner-configuration.md){ .md-button .md-button--primary }

---

!!! note "About this site"
    This site is built from the markdown in the repository's `docs/` directory
    with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and
    deployed to GitHub Pages when documentation changes are pushed to `main`.
