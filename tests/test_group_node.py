import textwrap

from ..libretch.node_factory import NodeFactory
from ..libretch.rcfile_renderer import RCFileRenderer

def test_group_node():
    rcdict = {'group_name': 'top',
              'path': '/top/',
              'children': [
                  {'group_name': 'lvl2_{_foo}',
                   'path': 'second/',
                   'children': ['signal1']},
                  ]}

    nf = NodeFactory()
    renderer = RCFileRenderer()
    dut_node = nf.new_node(parent=None, renderer=renderer, candidate=rcdict, var_dict={'_foo': 'bar'})
    exp = textwrap.dedent("""\
    addGroup top
    addSubGroup lvl2_bar
    addSignal -h 15 /top/second/signal1
    endSubGroup lvl2_bar\
    """).strip()
    assert ("\n".join(dut_node.render()) == exp)
