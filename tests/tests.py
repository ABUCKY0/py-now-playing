import unittest
import asynctest
from unittest.mock import MagicMock, patch
from py_now_playing import NowPlaying  # replace 'your_module' with the name of the module that contains the NowPlaying class

class TestNowPlaying(asynctest.TestCase):
    def setUp(self):
        self.now_playing = NowPlaying()

    @asynctest.patch('your_module.MediaManager.request_async')
    async def test_initalize_mediamanger(self, mock_request_async):
        mock_request_async.return_value = 'mock manager'
        await self.now_playing.initalize_mediamanger()
        self.assertEqual(self.now_playing._manager, 'mock manager')

    async def test_get_sessions(self):
        self.now_playing._manager = MagicMock()
        self.now_playing._manager.get_sessions.return_value = ['session1', 'session2']
        sessions = await self.now_playing._get_sessions()
        self.assertEqual(sessions, ['session1', 'session2'])

    @asynctest.patch('your_module.subprocess.check_output')
    @asynctest.patch('your_module.json.loads')
    async def test_get_active_app_user_model_ids(self, mock_loads, mock_check_output):
        mock_check_output.return_value = 'mock output'
        mock_loads.return_value = ['app1', 'app2']
        self.now_playing._get_app_user_model_ids = asynctest.CoroutineMock()
        self.now_playing._get_app_user_model_ids.return_value = ['app2']
        active_app_ids = await self.now_playing.get_active_app_user_model_ids()
        self.assertEqual(active_app_ids, ['app2'])

if __name__ == '__main__':
    asynctest.main()