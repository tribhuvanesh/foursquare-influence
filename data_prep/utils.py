#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 sids <sids@siddharth-dev>
#
# Distributed under terms of the MIT license.

"""
Set of functions I will need again and again
"""


def read_csv_file_and_return_tuples(filename):
    tuples = []
    with open(filename, "rb") as f:
        for line in f.readlines():
            line = line.strip()
            tuples.append(line.split(','))
    return tuples


def get_unconnected_users(no_users_fn):
    fnofriends = open(no_users_fn, 'r')
    no_friends = {}
    for line in fnofriends:
        no_friends[int(line.strip())] = 1
    return no_friends


def get_friendship_edges_dict(filename):
    tuples = read_csv_file_and_return_tuples(filename)
    edges = {}
    for t in tuples:
        u, v = t
        #u, v = (min(u, v), max(u, v))
        edges[(u, v)] = edges.setdefault((u, v), 0) + 1
    return edges
