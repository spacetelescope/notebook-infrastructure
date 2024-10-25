## NOTES
# I think this is pretty close to maximum efficiency, but
# it would converge faster if pk_counter were recomputed after each step because
# if recomputed, it could skip packages that were only requested by one notebook
# 
# 1. there would be fewer requirements (in the case where one notebook is the only one requesting multiple packages)
# 2. if a notebook fails and is deleted, we no longer need to consider its packages

import subprocess
from collections import Counter
import re
import numpy as np

target_dir = "./notebooks/TESS/"

# maybe this is dumb, but use grep to get the contents of every requirements file
p1 = subprocess.Popen(["grep", "-r", "--include", f"{target_dir}*requirements.txt", "."], stdout=subprocess.PIPE)
grep_out, err = p1.communicate()

# convert bytes to string
grep_out = str(grep_out)

# list all of the packages used, then count how many times each appears
packages = re.findall(":([a-zA-Z0-9]+)", grep_out)
pk_counter = Counter(packages)

# get a list of notebooks that corresponds with package needs
nbs = re.findall("/([^/]*?)/requirements.txt", grep_out)

# iterate through the notebooks and packages, assembling them into a nice dictionary
nb_needs = dict()
for a, b in zip(nbs, packages, strict=True):
    # if key doesn't exist, create an empty list. if it does, append the package list
    nb_needs[a] = nb_needs.get(a, []) + [b]

# unfortunately, we need the package list to be a set to do .issubset later
for a, b in nb_needs.items():
    nb_needs[a] = set(b)

# create lists for "already included packages" and "passing notebooks"
removing_pk = []
packages = list(set(packages))
passing_nb = []
# count of how many notebooks "fail" with this additional package
n_passing = 18

# loop through the counted packages. 
# don't care about how many times they show up (most_common preserves frequency order)
for pk, _ in pk_counter.most_common().__reversed__():
    # add the latest package to prune
    packages.remove(pk)
    removing_pk.append(pk)
    # delete any failing notebooks so we don't count them again
    del_keys = []
    # loop through the notebooks and their required packages
    for nb, pks in nb_needs.items():
        # if the requested packages are not already included, this notebook "fails"
        if not pks.issubset(packages):
            # count it as failing
            n_passing -= 1
            # schedule for deletion
            del_keys.append(nb)
    # add this round's passing notebook count
    passing_nb.append(n_passing)
    # delete any passing notebooks: they will always pass now, and thus be counted multiple times
    for key in del_keys:
        nb_needs.pop(key)

# answers the question "if I remove [package], how many notebooks will still pass?"
print(list(zip(removing_pk, passing_nb)))