#!/usr/bin/python3
"""
Distributes an archive to my web servers,
using the function do_deploy
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['3.83.238.226', '34.202.234.56']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    
    if not exists(archive_path):
        return False
    archive_file = archive_path.split("/")[-1]
    archive_folder = archive_file.split(".")[0]
    put(archive_path, "/tmp/")
    run("sudo mkdir -p /data/web_static/releases/{}".format(archive_folder))
    run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(archive_file, archive_folder))
    run("sudo rm /tmp/{}".format(archive_file))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s /data/web_static/releases/{} /data/web_static/current".format(archive_folder))
    return True
