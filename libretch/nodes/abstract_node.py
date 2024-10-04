import re
import abc
from functools import cache
from typing import Any

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')

class AbstractNode(abc.ABC):
    """RC Node abstract base class
    
    All other nodes should subclass this class (or one of its subclasses)
    
    Nodes have two types of storage: params, and vars.

    **Params** are stored in `self._params`, and mostly come from key/value pairs in the yaml 
    configuration file.  Params have to be registered via `self._register_param_def`, and can 
    be unregistered with `self._unregister_param_def`.  The register/unregister paradigm is 
    mostly to validate whether or not a node type has its requisite parameters.
    
    **Vars** are stored in `self._var_dict`, and mostly come from RepeatNodes or other RTL
    paramaters specified at invocation.  These vars are always searched recursively, backwards
    up the tree, like inherited parameters.
    """

    ### class methods
    @staticmethod
    def matches(candidate: dict|str) -> bool:
        """Checks if the provided candidate matches this node type.
        
        Must be implemented by concrete classes.
        """
        return False

    def __init__(self, nf: Any, parent: Any, renderer: Any = None, param_dict: dict | None = None, var_dict: dict | None = None) -> None:
        self._parent = parent
        self._params: dict = param_dict or {}
        self._param_defs: dict = {}
        self._node_factory = nf
        self._var_dict: dict = var_dict or {}
        self._renderer = renderer
        if (renderer == None):
            self._renderer = parent._renderer

        self._init_param_defs()

    ### private member methods
    def _update_param(self, k: str, fld: str, val: Any) -> None:
        """Update the value associated with a param."""
        if not k in self._param_defs:
            self.croak(f'Parameter {k} not yet registered with this NodeType')
        self._param_defs[k][fld] = val

    def _register_param_def(self, k: str, t: Any = str, required: bool = False, inherits: bool = False) -> None:
        """Register a new param."""
        self._param_defs[k] = {'type': t, 'required': required, 'inherits': inherits}

    def _unregister_param_def(self, k: str) -> None:
        """Unregister an existing param."""
        del self._param_defs[k]

    def _init_param_defs(self) -> None:
        """Initialize base params common to all nodes.
        
        Subclasses can implement their own _init_param_defs, but they should still call this one.
        """
        self._register_param_def('group_name', str, required=False, inherits=False)
        self._register_param_def('path'      , str, required=False, inherits=False)
    
    @cache
    def _get_full_var_dict(self) -> dict:
        """Return the fully populated var_dict recursively back to the top of the tree.
        
        Cache it because otherwise it's slow AF.
        """
        if self._parent == None:
            return self._var_dict
        else:
            return dict(**self._var_dict, **self._parent._get_full_var_dict()) 
        
    def _expand_str_with_var_dict(self, s:str|None) -> Any:
        """Resolve vars in s with the full var_dict (with string.format)"""
        if not isinstance(s,str):
            return s
        vd = self._get_full_var_dict()
        return s.format(**vd)
        
    def _set_var(self, k: str, v: Any) -> None:
        """Set a var in the var_dict"""
        self._var_dict[k] = v
    
    def _validate_param(self, k: str) -> None:
        """Check that a param_def has been defined"""
        if k not in self._param_defs:
            keys = "{" + ", ".join(sorted(self._param_defs.keys())) + "}"
            self.croak(f"Could not find key {k} in param_defs. Key must be one of: {keys}")

    def _get_full_param_dict(self) -> dict:
        """Return full param_dict, recursively back to the top of the tree.
        
        Note that not all params can be inherited, so that needs to be checked
        before a param from the resulting dictionary can be used!"""
        if self._parent != None:
            return self._parent._get_full_param_dict() | self._params #type: ignore
        else:
            return self._params

    def _get_param(self, k: str, dflt: Any = None) -> Any:
        """Return a parameter value.
        
        If the param is defined as being inheritable, look in the recursively-generated
        param dict... otherwise, only look locally."""
        self._validate_param(k)
        if self._param_defs.get(k,{}).get('inherits', False):
            return self._get_full_param_dict().get(k,dflt)
        else:
            return self._params.get(k,dflt)

    ### public methods
    def croak(self, msg: str | None = None) -> None:
        """Croak!  Signal an error and print some useful debug info."""
        if msg != None:
            print(f"> {msg}")
        exit(-1)

    @property
    def full_path(self):
        """Return the full path to the local node."""
        p  = self._parent.full_path if self._parent != None else ""
        p += self._expand_str_with_var_dict(self._get_param('path',''))
        return p

    @abc.abstractmethod
    def render(self) -> list[str]:
        """Return a list of lines, rendered into the format given by the renderer."""
        pass
