from typing import Any
from functools import cache

from .abstract_node import AbstractNode

class SignalNode(AbstractNode):
    ### class methods
    @staticmethod
    def matches(candidate: dict|str) -> bool:
        if isinstance(candidate, str):
            return True
        if not isinstance(candidate, dict):
            return False
        return candidate.get('type', 'group') == 'signal'

    ### private member methods
    def __init__(self, nf: Any, renderer:Any, parent: Any, param_dict: dict|str|None = None, var_dict: dict|None = None) -> None:
        if isinstance(param_dict, str):
            signal_name = param_dict
            param_dict = { 'group_name': signal_name,
                           'type': 'signal',
                          }
        super().__init__(nf=nf, renderer=renderer, param_dict=param_dict, parent=parent, var_dict=var_dict)
        self._update_param('group_name', 'required', True)

    ### Public methods
    def render(self) -> list[str]:
        return self._renderer.signal(self)
