def clear_str(string):  
    #������� ������ ������� �� ������ � ������ ������ �������
    new_str = ""
    if string != None and len(string)>0:
        string = string.lower()
        string = string[0].upper() + string[1:]
        for i in range (len(string)):
            if string[i].isalpha() or string[i]==" " or string[i]==".":
                new_str += string[i]
           
        #�������� ������ � ������� ����
        new = new_str.split()
        #���� ���� ��� �������� ��, ������ �������� � �������
        if len(new)==3:
            new[0] = new[0][0].upper() + new[0][1:]
            new[1] = f"{new[1][0].upper()}"
            if new[2][0]==".":
                new[2] = f"{new[2][1].upper()}"
            else:
                new[2] = f"{new[2][0].upper()}"
            new_str = f"{new[0]} {new[1]}.{new[2]}."
        #���� ���� ��� ��������, �� �������� ������, ����� ���� ��� ��� ��� �������� ������� ����� �����
        if len(new)==2:
            #���� ������� ��������
            counter = new[1].count('.')
            if counter==2:
                new[0] = new[0][0].upper() + new[0][1:]
                new_str_1 = f"{new[1][0].upper()}"
                ii = 1
                while new[1][ii]!=".":
                    ii += 1
                ii += 1
                new_str_2 = f"{new[1][ii].upper()}"
                new_str = f"{new[0]} {new_str_1}.{new_str_2}."
            #����� ��� ���, � � ���� ���� ������ �����
            else:
                new[0] = new[0][0].upper() + new[0][1:]
                new_str = f"{new[0]} {new[1][0].upper()}."

    return new_str