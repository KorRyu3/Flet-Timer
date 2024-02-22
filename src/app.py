import time
from datetime import datetime
from logging import Formatter, StreamHandler, getLogger
from threading import Thread

import flet as ft
from flet import (
    AlertDialog,
    Column,
    ElevatedButton,
    Page,
    Ref,
    Row,
    Text,
    TextField,
)

from count_down_timer import CountDownTimer

# logの設定
logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter("[%(levelname)s] %(asctime)s  %(message)s"))
logger.setLevel("INFO")
handler.setLevel("INFO")
logger.addHandler(handler)


def main(page: Page) -> None:
    # windowの設定
    page.title = "Count Down Timer"
    page.window_width = 400  # 幅
    page.window_height = 400  # 高さ
    page.window_maximizable = False  # 最大化ボタン
    page.window_resizable = False  # サイズ変更不可
    page.on_error = lambda e: logger.error(f"Page error: {e.data}")  # エラー時の処理
    page.window_center()
    page.update()
    page.fonts = {
        "NotoSansJP-Medium": "fonts/Noto_Sans_JP/NotoSansJP-Medium.ttf",
        "IBMPlexSerif-SemiBold": "fonts/IBM_Plex_Serif/IBMPlexSerif-SemiBold.ttf",
    }

    class FletTimer(CountDownTimer):
        """自作のタイマークラスをFletで使えるようにしたクラス"""

        def _update_remaining_time(self) -> None:
            minutes, seconds = self.get_remaining_time()
            if minutes < 10:
                minutes = f"0{minutes}"
            if seconds < 10:
                seconds = f"0{seconds}"
            remaining_time.current.value = f"{minutes}:{seconds}"  # 00:00表記
            remaining_time.current.update()

        def start(self, e) -> None:
            """タイマーのスタート"""
            logger.info("start")
            # any:""
            if input_min.current.value != "" and input_sec.current.value == "":
                input_sec.current.value = "0"
            # "":any
            if input_min.current.value == "" and input_sec.current.value != "":
                input_min.current.value = "0"
            page.update()
            # "":""
            if input_min.current.value == "" or input_sec.current.value == "":
                self._set_error_message("分と秒の両方を入力してください")
                return
            # 00:00
            if int(input_min.current.value) == 0 and int(input_sec.current.value) == 0:
                self._set_error_message("0分0秒は入力できません")
                return
            # 時間がセットされていなかったら
            if self.remaining_time == 0:
                # 入力の判定
                if (
                    int(input_min.current.value) > 59
                    or int(input_sec.current.value) > 59
                ):
                    self._set_error_message("60分, 60秒以上は入力できません")
                    input_min.current.value = "0"
                    input_sec.current.value = ""
                    input_sec.current.focus()
                    page.update()
                    return
                # タイマーをセット
                self.set_timer(
                    int(input_min.current.value), int(input_sec.current.value)
                )
                row_remaining_time.current.height = 160
                user_input.current.visible = False

            # タイマーがスタートしていなかったら
            if self.start_time is None:
                # ボタンの入力を受け付けない
                start_btn.current.disabled = True
                stop_btn.current.disabled = False
                reset_btn.current.disabled = False
                # エラーメッセージを非表示
                error_message.current.visible = False
                self.start_time = datetime.now()
                self.stop_event.clear()
                self.thread: Thread = Thread(target=self._run)
                self.thread.start()
            else:
                self._set_error_message("もう一度startボタンを押してください")
                start_btn.current.focus()

            end_time.current.visible = True
            # 終了時刻の更新
            for i, time_value in enumerate([end_hour, end_min, end_sec]):
                time_value.current.value = str(self.get_estimated_time()[i])
                if int(time_value.current.value) < 10:
                    # 00:00表記
                    time_value.current.value = f"0{time_value.current.value}"
            page.update()

        def stop(self, e) -> None:
            logger.info("stop")
            if self.start_time is None:
                self._set_error_message("タイマーがスタートしていません")
            else:
                start_btn.current.disabled = False
                stop_btn.current.disabled = True
            page.update()
            try:
                super().stop(e)
            except TypeError:
                self._set_error_message("もう一度stopボタンを押してください")
                start_btn.current.focus()

        def _run(self) -> None:
            """タイマーの動作を実行"""
            count = self.remaining_time
            if self.stop_event.is_set():
                count = self.remaining_time
            while not self.stop_event.is_set():
                self._update_remaining_time()
                if count <= 0:
                    self.start_time = None
                    self._open_dlg()
                    break
                time.sleep(1)
                count -= 1

        def reset(self, e) -> None:
            self.stop(e)
            logger.info("reset")
            self.set_timer(minutes=0, seconds=0)
            remaining_time.current.value = "00:00"

            end_time.current.visible = False
            user_input.current.visible = True
            error_message.current.visible = False

            start_btn.current.disabled = False
            stop_btn.current.disabled = True
            reset_btn.current.disabled = True

            row_remaining_time.current.height = 140
            # update
            page.update()

            input_sec.current.focus()

        def _open_dlg(self):
            page.dialog = ft.AlertDialog(
                ref=end_dlg,
                title=ft.Text("タイマーが終了しました。\nお疲れさまでした！", size=20),
                on_dismiss=timer.reset,
            )
            end_dlg.current.open = True
            page.update()

        def _set_error_message(self, message):
            error_message.current.value = message
            error_message.current.visible = True
            error_message.current.update()
            logger.error(message)

    # ----------------------Fletのメインプログラム-----------------------------

    timer = FletTimer()

    common_font = "NotoSansJP-Medium"
    num_font = "IBMPlexSerif-SemiBold"

    end_hour = Ref[Text]()
    end_min = Ref[Text]()
    end_sec = Ref[Text]()
    end_time = Ref[Row]()
    end_dlg = Ref[AlertDialog]()

    remaining_time = Ref[Text]()
    row_remaining_time = Ref[Row]()

    btn_padding = 40
    start_btn = Ref[ElevatedButton]()
    stop_btn = Ref[ElevatedButton]()
    reset_btn = Ref[ElevatedButton]()
    count_down_btns = Ref[Row]()

    input_width = 75
    input_height = 75
    input_min = Ref[TextField]()
    input_sec = Ref[TextField]()
    user_input = Ref[Row]()

    error_message = Ref[Text]()

    # アプリの配置
    page.add(
        Column(
            controls=[
                Row(
                    ref=end_time,
                    controls=[
                        Text("終了時刻: ", size=20, font_family=common_font),
                        Text(
                            ref=end_hour, value="00", size=20, font_family=common_font
                        ),
                        Text(":", size=20, font_family=common_font),
                        Text(ref=end_min, value="00", size=20, font_family=common_font),
                        Text(":", size=20, font_family=common_font),
                        Text(ref=end_sec, value="00", size=20, font_family=common_font),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    visible=False,
                    height=70,
                    spacing=3,
                ),
                Row(
                    ref=row_remaining_time,
                    controls=[
                        Text(
                            ref=remaining_time,
                            value="00:00",
                            size=100,
                            font_family=num_font,
                        ),
                    ],
                    height=140,
                    # 中央揃え
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.END,
        ),
        Column(
            controls=[
                Row(
                    ref=count_down_btns,
                    controls=[
                        ElevatedButton(
                            ref=start_btn,
                            text="Start",
                            on_click=timer.start,
                            style=ft.ButtonStyle(
                                shape=ft.CircleBorder(), padding=btn_padding
                            ),
                        ),
                        ElevatedButton(
                            ref=stop_btn,
                            text="Stop",
                            on_click=timer.stop,
                            style=ft.ButtonStyle(
                                shape=ft.CircleBorder(), padding=btn_padding
                            ),
                            disabled=True,
                        ),
                        ElevatedButton(
                            ref=reset_btn,
                            text="Reset",
                            on_click=timer.reset,
                            style=ft.ButtonStyle(
                                shape=ft.CircleBorder(), padding=btn_padding
                            ),
                            disabled=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                Row(
                    ref=user_input,
                    controls=[
                        Text(
                            "入力: ",
                            size=20,
                            width=input_width,
                            height=50,
                            font_family=common_font,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        TextField(
                            ref=input_min,
                            label="分",
                            hint_text="0",
                            width=input_width,
                            height=input_height,
                            input_filter=ft.NumbersOnlyInputFilter(),
                            on_submit=timer.start,
                        ),
                        Text(
                            ":",
                            size=20,
                            width=20,
                            height=50,
                            font_family=common_font,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        TextField(
                            ref=input_sec,
                            label="秒",
                            hint_text="0",
                            width=input_width,
                            height=input_height,
                            input_filter=ft.NumbersOnlyInputFilter(),
                            on_submit=timer.start,
                            autofocus=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    # 非表示
                    visible=True,
                ),
            ],
            spacing=20,
        ),
        Text(ref=error_message, visible=False, size=15, color=ft.colors.ERROR),
    )


if __name__ == "__main__":
    ft.app(target=main)
