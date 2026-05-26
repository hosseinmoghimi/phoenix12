 
def str_to_html(value):
    html=""
    lines=value.splitlines()
    for line in lines:
        html=html+line+"<br>"
    return html
def fixed_length(lenn,vall):
    if len(vall)<lenn:
        zeroes=lenn-len(vall)
        vall=zeroes*'0'+str(vall)
    return vall