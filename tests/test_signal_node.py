import textwrap

from ..libretch.node_factory import NodeFactory
from ..libretch.rcfile_renderer import RCFileRenderer

def test_signal_node_basic():
    nf = NodeFactory()
    renderer = RCFileRenderer()
    dut_node = nf.new_node(parent=None, renderer=renderer, candidate="foo{_baz}", var_dict={'_baz': 'bar'})
    exp = "addSignal -h 15 foobar"
    assert ("\n".join(dut_node.render()) == exp)

def test_signal_node_dict():
    nf = NodeFactory()
    renderer = RCFileRenderer()
    cand = {
        'group_name': 'foobar',
        'type': 'signal'
    }
    dut_node = nf.new_node(parent=None, renderer=renderer, candidate=cand, var_dict={'_baz': 'bar'})
    exp = "addSignal -h 15 foobar"
    assert ("\n".join(dut_node.render()) == exp)

