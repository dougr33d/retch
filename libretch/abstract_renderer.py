import re
import abc
from functools import cache
from typing import Any

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')

from libretch.group_node import GroupNode
from libretch.abstract_node import AbstractNode

class AbstractRenderer(abc.ABC):
    """Abstract renderer class
    
    Renderers are used by Nodes to produce text.  They implement three methods:

    start_group() -> str
    end_group() -> str
    signal() -> str
    """

    @abc.abstractmethod
    def start_group(node: GroupNode) -> str:
        pass

    @abc.abstractmethod
    def end_group(node: GroupNode) -> str:
        pass

    @abc.abstractmethod
    def signal(node: AbstractNode) -> str:
        pass