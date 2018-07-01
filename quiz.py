#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import wx
import csv
import codecs
import time
import unicodedata

class Quiz(wx.Frame):

  #クラス変数の定義
  
  #ボタンを押した回数
  #現在の問題数のチェックにも使用
  push = -1

  #csvファイルから抽出した問題を保存する配列
  #各項目にさらに配列を格納していく
  question = []

  #登録されている問題数
  q_num = 0
  
  #現在出題されている問題の漢文と全文
  kanbun_now = ""
  zenbun_now = ""

  #reloadquestion周りの変数
  call_num = 0 #呼び出し回数
  pointer = 0 #現在対象としている漢字
  counter = 0 #カウンター
  frame = 200 #文字を送る時間間隔(ms)
  last_flg = True # 最後の1文字の表示に関するフラグ

  def __init__(self,*args,**kw):
    super(Quiz,self).__init__(*args,**kw)

    self.init_ui()

  #初期設定を行う関数
  def init_ui(self):

    #"question.csv"から問題情報を抽出
    self.collectquestion('question.csv')

    #ウィンドウの生成
    self.SetTitle('漢文テクニカルクイズ')
    self.SetBackgroundColour((210,255,212))
    self.SetPosition((200,100))
    self.SetSize((1000,700))
    self.Show()
    
    # 題字とボタンを表示するメインウィンドウ
    # sizeは横900*縦600 max使っても上下左右に50の余白
    panel_ui = wx.Panel(self, -1, pos=(50, 50), size=(900, 600))
    
    #題字
    #一回ボタンを押すとtextが差し替えられ、問題数などの表示になる
    self.main = wx.StaticText(panel_ui, -1, '漢文テクニカルクイズ')
    mainfont = wx.Font(40, wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    self.main.SetFont(mainfont)
    layout = wx.BoxSizer(wx.VERTICAL)
    layout.Add(self.main,flag=wx.GROW)

    # 各種ボタン

    #全体進行用のボタン
    btn = wx.Button(panel_ui,-1,'Next',pos=(420,550))
    btn.Bind(wx.EVT_BUTTON,self.clicked_next)


    #全文表示の停止用のボタン
    self.btn_stop = wx.Button(panel_ui,-1,'Stop', pos=(320,520))
    self.btn_stop.Bind(wx.EVT_BUTTON,self.clicked_stop)
    self.btn_stop.Disable() #問題進行中以外は非表示
    
    # 次はこの辺のボタンの有効無効をきちんとする

    #全文表示の再開用ボタン
    self.btn_start = wx.Button(panel_ui,-1,'Start',pos=(520,520))
    self.btn_start.Bind(wx.EVT_BUTTON, self.clicked_start)
    self.btn_start.Disable() # 問題進行中以外は非表示
   
    # 問題文用ウィンドウ
    # sizeは横900*縦400 題字と被らないように上のインデント広め
    panel_text = wx.Panel(self, -1, pos=(50,110),size=(900,400))

    # 問題文を表示
    # 最初は表示なし、あとでここにtext追加
    self.text = wx.StaticText(panel_text, -1, '')
    self.text.SetFont(mainfont)
    layout = wx.BoxSizer(wx.VERTICAL)
    layout.Add(self.text,flag=wx.GROW)
    
    # タイマーオブジェクト
    self.timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER,self.reloadquestion)
    self.Fit()
    self.counter = 0


      #self.text.SetLabel(str(Quiz.question[qnum][2]))

  #問題文の収集を行う関数
  # 問題はcsvファイルに記述するが、utf-8にencodeを施す必要あり
  def collectquestion(self,filepath):
    with open(filepath,'r') as f:
      reader = csv.reader(f,delimiter=',')
      index = 0
      for row in reader:
        #その問題を格納する配列を作成
        Quiz.question.append([])
        #問題番号
        Quiz.question[index].append(row[0])
        
        #問題漢文
        #漢字のみを抽出して漢文を作成する
        
        kanbun = ""

        for i in row[1]:

          # unicodeから漢字を判定
          if("CJK UNIFIED" in unicodedata.name(i)):
            kanbun += i
        Quiz.question[index].append(kanbun)
        
        #問題全文
        Quiz.question[index].append(row[1])

        #答え
        Quiz.question[index].append(row[2])

        index += 1
      
      # 全問題数を取得
      self.q_num = len(Quiz.question)

  #全体進行ボタンを押した際の制御を行う関数
  def clicked_next(self,event):
    Quiz.push += 1
    # 今、何問目？
    qnum = Quiz.push // 3

    #全問題終了
    if(Quiz.push == self.q_num * 3):
      self.timer.Stop() # reloadquestionの呼び出し終了
      self.main.SetLabel("終了")
      self.text.SetLabel("全{}問、お疲れ様でした".format(self.q_num))

    #漢文表示
    elif Quiz.push % 3 == 0:
      Quiz.kanbun_now = str(Quiz.question[qnum][1])
      Quiz.zenbun_now = str(Quiz.question[qnum][2])
      self.main.SetLabel("{}問目:漢文".format(str(qnum+1)))
      
      # 適切な箇所に改行を挟む
      kanbun_output = Quiz.kanbun_now
      for i in range(int(len(Quiz.kanbun_now)/20)):
        kanbun_output = kanbun_output[:20*(i+1)+i] + "\n" +kanbun_output[20*(i+1)+i:]
      
      self.text.SetLabel(kanbun_output)
    
    #全文表示
    elif Quiz.push % 3 == 1:
      
      # reloadquestionを呼び出すための各種準備
      self.call_num = len(Quiz.zenbun_now) - len(Quiz.kanbun_now)
      self.counter = 0
      self.pointer = 0
      self.last_flg = True
      self.btn_stop.Enable()
      self.main.SetLabel("{}問目:全文".format(str(qnum+1)))
      self.timer.Start(self.frame) #reloadquestionの呼び出し開始
  
    #解答表示
    else:
      self.timer.Stop() # reloadquestionの呼び出し終了
      self.btn_start.Disable()
      self.btn_stop.Disable()
      self.main.SetLabel("{}問目:回答".format(str(qnum+1)))
      self.text.SetLabel(str(Quiz.question[qnum][3]))
 
  # 問題文の更新を行う関数
  def reloadquestion(self, event):
    while True:
      if(self.counter == self.call_num):
        self.btn_start.Disable()
        self.btn_stop.Disable()
        self.timer.Stop()

      if(Quiz.zenbun_now[self.counter + self.pointer] == Quiz.kanbun_now[self.pointer] and self.pointer < len(Quiz.kanbun_now) - 1):
        self.pointer += 1
      elif(Quiz.zenbun_now[self.counter + self.pointer] == Quiz.kanbun_now[self.pointer] and self.pointer == len(Quiz.kanbun_now) - 1 and self.last_flg):
        self.last_flg = False
        break
      else:
        break
    
    zenbun_output = Quiz.zenbun_now[:self.counter + self.pointer + 1]
    if(self.pointer != len(Quiz.kanbun_now) -1 or self.last_flg):
      zenbun_output += Quiz.kanbun_now[self.pointer:]

    for i in range(int(len(Quiz.zenbun_now)/20)):
      zenbun_output = zenbun_output[:20*(i+1)+i] + "\n" + zenbun_output[20*(i+1)+i:]
    
    self.text.SetLabel(zenbun_output)
    self.counter += 1
    return 0

  # 全文表示の停止・再開ボタンを制御する関数
  def clicked_stop(self,event):
    self.btn_stop.Disable()
    self.btn_start.Enable()
    self.timer.Stop()
    return 0
 
  def clicked_start(self,event):
    self.btn_start.Disable()
    self.btn_stop.Enable()
    self.timer.Start(self.frame)
    return 0

quiz = wx.App()
Quiz(None)
quiz.MainLoop()

