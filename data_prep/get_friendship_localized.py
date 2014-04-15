#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 sids <sids@siddharth-dev>
#
# Distributed under terms of the MIT license.

"""
Get users from checkins
"""
from utils import *
import sys


def get_users_from_checkins(filename, user_file):
    tuples = read_csv_file_and_return_tuples(filename)
    users = set()
    for t in tuples:
        users.add(t[0])
    with open(user_file, "w") as f:
        for u in users:
            f.write(u + "," + u + "\n")


def get_local_friendships(checkins_file, user_file, friendship_file, output_file, no_friends_file):
    get_users_from_checkins(checkins_file, user_file)
    users = read_csv_file_and_return_tuples(user_file)
    users_map = {}
    for u in users:
        users_map[u[0]] = 0
    friendships = []
    for f in read_csv_file_and_return_tuples(friendship_file):
        a, b = f
        if a in users_map and b in users_map:
            friendships.append((a, b))
            users_map[a] = 1
            users_map[b] = 1

    with open(output_file, "w") as f:
        for u, v in friendships:
            f.write(u + "," + v + "\n")

    with open(no_friends_file, "w") as f:
        for u in users_map:
            if users_map[u] == 0:
                f.write(u + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.exit("Format: get_friendship_localized.py checkins_file user_file overall_friendship_file output_file no_friends_file")
    get_local_friendships(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
