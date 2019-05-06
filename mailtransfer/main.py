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
            imap_config = config['imap']
            smtp_config = config['smtp']
            other_config = config['other']
            mt = MailTransfer(imap_config['imap_server'],
                              imap_config['imap_login'],
                              imap_config['imap_password'],
                              smtp_config['smtp_server'],
                              smtp_config['smtp_login'],
                              smtp_config['smtp_password'],
                              other_config['mail_to'],
                              other_config['check_interval'])
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
