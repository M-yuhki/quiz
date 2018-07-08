# Quiz

# What is this?
好きな問題を漢文テクニカルクイズ風に出題するプログラムです。

# Motivation
SEGAが展開していたクイズゲーム"Answer×Answer"で一番好きだったルールが漢文テクニカルクイズなのですが、An×Anがサービス終了した今、演出上中々プレイし辛いルールなので、簡単にやりたくてとりかかりました。

# Install
## ファイル構成
本プログラムは"quiz.py"と"question"からなります。  
quiz.pyがプログラム本体です。  
questionは問題を記述したcsvファイルを入れておくディレクトリです。ここに問題を記載したcsvファイルを置いておきます(執筆方法等は後述)。

## パッケージの導入
本アプリケーションにはwxPythonを使用していますので、インストールしていない方はインストールをお願いします。  
`pip install wxPython`あたりで簡単に導入できます。

## 実行
quiz.pyとquestion.csvが同一ディレクトリにある状態で`pythonw quiz.py`で実行してください。  
通常のpythonプログラムとは違い`python quiz.py`では実行できませんので、ご注意ください。

# Let's Play!
## タイトル画面
起動すると、最初にこのような画面が立ち上がります。  
![タイトル画面](https://github.com/M-yuhki/quiz/blob/fig/title.png)
まずは問題ファイルを選択します。中央のプルダウンメニューからプレイしたいクイズファイルを選択し、loadボタンを押してください。  
loadボタンを押し、問題の読み込みが成功すると画面最下部のnextボタンが有効化します。  
nextボタンが進行用のボタンです。このボタンを押すとゲームが開始されます。  
なお、問題ファイルはnextボタンを押すまで何度でも選び直せます。loadを押さないと反映されないので注意してください。

## 漢文出題画面
タイトル画面あるいは直前の問題の回答画面からnextボタンを押すと、まず漢文（問題文中の漢字だけを抽出した文字列）が表示されます。
![漢文画面](https://github.com/M-yuhki/quiz/blob/fig/question_kanbun.png)
回答者は、漢文から問題を推測し、答えを導きだします。

## 全文出題画面
漢文出題画面からnextボタンを押すと、全文出題が開始されます。  
![全文画面](https://github.com/M-yuhki/quiz/blob/fig/question_zenbun.png)
回答者は、徐々に現れる問題文から、答えを導きだします。  
全文出題中は、stopボタンまたはstartボタンが有効になります。これは問題文の表示を一時停止・再開するボタンです。  
早押しクイズなどで第一回答者の回答中に問題を停止→誤答したら再開、といった状況で使用してください。

## 回答画面
全文出題画面からnextボタンを押すと、回答が表示されます。
![回答画面](https://github.com/M-yuhki/quiz/blob/fig/answer.png)
この状態でnextボタンを押すと、次の問題の漢文出題画面に移ります。

## 終了画面
登録された問題数が終了した状態で回答画面からnextボタンを押すと、終了画面に移り、プレイした問題数が表示されます  
この状態でnextボタンを押すと、タイトル画面に戻ります。

# Make Quiz Yourself!
クイズ問題を記述するファイルはcsv形式です。  
各行には"問題番号","問題文","回答"を半角カンマ区切りで記載してください。  
問題文と回答は基本的に全角で記述してください。また、半角カンマは絶対に使用しないでください(csvファイルなので)。  
*例:1,「なぜ山に登るのか」という質問に対し「そこに山があるからだ」と答えたことで知られる登山家は誰でしょう？,ジョージ・マロリー*  
作成したファイルはquestionディレクトリに保存してください。ファイル名は任意ですが、名前が同じファイルを複数保存しないでください。

# To Do
* プログラムを関数化して整理する
* UIをより美しくする
* 回答の記録機能をつける
* and so on...

# Version
* python:3.5.5  
* wxPython:4.0.1
