## WebSSH customize
- ace editorとの連携
- 

## Setup on Windows Subsystem for Linux
- WSLにubuntuをインストール
- ubuntuを開いてから下記を実行する

```sh
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt install unzip
$ sudo apt install python3-pip python3-dev
$ pip3 install -U pip
```
- 仮想環境を作る(websshは作成されるディレクトリの名前であり，仮想環境名でもある）
  - 仮想環境ディレクトリを複数作ることを想定してるので，venvディレクトリ以下にwebssh作成する
`$ python3.6 -m venv ./venv/webssh`
- 仮想環境を起動
`$ source ./venv/webssh/bin/activate`
- pythonのバージョン確認
`$ python --version`
  - 上でインストールした3系になるはず
- websshのセットアップ

```sh
$ git clone https://github.com/mkhrResearch/webssh.git
$ cd webssh
$ python setup.py install
```
- 開発中は python setup.py developにしておくと，setupを都度実行しなくて良くなる（wsshは再起動必要)
- websshの起動
`$ wssh --fbidhttp=False --address='0.0.0.0' --port=2000 --logging=debug`

## Trouble Shooting
- setup.py実行時に`build/temp.linux-x86_64-3.6/_openssl.c:498:10: fatal error: openssl/opensslv.h: No such file or directory`と言われた場合
  - `sudo apt install libssl-dev`をインストールすると良いらしい
- ソース変更して`python setup.py install`しても適用されない
  - `python setup.py clean --all`実行してから`python setup.py develop`でいけた．
  - developは開発用のビルドっぽい．

## Try History
### Ace editorからのSave機能
- xterm.jsの画面とace editorを並べて表示
- aceの現在情報をpostし，サーバ側にファイル保存

### aceコマンドの実装
- ace Hoge.java とターミナルで叩く
- サーバ側でaceコマンドが実行されて， [[ace]] will open /home/user1/Hoge.java とサーバ側に出力
  - サーバ側aceコマンドではファイルの絶対パス変換等を実施
- main.js側で[[ace]]を検知し，aceに変更しつつ，connect_without_options_getfile(filepath)を呼び出す
  - filepathはace will open /home/user1/Hoge.javaからparseした最後のファイルのパス
  - connect_without..の中で，form.actionに/getfileを追加，data変数にfilepathを追加し，ajax_postを実行
- main.pyにGetfileHandlerを追加，handler.pyにGetfileHandlerを追加．
- handler.pyのget_argsでfilepathを取得し，aceコマンドを実行する
  - handler.pyのssh_connect関数のところでcat filepathを実行するように変更．戻り値もworkerじゃなくてコマンド実行結果に変更
  - handler.pyのpost関数のところで，ssh_connectのstdoutを返すように変更．write関数に渡すjsonをeditor:resultに変更．同時にfilepathも追加して返却
- msg.editorをmain.jsのajax_complete_callback_getfileの冒頭でace.setValue実行．msg.filepathにファイルパスが保存されているのでそれも利用できる

