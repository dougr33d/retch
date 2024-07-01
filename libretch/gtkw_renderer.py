import re
from functools import cache
from typing import Any
from enum import IntEnum,auto

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')

from libretch.group_node import GroupNode
from libretch.abstract_node import AbstractNode
from libretch.abstract_renderer import AbstractRenderer

class TraceEntFlagBits(IntEnum):
    TR_HIGHLIGHT = 0
    TR_HEX = auto()
    TR_DEC = auto()
    TR_BIN = auto()
    TR_OCT = auto()
    TR_RJUSTIFY = auto()
    TR_INVERT = auto()
    TR_REVERSE = auto()
    TR_EXCLUDE = auto()
    TR_BLANK = auto()
    TR_SIGNED = auto()
    TR_ASCII = auto()
    TR_COLLAPSED = auto()
    TR_FTRANSLATED = auto()
    TR_PTRANSLATED = auto()
    TR_ANALOG_STEP = auto()
    TR_ANALOG_INTERPOLATED = auto()
    TR_ANALOG_BLANK_STRETCH = auto()
    TR_REAL = auto()
    TR_ANALOG_FULLSCALE = auto()
    TR_ZEROFILL = auto()
    TR_ONEFILL = auto()
    TR_CLOSED = auto()
    TR_GRP_BEGIN = auto()
    TR_GRP_END = auto()
    TR_BINGRAY = auto()
    TR_GRAYBIN = auto()
    TR_REAL2BITS = auto()
    TR_TTRANSLATED = auto()
    TR_POPCNT = auto()
    TR_FPDECSHIFT = auto()
    TR_TIME = auto()
    TR_ENUM = auto()
    TR_CURSOR = auto()
    TR_FFO = auto()

class GTKWaveRenderer(AbstractRenderer):
    """GTKWave Renderer
    
    Renders signals and groups in gtkwave save files
    """

    def _to_magic(self, *flags) -> str:
        magic = 0
        for f in flags:
            magic |= 1 << f
        return f"@{magic:x}"

    def start_group(self, node: GroupNode) -> list:
        magic = self._to_magic(TraceEntFlagBits.TR_GRP_BEGIN, TraceEntFlagBits.TR_BLANK)
        if (not node._is_expanded()):
            magic = self._to_magic(TraceEntFlagBits.TR_GRP_BEGIN, TraceEntFlagBits.TR_BLANK, TraceEntFlagBits.TR_COLLAPSED)

        grp = node._expand_str_with_var_dict(node._get_param('group_name',None))

        lines = [magic,'-' + grp]
        return lines

    def end_group(self, node: GroupNode) -> list:
        magic = self._to_magic(TraceEntFlagBits.TR_GRP_END, TraceEntFlagBits.TR_BLANK)
        grp = node._expand_str_with_var_dict(node._get_param('group_name',None))

        lines = [magic, '-' + grp]
        return lines

    def signal(self, node: AbstractNode) -> list:
        magic = self._to_magic(TraceEntFlagBits.TR_HEX, TraceEntFlagBits.TR_RJUSTIFY)

        sig = node._expand_str_with_var_dict(node._get_param('group_name'))
        full_sig = f"{node.full_path}{sig}".replace('/', '.')
        if full_sig[0] == '.':
            full_sig = full_sig[1:]

        lines = [magic, full_sig]
        return lines
