from asynctest import (
    mock as async_mock,
    TestCase as AsyncTestCase,
)

from ......messaging.request_context import RequestContext
from ......messaging.responder import MockResponder
from ......transport.inbound.receipt import MessageReceipt

from ...messages.cred_offer import V20CredOffer

from .. import cred_offer_handler as test_module


class TestV20CredOfferHandler(AsyncTestCase):
    async def test_called(self):
        request_context = RequestContext.test_context()
        request_context.message_receipt = MessageReceipt()
        request_context.settings["debug.auto_respond_credential_offer"] = False
        request_context.connection_record = async_mock.MagicMock()

        with async_mock.patch.object(
                test_module, "V20CredManager", autospec=True
        ) as mock_cred_mgr:
            mock_cred_mgr.return_value.receive_offer = async_mock.CoroutineMock()
            request_context.message = V20CredOffer()
            request_context.connection_ready = True
            handler_inst = test_module.V20CredOfferHandler()
            responder = MockResponder()
            await handler_inst.handle(request_context, responder)

        mock_cred_mgr.assert_called_once_with(request_context.profile)
        mock_cred_mgr.return_value.receive_offer.assert_called_once_with(
            request_context.message, request_context.connection_record.connection_id
        )
        assert not responder.messages

    async def test_called_auto_request(self):
        request_context = RequestContext.test_context()
        request_context.message_receipt = MessageReceipt()
        request_context.settings["debug.auto_respond_credential_offer"] = True
        request_context.connection_record = async_mock.MagicMock()
        request_context.connection_record.my_did = "dummy"

        with async_mock.patch.object(
                test_module, "V20CredManager", autospec=True
        ) as mock_cred_mgr:
            mock_cred_mgr.return_value.receive_offer = async_mock.CoroutineMock()
            mock_cred_mgr.return_value.create_request = async_mock.CoroutineMock(
                return_value=(None, "cred_request_message")
            )
            request_context.message = V20CredOffer()
            request_context.connection_ready = True
            handler_inst = test_module.V20CredOfferHandler()
            responder = MockResponder()
            await handler_inst.handle(request_context, responder)

        mock_cred_mgr.assert_called_once_with(request_context.profile)
        mock_cred_mgr.return_value.receive_offer.assert_called_once_with(
            request_context.message, request_context.connection_record.connection_id
        )
        messages = responder.messages
        assert len(messages) == 1
        (result, target) = messages[0]
        assert result == "cred_request_message"
        assert target == {}

    async def test_called_not_ready(self):
        request_context = RequestContext.test_context()
        request_context.message_receipt = MessageReceipt()
        request_context.connection_record = async_mock.MagicMock()

        with async_mock.patch.object(
                test_module, "V20CredManager", autospec=True
        ) as mock_cred_mgr:
            mock_cred_mgr.return_value.receive_offer = async_mock.CoroutineMock()
            request_context.message = V20CredOffer()
            request_context.connection_ready = False
            handler_inst = test_module.V20CredOfferHandler()
            responder = MockResponder()
            with self.assertRaises(test_module.HandlerException):
                await handler_inst.handle(request_context, responder)

        assert not responder.messages
