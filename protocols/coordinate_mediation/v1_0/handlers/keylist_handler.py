"""Handler for keylist message."""
import logging

from .....messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    HandlerException,
    RequestContext,
)
from .....storage.error import StorageNotFoundError
from ..messages.keylist import Keylist
from ..models.mediation_record import MediationRecord

LOG = logging.getLogger(__name__)


class KeylistHandler(BaseHandler):
    """Handler for keylist message."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """Handle keylist message."""
        self._logger.debug(
            "%s called with context %s", self.__class__.__name__, context
        )
        assert isinstance(context.message, Keylist)

        if not context.connection_ready:
            raise HandlerException("Received keylist message from inactive connection")

        session = await context.session()
        try:
            await MediationRecord.retrieve_by_connection_id(
                session, context.connection_record.connection_id
            )
        except StorageNotFoundError as err:
            LOG.warning(
                "Received keylist from connection that is not acting as mediator: %s",
                err,
            )
            return

        # TODO verify our keylist matches?
        LOG.info("Keylist received: %s", context.message)
