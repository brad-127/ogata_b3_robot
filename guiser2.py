from doctest import master
import tkinter as tk
import tkinter.font as tkFont
from turtle import forward
from tkinter import messagebox

import serial
import time
import threading
inkey=''
ser = serial.Serial('COM3', 9600, timeout = 0.01)
time.sleep(1)
serial_flg=True

arm1=90 #0-180
arm2=90 #0-180
arm3=90 #0-180
arm4=90 #20-90
interval_=60 #方向ボタンの反応間隔
arm_interval = 50 #armの上下ボタンの反応間隔

class Application(tk.Frame):
    
    def __init__(self, master = None):
        super().__init__(master)
        self.master.title("ロボットコントローラ")     # ウィンドウタイトル
        self.master.geometry("600x600")       # ウィンドウサイズ(幅x高さ)

        #--------------------------------------------------------
        # ラベルフレーム1の作成
        padx1=20
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
        
        self.armframe1 = tk.LabelFrame(self.labelframe1, relief="flat")
        self.armframe2 = tk.LabelFrame(self.labelframe1, relief="flat")
        self.armframe3 = tk.LabelFrame(self.labelframe1, relief="flat")
        self.armframe4 = tk.LabelFrame(self.labelframe1, relief="flat")
        self.armframe1.grid(row=2,column=0,padx=padx1)
        self.armframe2.grid(row=2,column=1,padx=padx1)
        self.armframe3.grid(row=2,column=2,padx=padx1)
        self.armframe4.grid(row=2,column=3,padx=padx1)
        self.arm1b1 = tk.Button(self.armframe1, width=4, text = "▲" , command=self.arm1up,repeatdelay=1,repeatinterval=arm_interval)
        self.arm1b2 = tk.Button(self.armframe1, width=4, text = "▼" , command=self.arm1down,repeatdelay=1,repeatinterval=arm_interval)
        self.arm2b1 = tk.Button(self.armframe2, width=4, text = "▲", command=self.arm2up,repeatdelay=1,repeatinterval=arm_interval)
        self.arm2b2 = tk.Button(self.armframe2, width=4, text = "▼", command=self.arm2down,repeatdelay=1,repeatinterval=arm_interval)
        self.arm3b1 = tk.Button(self.armframe3, width=4, text = "▲", command=self.arm3up,repeatdelay=1,repeatinterval=arm_interval)
        self.arm3b2 = tk.Button(self.armframe3, width=4, text = "▼", command=self.arm3down,repeatdelay=1,repeatinterval=arm_interval)
        self.arm4b1 = tk.Button(self.armframe4, width=4, text = "▲", command=self.arm4up,repeatdelay=1,repeatinterval=arm_interval)
        self.arm4b2 = tk.Button(self.armframe4, width=4, text = "▼", command=self.arm4down,repeatdelay=1,repeatinterval=arm_interval)

        self.arm1txt.grid(row=0,column=0,padx=padx1,pady=pady1)
        self.arm2txt.grid(row=0,column=1,padx=padx1,pady=pady1)
        self.arm3txt.grid(row=0,column=2,padx=padx1,pady=pady1)
        self.arm4txt.grid(row=0,column=3,padx=padx1,pady=pady1)
        self.arm1ent.grid(row=1,column=0,padx=padx1,pady=pady1)
        self.arm2ent.grid(row=1,column=1,padx=padx1,pady=pady1)
        self.arm3ent.grid(row=1,column=2,padx=padx1,pady=pady1)
        self.arm4ent.grid(row=1,column=3,padx=padx1,pady=pady1)

        self.scale_var1 = tk.IntVar()
        scalev1 = tk.Scale( self.armframe1, 
                    variable = self.scale_var1,
                    command = self.slider_scroll1,
                    orient=tk.VERTICAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 200,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 180,            # 最大値（開始の値）
                    to = 0,               # 最小値（終了の値）
                    resolution=1,         # 変化の分解能(初期値:1)
                    tickinterval=60,         # 目盛りの分解能(初期値0で表示なし)
                    showvalue=0
                    )
        scalev1.pack(side=tk.LEFT)
        self.arm1b2.pack(side=tk.BOTTOM , pady=3)
        self.arm1b1.pack(side=tk.BOTTOM , pady=3)

        self.scale_var2 = tk.IntVar()
        scalev2 = tk.Scale( self.armframe2, 
                    variable = self.scale_var2,
                    command = self.slider_scroll2,
                    orient=tk.VERTICAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 200,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 180,            # 最大値（開始の値）
                    to = 0,               # 最小値（終了の値）
                    resolution=1,         # 変化の分解能(初期値:1)
                    tickinterval=60,         # 目盛りの分解能(初期値0で表示なし)
                    showvalue=0
                    )
        scalev2.pack(side=tk.LEFT)
        self.arm2b2.pack(side=tk.BOTTOM , pady=3)
        self.arm2b1.pack(side=tk.BOTTOM , pady=3)

        self.scale_var3 = tk.IntVar()
        scalev3 = tk.Scale( self.armframe3, 
                    variable = self.scale_var3,
                    command = self.slider_scroll3,
                    orient=tk.VERTICAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 200,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 180,            # 最大値（開始の値）
                    to = 0,               # 最小値（終了の値）
                    resolution=1,         # 変化の分解能(初期値:1)
                    tickinterval=60,         # 目盛りの分解能(初期値0で表示なし)
                    showvalue=0
                    )
        scalev3.pack(side=tk.LEFT)
        self.arm3b2.pack(side=tk.BOTTOM , pady=3)
        self.arm3b1.pack(side=tk.BOTTOM , pady=3)

        self.scale_var4 = tk.IntVar()
        scalev4 = tk.Scale( self.armframe4, 
                    variable = self.scale_var4,
                    command = self.slider_scroll4,
                    orient=tk.VERTICAL,   # 配置の向き、水平(HORIZONTAL)、垂直(VERTICAL)
                    length = 200,           # 全体の長さ
                    width = 20,             # 全体の太さ
                    sliderlength = 20,      # スライダー（つまみ）の幅
                    from_ = 90,            # 最大値（開始の値）
                    to = 20,               # 最小値（終了の値）
                    resolution=1,         # 変化の分解能(初期値:1)
                    tickinterval=14,         # 目盛りの分解能(初期値0で表示なし)
                    showvalue=0
                    )
        scalev4.pack(side=tk.LEFT)
        self.arm4b2.pack(side=tk.BOTTOM , pady=3)
        self.arm4b1.pack(side=tk.BOTTOM , pady=3)
        #--------------------------------------------------------------

        # ラベルの配置
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
        self.close_button = tk.Button(self.master, text = "CLOSE",font=("family",30),command=self.close_)
        self.close_button.pack(pady=10,side=tk.TOP,fill=tk.X,padx=20)
        #--------------------------------------------------------
    def close_(self, event=None):
        global serial_flg
        serial_flg = False
        time.sleep(0.01)
        self.master.destroy()

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
        inkey ='forward'
        inkeys = bytes(inkey, 'utf-8')
        ser.write(inkeys)
        #print(inkeys)

    def right_(self, event=None):
        print("right")
        inkey ='right'
        inkeys = bytes(inkey, 'utf-8')
        ser.write(inkeys)

    def left_(self, event=None):
        print("left")
        inkey ='left'
        inkeys = bytes(inkey, 'utf-8')
        ser.write(inkeys)

    def back_(self, event=None):
        print("back")
        inkey ='back'
        inkeys = bytes(inkey, 'utf-8')
        ser.write(inkeys)
    
    def arm1up(self, event=None):
        global arm1
        #print("arm1up")
        if(self.arm_flg(0,arm1+1)):
            inkeys = bytes('arm1up', 'utf-8')
            ser.write(inkeys)
            arm1+=1
            set_value_not_send()
    def arm1down(self, event=None):
        global arm1
        if(self.arm_flg(0,arm1-1)):
            inkeys = bytes('arm1down', 'utf-8')
            ser.write(inkeys)
            
            arm1-=1
            set_value_not_send()
    def arm2up(self, event=None):
        global arm2
        if(self.arm_flg(1,arm2+1)):
            inkeys = bytes('arm2up', 'utf-8')
            ser.write(inkeys)
            arm2+=1
            set_value_not_send()
    def arm2down(self, event=None):
        global arm2
        if(self.arm_flg(1,arm2-1)):
            inkeys = bytes('arm2down', 'utf-8')
            ser.write(inkeys)
            arm2-=1
            set_value_not_send()
    def arm3up(self, event=None):
        global arm3
        if(self.arm_flg(2,arm3+1)):
            inkeys = bytes('arm3up', 'utf-8')
            ser.write(inkeys)
            arm3+=1
            set_value_not_send()
    def arm3down(self, event=None):
        global arm3
        if(self.arm_flg(2,arm3-1)):
            inkeys = bytes('arm3down', 'utf-8')
            ser.write(inkeys)
            arm3-=1
            set_value_not_send()
    def arm4up(self, event=None):
        global arm4
        if(self.arm_flg(3,arm4+1)):
            inkeys = bytes('arm4up', 'utf-8')
            ser.write(inkeys)
            arm4+=1
            set_value_not_send()
    def arm4down(self, event=None):
        global arm4
        if(self.arm_flg(3,arm4-1)):
            inkeys = bytes('arm4down', 'utf-8')
            ser.write(inkeys)
            arm4-=1
            set_value_not_send()
    
    def arm_flg(self,sub,arg):
        #腕の可動範囲内なのか判定
        if (arg < 0 or arg > 180) and sub == 0:    return False
        if (arg < 0 or arg > 180) and sub == 1:    return False
        if (arg < 0 or arg > 180) and sub == 2:    return False
        if (arg < 20 or arg > 90) and sub == 3:    return False
        return True

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
    send_value()

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
    send_value()

def set_value_not_send():
    #スライドバーの値をセットする
    app.scale_var1.set(arm1)
    app.scale_var2.set(arm2)
    app.scale_var3.set(arm3)
    app.scale_var4.set(arm4)
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

def send_value():
    global arm1
    global arm2
    global arm3
    global arm4
    inkey ='<'+str(arm1)+','+str(arm2)+','+str(arm3)+','+str(arm4)+'>'
    inkeys = bytes(inkey, 'utf-8')
    print(inkey)
    ser.write(inkeys)

def serial_read():
    global serial_flg
    serial_flg = True
    while serial_flg:
        time.sleep(0.01)
        result = ser.read_all()
        if result.decode(errors='ignore') != "":
            print(result.decode(errors='ignore'))
    print("終了")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    reset_value()
    #messagebox.showinfo()
    thread1 = threading.Thread(target=serial_read)
    thread1.start()
    app.mainloop()
    ser.close()