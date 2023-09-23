def clear_str(str):
    new_str = ""
    if str != None:
        for i in range (len(str)):
            if str[i].isalpha() or str[i]==" " or str[i]==".":
                new_str += str[i]
    return new_str