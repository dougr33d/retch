import textwrap

from ..libretch.node_factory import NodeFactory
from ..libretch.gtkw_renderer import GTKWaveRenderer

def test_group_node():
    rcdict = {'group_name': 'top',
              'path': '/top/',
              'children': [
                  {'group_name': 'lvl2_{_foo}',
                   'path': 'second/',
                   'children': ['signal1']},
                  ]}

    nf = NodeFactory()
    renderer = GTKWaveRenderer()
    dut_node = nf.new_node(parent=None, renderer=renderer, candidate=rcdict, var_dict={'_foo': 'bar'})
    exp = textwrap.dedent("""\
    @800200
    -top
    @800200
    -lvl2_bar
    @22
    top.second.signal1
    @1000200
    -lvl2_bar
    @1000200
    -top
    """).strip()
    assert ("\n".join(dut_node.render()) == exp)
