from mitmproxy import http
from datetime import datetime, timedelta
import uuid

class FreeBus:
    time_format = '%Y-%m-%d %H:%M:%S'

    def get_file(self, filename):
        with open(filename) as f:
            content = f.read()
        return content

    def activate_ticket(self, path):
        json = self.get_file('activate_response.json')
        now = datetime.today()
        purchase_date = now - timedelta(minutes = 2)
        activation_date = now - timedelta(minutes = 1)
        expiration_date = now + timedelta(hours = 1, minutes = 13)
        return json.format(path[-39:-3],
            purchase_date.strftime(self.time_format),
            activation_date.strftime(self.time_format),
            expiration_date.strftime(self.time_format)).replace('(', '{').replace(')', '}')

    def valid_ticket(self):
        json = self.get_file('valid_ticket_response.json')
        token = uuid.uuid4()
        now = datetime.today()
        purchase_date = now - timedelta(minutes = 3)
        return json.format(token,
            purchase_date.strftime(self.time_format)).replace('(', '{').replace(')', '}')

    def request(self, flow):
        if (flow.request.pretty_host == "app.straeto.is"):
            if (flow.request.path.startswith("/pele/api/v1/tickets/activate/")):
                body = self.activate_ticket(flow.request.path)
            elif (flow.request.path.startswith("/pele/api/v1/tickets/valid/")):
                body = self.valid_ticket()
        if ("body" in locals()):
            flow.response = http.Response.make(
                200,
                bytes(body, 'utf-8'),
                {"Content-Type": "application/json;charset=UTF-8"}
            )

addons = [
    FreeBus()
]
