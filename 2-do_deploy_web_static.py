#!/usr/bin/python3
"""a fabric script that compressed"""
from fabric.api import local, put, run, env, task
from fabric.contrib.files import exists
from datetime import datetime
import os

env.hosts = ['100.25.220.64', '100.26.233.66']


@task
def do_pack():
    """compress a webstatic folder into a .tgz"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    # -c: creates a new archive, -v: verbose, -z: compression, -f: file
    result = local(f"tar -cvzf versions/web_static{date}.tgz web_static")
    if result.return_code == 0:
        return f"versions/web_static{date}.tgz"
    else:
        return None


@task
def do_deploy(archive_path):
    """ deploy an archive to your web servers """
    if not os.path.exists(archive_path):
        return False
    try:
        releases_path = "/data/web_static/releases/"
        file_name = os.path.basename(archive_path)
        file_name_no_ext = file_name.split(".")[0]
        current = "/data/web_static/current"

        put(archive_path, '/tmp/')
        if not exists(releases_path):  # if the path dosen't exist create it
            run(f"sudo mkdir -p {releases_path}")
            run(f"sudo mkdir -p /data/web_static/shared/")
        run(f"sudo tar -xf /tmp/{file_name} -C {releases_path} && sudo mv \
            {releases_path}web_static {releases_path}{file_name_no_ext}")
        run(f"rm '/tmp/{file_name}'")

        # checks if "current" exists on the server before attempting to delete
        if exists(current):
            run(f"sudo rm {current}")
        else:
            pass
        run(f"sudo ln -s {releases_path}{file_name_no_ext} {current}")
        print("New version deployed!")
        return True
    except Exception:
        return False
