import base64

msg="Hello, world!"

# b64encode requires a bytes, not string
data = base64.b64encode(msg.encode())
print(data)

s = base64.b64decode(data).decode()
print(s)