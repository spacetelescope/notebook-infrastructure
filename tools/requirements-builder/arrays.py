import numpy as np

#a = [[0,2,1],[2,0,3],[1,3,0]]

def setup_distances_matrix(a):
    # you actually need a square root to calculate distances,
    # but we don't care about the absolute distance, only the relative.
    # thus, let's skip the extra computational step
    return np.sum(np.square(a-a[:,None]), axis=-1)

def drop_notebook_dist(input_matrix, idx):
    deleted_row = np.delete(input_matrix, idx, axis=0)
    deleted_column = np.delete(deleted_row, idx, axis=1)
    return deleted_column

def drop_notebook_reqs(input_matrix, idx):
    deleted_row = np.delete(input_matrix, idx, axis=0)
    column_sum = np.sum(input_matrix, axis=0)
    dropped_packages = column_sum == 0
    return deleted_row, dropped_packages

#print(drop_notebook(a, np.array([[1],[2]])))

def nb_packages_to_row(pack_dict, nb_packages):
    """ Each package has a numerical index (in pack_dict).
    Pass in a list of packages, convert to an array of 1s and 0s
    """
    package_array = np.zeros(len(pack_dict))
    idxs = [pack_dict[pac] for pac in nb_packages]
    for i in idxs: package_array[i] = 1
    return np.array(package_array)

def make_pack_dict(all_packages):
    """Convert array of package names into a numbered dictionary
    """
    pk_dict = dict()
    package_set = set(all_packages)
    for i, pk in enumerate(package_set):
        pk_dict[pk] = i
    return pk_dict

def parse_mega_list(mega_list):
    """Take the list of (notebook, package) and turn it into a dictionary of
    notebook: all needed packages, i.e.
    {notebook1: [p1, p2, p3], nb2: [p1, p4]}
    """
    nb_dict = dict()
    for nb, pack in mega_list:
        try: nb_dict[nb].append(pack)
        except KeyError: 
            nb_dict[nb] = []
            nb_dict[nb].append(pack)
    return nb_dict

def get_packages_only(nb_dict):
    # need to flatten out this list of lists
    nbd = [x for xs in nb_dict.values() for x in xs]
    return set(nbd)

# pd = {"numpy":0, "astropy":1, "fake_package":2}
# nbp = ["fake_package", "numpy"]

# print(nb_packages_to_row(pd, nbp))
