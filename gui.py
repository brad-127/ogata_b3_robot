
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

arm1=90 #0-180
arm2=90 #0-180
arm3=90 #0-180
arm4=90 #20-90
interval_=1000 #方向ボタンの反応間隔

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.title("ロボットコントローラ")     # ウィンドウタイトル
        self.master.geometry("600x600")       # ウィンドウサイズ(幅x高さ)

        #--------------------------------------------------------
        # ラベルフレーム1の作成
        padx1=40
        pady1=5
        self.labelframe1 = tk.LabelFrame(self.master, text = "アーム角度制御")
        self.arm1txt = tk.Label(self.labelframe1, text = "肩")
        self.arm2txt = tk.Label(self.labelframe1, text = "肘")
        self.arm3txt = tk.Label(self.labelframe1, text = "手首")
        self.arm4txt = tk.Label(self.labelframe1, text = "手")
        self.arm1ent = tk.Entry(self.labelframe1, width=5)
        self.arm2ent = tk.Entry(self.labelframe1, width=5)
        self.arm3ent = tk.Entry(self.labelframe1, width=5)
        self.arm4ent = tk.Entry(self.labelframe1, width=5)
        self.arm1txt.grid(row=0,column=0,padx=padx1,pady=pady1)
        self.arm2txt.grid(row=0,column=1,padx=padx1,pady=pady1)
        self.arm3txt.grid(row=0,column=2,padx=padx1,pady=pady1)
        self.arm4txt.grid(row=0,column=3,padx=padx1,pady=pady1)
        self.arm1ent.grid(row=1,column=0,padx=padx1,pady=pady1)
        self.arm2ent.grid(row=1,column=1,padx=padx1,pady=pady1)
        self.arm3ent.grid(row=1,column=2,padx=padx1,pady=pady1)
        self.arm4ent.grid(row=1,column=3,padx=padx1,pady=pady1)

        self.scale_var1 = tk.IntVar()
        scalev1 = tk.Scale( self.labelframe1, 
                    variable = self.scale_var1,
                    command = self.slider_scroll1,
                    orient=tk.VERTICAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 200,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 0,            # 最小値（開始の値）
                    to = 180,               # 最大値（終了の値）
                    resolution=1,         # 変化の分解能(初期値:1)
                    tickinterval=60,         # 目盛りの分解能(初期値0で表示なし)
                    showvalue=0
                    )
        scalev1.grid(row=2,column=0,padx=padx1,pady=pady1)

        self.scale_var2 = tk.IntVar()
        scalev2 = tk.Scale( self.labelframe1, 
                    variable = self.scale_var2,
                    command = self.slider_scroll2,
                    orient=tk.VERTICAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 200,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 0,            # 最小値（開始の値）
                    to = 180,               # 最大値（終了の値）
                    resolution=1,         # 変化の分解能(初期値:1)
                    tickinterval=60,         # 目盛りの分解能(初期値0で表示なし)
                    showvalue=0
                    )
        scalev2.grid(row=2,column=1,padx=padx1,pady=pady1)

        self.scale_var3 = tk.IntVar()
        scalev3 = tk.Scale( self.labelframe1, 
                    variable = self.scale_var3,
                    command = self.slider_scroll3,
                    orient=tk.VERTICAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 200,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 0,            # 最小値（開始の値）
                    to = 180,               # 最大値（終了の値）
                    resolution=1,         # 変化の分解能(初期値:1)
                    tickinterval=60,         # 目盛りの分解能(初期値0で表示なし)
                    showvalue=0
                    )
        scalev3.grid(row=2,column=2,padx=padx1,pady=pady1)

        self.scale_var4 = tk.IntVar()
        scalev4 = tk.Scale( self.labelframe1, 
                    variable = self.scale_var4,
                    command = self.slider_scroll4,
                    orient=tk.VERTICAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 200,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 20,            # 最小値（開始の値）
                    to = 90,               # 最大値（終了の値）
                    resolution=1,         # 変化の分解能(初期値:1)
                    tickinterval=14,         # 目盛りの分解能(初期値0で表示なし)
                    showvalue=0
                    )
        scalev4.grid(row=2,column=3,padx=padx1,pady=pady1)
        #--------------------------------------------------------------

        # ラベルの配置
        #self.labelframe1.propagate(False)
        self.labelframe1.pack(padx=20,fill=tk.BOTH)

        #--------------------------------------------------------
        # ラベルフレーム2の作成
        self.labelframe2 = tk.LabelFrame(self.master, text = "キャタピラ制御")
        #self.labelframe2.propagate(False) # 幅と高さを指定する場合はこの設定が必要

        # 方向ボタンの作成
        global interval_
        self.forward_button = tk.Button(self.labelframe2, text = "↑",font=("family",40),command=self.forward_,repeatdelay=1,repeatinterval=interval_)
        self.right_button = tk.Button(self.labelframe2, text = "→",font=("family",40),command=self.right_,repeatdelay=1,repeatinterval=interval_)
        self.left_button = tk.Button(self.labelframe2, text = "←",font=("family",40),command=self.left_,repeatdelay=1,repeatinterval=interval_)
        self.back_button = tk.Button(self.labelframe2, text = "↓",font=("family",40),command=self.back_,repeatdelay=1,repeatinterval=interval_)
        self.forward_button.grid(row=0,column=1,padx=5,pady=5)
        self.right_button.grid(row=1,column=2,padx=10,pady=5)
        self.left_button.grid(row=1,column=0,padx=10,pady=5)
        self.back_button.grid(row=1,column=1,pady=5)

        # ラベルの配置
        self.labelframe2.pack(ipady=5,side=tk.LEFT,padx=20)
        #--------------------------------------------------------

        self.set_button = tk.Button(self.master, text = "SET",font=("family",30),command=get_value)
        self.set_button.pack(pady=10,side=tk.TOP,fill=tk.X,padx=20)
        self.reset_button = tk.Button(self.master, text = "RESET",font=("family",30),command=reset_value)
        self.reset_button.pack(pady=10,side=tk.TOP,fill=tk.X,padx=20)
        self.close_button = tk.Button(self.master, text = "CLOSE",font=("family",30),command=self.master.destroy)
        self.close_button.pack(pady=10,side=tk.TOP,fill=tk.X,padx=20)
        #--------------------------------------------------------

    def slider_scroll1(self, event=None):
        '''スライダーを移動したとき'''
        global arm1
        arm1=self.scale_var1.get()
        set_entry_value()
    def slider_scroll2(self, event=None):
        global arm2
        arm2=self.scale_var2.get()
        set_entry_value()
    def slider_scroll3(self, event=None):
        global arm3
        arm3=self.scale_var3.get()
        set_entry_value()
    def slider_scroll4(self, event=None):
        global arm4
        arm4=self.scale_var4.get()
        set_entry_value()

    def forward_(self, event=None):
        print("forward")

    def right_(self, event=None):
        print("right")

    def left_(self, event=None):
        print("left")

    def back_(self, event=None):
        print("back")

