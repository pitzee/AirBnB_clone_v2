#!/usr/bin/python3
""" This module contains the function do_pack that generates a .tgz archive
  from the contents of the web_static folder (fabric script) """


from fabric.api import local
from datetime import datetime


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
