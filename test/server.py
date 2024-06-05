"""This is a script to set up Github-Pages with Docker on your machine."""
# SYSTEM: Python 3.11.1
#
# これは、Jekyllサーバを立てるスクリプトです。
#
# このスクリプトは、以下の内容を実行します。
# * jekyll-build-pagesのDockerイメージを作成
# * jekyll-build-pagesのDockerコンテナを作成
#   * デーモンで起動する

import sys
import os
import argparse
import subprocess

__version__ = "0.0.1"
parser = argparse.ArgumentParser(
    description="Setup Github-Pages on a local machine with Docker"
)
parser.add_argument("-v", "--version", action="version",
                    version="%(prog)s ver." + __version__)


parser.add_argument("--image_name", type=str, default="github_pages_server_image",
                    help="Docker image name")
parser.add_argument("--image_version", type=str, default="latest",
                    help="Docker image version")
parser.add_argument("--container_name", type=str, default="server_jekyll",
                    help="Docker container name")

parser.add_argument("--port", type=int, default=4000, help="publish port")
parser.add_argument("--src", type=str, default="docs", help="Build directory")

parser.add_argument("--root_dir", type=str,
                    default=os.path.abspath(os.path.join(
                        os.path.dirname(__file__), "./..")),
                    help="Root directory")
parser.add_argument("--dockerfile_path", type=str, default="test/server/Dockerfile",
                    help="Dockerfile path")
parser.add_argument("--gemfile_dir", type=str, default="test/server",
                    help="Gemfile directory")
parser.add_argument("--config_path", type=str, default="test/server/_config.yml",
                    help="config.yml path")

parser.add_argument("--volume_site", type=str, default="_site",
                    help="Folder where build results are stored")
parser.add_argument("--ruby_version", type=str, default="",
                    help="Ruby version")
parser.add_argument("--build_only", action='store_true',
                    help="Build the site")
parser.add_argument("--remake_container_only", action='store_true',
                    help="Remake from container")


