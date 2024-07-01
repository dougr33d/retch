from typing import Any
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')

from .nodes.group_node import GroupNode
from .nodes.signal_node import SignalNode
from .nodes.repeat_node import RepeatNode

class NodeFactory:
    def __init__(self):
        self._node_types = []
        self._node_types.append(GroupNode)
        self._node_types.append(RepeatNode)
        self._node_types.append(SignalNode)

    def register_node_type(self, nt):
        self._node_types.append(nt)

    def new_node(self, parent: Any, candidate: dict|str, renderer: Any = None, var_dict: dict|None = None):
        mats = [nt for nt in self._node_types if nt.matches(candidate)]
        if len(mats) == 0:
            logger.error("Could not find suitable NodeType!")
            logger.error(self._node_types)
            logger.error(candidate.__repr__()[:100] + "...")
            exit(-1)
        elif len(mats) > 1:
            logger.error("Found multiple matching NodeTypes!")
            exit(-1)
        else:
            nt = mats[0]
            return nt(nf=self, renderer=renderer, parent=parent, param_dict=candidate, var_dict=var_dict)
