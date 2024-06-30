import textwrap

from ..libretch.repeat_node import RepeatNode
from ..libretch.signal_node import SignalNode
from ..libretch.node_factory import NodeFactory
from ..libretch.rcfile_renderer import RCFileRenderer

def test_repeat_node():
    node_factory = NodeFactory()
    renderer = RCFileRenderer()

    rcdict = {'group_name': 'top',
              'path': '/top/',
              'type': 'repeat',
              'count': 3,
              'var': '_ent_id',
              'child': 'test[{_ent_id}]'}

    dut_node = node_factory.new_node(parent=None, renderer=renderer, candidate=rcdict)
    exp = textwrap.dedent("""\
    addGroup top
    addSignal -h 15 /top/test[0]
    addSignal -h 15 /top/test[1]
    addSignal -h 15 /top/test[2]
    """).strip()
    assert ("\n".join(dut_node.render()).strip() == exp)
