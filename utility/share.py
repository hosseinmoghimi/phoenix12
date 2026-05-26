def whatsapp_link(number):
    if number[0:2]=="09":
        number="+98"+number[1:]
    return f"https://wa.me/{number}"