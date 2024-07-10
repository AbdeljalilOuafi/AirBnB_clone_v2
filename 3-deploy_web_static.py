#!/usr/bin/python3

"""a fabric script that compressed"""
from fabric.api import local, put, run, env
from datetime import datetime
import os

env.hosts = ['100.25.220.64', '100.26.233.66']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_pack():
    """compress a webstatic folder into a .tgz"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    #-c : creates a new archive
    #-v : verbose
    #-z : compression
    #-f : file
    result = local(f"tar -cvzf versions/web_static{date}.tgz web_static")
    if result.return_code == 0:
        return f"versions/web_static{date}.tgz"
    else:
        return None

def do_deploy(archive_path):
    """deploy"""
    if not os.path.exists(archive_path):
        return False
    try:
        remote_path = "/data/web_static/releases/"
        versions, compressed_file_name = archive_path.split('/')
        compressed_file_name_no_extension, ext = compressed_file_name.split(".")
        current = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run(f"tar -xf /tmp/{compressed_file_name} -C {remote_path} && mv {remote_path}web_static {remote_path}{compressed_file_name_no_extension}")
        run(f"rm '/tmp/{compressed_file_name}'")
        run(f"rm {current}")
        run(f"ln -s {remote_path}{compressed_file_name_no_extension} {current}")
        return True
    except Exception:
        return False

def deploy():
    """deploy again"""
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)



