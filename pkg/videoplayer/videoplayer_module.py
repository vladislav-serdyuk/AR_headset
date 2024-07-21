import typing
import time
from threading import Thread

import cv2
import numpy as np
# import numpy as np
from ffpyplayer.player import MediaPlayer


# def convert_pic_to_np(pic):
#     frame_size = pic.get_size()
#     img_frame = np.asarray(pic.to_memoryview()[0]).reshape((frame_size[1], frame_size[0], 3), order='C')
#     return cv2.cvtColor(img_frame, cv2.COLOR_RGB2BGR)


class VideoPlayer:
    def __init__(self, filename):
        self._is_stop = False
        self._is_pause = False
        self._frame: np.ndarray | None = None
        self._callback = None
        self._cap = cv2.VideoCapture(filename)
        self._player = MediaPlayer(filename)
        Thread(target=self._playing, daemon=True).start()

    def _playing(self):
        while self._cap.isOpened():
            if self._is_stop:
                break
            if self._is_pause:
                continue
            ret, frame = self._cap.read()
            if not ret:
                self._is_stop = True
                if self._callback is not None:
                    self._callback('eof', 0)
                break
            ff_frame, val = self._player.get_frame(show=False)
            if val == 'eof':
                self._is_stop = True
                if self._callback is not None:
                    self._callback('eof', 0)
                break
            pts = self._player.get_pts()
            elapsed = pts - 0.3
            play_time = self._cap.get(cv2.CAP_PROP_POS_MSEC)
            time.sleep(max(0.0, play_time/1000 - elapsed))
            self._frame = frame
        self._player.close_player()
        self._cap.release()

    def get_frame(self) -> np.ndarray:
        return self._frame

    def get_time(self):
        return self._cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

    def get_pause(self):
        return self._is_pause

    def stop(self):
        self._is_stop = True

    def pause(self):
        self._is_pause = True
        self._player.set_pause(True)

    def play(self):
        self._is_pause = False
        self._player.set_pause(False)

    def get_stop(self):
        return self._is_stop

    def set_callback(self, func: typing.Callable[[str, int], typing.Any]):
        """
        func(event, value)
        event in ['eof']
        """
        self._callback = func
