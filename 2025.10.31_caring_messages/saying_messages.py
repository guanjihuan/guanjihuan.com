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
                window_width, window_height = 350, 150
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
                bg = 'lightpink'
                
                frame = tk.Frame(window, bg=bg)
                frame.pack(fill='both', expand=True)
                
                tk.Label(frame, text='人民万岁！', bg=bg, font=('微软雅黑', 28, 'bold'),
                        fg='red').place(relx=0.5, rely=0.5, anchor='center')
                
                window.protocol("WM_DELETE_WINDOW", lambda: self.quit_app(window))
                window.title('人民万岁')
            else:
                window_width, window_height = 350, 150
                x = random.randint(0, max(0, screen_width - window_width))
                y = random.randint(0, max(0, screen_height - window_height))
                
                # 毛主席语录
                quotes = [
                    # 革命与斗争
                    "枪杆子里面出政权。",
                    "星星之火，可以燎原。",
                    "下定决心，不怕牺牲，排除万难，去争取胜利。",
                    "人不犯我，我不犯人；人若犯我，我必犯人。",
                    "一切反动派都是纸老虎。",
                    "宜将剩勇追穷寇，不可沽名学霸王。",

                    # 政治与领导
                    "我们的原则是党指挥枪，而决不容许枪指挥党。",
                    "谁是我们的敌人？谁是我们的朋友？这个问题是革命的首要问题。",
                    "统一战线，武装斗争，党的建设，是中国共产党在中国革命中战胜敌人的三个法宝。",
                    "政策和策略是党的生命，各级领导同志务必充分注意，万万不可粗心大意。",
                    "我们应该谦虚、谨慎、戒骄、戒躁，全心全意地为中国人民服务。",

                    # 军事与战略
                    "敌进我退，敌驻我扰，敌疲我打，敌退我追。",
                    "打得赢就打，打不赢就走。",
                    "战争的伟力之最深厚的根源，存在于民众之中。",
                    "集中优势兵力，各个歼灭敌人。",
                    "伤其十指，不如断其一指。",
                    "兵民是胜利之本。",
                    "战略上藐视敌人，战术上重视敌人。",

                    # 思想与方法
                    "没有调查，就没有发言权。",
                    "实践、认识、再实践、再认识，这种形式，循环往复以至无穷，而实践和认识之每一循环的内容，都比较地进到了高一级的程度。",
                    "矛盾存在于一切事物的发展过程中；每一事物的发展过程中存在着自始至终的矛盾运动。",
                    "马克思主义的哲学认为十分重要的问题，不在于懂得了客观世界的规律性，因而能够解释世界，而在于拿了这种对于客观规律性的认识去能动地改造世界。",
                    "世上无难事，只要肯登攀。",
                    "人的正确思想，只能从社会实践中来，只能从社会的生产斗争、阶级斗争和科学实验这三项实践中来。",
                    "一切结论产生于调查情况的末尾，而不是在它的先头。",
                    "知识的问题是一个科学问题，来不得半点的虚伪和骄傲，决定地需要的倒是其反面——诚实和谦逊的态度。",

                    # 群众与服务
                    "为人民服务。",
                    "军民团结如一人，试看天下谁能敌。",
                    "我们共产党人好比种子，人民好比土地。我们到了一个地方，就要同那里的人民结合起来，在人民中间生根、开花。",
                    "人民，只有人民，才是创造世界历史的动力。",

                    # 文化与教育
                    "古为今用，洋为中用。",
                    "百花齐放，百家争鸣。",
                    "好好学习，天天向上。",

                    # 经济与建设
                    "自己动手，丰衣足食。",
                    "只有社会主义能够救中国。",

                    # 青年与未来
                    "世界是你们的，也是我们的，但是归根结底是你们的。你们青年人朝气蓬勃，正在兴旺时期，好像早晨八九点钟的太阳。希望寄托在你们身上。",
                    "自信人生二百年，会当水击三千里。",

                    # 哲理与励志
                    "不管风吹浪打，胜似闲庭信步。",
                    "要想不经过艰难曲折，不付出极大努力，总是一帆风顺，容易得到成功，这种想法，只是幻想。",
                    "读书是学习，使用也是学习，而且是更重要的学习。",
                    "我们的同志在困难的时候，要看到成绩，要看到光明，要提高我们的勇气。",
                    "错误和挫折教训了我们，使我们比较地聪明起来了，我们的事情就会办得好一些。"
                ]
                bg_colors = ['lightyellow', 'lightblue', 'lightgreen', 'lavender', 'mistyrose', 'bisque', 'aquamarine']
                
                tip = random.choice(quotes)
                bg = random.choice(bg_colors)
                
                frame = tk.Frame(window, bg=bg)
                frame.pack(fill='both', expand=True)
                
                tk.Label(frame, text=tip, bg=bg, font=('微软雅黑', 14),
                        fg='black', wraplength=320, justify='center').place(relx=0.5, rely=0.5, anchor='center')
                
                window.title('毛主席语录')
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