from google.protobuf import message as _message
def generateColumnDefsFromMessage(message: _message, response):
    for field in message.DESCRIPTOR.fields:
        try:
            c = response.columnDefs.add()
            c.headerName = field.name
            c.field = field.name
        except Exception as ex:
            print(ex)


