#!/usr/bin/python3

import sys
from configobj import ConfigObj
from .mailtransfer import MailTransfer
from .utils import check_config_permissions
from .utils import get_configfile_path
from .utils import get_pidfile_path
from .utils import restart
from .utils import start
from .utils import status
from .utils import stop
from .utils import usage


def main():
    if len(sys.argv) == 1:
        usage()
    else:
        config_file_path = get_configfile_path()
        if check_config_permissions(config_file_path):
            action = sys.argv[1]
            config = ConfigObj(config_file_path)
            imap_server = config['imap_server']
            smtp_server = config['smtp_server']
            user_password = config['user_password']
            address_from = config['address_from']
            address_to = config['address_to']
            check_interval = config['check_interval']
            mt = MailTransfer(imap_server,
                              smtp_server,
                              address_from,
                              address_to,
                              user_password,
                              check_interval)
            if action == "start":
                start(mt)
            elif action == "stop":
                stop()
            elif action == "restart":
                restart(mt)
            elif action == "status":
                status()
            else:
                usage()


if __name__ == "__main__":
    main()
