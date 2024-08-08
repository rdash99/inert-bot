# Logging module
import logging
# Importing subcommands
from .levels import Levels


log = logging.getLogger(__name__)


class ExpCategory(Levels, name=__name__[9:]):
    """
    Full of lots of fun commands
    """

    def __init__(self, client):
        self.client = client
        Levels.__init__(self, client)


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(ExpCategory(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
