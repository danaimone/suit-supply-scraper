from twilio.rest import Client


class Send_SMS:
    client = None

    def __init__(self, SID, Auth):
        self.client = Client(SID, Auth)

    def send_message(self, body, to_number, from_number):
        self.client.messages.create(to_number, from_number, body)
