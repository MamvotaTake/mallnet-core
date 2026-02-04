import routeros_api


class MikroTikClient:
    def __init__(self, host, username, password, port=8728):
        self.connection = None
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.api = None

    def connect(self):
        self.connection = routeros_api.RouterOsApiPool(
            self.host,
            username=self.username,
            password=self.password,
            port=self.port,
            plaintext_login=True,
        )
        api = self.connection.get_api()
        return api

    def create_mac_user(self, mac_address: str, profile: str):
        users = self.api.get_resource("/ip/hotspot/user")

        users.add(
            name=mac_address,
            mac_address=mac_address,
            profile=profile,
            disabled="no",
        )

    def disable_mac_user(self, mac_address: str):
        users = self.api.get_resource("/ip/hotspot/user")
        found = users.get(name=mac_address)
        if found:
            users.set(id=found[0][".id"], disabled="yes")
