
from __future__ import annotations


import os

from hypothesis import given
from hypothesis.strategies import integers
from typing import Tuple
from tm_trees import TMTree, FileSystemTree

EXAMPLE_PATH_10_FILES = ''

tree_10_file = FileSystemTree(EXAMPLE_PATH_10_FILES)


def is_valid_colour(colour: Tuple[int, int, int]) -> bool:
    """Return True iff <colour> is a valid colour. That is, if all of its
    values are between 0 and 255, inclusive.
    """
    for i in range(3):
        if not 0 <= colour[i] <= 255:
            return False
    return True


def test_10_files_folder_initializer() -> None:
    """test a folder with 10 files"""
    assert tree_10_file._name == 'Test_10_files'
    for j in tree_10_file._subtrees:
        assert j._subtrees == []
        print(j.data_size)
    assert tree_10_file._parent_tree is None
    i = 0
    for k in tree_10_file._subtrees:
        i += k.data_size
    assert tree_10_file.data_size == i
    assert is_valid_colour(tree_10_file._colour)


def test_10_files_folder_image() -> None:
    tree_10_file.update_rectangles((0, 0, 200, 100))
    rects = tree_10_file.get_rectangles()
    assert len(rects) == 1

    tree_10_file.expand()
    tree_10_file.update_rectangles((0, 0, 200, 100))
    rects_1 = tree_10_file.get_rectangles()
    assert len(rects_1) == 10
    width = 0
    for i in tree_10_file._subtrees:
        assert i.rect[0] == width
        width += 20
        assert i.rect[1] == 0
        assert i.rect[2] == 20
        assert i.rect[3] == 100


EXAMPLE_PATH_EMPTY = '/Test_empty_folder'

tree_empty_file = FileSystemTree(EXAMPLE_PATH_EMPTY)


def test_tree_empty_file_initializer() -> None:
    """test a folder with 10 files"""
    assert tree_empty_file._name == 'Test_empty_folder'
    assert tree_empty_file._subtrees == []
    assert tree_empty_file._parent_tree is None
    assert tree_empty_file.data_size == 0
    assert is_valid_colour(tree_empty_file._colour)


def test_tree_empty_file_image() -> None:
    tree_empty_file.update_rectangles((0, 0, 200, 100))
    rects = tree_empty_file.get_rectangles()
    assert len(rects) == 1

    tree_empty_file.expand()
    tree_empty_file.update_rectangles((0, 0, 200, 100))
    rects_1 = tree_empty_file.get_rectangles()
    assert len(rects_1) == 1


EXAMPLE_PATH_5_HEIGHT = '/Test_tree_height_5'

tree_5_height = FileSystemTree(EXAMPLE_PATH_5_HEIGHT)


def test_tree_5_height_initializer() -> None:
    """test a folder with 10 files"""
    assert tree_5_height._name == 'Test_tree_height_5'
    assert len(tree_5_height._subtrees) == 3
    assert tree_5_height._parent_tree is None
    assert is_valid_colour(tree_5_height._colour)


def test_tree_5_height_image() -> None:
    tree_5_height.update_rectangles((0, 0, 400, 200))
    rects = tree_5_height.get_rectangles()
    assert len(rects) == 1
    assert rects[0][0] == (0, 0, 400, 200)

    tree_5_height.expand()
    tree_5_height.update_rectangles((0, 0, 400, 200))
    rects_1 = tree_5_height.get_rectangles()
    assert len(rects_1) == 3
    a = tree_5_height._subtrees[0]
    b = tree_5_height._subtrees[1]
    c = tree_5_height._subtrees[2]
    assert a.rect == (0, 0, 171, 200)
    assert b.rect == (171, 0, 129, 200)
    assert c.rect == (300, 0, 100, 200)

    a.expand()
    d = a._subtrees[0]
    assert d.rect == (0, 0, 171, 30)
    e = a._subtrees[1]
    assert e.rect == (0, 30, 171, 30)
    f = a._subtrees[2]
    assert f.rect == (0, 60, 171, 117)
    g = a._subtrees[3]
    assert g.rect == (0, 177, 171, 12)
    h = a._subtrees[4]
    assert h.rect == (0, 189, 171, 11)

    g.change_size(0.01)
    assert g.data_size == 53523

    h.change_size(-0.01)
    assert h.data_size == 40135

    g.move(f)
    assert len(f._subtrees) == 6
    assert len(a._subtrees) == 4

    tree_5_height.update_data_sizes()
    assert a.data_size == 856660
    assert f.data_size == 557746

    g.collapse_all()

    assert tree_5_height._expanded == False
    for i in tree_5_height._subtrees:
        assert i._expanded is False
        for j in i._subtrees:
            assert j._expanded is False
            for k in j._subtrees:
                assert k._expanded is False
                for l in k._subtrees:
                    assert l._expanded is False
                    for m in l._subtrees:
                        assert m._expanded is False


if __name__ == '__main__':
    import pytest
    pytest.main(['TMTree_tests.py'])
