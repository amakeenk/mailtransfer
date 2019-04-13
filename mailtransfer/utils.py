import os
import sys
import stat
from colorama import Fore, Style
from pathlib import Path


def get_config_dir():
    home_dir = str(Path.home())
    config_dir_name = ".mailtransfer"
    config_dir_path = os.path.join(home_dir, config_dir_name)
    return config_dir_path


def get_configfile_path():
    config_dir = get_config_dir()
    config_file_name = "mailtransfer.cfg"
    config_file_path = os.path.join(config_dir, config_file_name)
    if os.path.exists(config_file_path):
        return config_file_path
    else:
        print("{}Config file {} not found{}"
              .format(Fore.RED, config_file_path, Style.RESET_ALL))
        sys.exit(1)


def get_pidfile_path():
    config_dir = get_config_dir()
    pidfile_name = "mailtransfer.pid"
    pidfile_path = os.path.join(config_dir, pidfile_name)
    return pidfile_path


def check_config_permissions(config_path):
    config_permissions = oct(stat.S_IMODE(os.lstat(config_path).st_mode))
    if config_permissions == "0o600":
        return True
    else:
        print("{}Config file {} have unsafely permissions (must be 0600).{}"
              .format(Fore.RED, config_path, Style.RESET_ALL))
        sys.exit(1)
