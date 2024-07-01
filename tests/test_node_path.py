import pytest

from ..libretch.nodes.group_node import GroupNode
from ..libretch.nodes.signal_node import SignalNode
from ..libretch.node_factory import NodeFactory
from ..libretch.renderers.rcfile_renderer import RCFileRenderer

def test_node_path():
    node_factory = NodeFactory()
    node_factory.register_node_type(GroupNode)
    node_factory.register_node_type(SignalNode)
    renderer = RCFileRenderer()

    rcdict = {'group_name': 'top',
              'path': '/top/',
              'children': [
                  {'group_name': 'lvl2',
                   'path': 'second/',
                   'children': ['signal1']},
                  ]}

    dut_node = GroupNode(nf=node_factory, renderer=renderer, parent=None, param_dict=rcdict)
    assert (dut_node.full_path == "/top/")
