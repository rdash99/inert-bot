# Logging module
import logging
# Importing subcommands
from .hug import Hug
from .bottom import Bottom
from .urbandictionary import UrbanDictionary
from .uwu import Uwu
from .xkcd import XKCD

log = logging.getLogger(__name__)


class FunCategory(Hug, Bottom, Uwu, UrbanDictionary, XKCD, name=__name__[9:]):
    """
    Full of lots of fun commands
    """

    def __init__(self, client):
        self.client = client
        Hug.__init__(self, client)
        Bottom.__init__(self, client)
        Uwu.__init__(self, client)
        UrbanDictionary.__init__(self, client)
        XKCD.__init__(self, client)


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(FunCategory(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
