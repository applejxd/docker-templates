# Docker のパーミッション

- [DockerのUID/GIDあれこれ: Linux版通常モード & Docker Desktop for Mac編](https://qiita.com/yuyakato/items/b4ea7e123cd47b22b2c7)
- [Docker for WindowsとWSLを併用するときのパーミッションとファイルユーザ](https://zenn.dev/rotelstift/articles/docker-for-windows-permission)

## OS 毎の違い

### Ubuntu

適切に user 指定をすることで指定のユーザの権限を持ったファイルが作成できる。

- user オプション無し実行
  - 実行ユーザ：root (0:0)
  - 作成したファイルのパーミッション：root(0:0)
- user オプション有り実行
  - 実行ユーザ：指定ユーザ
  - 作成したファイルのパーミッション：指定ユーザ

### Docker Desktop for Mac

いずれにせよホスト側のファイルパーミッションは「ホストUID:0」になる。

- user オプション無し実行
  - 実行ユーザ：root (0:0)
  - コンテナ内での作成したファイルのパーミッション：root(0:0)
  - ホストでの作成したファイルのパーミッション：ホストUID:0

```shell
docker run --rm -it ubuntu:20.04 id
# uid=0(root) gid=0(root) groups=0(root)
docker run --rm -it -v $PWD:/tmp/workspace -w /tmp/workspace ubuntu:20.04 /bin/bash -c "touch test.bin && ls -ln /tmp/workspace"
# -rw-r--r-- 1 0 0    0 Apr 29 00:01 test.bin
ls -ln
# -rw-r--r-- 1 501    0  4 29 09:01 test.bin
```

- user オプション有り実行
  - 実行ユーザ：指定ユーザ
  - コンテナ内での作成したファイルのパーミッション：指定ユーザ
  - ホストでの作成したファイルのパーミッション：ホストUID:0

```shell
docker run --rm -it -u 501:20 ubuntu:20.04 id
# uid=501 gid=20(dialout) groups=20(dialout)
docker run --rm -it -u 501:20 -v $PWD:/tmp/workspace -w /tmp/workspace ubuntu:20.04 /bin/bash -c "touch test.bin && ls -ln /tmp/workspace"
# -rw-r--r-- 1 501 20    0 Apr 28 22:51 test.bin
ls -ln
# -rw-r--r-- 1 501    0  4 29 07:51 test.bin
```

### Docker Desktop for Windows (WSL)
