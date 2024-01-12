import flet as ft
import threading
import time

def main(page: ft.Page):

    def update_time():
        start_time = time.time()
        max_time = int(minutes.value) * 60 + int(seconds.value)
        while time.time() - start_time <= max_time:
            if not running:
                break
            elapsed = time.time() - start_time
            timer_text.value = f"経過時間: {int(elapsed // 60)}分 {int(elapsed % 60)}秒"
            progress_bar.value = elapsed / max_time
            page.update()
            time.sleep(1)

        if running:
            ft.MessageBox.show(page, "時間です！", "指定の時間になりました。")

    def start_timer(e):
        global running
        running = True
        threading.Thread(target=update_time).start()

    def stop_timer(e):
        global running
        running = False

    running = False
    page.add(
        ft.Text("分:"),
        ft.TextField(id="minutes", width=50),
        ft.Text("秒:"),
        ft.TextField(id="seconds", width=50),
        ft.Progress(id="progress_bar", value=0, width=200),
        ft.Text(id="timer_text", text="経過時間: 0分 0秒"),
        ft.Row([
            ft.ElevatedButton("スタート", on_click=start_timer),
            ft.ElevatedButton("ストップ", on_click=stop_timer)
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)
