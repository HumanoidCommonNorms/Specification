"""This is a script to set up Github-Pages with Docker on your machine."""
# SYSTEM: Python 3.11.1
#
# これは、Github-PagesをローカルマシンにDockerでセットアップするためのスクリプトです。
#
# このスクリプトは、以下の内容を実行します。
# * .buildフォルダにjekyll-build-pagesをダウンロード
# * jekyll-build-pagesのDockerイメージを作成
# * jekyll-build-pagesのDockerコンテナを作成

import sys
import os
import argparse
import shutil
import subprocess

__version__ = "0.0.1"
parser = argparse.ArgumentParser(
    description="Setup Github-Pages on a local machine with Docker"
)
parser.add_argument("-v", "--version", action="version",
                    version="%(prog)s ver." + __version__)

parser.add_argument("--url", type=str, default="https://github.com/actions/jekyll-build-pages.git",
                    help="URL where jekyll-build-pages can be downloaded")
parser.add_argument("--branch", type=str, default="v1.0.12",
                    help="Branch name of jekyll-build-pages")

parser.add_argument("--image_name", type=str, default="humanoid_common_norms_specification",
                    help="Docker image name")
parser.add_argument("--image_version", type=str, default="0.0.1",
                    help="Docker image version")
parser.add_argument("--container_name", type=str, default="build_jekyll",
                    help="Docker container name")
parser.add_argument("--dockerfile_name", type=str, default="Dockerfile",
                    help="Dockerfile name")
parser.add_argument("--gemfile_path", type=str, default="test/.build/Gemfile",
                    help="Gemfile path")

parser.add_argument("--src", type=str, default="docs", help="Build directory")
parser.add_argument("--root_dir", type=str,
                    default=os.path.abspath(os.path.join(
                        os.path.dirname(__file__), "./..")),
                    help="Root directory")
parser.add_argument("--download_dir", type=str, default="test/.build",
                    help="Download directory")
parser.add_argument("--volume_site", type=str, default="_site",
                    help="Folder where build results are stored")
parser.add_argument("--ruby_version", type=str, default="3.3.2",
                    help="Ruby version")
parser.add_argument("--clone_again", action='store_true',
                    help="Execute a git clone again")
parser.add_argument("--remake_image", action='store_true',
                    help="Remake Docker image")


