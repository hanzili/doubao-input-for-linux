"""麦克风统计回归与关闭面板后仍可重新打开。"""
import unittest
from unittest.mock import MagicMock, patch

from doubao_input.app import DoubaoInputApp
from doubao_input.ui.control_window import ControlWindow


class BackgroundTests(unittest.TestCase):
    def test_microphone_test_callback_survives_start_wrapper(self):
        app = DoubaoInputApp()
        capture = MagicMock()
        capture._on_rms = None
        with patch('doubao_input.app.Overlay'), \
             patch('doubao_input.app.Injector'), \
             patch('doubao_input.app.TranscriptionManager'), \
             patch('doubao_input.app.ControlWindow'), \
             patch('doubao_input.app.EvdevPtt'), \
             patch('doubao_input.app.start_tray'), \
             patch('doubao_input.doubao.audio_capture.AudioCapture', return_value=capture):
            app._build()
        received = []
        callback = received.append
        capture._on_rms = callback
        capture.start(lambda _data: None)
        capture._on_rms(0.25)
        self.assertEqual(received, [0.25])
        capture._on_rms = None
        capture.start(lambda _data: None)
        self.assertEqual(capture._on_rms, app._overlay.push_rms)

    def test_close_hides_and_reopen_keeps_same_window(self):
        control = ControlWindow(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        window = MagicMock()
        control._window = window
        self.assertTrue(control._on_close_request(window))
        window.set_visible.assert_called_once_with(False)
        window.destroy.assert_not_called()
        control.show()
        window.present.assert_called_once()
        self.assertIs(control._window, window)


if __name__ == '__main__':
    unittest.main()
