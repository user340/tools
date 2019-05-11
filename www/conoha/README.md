# ConoHa VPS Control Command

<!-- vim-markdown-toc GFM -->

* [Motivation](#motivation)
* [Requires](#requires)
* [How to use](#how-to-use)
    * [Configuration](#configuration)
    * [VM list](#vm-list)
    * [Billing invoices](#billing-invoices)
    * [VM information](#vm-information)
    * [Start/Stop/Reboot VM](#startstopreboot-vm)
    * [Change billing plan](#change-billing-plan)
* [Directories](#directories)
* [Features](#features)
* [Note](#note)
    * [PyYAML](#pyyaml)
    * [認証](#認証)
    * [512MB Billing Plan](#512mb-billing-plan)
    * [課金](#課金)
    * [ユニットテスト](#)
* [TODO](#todo)
* [Documentations](#documentations)
    * [Python](#python)
    * [Requests](#requests)
    * [OpenStack](#openstack)
    * [ConoHa](#conoha)

<!-- vim-markdown-toc -->

## Motivation

Python、Web API、テスト駆動開発の勉強を兼ねて、ConoHa VPSで契約しているVPSをコマンドラインから管理したい。

## Requires

|ソフトウェア|バージョン|アーキテクチャ|
|:--|:--|:--|
|NetBSD|8.0|amd64|
|pkgsrc|2019Q1|-|
|Python|3.7.1|x86\_64|

```
$ python3.7 -m venv ~/.venv/conohactl
$ source ~/.venv/conohactl/bin/activate
$ pip install -r requirements.txt
```

## How to use

```
$ ./src/conoha.py -h
usage: conoha.py [-h] {info,list,bill,start,stop,reboot,change} ...

positional arguments:
  {info,list,bill,start,stop,reboot,change}
    info                Show information of specified virtual machine
    list                Show list of all vm
    bill                Show billing invoices
    start               Power on target vm
    stop                Shut off target vm
    reboot              Reboot target vm
    change              Change billing plan

optional arguments:
  -h, --help            show this help message and exit
```

### Configuration

`src/conf/conohactl.conf`を編集してください。必要な情報はConoHa VPSの管理コンソール画面から確認できます。

```
username: ConoHa VPSのAPIユーザ名
password: APIユーザのパスワード
tenantid: テナントID
region: リージョン
```

### VM list

VM一覧は`list`コマンドで確認します。

```
$ ./src/conoha.py list
    Name                        UUID
====================================================
192-168-1-100   ffffffff-ffff-ffff-ffff-ffffffffffff
```

### Billing invoices

`bill`コマンドから請求情報を確認できます。デフォルトでは、最新10件の請求情報を出力します。

```
$ ./src/conoha.py bill
Invoice ID    Type    Yen (include tax)           Due
==============================================================
13862853     Credit   1032                2019-05-19T15:00:00Z
11687886     Credit   1091                2019-02-19T15:00:00Z
```

### VM information

VMの詳細は`info`コマンドにUUIDを渡すことで確認できます。

```
$ ./src/conoha.py info ffffffff-ffff-ffff-ffff-ffffffffffff
    Name         Tag                     UUID
=============================================================
192-168-1-100   NetBSD   ffffffff-ffff-ffff-ffff-ffffffffffff

    IPv4        IPv6   Status    Plan
======================================
192.168.1.100   None   SHUTOFF   g-1gb
```

### Start/Stop/Reboot VM

サーバの起動・停止・再起動ができます。サーバのUUIDは`list`で確認してください。

```
$ ./src/conoha.py start ffffffff-ffff-ffff-ffff-ffffffffffff
 Tag     Previous   ->    Now
===============================
NetBSD   SHUTOFF    ->   ACTIVE
```

```
$ ./src/conoha.py stop ffffffff-ffff-ffff-ffff-ffffffffffff
 Tag     Previous   ->     Now
================================
NetBSD   ACTIVE     ->   SHUTOFF
```

```
$ ./src/conoha.py reboot ffffffff-ffff-ffff-ffff-ffffffffffff
 Tag     Previous   ->    Now
===============================
NetBSD   ACTIVE     ->   ACTIVE
```

### Change billing plan

`change`コマンドにUUIDと課金プランを渡すことで、課金プランの変更ができます。

```
$ ./src/conoha.py change ffffffff-ffff-ffff-ffff-ffffffffffff g-1gb
 Tag     Previous   ->    Now
==============================
NetBSD   g-2gb      ->   g-1gb

```

## Directories

```
.
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── setup.py
└── src
    ├── conf
    │   └── conohactl.conf.sample
    ├── conoha.py            # 本体
    ├── lib
    │   ├── __init__.py
    │   ├── api.py          # API Wrapper
    │   ├── cmd.py          # ユーザコマンド
    │   └── exceptions.py   # 例外処理
    └── tests
        ├── conf
        │   └── server_id.conf.sample
        ├── unittest_api.py  # lib.apiのユニットテスト
        └── unittest_cmd.py  # lib.cmdのユニットテスト

```

## Features

**WIP**

- 支払い情報を見る。
- VPS一覧を表示する。
- 特定のVPSの情報を表示する。
- VPSの電源をつける。
- VPSの電源を切る。
- VPSを再起動する。
- VPSのプランを変更する。

## Note

### PyYAML

`load()`の代わりに`safe_load()`を使う。

### 認証

ConoHa APIはOpenStack準拠なので、認証に関してはOpenStackの文書を読む。

> OpenStack サービスへのアクセスの認証を行うには、まず最初に、ペイロードにクレデンシャルを指定して OpenStack Identity に認証リクエストを行って、認証トークンを取得する必要があります。

- User Domain
- ユーザ名
- パスワード

……を[/v2.0/tokens](https://www.conoha.jp/docs/identity-post_tokens.html)へ投げると認証トークンが返ってくる。このトークンは一定の時間が過ぎると失効する。いつ失効するかはAPIを叩いたときに返ってきたJSONの中に収められている。

### 512MB Billing Plan

RAM 1GB以上のプランから512MBのプランへと変更できない。逆も同様。

### 課金

ConoHaは1時間単位での課金なので、料金プランを変更し続けると余計に課金額が増える。

### ユニットテスト

- テストが他のテストに影響しないように書く。たとえば、仮想マシンの電源をつけるテストをしたのであれば、マシンの電源を消してからテストを終了させる。
- 異常系のテストができるように、テスト対象のコードでちゃんと例外処理を書く。

## TODO

- APIテストの実行時間を削減する。

## Documentations

### Python

- [Argparse チュートリアル](https://docs.python.org/ja/3/howto/argparse.html)
- [8. エラーと例外](https://docs.python.org/ja/3/tutorial/errors.html)
- [collections -- コンテナデータ型](https://docs.python.org/ja/3/library/collections.html)
- [json --- JSONエンコーダおよびデコーダ](https://docs.python.org/ja/3/library/json.html)
- [unittest --- ユニットテストフレームワーク](https://docs.python.org/ja/3/library/unittest.html)
- [tempfile -- 一時ファイルやディレクトリの作成](https://docs.python.org/ja/3/library/tempfile.html)
- [Example Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

### Requests

- [クイックスタート](https://requests-docs-ja.readthedocs.io/en/latest/user/quickstart/)

### OpenStack

- [OpenStack API Documentation](https://developer.openstack.org/ja/api-guide/quick-start/api-quick-start.html)

### ConoHa

- [API](https://www.conoha.jp/vps/function/api/?btn_id=function_api)
- [ConoHa API Index](https://www.conoha.jp/docs/)
