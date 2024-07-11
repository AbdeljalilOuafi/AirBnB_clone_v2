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
#         # create directory if they don't exists on the new machine
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

@task
def do_deploy(archive_path):
    """ method doc
        fab -f 2-do_deploy_web_static.py do_deploy:
        archive_path=versions/web_static_20231004201306.tgz
        -i ~/.ssh/id_rsa -u ubuntu
    """
    try:
        if not os.path.exists(archive_path):
            return False
        fn_with_ext = os.path.basename(archive_path)
        fn_no_ext, ext = os.path.splitext(fn_with_ext)
        dpath = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("rm -rf {}{}/".format(dpath, fn_no_ext))
        run("mkdir -p {}{}/".format(dpath, fn_no_ext))
        run("tar -xzf /tmp/{} -C {}{}/".format(fn_with_ext, dpath, fn_no_ext))
        run("rm /tmp/{}".format(fn_with_ext))
        run("mv {0}{1}/web_static/* {0}{1}/".format(dpath, fn_no_ext))
        run("rm -rf {}{}/web_static".format(dpath, fn_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(dpath, fn_no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False





