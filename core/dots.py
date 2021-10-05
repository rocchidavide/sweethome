import os
import shutil
import subprocess
from pathlib import Path
import yaml

from core.builder import BuildFile, get_sweethomerc, get_sweethomeprofile
from core.console import Colors, print_row_group, print_row_status, print_dot_title
from core.constants import COMMAND_INSTALL, COMMAND_REMOVE
from core.files import (
    create_symlinks_from_files_in_dir,
    delete_symlinks_in_dir,
    create_symlink,
    delete_symlink,
)


class Dot:
    def __init__(self, dot_name, basepath, config, builder):
        self.dot_name = dot_name
        dots_dir = config.get_dot_path(dot_name)
        self.dot_path = basepath / dots_dir / dot_name
        self.config = config
        self.builder = builder

        # self.bin_path = self.dot_path / "bin"
        self.desktop_entries_path = self.dot_path / "desktop_entries"
        self.dotbuild_file_path = self.dot_path / "dotbuild.yml"
        self.dotfiles_build_path = self.builder.build_path / self.dot_name
        self.dotfiles_path = self.dot_path / "dotfiles"
        self.icons_path = self.dot_path / "icons"
        self.local_apps_path = Path.home() / ".local" / "share" / "applications"
        self.profile_file_path = self.dot_path / f"{self.dot_name}.sweethome_profile"
        self.rc_file_path = self.dot_path / f"{self.dot_name}.sweethome_rc"

    def manage(self, args):
        if args.command == COMMAND_INSTALL:
            self.install(args)
        elif args.command == COMMAND_REMOVE:
            self.remove(args)

    def install(self, args):
        print_dot_title("Install", self.dot_name)
        overwrite = args.force

        if self.profile_file_path.exists():
            print_row_group(f"Append {self.rc_file_path.name} to profile")
            with open(self.profile_file_path, "r") as file:
                get_sweethomeprofile(self.builder).append_content(
                    file.read(), comment=f"Source: {self.dot_name}/{self.profile_file_path.name}"
                )

        if self.rc_file_path.exists():
            print_row_group(f"Append {self.rc_file_path.name} to rc")
            with open(self.rc_file_path, "r") as file:
                get_sweethomerc(self.builder).append_content(
                    file.read(), comment=f"Source: {self.dot_name}/{self.rc_file_path.name}"
                )

        # TODO: use dotfiles/.local/bin/ instead
        # if self.bin_path.exists():
        #     print_row_group(f"Install bin scripts")
        #     for src_file, dst_path in self.bin_items():
        #         create_symlink(src_file, dst_path, overwrite=overwrite)

        if self.dotfiles_path.exists():
            print_row_group(f"Install dotfiles")
            self.create_dotfiles_symlinks(self.dotfiles_path, overwrite=overwrite)

        if self.dotbuild_file_path.exists():
            print_row_group("Build dotfiles")
            self.build_dotfiles()
            print_row_group(f"Install dotfiles just built")
            self.create_dotfiles_symlinks(self.dotfiles_build_path, overwrite=overwrite)

        if self.desktop_entries_path.exists():
            print_row_group(f"Install desktop entries")
            for src_file, dst_path in self.desktop_entries_items():
                create_symlink(src_file, dst_path, overwrite=overwrite)

            if self.update_desktop_database(self.local_apps_path):
                status = f"{Colors.OKGREEN}OK{Colors.ENDC}"
            else:
                status = f"{Colors.FAIL}error{Colors.ENDC}"
            print_row_status("Update desktop database...", status)

        if self.icons_path.exists():
            print_row_group(f"Install icons")
            self.install_icons()

    def remove(self, args):
        print_dot_title("Remove", self.dot_name)

        # if self.bin_path.exists():
        #     print_row_group(f"Remove bin scripts")
        #     for src_file, dst_path in self.bin_items():
        #         delete_symlink(dst_path)

        if self.dotfiles_path.exists():
            print_row_group(f"Remove dotfiles")
            self.remove_dotfiles_symlinks(self.dotfiles_path)

        if self.dotfiles_build_path.exists():
            print_row_group("Remove built dotfiles")
            self.remove_dotfiles_symlinks(self.dotfiles_build_path)
            if os.path.exists(self.dotfiles_build_path):
                shutil.rmtree(self.dotfiles_build_path)

        if self.desktop_entries_path.exists():
            print_row_group(f"Remove desktop entries")
            # TODO: remove broken symlinks in self.local_apps_path?
            for src_file, dst_path in self.desktop_entries_items():
                delete_symlink(dst_path)

            if self.update_desktop_database(self.local_apps_path):
                status = f"{Colors.OKGREEN}OK{Colors.ENDC}"
            else:
                status = f"{Colors.FAIL}error{Colors.ENDC}"
            print_row_status("Update desktop database...", status)

        if self.icons_path.exists():
            print_row_group(f"Remove icons")
            self.remove_icons()

    # def bin_items(self):
    #     # TODO: parametrize in settings dst_basepath (maybe a user wants to use the ~/bin/ folder)
    #     dst_basepath = Path.home() / ".local" / "bin"
    #     for src_file in self.bin_path.iterdir():
    #         dst_path = dst_basepath / src_file.name
    #         yield src_file, dst_path

    def desktop_entries_items(self):
        for src_file in self.desktop_entries_path.iterdir():
            dst_path = self.local_apps_path / src_file.name
            yield src_file, dst_path

    @staticmethod
    def update_desktop_database(applications_path):
        udd_output = subprocess.run(
            ["update-desktop-database", applications_path], capture_output=True
        )
        try:
            udd_output.check_returncode()
            return True
        except subprocess.CalledProcessError:
            return False

    def build_dotfiles(self):
        with open(self.dotbuild_file_path, "r") as stream:
            try:
                dotbuild = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                raise

        for buildset in dotbuild["builds"]:
            output_dir = self.dot_name / Path(buildset.get("output_dir"))
            bf = BuildFile(buildset["filename"], output_dir=output_dir)
            for fragment in buildset["includes"]:
                with open(self.dot_path / fragment, "r") as file:
                    bf.append_content(file.read(), comment=f"Source: {fragment}")
            self.builder.add_buildfile(bf)
            self.builder.store_file(buildset["filename"])

    def create_dotfiles_symlinks(self, dotfiles_path, overwrite=False):
        self._process_dotfiles_symlinks(COMMAND_INSTALL, dotfiles_path, overwrite)

    def remove_dotfiles_symlinks(self, dotfiles_path):
        self._process_dotfiles_symlinks(COMMAND_REMOVE, dotfiles_path)

    def install_icons(self):
        self._process_icons(COMMAND_INSTALL)

    def remove_icons(self):
        self._process_icons(COMMAND_REMOVE)

    def _process_dotfiles_symlinks(self, action, dotfiles_path, overwrite=False):
        for src_file in dotfiles_path.iterdir():
            dst_path = Path.home() / src_file.name

            if src_file.is_dir() and src_file.name == ".config":
                if action == COMMAND_INSTALL:
                    create_symlinks_from_files_in_dir(src_file, dst_path, overwrite=overwrite)
                elif action == COMMAND_REMOVE:
                    delete_symlinks_in_dir(src_file, dst_path)
            elif src_file.is_dir() and src_file.name == '.local':
                src_local_bin_path = src_file / 'bin'
                if src_local_bin_path.exists():
                    dst_path = Path.home() / '.local' / 'bin'
                    if action == COMMAND_INSTALL:
                        create_symlinks_from_files_in_dir(src_local_bin_path, dst_path, overwrite=overwrite)
                    elif action == COMMAND_REMOVE:
                        delete_symlinks_in_dir(src_local_bin_path, dst_path)
            else:
                if action == COMMAND_INSTALL:
                    create_symlink(src_file, dst_path, overwrite=overwrite)
                elif action == COMMAND_REMOVE:
                    delete_symlink(dst_path)

    def _process_icons(self, action):
        # https://wiki.archlinux.org/title/icons
        for icon in self.icons_path.iterdir():
            if action == COMMAND_INSTALL:
                subprocess_cmd = ["xdg-icon-resource", "install", "--size", "48", icon]
                status_label = 'OK'
            elif action == COMMAND_REMOVE:
                subprocess_cmd = [
                    "xdg-icon-resource",
                    "uninstall",
                    "--size",
                    "48",
                    icon.stem,
                ]
                status_label = 'removed'
            xir_output = subprocess.run(subprocess_cmd, capture_output=True)
            try:
                xir_output.check_returncode()
                status = f"{Colors.OKGREEN}{status_label}{Colors.ENDC}"
            except subprocess.CalledProcessError:
                status = f"{Colors.FAIL}error{Colors.ENDC}"
            print_row_status(icon.name, status)
