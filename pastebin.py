"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all sub-directories are:
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
    However, part of this asignment will involve you implementing new public
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
    _name: Optional[str]
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
        # Setting random colour
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))

        # for task 5
        self._expanded = False

        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        if subtrees == [] or name is None:
            self.data_size = data_size

        else:
            x = 0
            for tree in subtrees:
                x += tree.data_size
                # 2. Set this tree as the parent for each of its subtrees.
                tree._parent_tree = self

            self.data_size = x

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # get the input into usable shit
        x, y, w, h = rect
        total_h, total_w = 0, 0

        # used for task 5, as a way to know if this needs to be displayed

        if not self._expanded:
            self.rect = rect

        # from the website
        if self.is_empty():
            return []

        elif self.get_suffix() == ' (folder)':

            # if we need to split horizontally or vertically
            if w > h:

                for subtree in self._subtrees:

                    if subtree == self._subtrees[-1]:
                        subtree.update_rectangles((x, y, w - total_w, h))

                    else:

                        scale = math.trunc(subtree.data_size * w / self.data_size)

                        subtree.update_rectangles((x, y, scale, h))

                        total_w += scale
                        x += scale
            else:

                for subtree in self._subtrees:

                    if subtree == self._subtrees[-1]:
                        subtree.update_rectangles((x, y, w, h - total_h))

                    else:
                        scale = math.trunc(subtree.data_size * h
                                           / self.data_size)

                        subtree.update_rectangles((x, y, w, scale))

                        total_h += scale
                        y += scale

        # if this is a file just return the rectangle given to us
        # by the parent folder calculated above
        if self.get_suffix() == ' (file)':
            self.rect = rect

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """

        if self.data_size == 0:
            return []

        if not self._expanded:
            return [(self.rect, self._colour)]

        if self.get_suffix() == ' (file)':
            return [(self.rect, self._colour)]

        output = []
        if self.get_suffix() == ' (folder)':
            for sub_tree in self._subtrees:
                output.extend(sub_tree.get_rectangles())

            return output

    def _better_get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           TMTree]]:
        """Its just better... """

        if self.data_size == 0:
            return []

        if not self._expanded:
            return [(self.rect, self)]

        if self.get_suffix() == ' (file)':
            return [(self.rect, self)]

        output = []
        if self.get_suffix() == ' (folder)':
            for sub_tree in self._subtrees:
                output.extend(sub_tree._better_get_rectangles())

            return output

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        ties should be broken by choosing the rectangle on the left for a
        vertical boundary, or the rectangle above for a horizontal boundary.

        """
        x, y = pos

        check_list = self._better_get_rectangles()
        output = []

        for tree in check_list:
            x1, y1, w, h = tree[0]
            x2 = x1+w
            y2 = y1+h

            if (x1 <= x <= x2) and (y1 <= y <= y2):
                output.append(tree[1])

        if len(output) == 4:
            # 4 Way Tie
            x -= 1
            y -= 1
            output.clear()
            output.append(self.get_tree_at_position((x, y)))

        if len(output) == 3:
            # 3 Way Tie
            # EDGE CASE
            if x == 0:
                output.clear()
                output.append(self.get_tree_at_position((x, y - 1)))
            elif y == 0:
                output.clear()
                output.append(self.get_tree_at_position((x - 1, y)))

            if x!= 0 :
                output.clear()
                output.append(self.get_tree_at_position((x - 1, y)))

            if y!=0 :
                output.clear()
                output.append(self.get_tree_at_position((x, y - 1)))

        if len(output) == 2:
            # 2 Way Tie
            # EDGE CASE
            if x == 0:
                output.clear()
                output.append(self.get_tree_at_position((x, y - 1)))
            elif y == 0:
                output.clear()
                output.append(self.get_tree_at_position((x - 1, y)))

            # IF WE STILL HAVE A TIE RETURN IS NONE

            elif not self._tie_finder((x, y - 1)):
                output.clear()
                output.append(self.get_tree_at_position((x, y - 1)))

            elif not self._tie_finder((x - 1, y)):
                output.clear()
                output.append(self.get_tree_at_position((x - 1, y)))

        if len(output) == 1:
            return output[0]

        return None

    def _tie_finder(self, pos: Tuple[int, int]) -> bool:
        x, y = pos

        check_list = self._better_get_rectangles()
        output = []

        for tree in check_list:
            x1, y1, w, h = tree[0]
            x2 = x1+w
            y2 = y1+h

            if (x1 <= x <= x2) and (y1 <= y <= y2):
                output.append(tree[1])

        return len(output) > 1 and len(output) != 0

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self.get_suffix() == ' (file)':
            return self.data_size
        else:
            x = 0
            for tree in self._subtrees:
                x += tree.update_data_sizes()
            self.data_size = x
            return x

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """

        if self.get_suffix() == ' (file)' \
                and destination.get_suffix() == ' (folder)':

            self.collapse()

            parent_tree = self._parent_tree
            parent_tree._subtrees.remove(self)

            self._parent_tree = destination
            destination._subtrees.append(self)

            # Update data sizes after the move
            parent_tree.update_data_sizes()
            destination.update_data_sizes()

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.

        """
        if self.get_suffix() == ' (file)':
            if factor > 0:
                factor += 1
                self.data_size = math.ceil(self.data_size * factor)
            elif factor < 0:
                self.data_size = int(self.data_size * factor + self.data_size)
        else:
            pass

    def expand(self) -> None:
        if self._name is not None:
            if self._subtrees is not []:
                self._expanded = True
                for subtree in self._subtrees:
                    subtree._expanded = True

    def expand_all(self) -> None:

        curr = self

        while curr._parent_tree is not None:
            curr = curr._parent_tree

        curr._expand_all()

    def _expand_all(self) -> None:
        if self._name is not None:
            if self._subtrees is not []:
                self._expanded = True

                for tree in self._subtrees:
                    tree._expand_all()

    def collapse(self) -> None:
        try:
            self._expanded = False
            parent = self._parent_tree
            parent._expanded = False
            for subtree in parent._subtrees:
                subtree._expanded = False

            curr = self
            while curr._parent_tree is not None:
                curr = curr._parent_tree

            curr.update_rectangles(curr.rect)

        except AttributeError:
            pass

    def collapse_all(self) -> None:
        try:
            curr = self
            while curr._parent_tree is not None:
                curr = curr._parent_tree

            to_be_collapsed = curr._better_get_rectangles()

            for tree in to_be_collapsed:
                tree[1].collapse()
        except AttributeError:
            pass

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

        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!

        # if its a file
        if os.path.isfile(path):
            name = os.path.basename(path)
            TMTree.__init__(self, name, [], os.path.getsize(path))

        # if its a folder
        if os.path.isdir(path):
            subtree_files = os.listdir(path)
            subtree_objects = []

            for file_name in subtree_files:
                new_path = os.path.join(path, file_name)
                subtree_objects.append(FileSystemTree(new_path))

            name = os.path.basename(path)

            TMTree.__init__(self, name, subtree_objects, os.path.getsize(path))

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
