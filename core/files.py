import os
from pathlib import Path

from core.console import print_row_status, Colors


def create_symlinks_from_files_in_dir(files_path, dst_basepath, overwrite=False):
    for src_path in files_path.iterdir():
        create_symlink(src_path, dst_basepath / src_path.name, overwrite)


def create_symlink_in_home(src_path, overwrite=False):
    dst_path = Path.home() / src_path.name
    create_symlink(src_path, dst_path, overwrite=overwrite)


def create_symlink(src_path, dst_path, overwrite=False):
    try:
        os.symlink(src_path, dst_path)
        status = f"{Colors.OKGREEN}created{Colors.ENDC}"
    except FileExistsError:
        if overwrite:
            os.unlink(dst_path)
            os.symlink(src_path, dst_path)
            status = f"{Colors.WARNING}overwritten{Colors.ENDC}"
        else:
            status = "already exists"
    print_row_status(dst_path, status)


def delete_symlinks_in_dir(files_path, dst_basepath):
    for src_path in files_path.iterdir():
        delete_symlink(dst_basepath / src_path.name)


def delete_symlink(dst_path):
    status = f"{Colors.OKGREEN}removed{Colors.ENDC}"
    try:
        os.unlink(dst_path)
    except IsADirectoryError:
        os.rmdir(dst_path)
    except FileNotFoundError:
        status = "not found"
    print_row_status(dst_path, status)
