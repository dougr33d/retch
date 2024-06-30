import pytest

from ..libretch.group_node import GroupNode
from ..libretch.signal_node import SignalNode
from ..libretch.node_factory import NodeFactory

def test_node_path():
    node_factory = NodeFactory()
    node_factory.register_node_type(GroupNode)
    node_factory.register_node_type(SignalNode)

    rcdict = {'group_name': 'top',
              'path': '/top/',
              'children': [
                  {'group_name': 'lvl2',
                   'path': 'second/',
                   'children': ['signal1']},
                  ]}

    dut_node = GroupNode(nf=node_factory, parent=None, param_dict=rcdict)
    assert (dut_node.full_path == "/top/")
