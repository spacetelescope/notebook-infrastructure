## Setting up a new repository for notebook CI

To get started with the notebook CI system, you'll need to create a new repository and set up the necessary structure. Here's how to do it:

1. Create a new repository on GitHub. You can give it any name you like, but make sure to include the word "notebook" in the name so that it's clear what the repository is for. 

2. Clone the 'notebook-ci-template' repository using the following command:

git clone https://github.com/spacetelescope/notebook-ci-template.git

3. Copy the entire structure of the `notebook-ci-template` repository, including all files and directories, into your new repository.

4. Edit `_toc.yml` to include the notebooks that you want to include in your jupyterbook documentation. Simply add the name and path of each notebook to the list.

5. Edit `_config.yml` to configure the jupyterbook system. You'll need to specify the author, mission name, location of the repository, and any other options you'd like to include. You can also add a GitHub Analytics ID to gather usage statistics for your documentation.

6. Set up GitHub Pages for your repository by creating a new branch called `gh-pages`. You can do this using the following command:

git checkout -b gh-pages

Then, push the `gh-pages` branch to GitHub using the following command:

git push origin gh-pages


Finally, go to the repository settings and select the `gh-pages` branch under the "Source" section of the "GitHub Pages" section. This will allow you to access your documentation at `https://<USERNAME>.github.io/<REPO>`.

7. Add and commit your changes to the repository using the following commands:

git add .
git commit -m "Initial commit"

8. Push your changes to GitHub using the following command:

git push origin master

Once you've set up the structure and configured jupyterbook, your repository should be ready to start running checks and weekly tests on notebooks submitted by PR as described in the previous documentation. You can access your documentation at `https://<USERNAME>.github.io/<REPO>`.

We hope this helps you get started with the notebook CI system. If you have any questions or need further assistance, please don't hesitate to ask.
