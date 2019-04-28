# mailtransfer
Simple linux tool for transfer mails from one mailserver to another mailserver

# Installation
```bash
$ git clone https://github.com/amakeenk/mailtransfer
$ cd mailtransfer
$ python3 setup.py install
```
# Usage
```bash
$ mkdir ~/.mailtransfer
$ cp mailtransfer-sample.cfg ~/.mailtransfer/mailtransfer.cfg
$ chmod 0600 ~/.mailtransfer/mailtransfer.cfg
$ vim mailtransfer.cfg
$ mailtransfer start
```
# Dependencies
- colorama
- configobj
- daemon
- emails
- imap_tools
