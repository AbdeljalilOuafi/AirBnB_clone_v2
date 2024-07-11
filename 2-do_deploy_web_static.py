#!/usr/bin/python3
"""a fabric script that compressed"""
from fabric.api import local, put, run, task, sudo, env
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


# @task
# def do_deploy(archive_path):
#     """ deploy an archive to your web servers """
#     if not os.path.exists(archive_path):
#         return False
#     try:
#         releases_path = "/data/web_static/releases/"
#         file_name = os.path.basename(archive_path)
#         file_name_no_ext = file_name.split(".")[0]
#         current = "/data/web_static/current"

#         put(archive_path, '/tmp/')
#         # check if the path dosen't exist, it must be created
#         if not exists(releases_path):
#             sudo(f"mkdir -p {releases_path}")
#             sudo(f"mkdir -p /data/web_static/shared/")
#         sudo(f"tar -xzf /tmp/{file_name} -C {releases_path} && sudo mv \
#             {releases_path}web_static {releases_path}{file_name_no_ext}")
#         run(f"rm '/tmp/{file_name}'")

#         # checks if "current" exists on the server before attempting to delete
#         if exists(current):
#             sudo(f"rm {current}")
#         else:
#             pass
#         sudo(f"ln -s {releases_path}{file_name_no_ext} {current}")
#         print("New version deployed!")
#         return True
#     except Exception:
#         return False

def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
