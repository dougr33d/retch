import re
from functools import cache
from typing import Any
from enum import IntEnum,auto

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')

from libretch.nodes.group_node import GroupNode
from libretch.nodes.abstract_node import AbstractNode
from libretch.renderers.abstract_renderer import AbstractRenderer

class TraceEntFlagBits(IntEnum):
    TR_HIGHLIGHT = 0  # 0
    TR_HEX = auto()  # 1
    TR_DEC = auto()  # 2
    TR_BIN = auto()  # 3
    TR_OCT = auto()  # 4
    TR_RJUSTIFY = auto()  # 5
    TR_INVERT = auto()  # 6
    TR_REVERSE = auto()  # 7
    TR_EXCLUDE = auto()  # 8
    TR_BLANK = auto()  # 9
    TR_SIGNED = auto()  # 10
    TR_ASCII = auto()  # 11
    TR_COLLAPSED = auto()  # 12
    TR_FTRANSLATED = auto()  # 13
    TR_PTRANSLATED = auto()  # 14
    TR_ANALOG_STEP = auto()  # 15
    TR_ANALOG_INTERPOLATED = auto()  # 16
    TR_ANALOG_BLANK_STRETCH = auto()  # 17
    TR_REAL = auto()  # 18
    TR_ANALOG_FULLSCALE = auto()  # 19
    TR_ZEROFILL = auto()  # 20
    TR_ONEFILL = auto()  # 21
    TR_CLOSED = auto()  # 22
    TR_GRP_BEGIN = auto()  # 23
    TR_GRP_END = auto()  # 24
    TR_BINGRAY = auto()  # 25
    TR_GRAYBIN = auto()  # 26
    TR_REAL2BITS = auto()  # 27
    TR_TTRANSLATED = auto()  # 28
    TR_POPCNT = auto()  # 29
    TR_FPDECSHIFT = auto()  # 30
    TR_TIME = auto()  # 31
    TR_ENUM = auto()  # 32
    TR_CURSOR = auto()  # 33
    TR_FFO = auto()  # 34

class GTKWaveRenderer(AbstractRenderer):
    """GTKWave Renderer
    
    Renders signals and groups in gtkwave save files
    """

    format = 'gtkw'

    def _to_magic(self, *flags) -> str:
        magic = 0
        for f in flags:
            magic |= 1 << f
        return f"@{magic:x}"

    def start_group(self, node: GroupNode) -> list:
        magic = self._to_magic(TraceEntFlagBits.TR_GRP_BEGIN, TraceEntFlagBits.TR_BLANK)
        if (not node.is_expanded):
            magic = self._to_magic(TraceEntFlagBits.TR_GRP_BEGIN, TraceEntFlagBits.TR_BLANK, TraceEntFlagBits.TR_CLOSED)

        grp = node._expand_str_with_var_dict(node._get_param('group_name',None))

        if grp == None:
            return []

        lines = [magic,'-' + grp]
        return lines

    def end_group(self, node: GroupNode) -> list:
        magic = self._to_magic(TraceEntFlagBits.TR_GRP_END, TraceEntFlagBits.TR_BLANK)
        grp = node._expand_str_with_var_dict(node._get_param('group_name',None))

        if grp == None:
            return []

        lines = [magic, '-' + grp]
        return lines

    def signal(self, node: AbstractNode) -> list:
        flags = [TraceEntFlagBits.TR_HEX, TraceEntFlagBits.TR_RJUSTIFY]
        if node._get_param('enum', False):
            flags = [TraceEntFlagBits.TR_ENUM, TraceEntFlagBits.TR_BIN, TraceEntFlagBits.TR_RJUSTIFY]
        magic = self._to_magic(*flags)

        sig = node._expand_str_with_var_dict(node._get_param('group_name'))
        full_sig = f"{node.full_path}{sig}".replace('/', '.')
        if full_sig[0] == '.':
            full_sig = full_sig[1:]

        lines = [magic, full_sig]
        return lines
