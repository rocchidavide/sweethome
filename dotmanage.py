#! /usr/bin/python3
import argparse
import sys
from pathlib import Path

from core.builder import (
    Builder,
    init_sweethomeprofile,
    init_sweethomerc,
    save_sweethomeprofile,
    save_sweethomerc,
    create_sweethomeprofile_symlink,
    create_sweethomerc_symlink,
    remove_sweethomeprofile_symlink,
    remove_sweethomerc_symlink,
)
from core.config import Config
from core.console import Colors
from core.constants import COMMAND_INSTALL, COMMAND_REMOVE
from core.dots import Dot
from core.settings import SWEETHOME_PATH

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An easy and modular dotfiles manager")
    subparsers = parser.add_subparsers(dest="command")
    parser_install = subparsers.add_parser(
        COMMAND_INSTALL, help="Install all dots listed or the one specified"
    )
    parser_install.add_argument(
        "dot", type=str, nargs="?", default="all", help="dot's name to be installed"
    )
    parser_install.add_argument(
        "--force", action="store_true", help="overwrite existing symlinks"
    )
    parser_remove = subparsers.add_parser(
        COMMAND_REMOVE, help="Remove all dots listed or the one specified"
    )
    parser_remove.add_argument(
        "dot", type=str, nargs="?", default="all", help="dot's name to be removed"
    )
    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_usage()
        sys.exit()

    config = Config()
    config.add_config_from_yaml(Path(SWEETHOME_PATH / "dots" / "config.yml"))
    config_local_path = Path(SWEETHOME_PATH / "dots.local" / "config.yml")
    if config_local_path.exists():
        config.add_config_from_yaml(config_local_path)

    builder = Builder(SWEETHOME_PATH)
    if args.command == COMMAND_INSTALL:
        builder.init_build_folder()
    init_sweethomeprofile(builder)
    init_sweethomerc(builder)

    args_dot_name = args.dot
    if args_dot_name == "all":
        for dot_name in config.installed_dots:
            Dot(dot_name, SWEETHOME_PATH, config, builder).manage(args)
    else:
        Dot(args_dot_name, SWEETHOME_PATH, config, builder).manage(args)

    if args.command == COMMAND_INSTALL:
        print(f"\n{Colors.OKBLUE}> Save and create symlink for rc and profile{Colors.ENDC}")
        save_sweethomerc(builder)
        create_sweethomerc_symlink(builder)
        save_sweethomeprofile(builder)
        create_sweethomeprofile_symlink(builder)
    elif args.command == COMMAND_REMOVE:
        builder.destroy_build_folder()
        remove_sweethomerc_symlink(builder)
        remove_sweethomeprofile_symlink(builder)

    print(f"\n\U0001F389 {Colors.BOLD}Done!{Colors.ENDC}")
