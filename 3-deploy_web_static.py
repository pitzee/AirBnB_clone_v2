#!/usr/bin/python3
"""
Distributes an archive to my web servers,
using the function deploy
"""
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists

env.hosts = ['3.83.238.226', '34.202.234.56']

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")
    # Get the current date and time in the format yyyymmddhhmmss
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    # Create the archive name using the web_static prefix and the date and time
    archive_name = "web_static_{}.tgz".format(now)
    # Use the local command to create the archive with tar
    result = local("tar -cvzf versions/{} web_static".format(archive_name))
    # If the command was successful, return the archive path, otherwise return None
    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    # Check if the archive path exists
    if not exists(archive_path):
        return False
    # Get the archive filename without the path (ex: web_static_20211020190000.tgz)
    archive_file = archive_path.split("/")[-1]
    # Get the archive filename without the extension (ex: web_static_20211020190000)
    archive_folder = archive_file.split(".")[0]
    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/")
    # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
    run("mkdir -p /data/web_static/releases/{}".format(archive_folder))
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(archive_file, archive_folder))
    # Delete the archive from the web server
    run("rm /tmp/{}".format(archive_file))
    # Delete the symbolic link /data/web_static/current from the web server
    run("rm -rf /data/web_static/current")
    # Create a new the symbolic link /data/web_static/current on the web server, linked to the new version of your code
    run("ln -s /data/web_static/releases/{} /data/web_static/current".format(archive_folder))
    # Return True if all operations have been done correctly, otherwise return False
    return True


def deploy():
    """Creates and distributes an archive to the web servers"""
    # Call the do_pack() function and store the path of the created archive
    archive_path = do_pack()
