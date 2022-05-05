#!/usr/bin/env python
"""Create a badge SVG for testing."""
import os

from cloud_build_badge import BadgeMaker


def _main():
    for trigger in BadgeMaker.TRIGGERS:
        BadgeMaker.make_badge(trigger, "canceled", dir=os.path.curdir)


if __name__ == "__main__":
    _main()
