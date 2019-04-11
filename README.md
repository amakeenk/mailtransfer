# ! Work-In-Progress !

# mailtransfer
Simple linux tool for transfer mails from one mailserver to another mailserver

# Installation
```bash
$ pip install git+https://github.com/amakeenk/mailtransfer
```
or 
```bash
$ git clone https://github.com/amakeenk/mailtransfer
$ cd mailtransfer
$ python setup.py install
```
# Usage
```bash
$ mkdir ~/.mailtransfer
$ cp mailtransfer-sample.cfg ~/.mailtransfer/mailtransfer.cfg
$ chmod 0600 ~/.mailtransfer/mailtransfer.cfg
$ vim mailtransfer.cfg
$ mailtransfer
```
# Dependencies
- colorama
- configobj
- emails
- imap_tools