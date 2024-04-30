# from https://qiita.com/yohm/items/047b2e68d008ebb0f001
FROM ubuntu:22.04

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  gosu \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# RUN apt-get update && apt-get -y install gosu

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]