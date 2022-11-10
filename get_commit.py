"""Construct a commit message"""

from __future__ import annotations

from typing import NamedTuple
from collections.abc import Iterable
import argparse

import yaml

TEMPLATE = """\n
New admins:     {}
Removed admins: {}
New bans:       {}
Removed bans:   {}
"""

class Diff(NamedTuple):
    new: list[int]
    old: list[int]

    def __bool__(self) -> bool:
        return bool(self.new) or bool(self.old)


def get_diff(lst_new: Iterable[int], lst_old: Iterable[int]) -> Diff:
    set_new = set(lst_new)
    set_old = set(lst_old)
    return Diff(new=sorted(set_new - set_old), old=sorted(set_old - set_new))


def main(path_new: str, path_old: str, commit_msg) -> str:
    with open(path_new, "r", encoding="utf8") as f:
        dct_new = yaml.load(f.read(), Loader=yaml.SafeLoader)

    with open(path_old, "r", encoding="utf8") as f:
        dct_old = yaml.load(f.read(), Loader=yaml.SafeLoader)

    admins = get_diff(dct_new["admin_list"], (dct_old["admin_list"]))
    bans = get_diff(dct_new["ban_list"], (dct_old["ban_list"]))
    if (admins or bans):
        return commit_msg + TEMPLATE.format(admins.new, admins.old, bans.new, bans.old)
    else:
        return commit_msg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./get_commit.py file1.yaml file1.yaml 'This is a commit message'", description=__doc__)
    parser.add_argument("path_new", help="Path to the new .yaml file")
    parser.add_argument("path_old", help="Path to the old .yaml file")
    parser.add_argument("commit_msg", help="The old commit message")
    args = parser.parse_args()
    print(main(args.path_new, args.path_old, args.commit_msg))
