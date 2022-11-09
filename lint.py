"""A script for linting .yaml files."""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

import yaml

if TYPE_CHECKING:
    from yaml.emitter import _WriteStream


class Representer(yaml.representer.SafeRepresenter):
    def represent_list(self, data: Iterable[object]) -> yaml.SequenceNode:
        return self.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)


Representer.add_representer(list, Representer.represent_list)


class Dumper(Representer, yaml.SafeDumper):
    def __init__(self, stream: _WriteStream, **kwargs: Any) -> None:
        super().__init__(stream, **kwargs)
        Representer.__init__(
            self,
            default_style=kwargs.get("default_style", None),
            default_flow_style=kwargs.get("default_flow_style", False),
            sort_keys=kwargs.get("sort_keys", True),
        )


def main(filename: str) -> None:
    with open(filename, "r", encoding="utf8") as f1:
        dct = yaml.load(f1.read(), Loader=yaml.SafeLoader)

    with open(filename, "w", encoding="utf8") as f2:
        yaml.dump(dct, f2, Dumper=Dumper, sort_keys=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./lint.py room_settings.yaml", description=__doc__)
    parser.add_argument("path", help="Path to the to-be linted .yaml file")
    args = parser.parse_args()
    main(args.path)
