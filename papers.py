"""Assignment 2: Modelling CS Education research paper data

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains a new class, PaperTree, which is used to model data on
publications in a particular area of Computer Science Education research.
This data is adapted from a dataset presented at SIGCSE 2019.
You can find the full dataset here: https://www.brettbecker.com/sigcse2019/

Although this data is very different from filesystem data, it is still
hierarchical. This means we are able to model it using a TMTree subclass,
and we can then run it through our treemap visualisation tool to get a nice
interactive graphical representation of this data.
"""
import csv
from typing import List, Dict
from tm_trees import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    _authors:
        The author(s) of the paper represented by this tree.
    _doi:
        The digital object identifier (DOI) used to identify the specific
        paper represented by this tree.

    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - All TMTree RIs are inherited.
    """
    _authors: str
    _doi: str
    _by_year: bool
    _all_paper: bool

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>,
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        if all_papers is True:
            year = by_year
            sample_dict = _load_papers_to_dict(DATA_FILE, by_year)
            subtrees_2 = _build_tree_from_dict(sample_dict, year)
            TMTree.__init__(self, name, subtrees_2, citations)
            self._authors = authors
            self._doi = doi
            self._by_year = by_year
            self._all_paper = all_papers
        else:
            TMTree.__init__(self, name, subtrees, citations)
            self._authors = authors
            self._doi = doi
            self._by_year = by_year
            self._all_paper = all_papers

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        return '\\'

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        if len(self._subtrees) == 0:
            return ' (paper)'
        else:
            return ' (category)'


def _load_papers_to_dict(dataset: csv, by_year: bool = True) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    data = {}
    with open(dataset, newline='') as csvfile:
        data_reader = csv.reader(csvfile, delimiter=',')
        next(data_reader)
        for line in data_reader:
            for item in line:
                item.strip(' ')
            year = line[2]
            if by_year is True:
                if year not in data.keys():
                    data[year] = {}
            categories = line[3].split(': ')
            check = _subcategories(data, year, categories, by_year)
            current_category = _add_category(data, year, categories, check,
                                             by_year)
            current_category['papers'].append({'authors': line[0],
                                               'name': line[1], 'doi': line[4],
                                               'citations': int(line[5])})
    csvfile.close()
    return data


def _subcategories(overall_data: Dict, yr: str, lst: List, by_year: bool) -> \
        int:
    """Return the depth up until categories do not exist in nested dictionary
    <overall_data>.
    """
    if by_year is True:
        dic = overall_data[yr]
    else:
        dic = overall_data
    pos = 0
    while pos < len(lst):
        sub = lst[pos]
        if sub not in dic.keys():
            return pos
        dic = dic[sub]
        pos += 1
    return pos


def _add_category(overall_data: Dict, yr: str, lst: List, index: int,
                  by_year: bool) -> Dict:
    """Add non-existing categories as nested dictionaries into an existing
    category that is an dictionary and return dictionary of deepest depth.
    """
    curr_d = 0
    if by_year is True:
        curr = overall_data[yr]
    else:
        curr = overall_data
    while curr_d != index:
        curr = curr[lst[curr_d]]
        curr_d += 1
    while curr_d != len(lst):
        curr[lst[curr_d]] = {'papers': []}
        curr = curr[lst[curr_d]]
        curr_d += 1
    return curr


def _build_tree_from_dict(nested_dict: Dict, year: bool) -> List[PaperTree]:
    """Return a list of trees from the nested dictionary <nested_dict>.
    """
    tree = []
    for i in nested_dict.keys():
        if isinstance(nested_dict[i], list) and len(nested_dict[i]) != 0:
            for j in nested_dict[i]:
                tree.append(PaperTree(j['name'], [], j['authors'],
                                      j['doi'], j['citations'], year))
        elif isinstance(nested_dict[i], list) and len(nested_dict[i]) == 0:
            pass
        elif isinstance(nested_dict[i], dict):
            subtree = []
            subtree.extend(_build_tree_from_dict(nested_dict[i], year))
            tree.extend([PaperTree(i, subtree)])
    return tree


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_load_papers_to_dict'],
        'max-args': 8
    })
