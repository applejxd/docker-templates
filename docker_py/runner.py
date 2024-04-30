from contextlib import contextmanager
import datetime
import os
import time
from typing import Optional
import docker


@contextmanager
def timer(name):
    t0 = time.time()
    print(f"----------[Start: {name}]----------")
    yield
    print(f"-----------[End: {name}]-----------")
    print(f"[{name}] done in {time.time() - t0:.0f} s")


class DockerRunner:
    def __init__(
        self,
        img_name: str = "local/dockerfile",
    ):
        self.client = docker.from_env()
        self.img_name = img_name

        # 実行時に書き換え
        self.tag: str = ""
        self.source_root: str = ""
        self.target_root: str = ""

    def get_image_tags(self):
        images = self.client.images.list()
        tags = [image.tags[0] for image in images]
        return tags

    def build(
        self,
        path: str = ".",
        force: bool = False,
    ) -> None:
        # タグがなければ日付から生成して追加
        if ":" not in self.img_name:
            dt = datetime.datetime.now()
            dt = dt.strftime("%y%m%d")
            self.img_name = f"{self.img_name}:{dt}"

        # image が存在する場合
        if self.img_name in self.get_image_tags():
            if force:
                self.client.images.remove(image=self.img_name, force=True)
                print(f"This image removed: {self.img_name}")
            else:
                print(f"This image already exists: {self.img_name}")
                return

        with timer("Build"):
            self.client.images.build(path=path, tag=self.img_name)

    def replace_path(self, file_path):
        container_path = file_path.replace(self.source_root, self.target_root, 1)
        return container_path

    def run(
        self,
        source_root: str,
        target_root: str = "/var/tmp/workspace",
        cmd="id",
    ):
        # cf. https://docker-py.readthedocs.io/en/stable/containers.html
        options = {
            "tty": True,
            "remove": True,
            "detach": True,
            "volumes": [f"{source_root}:{target_root}"],
            "working_dir": target_root,
        }

        with timer("Run"):
            # 複数コマンドが実行できる & attach が間に合うように wrap
            cmd = f'/bin/bash -c "sleep 1; {cmd}"'

            container = self.client.containers.run(
                image=self.img_name, command=cmd, **options
            )

            output = container.attach(stdout=True, stream=True, logs=True)
            for line in output:
                print(line.decode(), end="")


def _main():
    runner = DockerRunner()
    runner.build(path=".", force=False)
    runner.run(
        source_root="/Users/applejxd/src/docker-templates/docker_py",
        cmd="pwd; ls",
    )


if __name__ == "__main__":
    _main()
