# Logging module
import logging
# Importing subcommands
from .setprefix import SetPrefix
from .role import Role
from .kick import Kick
from .ban import Ban

log = logging.getLogger(__name__)


class AdminCategory(SetPrefix, Role, Kick, Ban, name=__name__[9:]):
    """
    Administration commands
    """

    def __init__(self, client):
        self.client = client
        SetPrefix.__init__(self, client)
        Role.__init__(self, client)
        Kick.__init__(self, client)
        Ban.__init__(self, client)


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(AdminCategory(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')

5