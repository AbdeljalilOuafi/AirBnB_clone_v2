#!/usr/bin/python3
"""a fabric script that compressed"""
from fabric.api import local, put, run, env, task
from datetime import datetime
import os

env.hosts = ['100.25.220.64', '100.26.233.66']
# env.user = 'ubuntu'
# env.key_filename = '~/.ssh/id_rsa'


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
    """deploy"""
    if not os.path.exists(archive_path):
        return False
    try:
        releases_path = "/data/web_static/releases/"
        file_name = archive_path.split('/')[1]
        file_name_no_ext = file_name.split(".")[0]
        current = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run(f"tar -xf /tmp/{file_name} -C {releases_path} && mv \
            {releases_path}web_static {releases_path}{file_name_no_ext}")
        run(f"rm '/tmp/{file_name}'")
        run(f"rm {current}")
        run(f"ln -s {releases_path}{file_name_no_ext} {current}")
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """deploy again"""
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)



