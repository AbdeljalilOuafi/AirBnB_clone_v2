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
#         run("rm -rf {}{}/".format(releases_path, file_name_no_ext))
#         # create directory if they don't exists on a new machine, skip
#         # if already exists
#         run(f"mkdir -p {releases_path}")
#         run(f"tar -xf /tmp/{file_name} -C {releases_path} && mv \
#             {releases_path}web_static {releases_path}{file_name_no_ext}")
#         run(f"rm '/tmp/{file_name}'")
#         run(f"rm {current}")
#         run(f"ln -s {releases_path}{file_name_no_ext} {current}")
#         print("New version deployed!")
#         return True
#     except Exception:
#         return False

def do_deploy(archive_path):
    """deploy package to remote server
    Arguments:
        archive_path: path to archive to deploy
    """
    if not archive_path or not os.path.exists(archive_path):
        return False
    put(archive_path, '/tmp')
    ar_name = archive_path[archive_path.find("/") + 1: -4]
    try:
        run('mkdir -p /data/web_static/releases/{}/'.format(ar_name))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'.format(
                ar_name, ar_name
        ))
        run('rm /tmp/{}.tgz'.format(ar_name))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(
                ar_name, ar_name
        ))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            ar_name
        ))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(
            ar_name
        ))
        print("New version deployed!")
        return True
    except:
        return False
