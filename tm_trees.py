"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations
import os
import math
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
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
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))

        if len(subtrees) == 0:
            self.data_size = data_size
        else:
            self.data_size = 0
            for subtree in subtrees:
                self.data_size += subtree.data_size

        for subtree in subtrees:
            subtree._parent_tree = self

        self._expanded = False

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        if self._name is None:
            self.rect = (0, 0, 0, 0)
        elif self._subtrees == []:
            self.rect = rect
        elif self.data_size > 0:
            x, y, width, height = rect
            self.rect = rect
            save_x = x
            save_y = y
            if width > height:
                for i in self._subtrees[:-1]:
                    proportion_i = i.data_size / self.data_size
                    i.rect = (x, y, math.floor(width * proportion_i), height)
                    x += i.rect[2]
                    i.update_rectangles(i.rect)
                self._subtrees[-1].rect = (x, y, save_x + width - x, height)
                self._subtrees[-1].update_rectangles(self._subtrees[-1].rect)
            else:
                for j in self._subtrees[:-1]:
                    proportion_j = j.data_size / self.data_size
                    j.rect = (x, y, width, math.floor(height * proportion_j))
                    y += j.rect[3]
                    j.update_rectangles(j.rect)
                self._subtrees[-1].rect = (x, y, width, save_y + height - y)
                self._subtrees[-1].update_rectangles(self._subtrees[-1].rect)
        elif self.data_size == 0:
            self.rect = rect
            x, y, width, height = rect
            if width > height:
                for i in self._subtrees[:-1]:
                    i.rect = (x, y, 0, height)
                    i.update_rectangles(i.rect)
                self._subtrees[-1].rect = rect
                self._subtrees[-1].update_rectangles(self._subtrees[-1].rect)
            else:
                for j in self._subtrees[:-1]:
                    j.rect = (x, y, width, 0)
                    j.update_rectangles(j.rect)
                self._subtrees[-1].rect = rect
                self._subtrees[-1].update_rectangles(self._subtrees[-1].rect)

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self._expanded is False and self.data_size == 0:
            return []
        elif self._expanded is False:
            return [(self.rect, self._colour)]
        else:
            result = []
            if self._expanded is True:
                for sub in self._subtrees:
                    result.extend(sub.get_rectangles())
            return result

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        if self.data_size == 0:
            return None
        elif self.rect[0] <= pos[0] <= (self.rect[0] + self.rect[2]) and \
                self.rect[1] <= pos[1] <= (self.rect[1] + self.rect[3]) \
                and (self._subtrees == [] or not self._expanded):
            return self
        else:
            leaves = []
            for sub in self._subtrees:
                leaves.append(sub.get_tree_at_position(pos))
            leaves = [item for item in leaves if item is not None]
            if len(leaves) == 0:
                return None
            smallest = math.sqrt((leaves[0].rect[0])**2 +
                                 (leaves[0].rect[1])**2)
            i = 0
            j = 0
            for leaf in leaves[1:]:
                j += 1
                c = math.sqrt((leaf.rect[0])**2 + (leaf.rect[1])**2)
                if c < smallest:
                    smallest = c
                    i = j
            return leaves[i]

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self._subtrees == []:
            return self.data_size
        else:
            self.data_size = 0
            for sub in self._subtrees:
                self.data_size += sub.update_data_sizes()
            return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if self._subtrees == [] and len(destination._subtrees) != 0:
            current_parent = self._parent_tree
            current_parent._subtrees.remove(self)
            destination._subtrees.append(self)
            self._parent_tree = destination

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if self.data_size == 1 and factor < 0:
            pass
        elif self._subtrees == []:
            if factor < 0:
                self.data_size = self.data_size + \
                                 -math.ceil(-factor*self.data_size)
            else:
                self.data_size = self.data_size + \
                                 math.ceil(factor*self.data_size)
        else:
            pass

    def expand(self) -> None:
        """Expand the tree corresponding the chosen rectangle in the
        displayed-tree.
        If the tree is a leaf, nothing happens.
        """
        if self._subtrees != []:
            self._expanded = True

    def expand_all(self) -> None:
        """Expand the tree corresponding to the chosen rectangle, as well as
        all of its subtrees in the displayed tree.
        """
        if self._subtrees != []:
            self.expand()
            for sub in self._subtrees:
                sub.expand_all()

    def collapse(self) -> None:
        """Collapse the parent of the selected tree.
        """
        if self._parent_tree is None:
            pass
        else:
            self._parent_tree._collapse_all_helper()

    def collapse_all(self) -> None:
        """Collapse the entire displayed tree down to just a single tree node
        """
        current_tree = self
        while current_tree._parent_tree is not None:
            current_tree = current_tree._parent_tree
        current_tree._collapse_all_helper()

    def _collapse_all_helper(self) -> None:
        """A private helper method that collapse the tree as well as all of its
        subtrees.
        """
        if self._subtrees != []:
            self._expanded = False
            for sub in self._subtrees:
                if sub._expanded:
                    sub._collapse_all_helper()

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        if os.path.isdir(path):
            subtrees = []
            for f in os.listdir(path):
                i = os.path.join(path, f)
                subtrees.append(FileSystemTree(i))
            TMTree.__init__(self, os.path.basename(path), subtrees,
                            os.path.getsize(path))
        else:
            TMTree.__init__(self, os.path.basename(path), [],
                            os.path.getsize(path))

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
