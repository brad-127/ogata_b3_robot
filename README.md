# ogata_b3_robot

## [03_final_tissue.ino](https://github.com/brad-127/ogata_b3_robot/blob/main/03_final_tissue.ino)
最終課題でティッシュを取って帰ってくる動きを作ったときのやつ。
- ライントレース
- 超音波で障害物を感知し、腕の動きで除去
- ティッシュを捻って取る
- 180度方向転換
- もと来た道をライントレースで戻る
- 最後まで戻ったらティッシュを手放す  
という感じで自動で動く。

## [03_gui_serial.ino](https://github.com/brad-127/ogata_b3_robot/blob/main/03_gui_serial.ino)
GUIでロボットを操作するコードの第一版。[gui2.py](https://github.com/brad-127/ogata_b3_robot/blob/main/gui2.py)を使うとき、その入力を受け取る側としてロボットに書き込むコード。

## [03_gui_serial_2.ino](https://github.com/brad-127/ogata_b3_robot/blob/main/03_gui_serial_2.ino)
GUIでロボットを操作するコードの最終完成版。[gui3.py](https://github.com/brad-127/ogata_b3_robot/blob/main/gui3.py)を使うとき、その入力を受け取る側としてロボットに書き込むコード。


## [03_sensor_avoid.ino](https://github.com/brad-127/ogata_b3_robot/blob/main/03_sensor_avoid.ino)
ライントレースして前に進ませ、超音波センサーで感知した障害物をどける。

## [03_serial_monitor.ino](https://github.com/brad-127/ogata_b3_robot/blob/main/03_serial_monitor.ino)
シリアル通信のインタフェース [myser.py](https://github.com/brad-127/ogata_b3_robot/blob/main/myser.py)を使うとき、その操作を受ける側としてロボットに書き込むコード。キーボードで操作できる。以下は操作方法
- "1" 腕の第1関節を選択
- "2" 腕の第2関節を選択
- "3" 腕の手首を選択
- "4" 指先を選択
- "5" カメラの向きを選択
- "6" カメラの角度を選択
- "0" キャタピラの操作を選択
- "w" 前に進むか、上に上がる
- "a" 左に進む
- "s" 後ろに下がるか、下に下がる
- "d" 右に進む

## [b3_robot_test.ino](https://github.com/brad-127/ogata_b3_robot/blob/main/b3_robot_test.ino)
一個上のコードを完成する前の試作段階。操作対象の切り替えだけできる。自動で動く。
- "1" 腕の第1関節を選択
- "2" 腕の第2関節を選択
- "3" 腕の手首を選択
- "4" 指先を選択
- "5" カメラの向きを選択
- "6" カメラの角度を選択

## [gui.py](https://github.com/brad-127/ogata_b3_robot/blob/main/gui.py)
guiの試作段階の画面。多分pythonが入ってるPCなら動く。

## [gui2.py](https://github.com/brad-127/ogata_b3_robot/blob/main/gui2.py)
guiの完成版から、シリアル通信機能を抜いたバージョン。多分pythonが入ってるPCなら動く。

## [guiser.py](https://github.com/brad-127/ogata_b3_robot/blob/main/guiser.py)
guiの試作段階。これでも普通に操作はできる。

## [guiser2.py](https://github.com/brad-127/ogata_b3_robot/blob/main/guiser2.py)
guiの第一版。tkinterで実装している。スライダーや数字の入力、角度のリセット機能も付いているが、4つの角度を同時に制御しなくてはならなかったため、serial通信でやりとりするbyteデータがやや複雑になり、stringからintに変換する作業などに時間がかかるようで、これらの機能は入力から反応までに1秒くらい遅れがある。  
それが気に食わなかったので、即時性にこだわり、各armの関節のスライダーの横に▲と▼のボタンをつけ、これに関してはそれぞれの関節を個別に制御できるため、素早くロボットが制御できるようになった。
キャタピラの移動は普通に素早く動くようにできてる。ただ、動かすときに50ms動いたら10ms停止する、というようにうまい具合に勢いを殺さないと、ボタンを押し終わった後も行き過ぎてしまう事があるので注意。  
入力ボックスは指定範囲内の数字でないと入力できないように作った。▲と▼のボタンによる操作でも、その範囲から出ないようになっている。  
本来はロボット側からPC側へのシリアル通信は必要ないが、debug用に相互のシリアル通信を実現したかった。しかしtkinterを用いていると、mainloopはGUIの入力受付に使われてしまい、シリアル通信のbyteデータを受け付けるwhile文を書けないと思ったので、マルチスレッド化して対応した。(もっと良いやり方はあったかもしれない)ちなみに普通に右上の×印で画面を閉じた場合、そのwhile文が終了しないまま画面を消すことになるので、エラーになる。右下のCLOSEボタンを使って画面を閉じればそれを回避できるようにした。  
sliderによるarm角度の制御は4つを同時に扱うため、<90,90,90,90>というように記号で区切った形でbyteデータをやり取りし、その記号によって角度を読み取り、制御するようにした。  
おそらく実行には`pip install serial`が必要。

## [guiser3.py](https://github.com/brad-127/ogata_b3_robot/blob/main/guiser3.py)
guiser2.pyでは、文字列をやり取りしてその文字列をarduino側で処理して、String型をint型に変換させることで変換していた。しかし、複数文字を読みこむSerial.readString関数や、Stiringをintに変換する関数は処理が重く、ロボットの操作のリアルタイム性に欠けていた。そこで、GUI側の処理で、現在の実際のロボットの腕の角度と、これから指示する腕の角度との差を求め、その回数だけ一文字のデータをarduinoに送りこむ形に書き換えた。これによって、すべての操作において、リアルタイムにロボットを操作できるようになった。

## [line_trace_b3.ino](https://github.com/brad-127/ogata_b3_robot/blob/main/line_trace_b3.ino)
ライントレースをするやつ。
## [myblink_01.ino](https://github.com/brad-127/ogata_b3_robot/blob/main/myblink_01.ino)
最初に書いたコード。LEDを点滅させて、機能しているか試す。
## [myser.py](https://github.com/brad-127/ogata_b3_robot/blob/main/myser.py)
シリアル通信ができるインタフェース。キーボードで操作できるが  
```
pip install serial  
pip install keyboard
```
が必要かもしれない。pipできなかったらpipのパスを通そう。
