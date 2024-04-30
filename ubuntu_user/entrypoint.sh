#!/bin/bash

export USER=nonroot
export HOME=/home/$USER

# カレントディレクトリの uid と gid を調べる
uid=$(stat -c "%u" .)
gid=$(stat -c "%g" .)

if [ "$uid" -ne 0 ]; then
  # nonroot ユーザーの gid とカレントディレクトリの gid が異なる
  if [ "$(id -g $USER)" -ne "$gid" ]; then
    # nonroot の gid をカレントディレクトリの gid に変更
    getent group "$gid" >/dev/null 2>&1 || groupmod -g "$gid" $USER
    # ホームディレクトリの gid を正常化
    chgrp -R "$gid" $HOME
  fi
  # nonroot ユーザーの uid とカレントディレクトリの uid が異なる
  if [ "$(id -u $USER)" -ne "$uid" ]; then
    # nonroot の uid をカレントディレクトリの uid に変更する。
    # ホームディレクトリは usermod によって正常化される。
    usermod -u "$uid" $USER
  fi
fi

# このスクリプト自体は root で実行されているので、uid/gid 調整済みの nonroot ユーザー
# として指定されたコマンドを実行する。
exec setpriv --reuid=$USER --regid=$USER --init-groups "$@"
