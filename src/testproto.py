import moreheat_pb2
msg = moreheat_pb2.Temperature()
msg.source = "alice"
msg.temperature = 20

print(str(msg))
