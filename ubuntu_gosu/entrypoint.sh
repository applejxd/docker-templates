#!/bin/bash

UNAME="nonroot"
USER_ID=${LOCAL_UID:-9001}
GROUP_ID=${LOCAL_GID:-9001}

echo "Starting with UID : $USER_ID, GID: $GROUP_ID"
useradd -u "${USER_ID}" -o -m "${UNAME}"
groupmod -g "${GROUP_ID}" "${UNAME}"
export HOME=/home/"${UNAME}"

exec /usr/sbin/gosu "${UNAME}" "$@"
