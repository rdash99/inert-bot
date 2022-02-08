# Logging module
import logging
# Importing subcommands
from .pfp import Pfp
from .recolor import Recolor
from .ping import Ping
from .help import Help

log = logging.getLogger(__name__)


class MiscCategory(Pfp, Recolor, Ping, Help, name=__name__[9:]):
    """
    Misc commands
    """

    def __init__(self, client):
        self.client = client
        Pfp.__init__(self, client)
        Recolor.__init__(self, client)
        Ping.__init__(self, client)
        Help.__init__(self, client)


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(MiscCategory(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
