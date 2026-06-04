from phoenix.server_settings import DEBUG
def leolog(*args, **kwargs):
    for arg in args:
        print(arg)
    if not DEBUG:
        return
    print("")
    print("")
    print(80*"#")
    for a in kwargs:
        print(a)
        print(80*"-")
        print(kwargs[a])
        print(80*"#")
    print("")
    print("")