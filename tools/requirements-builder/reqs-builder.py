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
import arrays as a
import numpy as np

target_dir = "./notebooks/"

# maybe this is dumb, but use grep to get the contents of every requirements file
p1 = subprocess.Popen(["grep", "-r", "--include", f"{target_dir}*requirements.txt", "."], stdout=subprocess.PIPE)
grep_out, err = p1.communicate()

# convert bytes to string
grep_out = str(grep_out)
#print(grep_out)

# with open("testing-reqs.txt", "wb") as outfile:
#     outfile.write(grep_out)


# get all of the packages used, with the corresponding notebooks
# a-zA-Z0-9 = normal package names, \+:\/\. = "include + / ." for github urls
packages = re.findall(r"notebooks/(.*?):([a-zA-Z0-9\+:\/\.]+)", grep_out)
#print(packages)
print(packages)

# get the list of requirements per notebook
nb_reqs_dict = a.parse_mega_list(packages)

# get a plain list of the packages used
all_packages = a.get_packages_only(nb_reqs_dict)

# number the list of packages to enable creating the matrix
numbered_packages = a.make_pack_dict(all_packages)

# create the matrix
nb_matrix = np.array([a.nb_packages_to_row(numbered_packages, nb_req) for nb_req in nb_reqs_dict.values()])

# create the distances matrix, which we'll need for later
dist_matrix = a.setup_distances_matrix(nb_matrix)


# we need to iterate: 
# 1 - calculate distances
# 2 - drop largest distance notebook(s) row/column from distance matrix
# 3 - drop largest distance notebook(s) row from notebook requirement matrix
# 4 - check nb-req matrix: 
#     if a column is zero, that package is not being used. note this as we iterate
#     number of rows = passing notebooks
#     number of non-zero columns = number of packages

lap = np.array(list(all_packages))
drop = np.array([])

while len(dist_matrix>2):
    # calculate distances
    s = np.sum(dist_matrix, axis=0)
    drop_idx = np.argwhere(max(s)==s)

    # drop values
    dist_matrix = a.drop_notebook_dist(dist_matrix, drop_idx)
    nb_matrix, dropped_packages = a.drop_notebook_reqs(nb_matrix, drop_idx)

    current_drop = lap[dropped_packages]
    
    if current_drop.size >= 1 and drop.size >= 1:
        new_drops = np.setdiff1d(current_drop, drop)
        print(len(nb_matrix)+len(drop_idx), new_drops)
    elif current_drop.size >= 1 and drop.size < 1:
        print(len(nb_matrix)+len(drop_idx), current_drop)
    
    drop = np.concatenate((drop, current_drop))
 

    #print(drop)


# we need a notebook translation matrix: 
# when I drop a nb, how do I tell its requirements?
# oh, wait. it's the row of the notebook matrix 

