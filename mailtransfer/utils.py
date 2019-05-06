import os
import sys
import stat
import subprocess
from datetime import datetime
from colorama import Fore
from colorama import Style
from configobj import ConfigObj
from daemon import DaemonContext
from daemon.pidfile import TimeoutPIDLockFile
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


def start(mt):
    pidfile = get_pidfile_path()
    if os.path.exists(pidfile):
        print("{}Mailtransfer already running{}"
              .format(Fore.RED, Style.RESET_ALL))
        sys.exit(1)
    else:
        logger("Starting mailtransfer...", "INFO")
        daemon_context = DaemonContext(pidfile=TimeoutPIDLockFile(pidfile))
        with daemon_context:
            mt.run()


def stop():
    pidfile = get_pidfile_path()
    if os.path.exists(pidfile):
        logger("Stopping mailtransfer...", "INFO")
        pid = subprocess.check_output('cat {}'.format(pidfile), shell=True)
        os.kill(int(pid), 9)
        os.system('rm -f {}'.format(pidfile))
    else:
        print("{}Mailtransfer is not running{}"
              .format(Fore.RED, Style.RESET_ALL))
        sys.exit(1)


def restart(mt):
    pidfile = get_pidfile_path()
    if os.path.exists(pidfile):
        logger("Restarting mailtransfer...", "INFO")
        stop()
        start(mt)
    else:
        print("{}Mailtransfer is not running{}"
              .format(Fore.RED, Style.RESET_ALL))
        sys.exit(1)


def status():
    pidfile = get_pidfile_path()
    config_file_path = get_configfile_path()
    config = ConfigObj(config_file_path)
    log_file = config['other']['log_file']
    if os.path.exists(pidfile):
        pid = subprocess.check_output('cat {}'.format(pidfile), shell=True)
        print("{}Mailtransfer is running{}"
              .format(Fore.GREEN, Style.RESET_ALL))
        print("PID: {}".format(int(pid)))
        print("Recent log messages:\n")
        os.system('tail -10 {}'.format(log_file))
    else:
        print("{}Mailtransfer is not running{}"
              .format(Fore.GREEN, Style.RESET_ALL))


def usage():
    print("Usage: mailtransfer start | stop | restart | status")
    sys.exit(1)


def logger(message, level):
    config_file_path = get_configfile_path()
    config = ConfigObj(config_file_path)
    log_file = config['other']['log_file']
    if not os.path.exists(log_file):
        try:
            os.system('touch {}'.format(log_file))
        except Exception:
            print(traceback.format_exc())
    log_message = "{} [{}] {}".format(datetime.now(), level, message)
    with open(log_file, 'a') as logfile:
        logfile.write("{} \n".format(log_message))
