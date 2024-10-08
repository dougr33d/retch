import re
from functools import cache
from typing import Any

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')

from libretch.nodes.group_node import GroupNode
from libretch.nodes.abstract_node import AbstractNode
from libretch.renderers.abstract_renderer import AbstractRenderer

class RCFileRenderer(AbstractRenderer):
    """RCFile Renderer
    
    Renders signals and groups in RC files
    """

    format = 'rc'

    def start_group(self, node: GroupNode) -> list:
        grp = node._expand_str_with_var_dict(node._get_param('group_name',None))
        if node._parent == None:
            return [f"addGroup {grp}"]
        else:
            # addSubGroup (or ignore if no group name)
            if grp != None:
                return [f"addSubGroup {grp}"]
            else:
                return []

    def end_group(self, node: GroupNode) -> list:
        grp = node._expand_str_with_var_dict(node._get_param('group_name',None))
        if node._parent == None:
            return []
        else:
            # endSubGroup (or ignore if no group name)
            if grp != None:
                return [f"endSubGroup {grp}"]
            else:
                return []

    def signal(self, node: AbstractNode) -> list:
        sig = node._expand_str_with_var_dict(node._get_param('group_name'))
        lines = [f"addSignal -h 15 {node.full_path}{sig}"]
        return lines
