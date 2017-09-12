def match(user_string, string_constant, min_length=1):
    if len(user_string.strip()) < min_length:
        return False
    return string_constant.lower().startswith(user_string.strip().lower())

class Unknown(object):
    def __repr__(self):
        return "?"

unknown = Unknown()
