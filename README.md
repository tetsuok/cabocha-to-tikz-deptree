cabocha-to-tikz-deptree
=======================

このプログラムは日本語係り受け解析器 [CaboCha](http://code.google.com/p/cabocha/) で
解析された文を [tikz-dependency](http://sourceforge.net/projects/tikz-dependency/)
フォーマット (LaTeX 形式) に出力します。

tikz-dependency は係り受け木を描画することができる TeX のパッケージです。本プログラムに
より出力されたファイルを日本語処理可能な TeX 処理系でコンパイルすることにより係り受け木を
pdf ファイルフォーマットで出力することができます。
なお、tikz-dependency は別途インストールしておく必要があります。

また、本ソフトウェアでは XeLaTeX を用いてコンパイルすることを想定しています。

コードは Mac OS X 10.8.2、python 2.7.2、XeTeX Version
3.1415926-2.3-0.9997.5 (TeX Live 2011)、CaboCha 0.66 でのみ動作確認しています。
pLaTeX などの日本語を扱うことのできる他の TeX 処理系では動作確認を行なっておりません。

### インストール ###

本ソフトウェアの動作には以下のものが必要です。

- Python (2.6 以降)

なお Python 3 以降では動作確認を行なっていません。

### 使い方 ###

あらかじめ CaboCha により解析された文を入力データとして用意する必要があります。
具体的には `cabocha -f1` で解析されたフォーマットである必要があります。
解析済みのデータを `converter.py` を用いて LaTeX 形式のファイルに変換します。

    $ ./converter.py [options] data

または

    $ cat data | ./converter.py

あるいは CaboCha で解析した結果を直接パイプでつないで渡すことも可能です。

    $ cat example/example.txt | cabocha -f1 | ./converter.py

なお、CaboCha に対する入力ファイルは一行一文になっている必要があります。
利用可能なオプションについては, `-h` またｈ `--help` を参照して下さい。
データフォーマットについては、CaboCha の web サイトまたは
[サンプルデータ](https://github.com/tetsuok/cabocha-to-tikz-deptree/blob/master/example/example.dep)
を参照して下さい。


#### 実行例 ####

パイプを使って CaboCha で解析した結果から `converter.py` で変換して XeLaTeX で pdf を出力する例

    $ echo "太郎は花子が読んでいる本を次郎に渡した" | cabocha -f1 | ./converter.py | xelatex

出力サンプル:

![sample output](https://raw.github.com/tetsuok/cabocha-to-tikz-deptree/master/example/example.png "Sample output")

### 入力データの文字コード ###

入力データの文字コードは UTF-8 のみをサポートしています。

## ライセンス ##

本ソフトウェアは new BSD ライセンスに従ったフリーソフトウェアです。
