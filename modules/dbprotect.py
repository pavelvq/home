def errintype(arg, type_):
    try:
        a = type_(arg)
        return False, a
    except:
        return True, None
        
def erringet(get, columns):
    for i in get:
        if not i in columns:
            return True
    return False