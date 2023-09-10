#(function) def Equals(
# source1: list,
# source2: list
#) -> tuple(add: list, remove: list)  

#tuple - ������
# add - ����, ���������� ������, ������� ���� ��������
# remove - ����, ���������� ������, ������� ���� �������

#example:
#add_list, remove_list = Equals(list_scopus, list_wos)

#����������:
#����� ���������� ����� �� ������ ����������


def Equals(source1, source2):
    #����� ����� ������ � ���� �������� ������
    add_new_list = []
    remove_new_list = []
    
    #��������� ������ �� ���� ����������
    for i in range(len(source2)):
        copy = False
        for j in range(len(source1)):
            if source2[i] == source1[j]:
                copy = True
                break
        if copy == False:
            add_new_list.append(source2[i])

    #��������� ������ �� ���� ��������
    for i in range(len(source1)):
        copy = False
        for j in range(len(source2)):
            if source1[i] == source2[j]:
                copy = True
                break
        if copy == False:
            remove_new_list.append(source1[i])


    print(str(len(source2) - len(source1)) + " = " + str(len(add_new_list)-len(remove_new_list)))
    return add_new_list, remove_new_list