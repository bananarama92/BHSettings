"""Construct a commit message"""

from __future__ import annotations

from typing import NamedTuple
from collections.abc import Iterable
import argparse

import yaml

TEMPLATE = """\n
Original commit hash: {commit_hash!r}

New admins:           {admins_added!r}
Removed admins:       {admins_removed!r}
New bans:             {bans_added!r}
Removed bans:         {bans_removed!r}
"""

class Diff(NamedTuple):
    added: list[int]
    removed: list[int]

    def __bool__(self) -> bool:
        return bool(self.added) or bool(self.removed)


def get_diff(lst_new: Iterable[int], lst_old: Iterable[int]) -> Diff:
    set_new = set(lst_new)
    set_old = set(lst_old)
    return Diff(added=sorted(set_new - set_old), removed=sorted(set_old - set_new))


def main(path_new: str, path_old: str, commit_msg: str, commit_hash: str) -> str:
    # Avoid accidentally appending the commit message a second time
    if "Original commit hash:" in commit_msg:
        return commit_msg

    with open(path_new, "r", encoding="utf8") as f:
        dct_new = yaml.load(f.read(), Loader=yaml.SafeLoader)
    with open(path_old, "r", encoding="utf8") as f:
        dct_old = yaml.load(f.read(), Loader=yaml.SafeLoader)

    admins = get_diff(dct_new["admin_list"], (dct_old["admin_list"]))
    bans = get_diff(dct_new["ban_list"], (dct_old["ban_list"]))
    if (admins or bans):
        return commit_msg + TEMPLATE.format(
            commit_hash=commit_hash,
            admins_added=admins.added,
            admins_removed=admins.removed,
            bans_added=bans.added,
            bans_removed=bans.removed,
        )
    else:
        return commit_msg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="python ./get_commit.py file1.yaml file1.yaml 'This is a commit message' 'f71bfc7f26b1ac003938d9e097bbd311bc59c8db'",
        description=__doc__,
    )
    parser.add_argument("path_new", help="Path to the new .yaml file")
    parser.add_argument("path_old", help="Path to the old .yaml file")
    parser.add_argument("commit_msg", help="The old commit message")
    parser.add_argument("commit_hash", help="The hash of the original commit")
    args = parser.parse_args()
    print(main(args.path_new, args.path_old, args.commit_msg, args.commit_hash))
