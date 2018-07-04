# quiz

# What is this?
好きな問題を漢文テクニカルクイズ風に出題するプログラムです

# Motivation
SEGAが展開していたクイズゲーム"Answer×Answer"で一番好きだったルールが漢文テクニカルクイズなのですが、An×Anがサービス終了した今、演出上中々プレイし辛いルールなので、簡単にやりたくてとりかかりました

# 準備
## ファイル構成
本プログラムは"quiz.py"と"question.csv"からなります。  
quiz.pyがプログラム本体です。question.csvは問題を記述しておくためのファイルです(執筆方法等は後述)。

## パッケージの導入
本アプリケーションにはwxPythonを使用していますので、インストールしていない方はインストールをお願いします。  
`pip install wxPython`あたりで簡単に導入できます。

## 実行
quiz.pyとquestion.csvが同一ディレクトリにある状態で`pythonw quiz.py`で実行してください  
通常のpythonプログラムとは違い`python quiz.py`では実行できません




# Version
ver1.0(2018/07/04):プロトタイプ完成
