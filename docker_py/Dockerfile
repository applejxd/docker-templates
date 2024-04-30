FROM ubuntu:20.04

# ビルド時のみ有効
ARG UNAME=nonroot
RUN useradd -m "${UNAME}"

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

WORKDIR /home/"${UNAME}"
CMD ["/bin/bash"]