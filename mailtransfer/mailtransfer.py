import emails
import time
import traceback
from imap_tools import MailBox
from .utils import logger


class MailTransfer():
    def __init__(self,
                 imap_server,
                 imap_login,
                 imap_password,
                 smtp_server,
                 smtp_login,
                 smtp_password,
                 mail_to,
                 check_interval):
        self.mailbox = ""
        self.imap_server = imap_server
        self.imap_login = imap_login
        self.imap_password = imap_password
        self.smtp_server = smtp_server
        self.smtp_login = smtp_login
        self.smtp_password = smtp_password
        self.mail_to = mail_to
        self.check_interval = check_interval

    def connect(self):
        try:
            return MailBox(self.imap_server)
        except Exception:
            logger(traceback.format_exc(), "EXCEPTION")

    def login(self):
        try:
            logger("Login...", "INFO")
            self.mailbox.login(self.imap_login, self.imap_password)
            logger("Successfully login to {}".format(self.imap_login), "INFO")
        except Exception:
            logger(traceback.format_exc(), "EXCEPTION")

    def logout(self):
        try:
            logger("Logout...", "INFO")
            self.mailbox.logout()
            logger("Successfully logout", "INFO")
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
                                          mail_from=self.imap_login)
                response = full_msg.send(to=self.mail_to,
                                         smtp={'host': self.smtp_server,
                                               'ssl': True,
                                               'user': self.smtp_login,
                                               'password': self.smtp_password})
                logger("Sending message status: {}".format(response), "INFO")
                if response.status_code != 250:
                    logger("Some error occured: {}".format(response.error), "ERROR")

        except Exception:
            logger(traceback.format_exc(), "EXCEPTION")

    def run(self):
        while True:
            self.mailbox = self.connect()
            self.login()
            unseen_messages = self.get_unseen_messages()
            if len(unseen_messages) == 0:
                logger("No new messages have", "INFO")
            else:
                self.send_messages(unseen_messages)
            self.logout()
            time.sleep(int(self.check_interval))
