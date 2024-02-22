# 設計: https://sizu.me/koromaru/posts/km8stwou1zss

import math
import time
from datetime import datetime, timedelta
from threading import Event, Thread
from typing import Tuple, Union


class CountDownTimer:
    """タイマークラス"""

    def __init__(self):
        self.start_time: Union[None, datetime] = None
        self.stop_event: Event = Event()
        self.remaining_time: int = 0

    def start(self, e) -> None:
        """タイマーのスタート"""
        if self.start_time is None:
            self.start_time = datetime.now()
            self.stop_event.clear()
            self.thread: Thread = Thread(target=self._run)
            self.thread.start()

    def stop(self, e) -> None:
        """タイマーの停止"""
        if self.start_time is not None:
            self.stop_event.set()
            self.thread.join()
            self.remaining_time -= math.floor(
                (datetime.now() - self.start_time).total_seconds()
            )
            self.start_time = None

    def _run(self) -> None:
        """タイマーの動作を実行"""
        count = self.remaining_time
        if self.stop_event.is_set():
            count = self.remaining_time
        while not self.stop_event.is_set():
            print(
                f"Elapsed Time: {self.get_remaining_time()[0]}:{self.get_remaining_time()[1]} seconds"
            )
            if count == 0:
                self.start_time = None
                break
            time.sleep(1)
            count -= 1

    def reset(self, e) -> None:
        """タイマーをリセット"""
        self.stop(e)
        self.set_timer(minutes=0, seconds=0)

    # setter
    def set_timer(self, minutes: int, seconds: int) -> None:
        """
        タイマーの秒数設定を初期化

        :param minutes: 分
        :param seconds: 秒
        """
        self.seconds: int = seconds
        self.minutes: int = minutes
        self.remaining_time = self.seconds + self.minutes * 60  # 秒数

    # getter
    def _get_datetime_date(self, time: datetime) -> Tuple[int, int, int]:
        """datetimeオブジェクトの時間、分、秒を取得"""
        return time.hour, time.minute, time.second

    def get_estimated_time(self) -> Tuple[int, int, int]:
        """タイマーの終了時刻を返す"""
        if self.start_time is None:
            return 00, 00, 00
        else:
            # datetime + timedeltaは、新しいdatetimeオブジェクトを返す
            end_time = self.start_time + timedelta(seconds=self.remaining_time)
            return self._get_datetime_date(end_time)

    def get_remaining_time(self) -> Tuple[int, int]:
        """タイマーの残り時間を返す"""
        if self.start_time is None:
            # raise ValueError('タイマーがスタートしていません')
            return 00, 00
        else:
            time = math.ceil(
                self.remaining_time - (datetime.now() - self.start_time).total_seconds()
            )
            return divmod(time, 60)


if __name__ == "__main__":
    timer = CountDownTimer()
    timer.set_timer(0, 5)
    timer.start()
    print(timer.get_estimated_time())
    time.sleep(5)
    timer.stop()
