"""Create a badge SVG for testing."""
import dataclasses
import os
from tempfile import mkstemp
from typing import Dict, Final, Optional

import yaml
from pybadges import badge


@dataclasses.dataclass
class Trigger:
    """A build trigger definition."""

    name: str
    left_text: str
    logo_uri: str


def _trigger_list_ctor(loader, node):
    sequence = loader.construct_sequence(node, deep=True)
    return {t["name"]: Trigger(**t) for t in sequence}


yaml.add_constructor("!TriggerList", _trigger_list_ctor)


def _load_triggers() -> Dict[str, Trigger]:
    with open("badges.yaml", "r", encoding="utf-8") as stream:
        data: Dict[str, Trigger] = yaml.unsafe_load(stream)["triggers"]
    return data


class BadgeMaker:
    """Create badges with custom text and icons."""

    TRIGGERS: Final[Dict[str, Trigger]] = _load_triggers()

    @classmethod
    def make_badge(
        cls, trigger_name: str, status: str, dir: Optional[str] = None
    ) -> str:
        """Create a badge for the specified trigger name."""
        trigger = cls.TRIGGERS[trigger_name]
        svg_data = badge(
            left_text=trigger.left_text,
            right_text=status,
            right_color="red",
            logo=trigger.logo_uri,
            embed_logo=True,
        )
        fileno, badge_file = mkstemp(suffix=".svg", dir=dir)
        with os.fdopen(fileno, "w+") as stream:
            stream.write(svg_data)
        return badge_file
