from typing import Any

from .abstract_node import AbstractNode
from .group_node import GroupNode

class RepeatNode(GroupNode):
    ### class methods
    @staticmethod
    def matches(candidate: dict|str) -> bool:
        if not isinstance(candidate, dict):
            return False
        return candidate.get('type', 'group') == 'repeat'

    ### private member methods
    def __init__(self, nf: Any, parent: Any, renderer: Any = None, param_dict: dict|None = None, var_dict: dict|None = None) -> None:
        super().__init__(nf=nf, renderer=renderer, parent=parent, param_dict=param_dict, var_dict=var_dict)
        self._register_param_def('var',   str, required=True, inherits=False)
        self._register_param_def('count', int, required=True, inherits=False)
        self._register_param_def('child', Any, required=True, inherits=False)

    ### Public methods

    def render(self) -> list[str]:
        lines = []
        lines.extend(self._render_start_group())

        kid   = self._get_param('child')
        var   = self._get_param('var')
        count = self._get_param('count')
        for n in range(count):
            knode = self._node_factory.new_node(parent=self, candidate=kid, var_dict={var: n})
            lines.extend(knode.render())

        lines.extend(self._render_end_group())
        return lines
