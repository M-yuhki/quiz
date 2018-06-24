#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import wx
import csv
import codecs
import time

class Quiz(wx.Frame):

  #クラス変数の定義
  
  #ボタンを押した回数&問題数のチェック
  push = -1

  #csvファイルから抽出した問題を保存する配列
  #各項目にさらに配列を格納していく
  question = []
  
  #現在出題されている問題の漢文と全文
  kanbun_now = ""
  zenbun_now = ""

  #reloadquestion周りの変数
  call_num = 0 #呼び出し回数
  pointer = 0 #現在対象としている漢字
  counter = 0 #カウンター
  frame = 250 #文字を送る時間(ms)

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

    #進行用のボタン
    btn = wx.Button(panel_ui,-1,'Next',pos=(420,550))
    btn.Bind(wx.EVT_BUTTON,self.clicked)
    
    # 問題文用ウィンドウ
    # sizeは横900*縦400 題字と被らないように上のインデント広め
    panel_text = wx.Panel(self, -1, pos=(50,110),size=(900,500))

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
        kanbun = []
        for i in row[1]:
          if('亜' <= i <= '話'):
            kanbun.append(i)
            if(len(kanbun)%10 == 0):
              kanbun.append("\n")
        kanbun = "".join(kanbun)

        Quiz.question[index].append(kanbun)
        
        #問題全文
        Quiz.question[index].append(row[1])

        #答え
        Quiz.question[index].append(row[2])

        index += 1
        

  #ボタンを押した際の制御を行う関数
  def clicked(self,event):
    Quiz.push += 1
    # 今、何問目？
    qnum = Quiz.push // 3

    #問題の表示
    if Quiz.push % 3 == 0:
      Quiz.kanbun_now = str(Quiz.question[qnum][1])
      Quiz.zenbun_now = str(Quiz.question[qnum][2])
      self.main.SetLabel(str(qnum+1) + "問目:漢文")
      self.text.SetLabel(Quiz.kanbun_now)
    elif Quiz.push % 3 == 1:
      self.call_num = len(Quiz.zenbun_now) - len(Quiz.kanbun_now)
      self.counter = 0
      self.main.SetLabel(str(qnum+1) + "問目:全文")
      self.timer.Start(self.frame) #問題の表示を開始
  
    else:
      self.timer.Stop()
      self.main.SetLabel(str(qnum+1) + "問目:回答")
      self.text.SetLabel(str(Quiz.question[qnum][3]))

  # 問題文の更新を行う関数
  def reloadquestion(self, event):
    self.text.SetLabel(Quiz.zenbun_now[:self.counter + self.pointer] + Quiz.kanbun_now[self.pointer:])
    self.counter += 1
    if(Quiz.zenbun_now[self.counter] == Quiz.kanbun_now[self.pointer] and self.pointer < len(Quiz.kanbun_now) - 1):
      self.pointer += 1
    if(self.counter == self.call_num):
      self.timer.Stop()
    return 0


quiz = wx.App()
Quiz(None)
quiz.MainLoop()

