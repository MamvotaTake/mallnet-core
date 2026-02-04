from app.mikrotik.client import MikroTikClient

client = MikroTikClient(
    host="192.168.88.1",
    username="admin",
    password="31R-cx70_90",
    port=8728,
)

print("Connecting...")
client.connect()
print("Connected OK")

print("Listing hotspot users...")
users = client.list_hotspot_users()
print(users[::10])

print("Creating test user...")
client.create_hotspot_user(
    username="test_user_091",
    password="1233",
    profile="default",
    comment="MallNet test"
)

print("Users after creation:")
print(client.list_hotspot_users())

client.disconnect()
