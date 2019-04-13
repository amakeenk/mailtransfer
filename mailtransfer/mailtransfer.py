import emails
import time
import traceback
from imap_tools import MailBox
from .utils import logger


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
            logger(traceback.format_exc(), "EXCEPTION")

    def login(self):
        try:
            self.mailbox.login(self.address_from, self.user_password)
            logger("Login ok", "INFO")
        except Exception:
            logger(traceback.format_exc(), "EXCEPTION")

    def logout(self):
        try:
            self.mailbox.logout()
            logger("Logout ok", "INFO")
        except Exception:
            logger(traceback.format_exc(), "EXCEPTION")

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
                logger("New message from {}, subject: {}"
                       .format(msg_from, msg_subject), "INFO")
            return unseen_messages
        except Exception:
            logger(traceback.format_exc(), "EXCEPTION")

    def send_messages(self, message_list):
        try:
            for msg in message_list:
                full_msg = emails.Message(html=msg['msg_html'],
                                          subject=msg['msg_subject'],
                                          mail_from=self.address_from)
                response = full_msg.send(to=self.address_to,
                                         smtp={'host': self.smtp_server,
                                               'ssl': True,
                                               'user': self.address_from,
                                               'password': self.user_password})
                logger(response, "INFO")
        except Exception:
            logger(traceback.format_exc(), "EXCEPTION")

    def run(self):
        while True:
            self.mailbox = self.connect()
            self.login()
            unseen_messages = self.get_unseen_messages()
            self.send_messages(unseen_messages)
            self.logout()
            time.sleep(int(self.check_interval))