class SetupGithubPages:
    """Setup Github-Pages on a local machine with Docker."""
    _root_dir = "."
    _download_dir = "."
    _src = "docs"
    _volume_site = "_site"
    _dockerfile_path = "Dockerfile"
    _gemfile_path = "test/Gemfile"
    _remake_image = False

    def __init__(self, ap):
        """Initialize the class."""
        # =========================================================
        self._root_dir = os.path.abspath(ap.root_dir)
        self._download_dir = os.path.abspath(
            os.path.join(ap.root_dir, ap.download_dir))
        self._src = os.path.abspath(
            os.path.join(ap.root_dir, ap.src))
        self._volume_site = os.path.abspath(
            os.path.join(ap.root_dir, ap.volume_site))
        self._gemfile_path = os.path.abspath(
            os.path.join(ap.root_dir, ap.gemfile_path))
        self._dockerfile_path = os.path.abspath(
            os.path.join(self._download_dir, ap.dockerfile_name))
        self._remake_image = ap.remake_image
        if ap.clone_again is True:
            self._remake_image = True
        # =========================================================
        # If there are any containers using the image, delete them.
        ret = self.remove_container(ap.image_name, ap.image_version)

        # =========================================================
        # If there is an image with the same name, delete it.
        if self._remake_image is True:
            if ret == 0:
                ret = self.remove_image(ap.image_name, ap.image_version)

        # =========================================================
        if ret == 0:
            ret = self.download_jekyll_build_pages(
                self._download_dir, ap.url, ap.branch, ap.clone_again)

        # =========================================================
        if self._remake_image is True:
            if ret == 0:
                ret = self.build_docker_image(self._root_dir, self._download_dir,
                                              self._dockerfile_path,
                                              ap.image_name, ap.image_version,
                                              ap.ruby_version)

        # =========================================================
        if ret == 0:
            ret = self.create_docker_container(ap.image_name, ap.image_version, ap.container_name,
                                               self._src, self._volume_site, self._gemfile_path)

        # =========================================================
        # self.print_container_list()
        # self.print_docker_logs(ap.container_name)
        # =========================================================

    def download_jekyll_build_pages(self, download_dir: str,
                                    url: str, branch: str,
                                    clone_again: bool):
        """Download jekyll-build-pages."""
        print("[## Download jekyll-build-pages]")
        ret = 0
        _flag_download = True
        # Delete the existing directory
        if os.path.exists(download_dir):
            if clone_again is True:
                print("  --> Remove directory :" + download_dir)
                shutil.rmtree(download_dir)
                _flag_download = True
            else:
                print("  --> exists directory :" + download_dir)
                _flag_download = False

        if _flag_download is True:
            # Clone the repository
            flag_autocrlf = "false"
            ret, result = self.get_process(
                ['git', 'config', '--global', 'core.autocrlf'])
            if ret == 0:
                flag_autocrlf = result
                print("  --> git config core.autocrlf : " + flag_autocrlf)

            ret, result = self.get_process(
                ['git', 'config', '--global', 'core.autocrlf', "input"])
            if ret == 0:
                print("  --> git config core.autocrlf : input")
            if ret == 0:
                # Clone the repository
                ret, result = self.get_process(['git', 'clone', '--quiet', '--no-progress', url,
                                                '--branch', branch, download_dir])
                if ret == 0:
                    print("  --> Get clone :" + url + "(" + branch + ")")
                else:
                    print("  [ERROR] :" + result)
            ret, result = self.get_process(
                ['git', 'config', '--global', 'core.autocrlf', flag_autocrlf])
            ret, result = self.get_process(
                ['git', 'config', '--global', 'core.autocrlf'])
            if ret == 0:
                print("  --> git config core.autocrlf :" + result)
        return ret

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

    def build_docker_image(self, _root_dir: str, download_dir: str, dockerfile_path: str,
                           image_name: str, image_version: str, ruby_version: str):
        """Build Docker Image."""
        print("[## Create a Docker image]")
        os.chdir(download_dir)
        ret = os.system('docker build'
                        + ' --no-cache'
                        + ' --build-arg RUBY_VERSION=' + ruby_version
                        + ' -t ' + image_name + ':' + image_version
                        + ' -f' + dockerfile_path
                        + " " + download_dir)
        os.chdir(_root_dir)
        if ret == 0:
            print(
                "  --> Create image: " + image_name + ':' + image_version + "(" + str(ret) + ")")

        return ret

    def create_docker_container(self, image_name: str, image_version: str,
                                container_name: str,
                                src: str, volume_site: str, gemfile_path: str):
        """Create Docker Container."""
        ret = 0
        print("[## Create Docker Container]")
        ret, _result = self.get_process(
            ['docker', 'run', '-dit',
             '--name', container_name,
             '--hostname', container_name,
             '--rm',
             '-v', gemfile_path + ":/root/src/Gemfile",
             '-v', src + ":/root/src",
             '-v', volume_site + ":/root/_site",
             '-e', "GITHUB_WORKSPACE=/root",
             '-e', "INPUT_SOURCE=src",
             '-e', "INPUT_DESTINATION=_site",
             '-e', "INPUT_FUTURE=true",
             '-e', "INPUT_VERBOSE=true",
             '-e', "INPUT_TOKEN=",
             '-e', "INPUT_BUILD_REVISION=",
             '--workdir', "/",
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

    def print_docker_logs(self, container_name: str):
        """Print Docker Logs."""
        print("[## docker logs]")
        ret = os.system('docker logs ' + container_name)
        return ret

    def print_container_list(self):
        """Print Docker Container"""
        print("[## Container list] ")
        ret, result = self.get_process(
            ['docker', 'ps', '-a', '--format', '"{{.Names}} : {{.Status}}"'])
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
