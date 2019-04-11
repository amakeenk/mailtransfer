import emails
import logging
import time
import traceback
from imap_tools import MailBox


class MailTransfer():
    def __init__(self,
                 imap_server,
                 smtp_server,
                 address_from,
                 address_to,
                 user_password,
                 check_interval):
        self.mailbox = ""
        self.imap_server = imap_server
        self.smtp_server = smtp_server
        self.address_from = address_from
        self.address_to = address_to
        self.user_password = user_password
        self.check_interval = check_interval

    def connect(self):
        try:
            return MailBox(self.imap_server) 
        except Exception:
            print(traceback.format_exc())

    def login(self):
        try:
            self.mailbox.login(self.address_from, self.user_password)
            logging.debug("Login ok")
        except Exception:
            print(traceback.format_exc())

    def logout(self):
        try:
            self.mailbox.logout()
        except Exception:
            print(traceback.format_exc())

    def get_unseen_messages(self):
        unseen_messages = []
        try:
            for message in self.mailbox.fetch('UNSEEN'):
                msg_from = message.from_
                msg_subject = message.subject
                msg_text = message.text
                msg_html = message.html
                new_message = {'msg_from': msg_from,
                               'msg_subject': msg_subject,
                               'msg_text': msg_text,
                               'msg_html': msg_html}
                unseen_messages.append(new_message)
            return unseen_messages
        except Exception:
            print(traceback.format_exc())

    def send_messages(self, message_list):
        for msg in message_list:
            try:
                full_message = emails.Message(html=msg['msg_html'],
                                              subject=msg['msg_subject'],
                                              mail_from=self.address_from)
                response = full_message.send(to=self.address_to,
                                             smtp={'host': self.smtp_server,
                                                   'ssl': True,
                                                   'user': self.address_from,
                                                   'password': self.user_password})
                logging.debug(response)
            except Exception:
                print(traceback.format_exc())

    def run(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Started")
        while True:
            self.mailbox = self.connect()
            self.login()
            unseen_messages = self.get_unseen_messages()
            self.send_messages(unseen_messages)
            self.logout()
            time.sleep(int(self.check_interval))
