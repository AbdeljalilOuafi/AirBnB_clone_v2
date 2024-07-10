#!/usr/bin/python3
"""a fabric script that compressed"""
from fabric.api import local
import tarfile
from datetime import datetime


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
