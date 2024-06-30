#!/bin/sh
"exec" "$(dirname $(readlink -f $0))/venv/bin/python3" "$0" "$@"

import argparse
import yaml
from pprint import pprint as pp
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')

from libretch import *
from libretch.node_factory import NodeFactory

def main(args):
    y = yaml.safe_load(args.rc_config)
    assert('duts' in y)
    assert(args.dut in y['duts'])
    td = y['duts'][args.dut]

    node_factory = NodeFactory()
    dut_node = GroupNode(nf=node_factory, parent=None, param_dict=td)
    print("\n".join(dut_node.render()))

if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='retch', description='RC file generator')
    parser.add_argument('rc_config', type=argparse.FileType('r'), help='YAML RC spec')
    parser.add_argument('-d', '--dut', type=str, default='core', help='DUT to build from RC spec')
    args = parser.parse_args()
    main(args)