def reset_value():
    #値を全てリセットする
    global arm1
    global arm2
    global arm3
    global arm4
    arm1=90
    arm2=90
    arm3=90
    arm4=90
    set_slide_value()
    set_entry_value()

def set_slide_value():
    #スライドバーの値をセットする
    app.scale_var1.set(arm1)
    app.scale_var2.set(arm2)
    app.scale_var3.set(arm3)
    app.scale_var4.set(arm4)

def set_entry_value():
    #入力欄の値をセットする
    app.arm1ent.delete(0,"end")
    app.arm1ent.insert(0,arm1)
    app.arm2ent.delete(0,"end")
    app.arm2ent.insert(0,arm2)
    app.arm3ent.delete(0,"end")
    app.arm3ent.insert(0,arm3)
    app.arm4ent.delete(0,"end")
    app.arm4ent.insert(0,arm4)

def get_value():
    #入力欄の値を読み取る
    if flg():
        global arm1
        global arm2
        global arm3
        global arm4
        arm1 = int(app.arm1ent.get())
        arm2 = int(app.arm2ent.get())
        arm3 = int(app.arm3ent.get())
        arm4 = int(app.arm4ent.get())
    set_entry_value()
    set_slide_value()

def flg():
    arm1_ = app.arm1ent.get()
    arm2_ = app.arm2ent.get()
    arm3_ = app.arm3ent.get()
    arm4_ = app.arm4ent.get()
    #数字なのか判定
    if not arm1_.isdecimal():   return False
    if not arm2_.isdecimal():   return False
    if not arm3_.isdecimal():   return False
    if not arm4_.isdecimal():   return False
    arm1_=int(arm1_)
    arm2_=int(arm2_)
    arm3_=int(arm3_)
    arm4_=int(arm4_)
    #腕の可動範囲内なのか判定
    if arm1_ < 0 or arm1_ > 180:    return False
    if arm2_ < 0 or arm2_ > 180:    return False
    if arm3_ < 0 or arm3_ > 180:    return False
    if arm4_ < 20 or arm4_ > 90:    return False
    return True

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    reset_value()
    messagebox.showinfo("使い方",
    "slider:角度制御\n"+
    "RESETボタン:全ての関節角度を初期値にリセット\n"+
    "CLOSEボタン:画面を閉じる\n"+
    "矢印ボタン:各方向にロボットが進む\n"+
    "テキストボックスに数字を入力してからSETボタンで角度指定も可")

    app.mainloop()