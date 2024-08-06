import moreheat_pb2
msg = moreheat_pb2.Temperature()
msg.source = "alice"
msg.temperature = 20


msglen = len(msg.SerializeToString())
print("length bits: " + str(msglen * 8))
print(msg.SerializeToString())
print(str(msg))
