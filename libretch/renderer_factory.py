from typing import Any
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')
 
from .renderers.abstract_renderer import AbstractRenderer
from .renderers.rcfile_renderer import RCFileRenderer
from .renderers.gtkw_renderer import GTKWaveRenderer

class RendererFactory:
    def __init__(self):
        self._renderers = []
        self._renderers.append(RCFileRenderer)
        self._renderers.append(GTKWaveRenderer)

    def register_node_type(self, nt):
        self._renderers.append(nt)

    def new_renderer(self, format: str) -> AbstractRenderer:
        mats = [renderer for renderer in self._renderers if renderer.format == format]
        if len(mats) == 0:
            logger.error("Could not find suitable RendererType!")
            logger.error(self._renderers)
            exit(-1)
        elif len(mats) > 1:
            logger.error("Found multiple matching RendererTypes!")
            exit(-1)
        else:
            renderer = mats[0]
            return renderer()

