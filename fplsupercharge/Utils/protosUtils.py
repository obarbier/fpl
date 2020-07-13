from google.protobuf.json_format import Parse, ParseDict


def parse_dict(js_dict, message):
    ParseDict(js_dict=js_dict, message=message, ignore_unknown_fields=True)


def parseArray(text, message):
    Parse(text=text, message=message, ignore_unknown_fields=True)
