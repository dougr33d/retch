import re
import abc
from functools import cache
from typing import Any

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')

class AbstractNode(abc.ABC):
    """RC Node abstract base class
    
    All other nodes should extend from this class.
    """

    ### class methods
    @staticmethod
    def matches(candidate: dict|str) -> bool:
        """Checks if the provided candidate matches this node type.
        
        Must be implemented by concrete classes.
        """
        return False

    ### private member methods
    def _update_param(self, k: str, fld: str, val: Any) -> None:
        if not k in self._param_defs:
            self._croak(f'Parameter {k} not yet registered with this NodeType')
        self._param_defs[k][fld] = val

    def _register_param_def(self, k: str, t: Any = str, required: bool = False, inherits: bool = False) -> None:
        self._param_defs[k] = {'type': t, 'required': required, 'inherits': inherits}

    def _unregister_param_def(self, k: str) -> None:
        del self._param_defs[k]

    def _init_param_defs(self) -> None:
        self._register_param_def('group_name', str, required=False, inherits=False)
        self._register_param_def('path'      , str, required=False, inherits=False)
    
    @cache
    def _get_full_var_dict(self) -> dict:
        if self._parent == None:
            return self._var_dict
        else:
            return dict(**self._var_dict, **self._parent._get_full_var_dict()) 
        
    def _expand_str_with_var_dict(self, s:str|None) -> str:
        if not isinstance(s,str):
            return s
        vd = self._get_full_var_dict()
        return s.format(**vd)
        
    def _set_var(self, k: str, v: Any) -> None:
        self._var_dict[k] = v
    
    def __init__(self, nf: Any, parent: Any, param_dict: dict | None = None, var_dict: dict | None = None) -> None:
        self._parent = parent
        self._params: dict = param_dict or {}
        self._param_defs: dict = {}
        self._node_factory = nf
        self._var_dict: dict = var_dict or {}

        self._init_param_defs()

    def _croak(self, msg: str | None = None) -> None:
        if msg != None:
            print(f"> {msg}")
        exit(-1)

    ### private methods
    def _validate_param(self, k: str) -> None:
        if k not in self._param_defs:
            keys = "{" + ", ".join(sorted(self._param_defs.keys())) + "}"
            self._croak(f"Could not find key {k} in param_defs. Key must be one of: {keys}")

    def _get_full_param_dict(self) -> dict:
        if self._parent != None:
            return dict(**self._parent._get_full_param_dict(), **self._params) #type: ignore
        else:
            return self._params

    def _get_param(self, k: str, dflt: Any = None) -> Any:
        self._validate_param(k)
        if self._param_defs.get(k,{}).get('inherits', False):
            return self._get_full_param_dict().get(k,dflt)
        else:
            return self._params.get(k,dflt)

    ### public methods
    @property
    def full_path(self):
        p  = self._parent.full_path if self._parent != None else ""
        p += self._expand_str_with_var_dict(self._get_param('path',''))
        return p

    @abc.abstractmethod
    def render(self) -> list[str]:
        pass
