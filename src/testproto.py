import moreheat_pb2

tmsg = moreheat_pb2.MhMessage()
tmsg.source = "alice"
tmsg.type = "temperature"
tmsg.value = 20.23


msglen = len(msg.SerializeToString())

print("length bits: " + str(msglen * 8))
print(msg.SerializeToString())
print(str(msg))


