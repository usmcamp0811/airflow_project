from json import JSONDecodeError
from typing import List

import docker
import argparse
import logging
import sys
import os.path
import json

import shutil, errno

LIBRARIES_TO_COPY = []

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--task", dest="taskname",
                    help="If you wish to build only specific task, specify its catalog name", required=False)

parser.add_argument("-l", "--loud", help="Log docker build process.", action='store_true', default=False)

class ImagesBuilder:

    def __init__(self, parser):
        self.args = parser.parse_args()
        self.loud = self.args.loud
        self.log = self.configure_and_get_logger()
        self.cli = docker.from_env()

    def build_images(self):
        directories = self.get_directories_to_browse()
        self.log.info(f"Browsing {directories}")
        for directory in directories:
            self.build_task(directory)

    def build_task(self, directory_name):
        self.log.info(f"Handling {directory_name}")
        try:
            self.copy_libraries(directory_name)
            self.log.info("Building image. (run script with -l to see docker logs)")
            image, build_logs = self.cli.images.build(path=f'./tasks/{directory_name}', tag=directory_name, rm=True)

            while True:
                try:
                    output = self.parse_output(next(build_logs))
                    if self.loud:
                        self.log.info(output)
                except StopIteration:
                    self.log.info("Image built.")
                    break
        finally:
            self.remove_libraries(directory_name)

    def parse_output(self, raw) -> str:
        try:
            return raw['stream'].strip('\n')
        except KeyError:
            return raw

    def copy_libraries(self, directory_name):
        for library in LIBRARIES_TO_COPY:
            src = f'./python/libraries/{library}'
            dest = f'./tasks/{directory_name}/{library}'
            self.log.info(f"Copying {src} to {dest}")
            self.copy_dirs(src, dest)

    def remove_libraries(self, directory_name):
        self.log.info("Cleaning up.")
        for library in LIBRARIES_TO_COPY:
            dest = f'./tasks/{directory_name}/{library}'
            self.log.info(f"Removing {dest}")
            shutil.rmtree(dest)

    def get_directories_to_browse(self) -> List[str]:
        taskname = self.args.taskname
        if taskname is not None:
            self.log.info(f"Taskname specified as {taskname}. Will build only that docker image.")
            path = f"{taskname}"
            if not os.path.isdir(f'./tasks/{taskname}'):
                raise Exception(f'''Directory /tasks/{taskname} does not exists.''')
            return [path]
        else:
            self.log.info(f"No particular task name specified. Will build every image in /tasks/.")
            return [x for x in os.listdir('./tasks') if not x.startswith('.') and os.path.isdir(f'./tasks/{x}')]

    def copy_dirs(self, src, dst):
        try:
            shutil.copytree(src, dst)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else:
                raise

    def configure_and_get_logger(self) -> logging.Logger:
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        root.addHandler(handler)
        return logging.getLogger("build_images")


ImagesBuilder(parser).build_images()
