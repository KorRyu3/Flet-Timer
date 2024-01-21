import time
from datetime import datetime
from threading import Thread

import flet as ft
from flet import Page, Text, ElevatedButton, TextField, Row, Column, Container
from count_down_timer import CountDownTimer

def main(page: Page):

    class FletTimer(CountDownTimer):
        """自作のタイマークラスをFletで使えるようにしたクラス"""
        def _update_remaining_time(self):
            minutes, seconds = self.get_remaining_time()
            if minutes < 10:
                minutes = f"0{minutes}"
            if seconds < 10:
                seconds = f"0{seconds}"
            remaining_time.value = f"{minutes}:{seconds}"
            remaining_time.update()

        def start(self, e) -> None:
            """タイマーのスタート"""
            # any:""
            if input_min.value != "" and input_sec.value == "":
                input_sec.value = "0"
            # "":any
            if input_min.value == "" and input_sec.value != "":
                input_min.value = "0"
            # "": ""
            if input_min.value == "" or input_sec.value == "":
                error_message.value = "分と秒の両方を入力してください"
                error_message.visible = True
                error_message.update()
                return
            # 0:0
            if int(input_min.value) == 0 and int(input_sec.value) == 0:
                error_message.value = "0分0秒は入力できません"
                error_message.visible = True
                error_message.update()
                return
            if self.remaining_time == 0:
                self.set_timer(int(input_min.value), int(input_sec.value))
                user_input.visible = False
            if self.start_time is None:
                start_btn.disabled = True
                stop_btn.disabled = False
                reset_btn.disabled = False
                error_message.visible = False
                self.start_time = datetime.now()
                self.stop_event.clear()
                self.thread: Thread = Thread(target=self._run)
                self.thread.start()
            else:
                error_message.value = "もう一度startボタンを押してください"
                error_message.visible = True

            end_time.visible = True
            for i, time in enumerate([end_hour, end_min, end_sec]):
                time.value = str(self.get_estimated_time()[i])
                if int(time.value) < 10:
                    time.value = f"0{time.value}"
            page.update()

        def stop(self, e) -> None:
            if self.start_time is None:
                error_message.value = "タイマーがスタートしていません"
                error_message.visible = True
            else:
                start_btn.disabled = False
                stop_btn.disabled = True
            page.update()
            try:
                super().stop(e)
            except TypeError:
                error_message.value = "もう一度stopボタンを押してください"
                error_message.visible = True
                error_message.update()

        def _run(self) -> None:
            """タイマーの動作を実行"""
            count = self.remaining_time
            if self.stop_event.is_set():
                count = self.remaining_time
            while not self.stop_event.is_set():
                self._update_remaining_time()
                print(count)
                if count == 0:
                    self.start_time = None
                    self._open_dlg()
                    break
                time.sleep(1)
                count -= 1

        def reset(self, e) -> None:
            self.stop(e)
            self.set_timer(minutes=0, seconds=0)
            remaining_time.value = "00:00"
            end_time.visible = False
            user_input.visible = True
            error_message.visible = False

            start_btn.disabled = False
            stop_btn.disabled = True
            reset_btn.disabled = True
            # update
            page.update()

            input_sec.focus()

        def _open_dlg(self):
            page.dialog = end_dlg
            end_dlg.open = True
            page.update()

    # Fletのメインプログラム---------------------------------------------------

    timer = FletTimer()

    page.title = "Count Down Timer"


    end_dlg = ft.AlertDialog(title=ft.Text("タイマーが終了しました。お疲れさまでした！", size=20), on_dismiss=timer.reset)

    end_hour = Text(value="00", size=20)
    end_min = Text(value="00", size=20)
    end_sec = Text(value="00", size=20)
    end_time = Row(
        controls=[
            Text("終了時刻: ", size=20),
            end_hour,
            Text(":", size=20),
            end_min,
            Text(":", size=20),
            end_sec,
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    end_time.visible = False

    remaining_time = Text(value="00:00", size=50)

    input_width = 75
    input_height = 100
    input_min = TextField(
        label="分",
        hint_text="0",
        width=input_width,
        height=input_height,
        input_filter=ft.NumbersOnlyInputFilter(),
        max_length=2,
        on_submit=timer.start,
    )
    input_sec = TextField(
        label="秒",
        hint_text="0",
        width=input_width,
        height=input_height,
        input_filter=ft.NumbersOnlyInputFilter(),
        max_length=2,
        on_submit=timer.start,
        autofocus=True,
    )
    user_input = Row(
        controls=[
            Text("入力: ", size=20, width=input_width, height=75, text_align=ft.TextAlign.CENTER),
            input_min,
            Text(":", size=20, width=20, height=75, text_align=ft.TextAlign.CENTER),
            input_sec,
        ],
        height=200,
        alignment=ft.MainAxisAlignment.CENTER,
        # 非表示
        visible=True
    )

    btn_padding = 50
    start_btn = ElevatedButton("Start", on_click=timer.start, style=ft.ButtonStyle(
        shape=ft.CircleBorder(), padding=btn_padding
    ))
    stop_btn = ElevatedButton("Stop", on_click=timer.stop, disabled=True, style=ft.ButtonStyle(
        shape=ft.CircleBorder(), padding=btn_padding
    ))
    reset_btn = ElevatedButton("Reset", on_click=timer.reset, disabled=True, style=ft.ButtonStyle(
        shape=ft.CircleBorder(), padding=btn_padding
    ))
    count_down_btns = Row(
        controls=[
            start_btn,
            stop_btn,
            reset_btn,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    error_message = Text()



    page.add(
        end_time,
        Row(
            controls=[
                remaining_time
            ],
            height=100,
            # 中央揃え
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        count_down_btns,
        user_input,
        error_message
    )

if __name__ == "__main__":
    ft.app(target=main)
