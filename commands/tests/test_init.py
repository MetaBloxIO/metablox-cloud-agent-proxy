from asynctest import TestCase as AsyncTestCase
from asynctest import mock as async_mock

from ... import commands as test_module


class TestInit(AsyncTestCase):
    def test_available(self):
        avail = test_module.available_commands()
        assert len(avail) == 3

    def test_run(self):
        with async_mock.patch.object(
                test_module, "load_command", async_mock.MagicMock()
        ) as mock_load:
            mock_module = async_mock.MagicMock()
            mock_module.execute = async_mock.MagicMock()
            mock_load.return_value = mock_module

            test_module.run_command("hello", ["world"])
            mock_load.assert_called_once()
            mock_module.execute.assert_called_once()
