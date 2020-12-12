# debian_dev

Debian GNU/Linuxによる開発環境のセットアップ用Ansible Playbook

## What deploy

Unikの実行に必要なパッケージ一式とQEMU

## How to deploy

`hosts` を自身の環境にあわせて直す。

`roles/docker/vars/main.yml` を編集し、セットアップホストで `docker` を動かすユーザをリストに列挙する。

```yaml
your_users:
  - uki
  - john
  - tom
```

`ansible-playbook` を実行する。

```console
$ ansible-playbook -i hosts site.yml --ask-become-pass
```
