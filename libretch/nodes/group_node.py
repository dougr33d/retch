from .abstract_node import AbstractNode
from typing import Any

class GroupNode(AbstractNode):
    ### class methods
    @staticmethod
    def matches(candidate: dict|str) -> bool:
        if not isinstance(candidate, dict):
            return False
        return candidate.get('type', 'group') == 'group'

    ### private member methods
    def _render_start_group(self) -> list[str]:
        return self._renderer.start_group(self)

    def _render_end_group(self) -> list[str]:
        return self._renderer.end_group(self)

    def __init__(self, nf: Any, renderer:Any, parent: Any, param_dict: dict | None = None, var_dict: dict|None = None) -> None:
        super().__init__(nf=nf, renderer=renderer, parent=parent, param_dict=param_dict, var_dict=var_dict)
        if self._parent == None:
            self._update_param('group_name', 'required', True)
        self._register_param_def('children', list, required=False, inherits=False)
        self._register_param_def('expand',   bool, required=False, inherits=False)
        self._register_param_def('expand_all',   bool, required=False, inherits=True)

    ### Public methods

    @property
    def is_expanded(self) -> bool:
        if (e := self._get_param('expand', None)) != None:
            return e
        return self._get_param('expand_all', True)

    def render(self) -> list[str]:
        lines = []
        lines.extend(self._render_start_group())

        for k in self._get_param('children',[]):
            knode = self._node_factory.new_node(parent=self, candidate=k)
            lines.extend(knode.render())

        lines.extend(self._render_end_group())
        return lines
