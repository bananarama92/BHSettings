"""A script for linting .yaml files."""

import argparse
import yaml

NO_COMMA = frozenset({"admin_list", "ban_list"})


def main(filename: str) -> None:
    with open(filename, "r", encoding="utf8") as f1:
        dct = yaml.load(f1.read(), Loader=yaml.SafeLoader)

    with open(filename, "w", encoding="utf8") as f2:
        for k, v in dct.items():
            if isinstance(v, list):
                v.sort()
                sep = "," if k in NO_COMMA else ", "
                f2.write(f"{k}: [{sep.join(repr(i) for i in v)}]\n")
            else:
                f2.write(f"{k}: {v!r}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./lint.py room_settings.yaml", description=__doc__)
    parser.add_argument("path", help="Path to the to-be linted .yaml file")
    args = parser.parse_args()
    main(args.path)
