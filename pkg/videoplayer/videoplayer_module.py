import cv2
import numpy as np
import time
from ffpyplayer.player import MediaPlayer
from threading import Thread

#
# def convert_pic_to_np(pic):
#     frame_size = pic.get_size()
#     img_frame = np.asarray(pic.to_memoryview()[0]).reshape((frame_size[1], frame_size[0], 3), order='C')
#     return cv2.cvtColor(img_frame, cv2.COLOR_RGB2BGR)


class VideoPlayer:
    def __init__(self, filename):
        self._is_pause = False
        self._frame = None
        self._cap = cv2.VideoCapture(filename)
        self._player = MediaPlayer(filename)
        self._start_time = time.time()
        Thread(target=self._playing, daemon=True).start()

    def _playing(self):
        while self._cap.isOpened():
            if self._is_pause:
                continue
            ret, frame = self._cap.read()
            if not ret:
                break
            ff_frame, val = self._player.get_frame(show=False)
            if val == 'eof':
                break
            # if ff_frame is None:
            #     continue
            # img, t = ff_frame
            # pts = self._player.get_pts()
            # new_frame = convert_pic_to_np(img)
            # time.sleep(max(0.0, t - pts))
            # self._frame = new_frame
            # print(img, t, val)
            # cv2.imshow('video', pl.get_frame())
            # cv2.waitKey(max(1, int(val * 1000)))

            # elapsed = (time.time() - self._start_time) * 1000  # msec
            elapsed = time.time() - self._start_time
            # elapsed = pts
            # time.sleep(max(0, t - elapsed))
            play_time = self._cap.get(cv2.CAP_PROP_POS_MSEC)
            # sleep = max(1, int(play_time - elapsed))
            # if cv2.waitKey(sleep) & 0xFF == ord("q"):
            #     break
            time.sleep(max(0.0, play_time/1000 - elapsed))
            self._frame = frame
            # print(val)
        self.stop()

    def get_frame(self):
        return self._frame

    def get_time(self):
        return self._cap.get(cv2.CAP_PROP_POS_MSEC)

    def get_pause(self):
        return self._is_pause

    def stop(self):
        self._player.close_player()
        self._cap.release()

    def pause(self):
        self._is_pause = True
        self._player.set_pause(True)

    def play(self):
        self._is_pause = False
        self._start_time = time.time() - self._cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        self._player.set_pause(False)
        # self._start_time = time.time() - self._player.get_pts()