class SetupGithubPages:
    """Setup Github-Pages on a local machine with Docker."""
    _root_dir = "."
    _src = "docs"
    _volume_site = "_site"
    _dockerfile_path = "Dockerfile"
    _gemfile_path = "test/Gemfile"
    _remake_container_only = False

    def __init__(self, ap):
        """Initialize the class."""
        # =========================================================
        self._root_dir = os.path.abspath(ap.root_dir)
        self._src = os.path.abspath(
            os.path.join(ap.root_dir, ap.src))
        self._dockerfile_path = os.path.abspath(
            os.path.join(ap.root_dir, ap.dockerfile_path))
        self._volume_site = os.path.abspath(
            os.path.join(ap.root_dir, ap.volume_site))
        self._gemfile_path = os.path.abspath(
            os.path.join(ap.root_dir, ap.gemfile_dir))
        self._config_path = os.path.abspath(
            os.path.join(ap.root_dir, ap.config_path))
        self._remake_container_only = ap.remake_container_only

        if ap.build_only is False:
            # =========================================================
            # If there are any containers using the image, delete them.
            ret = self.remove_container(ap.image_name, ap.image_version)

            # =========================================================
            # If there is an image with the same name, delete it.
            if self._remake_container_only is False:
                if ret == 0:
                    ret = self.remove_image(ap.image_name, ap.image_version)
            if ret == 0:
                ret = self.build_docker_image(self._root_dir, self._gemfile_path,
                                              self._dockerfile_path,
                                              ap.image_name, ap.image_version,
                                              ap.ruby_version)

            # =========================================================
            if ret == 0:
                ret = self.create_docker_container(ap.image_name, ap.image_version,
                                                   ap.container_name,
                                                   ap.port, self._src,
                                                   self._volume_site,
                                                   self._config_path)
        else:
            ret = 0

        if ret == 0:
            ret = self.build_jekyll_site(ap.container_name)
        # =========================================================
        self.print_container_list()
        if ret == 0:
            self.print_docker_logs(ap.container_name)
        # =========================================================

    def remove_container(self, image_name: str, image_version: str):
        """Remove Docker container."""
        print("[## Remove a container]")
        # ================================
        # If there are any containers using the image, delete them.
        ret, result = self.get_process(['docker', 'ps', '-a', '--format', '"{{.Names}}"',
                                        '--filter', 'ancestor=' + image_name + ':' + image_version])
        if ret == 0:
            for container_name in result.splitlines():
                if container_name == "":
                    continue
                ret2, _result2 = self.get_process(
                    ['docker', 'rm', '-f', container_name])
                print(
                    "  --> Remove container: " + container_name + "(" + str(ret2) + ")")
        return ret

    def remove_image(self, image_name: str, image_version: str):
        """Remove Docker image."""
        print("[## Remove a docker image]")
        ret, result = self.get_process(
            ['docker', 'images', '-q', image_name + ':' + image_version])
        if result != "":
            ret, _result2 = self.get_process(
                ['docker', 'rmi', image_name + ':' + image_version])
            if ret == 0:
                print(
                    "  --> Remove image: " + image_name + ':' + image_version)
            else:
                print("  [ERROR] Don't remove a Docker image")
        return ret

    def build_docker_image(self, root_dir: str, gemfile_dir: str, dockerfile_path: str,
                           image_name: str, image_version: str, ruby_version: str):
        """Build Docker Image."""
        print("[## Create a Docker image]")
        ret, result = self.get_process(
            ['docker', 'images', '-q', image_name + ':' + image_version])
        if result == "":
            os.chdir(gemfile_dir)
            ret = os.system('docker build'
                            + ' --no-cache'
                            + ' --build-arg RUBY_VERSION=' + ruby_version
                            + ' -t ' + image_name + ':' + image_version
                            + ' -f' + dockerfile_path
                            + " " + gemfile_dir)
            os.chdir(root_dir)
            if ret == 0:
                print("  --> Create image: "
                      + image_name + ':' + image_version + "(" + str(ret) + ")")
        else:
            print("  --> Already exists image: "
                  + image_name + ':' + image_version)

        return ret

    def create_docker_container(self, image_name: str, image_version: str,
                                container_name: str, open_port: int,
                                src: str, volume_site: str, config_path: str):
        """Create Docker Container."""
        ret = 0
        print("[## Create Docker Container]")
        ret, _result = self.get_process(
            ['docker', 'run', '-dit',
             '--name', container_name,
             '--hostname', container_name,
             '--publish', "127.0.0.1:" + str(open_port) + ":4000",
             '-v', config_path + ":/root/jekyll/_config.yml",
             '-v', src + ":/root/src",
             '-v', volume_site + ":/root/_site",
             '--workdir', "/root/jekyll",
             image_name + ":" + image_version,
             "/bin/bash"
             ])
        if ret == 0:
            print("  --> Create Docker container: " + container_name)
            print("        src:         " + src)
            print("        volume_site: " + volume_site)
        else:
            print("  [ERROR] Don't create a Docker container")
        return ret

    def build_jekyll_site(self, container_name: str):
        """Build Jekyll Site."""
        print("[## Build Jekyll Site]")
        ret, result = self.get_process(
            ['docker', 'exec', '-it', container_name, '/bin/bash',
             "-c",
             "bundler install"
             ])

        if ret == 0:
            print(result)
        else:
            print("  [ERROR] Failed to build Jekyll site")
        return ret

    def print_docker_logs(self, container_name: str):
        """Print Docker Logs."""
        print("[## docker logs]")
        ret = os.system('docker logs ' + container_name)
        return ret

    def print_container_list(self):
        """Print Docker Container"""
        print("[## Container list] ")
        ret, result = self.get_process(
            ['docker', 'ps', '-a', '--format', '"{{.Names}}\tState[{{.Status}}]\tProt:{{.Ports}}"'])
        if ret == 0:
            print("--------------------------------------------------")
            print(result)
            print("--------------------------------------------------")
        return ret

    def process_run(self, cmd: str, work_dir: str = ""):
        """Run the process."""
        try:
            if work_dir == "":
                work_dir = self._root_dir
            proc = subprocess.run(
                cmd, check=True, shell=True, cwd=work_dir, stdout=subprocess.PIPE)
            stdout = proc.stdout
            str_type = type(stdout)
            if str_type is bytes:
                stdout = stdout.decode('utf-8').replace('"', '')
            else:
                stdout = str(stdout).replace('"', '')
            return proc.returncode, stdout
        except Exception as e:
            return 1, str(e)

    def get_process(self, cmd: str, work_dir: str = ""):
        """Get the process."""
        try:
            if work_dir == "":
                work_dir = self._root_dir
            proc = subprocess.run(
                cmd, check=True, shell=True, cwd=work_dir, stdout=subprocess.PIPE)
            stdout = proc.stdout
            str_type = type(stdout)
            if str_type is bytes:
                stdout = stdout.decode('utf-8').replace('"', '')
            else:
                stdout = str(stdout).replace('"', '')
            return proc.returncode, stdout
        except Exception as e:
            return 1, str(e)


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        setup = SetupGithubPages(args)
    except Exception as e:
        print("[ERROR] " + str(e))

    sys.exit(0)
