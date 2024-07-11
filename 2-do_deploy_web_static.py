#!/usr/bin/python3
"""a fabric script that compressed"""
from fabric.api import local, put, run, env, task
from datetime import datetime
import os

env.hosts = ['100.25.220.64', '100.26.233.66']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


@task
def do_pack():
    """compress a webstatic folder into a .tgz"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    # -c : creates a new archive
    # -v : verbose
    # -z : compression
    # -f : file
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
        run("sudo rm -rf {}{}/".format(releases_path, file_name_no_ext))
        # create directory if they don't exists on a new machine, skip
        # if already exists
        run(f"sudo mkdir -p {releases_path}")
        run(f"sudo tar -xf /tmp/{file_name} -C {releases_path} && sudo mv \
            {releases_path}web_static {releases_path}{file_name_no_ext}")
        run(f"rm '/tmp/{file_name}'")
        run(f"sudo rm {current}")
        run(f"sudo ln -s {releases_path}{file_name_no_ext} {current}")
        print("New version deployed!")
        return True
    except Exception:
        return False

