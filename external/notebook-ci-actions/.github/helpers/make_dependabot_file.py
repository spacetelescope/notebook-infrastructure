"""
Automatic package version updating is controlled by the .github/dependabot.yml file. However, at this time,
wildcards are not supported, so the paths to all notebook-level requirements.txt files must be explicitly
listed in the file.
This script fully automates dynamic updates to the dependabot.yml file when notebooks are added or removed,
If no updates are required, the dependabot.yml file will not be regenerated. It is assumed that if they exist,
github-actions workflows are stored im .github/workflows/
"""

import argparse
import glob
import os

def generate_file_content_from_template(ecosystem, directory, exclude_list=[]):
    """
    Generates sections of yml code from template.

    Parameters
    ----------
    ecosystem : str
        Package manager to use

    directory : str
        Location of package manifests

    exclude_list: str, optional
        List of packages that should be excluded from dependabot version update tracking.
    Returns
    -------
    yml_content : list
        List of code lines to add to output list.
    """
    yml_content = []
    template_content = ['  - package-ecosystem: "{}"'.format(ecosystem),
                        '    directory: "{}"'.format(directory),
                        '    schedule:',
                        '     interval: "weekly"',
                        '     day: "sunday"',
                        '     time: "12:00"']

    # Tack on additional parameter set to ignore specific packages.
    if exclude_list:
        template_content.append('    ignore:')
        for pkg_name in exclude_list:
            template_content.append('      - dependency-name: "{}"'.format(pkg_name))
    for line in template_content:
        yml_content.append(line)
    return yml_content

def make_file(exclude_filename="", req_file_search_string="notebooks/**/requirements.txt"):
    """
    Generates the dependabot.yml file.

    Parameters
    ----------
    exclude_filename: str, optional.
        Text file containing names of specific requirements.txt files and lists of packages that should be
        skipped from dependabot version updating, one requirements.txt file and package list per line.
        File syntax: <path of requirements.txt file from repository root>: <package1>, ..., <packageN>,
        Example: skip depdendabot updates for packages "package1" and "package2" in file
        notebooks/foo/requirements.txt and package "package3" in file notebooks/bar/requirements.txt:
        notebooks/foo/requirements.txt: package1, package2
        notebooks/bar/requirements.txt: package3
        NOTE: unless explicitly specified, it is assumed that there is no file, and that all packages in all
        requirements.txt files should be included in dependabot version tracking.
    req_file_search_string : str, optional.
        Search pattern used to locate notebook-level requirements.txt files. The path in the search string is
        assumed to start from the repository root. If not explicitly specified by the user, the default value
        is "notebooks/**/requirements.txt", which will enable a fully recursive search.

    Returns
    -------
    Nothing!
    """
    output_file_name = ".github/dependabot.yml"
    output_file_content = ['version: 2',
                           'updates:']
    # 0: Add lines of code for github actions coverage if required
    if os.path.exists(".github/workflows"):
        output_file_content += generate_file_content_from_template("github-actions", "/")

    # 1: locate all paths with notebook-level requirements.txt files.
    req_file_list = glob.glob(req_file_search_string, recursive=True)

    # 2: Dynamically generate the dependabot.yml file content based on the paths identified by the above glob command.
    # 2a: read in ignore-file, if found.
    exclude_dict = {}
    if exclude_filename and os.path.exists(exclude_filename):
        with open(exclude_filename, 'r') as i_in:
            exclude_file_content = i_in.readlines()
        for line in exclude_file_content:
            line=line.strip()
            exclude_dict[line.split(":")[0]] = sorted([item.strip() for item in line.split(":")[1].split(",")])

    for rf_list_item in sorted(req_file_list):
        rf_path = rf_list_item.replace("requirements.txt", "")
        if rf_list_item in exclude_dict.keys():
            exclude_list = exclude_dict[rf_list_item]
        else:
            exclude_list = []
        output_file_content += generate_file_content_from_template("pip", rf_path, exclude_list=exclude_list)

    # 3: Write yml file content only if generated content and content of current file are not identical
    if os.path.isfile(output_file_name):
        with open(output_file_name, 'r') as f_in:
            old_file_content = f_in.readlines()
    else:
        old_file_content = []
    output_file_content = [line + "\n" for line in output_file_content]  # add carriage returns to all lines.
    if old_file_content != output_file_content:
        with open(output_file_name, 'w') as f_out:
            f_out.writelines(output_file_content)
        print("Successfully generated file {}.".format(output_file_name))
    else:
        print("No new changes found in comparison with current {} file. File generation skipped.".format(
            output_file_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--exclude_filename', required=False,
                        default='',type=str,
                        help='Text file containing names of specific requirements.txt files and lists of '
                             'packages that should be skipped from dependabot version updating, one '
                             'requirements.txt file and package list per line.  File syntax: '
                             '<path of requirements.txt file from repository root>: <package1>, ..., <packageN>,'
                             'Example: skip depdendabot updates for packages "package1" and "package2" in '
                             'file notebooks/foo/requirements.txt and package "package3" in file '
                             'notebooks/bar/requirements.txt:                                                '
                             'notebooks/foo/requirements.txt: package1, package2                             '
                             'notebooks/bar/requirements.txt: package3 '
                             'NOTE: unless explicitly specified, it is assumed that there is no file, and '
                             'that all packages in all requirements.txt files should be included in '
                             'dependabot version tracking.')
    parser.add_argument('-r', '--req_file_search_string', required=False,
                        default='notebooks/**/requirements.txt',type=str,
                        help='Search pattern used to locate notebook-level requirements.txt files. The path '
                             'in the search string is assumed to start from the repository root, which will '
                             'enable a fully recursive search.')
    args = parser.parse_args()
    if args.exclude_filename == "***NO FILE***": # So everything works when run from a github workflow.
        args.exclude_filename = ""
    make_file(exclude_filename=args.exclude_filename, req_file_search_string=args.req_file_search_string, )

