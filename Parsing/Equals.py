def Equals(source1, source2):
    #листы новых данных и лист удалённых данных
    add_new_list = []
    remove_new_list = []
    identical_new_list = []

    #проверяем данные на факт добавления (+ на повторки)
    for i in range(len(source2)):
        copy = False
        for j in range(len(source1)):
            if (
                source2[i].author == source1[j].author
                and source2[i].title == source1[j].title
                and source2[i].year == source1[j].year
                and source2[i].article == source1[j].article
                and source2[i].link == source1[j].link
                and source2[i].doi == source1[j].doi
            ):
                copy = True
                identical_new_list.append(source2[i])
                break
        if copy == False:
            add_new_list.append(source2[i])

    #проверяем данные на факт удаления
    for i in range(len(source1)):
        copy = False
        for j in range(len(source2)):
            if (
                source1[i].author == source2[j].author
                and source1[i].title == source2[j].title
                and source1[i].year == source2[j].year
                and source1[i].article == source2[j].article
                and source1[i].link == source2[j].link
                and source1[i].doi == source2[j].doi
            ):
                copy = True
                break
        if copy == False:
            remove_new_list.append(source1[i])

    print(f"Удалено записей(один автор): {len(remove_new_list)}")
    print(f"Добавлено записей(один автор): {len(add_new_list)}")
    print(f"Одинаковых записей(один автор): {len(identical_new_list)}")
    print("---------------------------------------")
    
    set_remove_new_list = set()
    set_add_new_list = set()
    set_identical_new_list = set()
    
    for i in range(len(remove_new_list)):
        set_remove_new_list.add((remove_new_list[i].link, remove_new_list[i].article, remove_new_list[i].doi, remove_new_list[i].title, remove_new_list[i].year))
      
    for i in range(len(add_new_list)):
        set_add_new_list.add((add_new_list[i].link, add_new_list[i].article, add_new_list[i].doi, add_new_list[i].title, add_new_list[i].year))
       
    for i in range(len(identical_new_list)):
        set_identical_new_list.add((identical_new_list[i].link, identical_new_list[i].article, identical_new_list[i].doi, identical_new_list[i].title, identical_new_list[i].year))

    print(f"Удалено строк(Много авторов): {len(set_remove_new_list)}")
    print(f"Добавлено строк(Много авторов): {len(set_add_new_list)}")
    print(f"Одинаковых строк(Много авторов): {len(set_identical_new_list)}")
    print("---------------------------------------")
    print(f"Для проверки: {(len(source2) - len(source1))} = {len(add_new_list)-len(remove_new_list)}")
    print("---------------------------------------")
    return add_new_list, remove_new_list, 


def IPublishingEquals(source1, source2):
    #листы новых данных и лист удалённых данных
    add_new_list = []
    remove_new_list = []
    identical_new_list = []

    #проверяем данные на факт добавления (+ на повторки)
    for i in range(len(source2)):
        copy = False
        for j in range(len(source1)):
            if (
                source2[i].author == source1[j].author
                and source2[i].title == source1[j].title
                and source2[i].year == source1[j].year
                and source2[i].article == source1[j].article
            ):
                copy = True
                identical_new_list.append(source2[i])
                break
        if copy == False:
            add_new_list.append(source2[i])

    #проверяем данные на факт удаления
    for i in range(len(source1)):
        copy = False
        for j in range(len(source2)):
            if (
                source1[i].author == source2[j].author
                and source1[i].title == source2[j].title
                and source1[i].year == source2[j].year
                and source1[i].article == source2[j].article
            ):
                copy = True
                break
        if copy == False:
            remove_new_list.append(source1[i])

    print(f"Удалено записей(один автор): {len(remove_new_list)}")
    print(f"Добавлено записей(один автор): {len(add_new_list)}")
    print(f"Одинаковых записей(один автор): {len(identical_new_list)}")
    print("---------------------------------------")
    
    set_remove_new_list = set()
    set_add_new_list = set()
    set_identical_new_list = set()
    
    for i in range(len(remove_new_list)):
        set_remove_new_list.add((remove_new_list[i].article, remove_new_list[i].title, remove_new_list[i].year))
      
    for i in range(len(add_new_list)):
        set_add_new_list.add((add_new_list[i].article, add_new_list[i].title, add_new_list[i].year))
       
    for i in range(len(identical_new_list)):
        set_identical_new_list.add((identical_new_list[i].article, identical_new_list[i].title, identical_new_list[i].year))

    print(f"Удалено строк(Много авторов): {len(set_remove_new_list)}")
    print(f"Добавлено строк(Много авторов): {len(set_add_new_list)}")
    print(f"Одинаковых строк(Много авторов): {len(set_identical_new_list)}")
    print("---------------------------------------")
    print(f"Для проверки: {(len(source2) - len(source1))} = {len(add_new_list)-len(remove_new_list)}")
    print("---------------------------------------")
    return add_new_list, remove_new_list, identical_new_list