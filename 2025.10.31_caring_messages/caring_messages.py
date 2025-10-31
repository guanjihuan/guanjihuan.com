"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/47900
"""

import tkinter as tk
import random
import threading
import time

class WarmTipApp:
    def __init__(self):
        self.total_windows = 150
        self.created_count = 0
        self.windows = []
        self.root = tk.Tk()
        self.root.withdraw()
        self.lock = threading.Lock()

    def create_window(self, is_final=False):
        def _create():
            window = tk.Toplevel(self.root)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            if is_final:
                window_width, window_height = 300, 100
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
                bg = 'lightpink'
                
                frame = tk.Frame(window, bg=bg)
                frame.pack(fill='both', expand=True)
                
                tk.Label(frame, text='我想你了', bg=bg, font=('微软雅黑', 20, 'bold'),
                        fg='red').place(relx=0.5, rely=0.5, anchor='center')
                
                window.protocol("WM_DELETE_WINDOW", lambda: self.quit_app(window))
                window.title('特别提示')
            else:
                window_width, window_height = 300, 100
                x = random.randint(0, max(0, screen_width - window_width))
                y = random.randint(0, max(0, screen_height - window_height))
                
                tips = [
                    # 健康相关
                    '多喝水哦，补充水分很重要',
                    '记得按时吃饭，别饿肚子啦',
                    '久坐了要起来活动活动哦',
                    '晚上别熬夜，早点休息呀',
                    '今天也要记得吃水果呀',
                    '天气变凉了，注意添衣服',
                    '保持良好作息，身体才会棒',
                    '累了就歇一歇，别硬撑呀',
                    
                    # 情绪与心态
                    '保持微笑呀，你笑起来很好看',
                    '每天都要元气满满哦',
                    '保持好心情，好运会降临',
                    '不管怎样，好好爱自己最重要',
                    '别给自己太大压力，慢慢来',
                    '遇到不开心的事，记得跟我说',
                    '今天过得开心吗？要多笑笑呀',
                    '烦恼都会过去的，别太在意',
                    
                    # 祝福与期待
                    '愿你每天都有小确幸',
                    '梦想一定会成真的',
                    '期待下一次见面呀',
                    '祝你事事顺顺利利',
                    '愿你被世界温柔以待',
                    '今天也要加油呀，你最棒',
                    '无论在哪，都有人惦记着你',
                    '愿所有美好都如期而至',
                    
                    # 生活细节
                    '出门记得带钥匙和手机呀',
                    '雨天记得带伞，别淋湿了',
                    '开车要注意安全，慢慢来',
                    '记得给家里打个电话呀',
                    '有空多出去走走，晒晒太阳',
                    '今天也要认真生活呀',
                    '记得整理房间，心情会变好'
                ]
                bg_colors = ['lightpink', 'skyblue', 'lightgreen', 'lavender', 'lightyellow', 'plum', 'coral', 'bisque', 'aquamarine', 'mistyrose']
                
                tip = random.choice(tips)
                bg = random.choice(bg_colors)
                
                frame = tk.Frame(window, bg=bg)
                frame.pack(fill='both', expand=True)
                
                tk.Label(frame, text=tip, bg=bg, font=('微软雅黑', 16),
                        fg='black').place(relx=0.5, rely=0.5, anchor='center')
                
                window.title('温馨提示')
                self.windows.append(window)

            window.geometry(f'{window_width}x{window_height}+{x}+{y}')
            window.attributes('-topmost', True)
            
            if not is_final:
                with self.lock:
                    self.created_count += 1
                    if self.created_count == self.total_windows:
                        threading.Thread(target=self.close_all_windows, daemon=True).start()

        self.root.after(0, _create)

    def close_all_windows(self):
        time.sleep(0.5)
        for window in self.windows[:]:
            self.root.after(0, window.destroy)
            time.sleep(0.01)
        self.windows.clear()
        self.root.after(0, lambda: self.create_window(is_final=True))

    def quit_app(self, window):
        window.destroy()
        self.root.quit()

    def start(self):
        def _create_all():
            for _ in range(self.total_windows):
                self.create_window()
                time.sleep(0.1)

        threading.Thread(target=_create_all, daemon=True).start()
        self.root.mainloop()

if __name__ == "__main__":
    app = WarmTipApp()
    app.start()