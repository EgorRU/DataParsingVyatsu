import logging

LOG_FILENAME = 'log.out'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO,  encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s')


def sort(add_new_list, identical_new_list, remove_new_list):
    try:
        add_new_list = sorted(add_new_list, key=lambda x: x.year, reverse=True)
    except Exception as e: 
        logging.exception(f"{str(e)}\n")
    try:
        identical_new_list = sorted(identical_new_list, key=lambda x: x.year, reverse=True)
    except Exception as e: 
        logging.exception(f"{str(e)}\n")
    try:
        remove_new_list = sorted(remove_new_list, key=lambda x: x.year, reverse=True)
    except Exception as e: 
        logging.exception(f"{str(e)}\n")
    return add_new_list, identical_new_list, remove_new_list


def identical_sources_equals(source1, source2):
    #листы новых данных и лист удалённых данных
    add_new_list = []
    remove_new_list = []
    identical_new_list = []

    #проверяем данные на факт добавления (+ на повторки)
    for i in range(len(source2)):
        copy = False
        for j in range(len(source1)):
            if hasattr(source2[i], 'eid') and hasattr(source1[j], 'eid'):
                if (
                    (source2[i].author == source1[j].author or (source2[i].author in source1[j].author) or (source1[j].author in source2[i].author))
                    and source2[i].title == source1[j].title and source2[i].eid == source1[j].eid
                ):
                    copy = True
                    identical_new_list.append(source2[i])
                    break
            else:
                if (
                    (source2[i].author == source1[j].author or (source2[i].author in source1[j].author) or (source1[j].author in source2[i].author))
                    and source2[i].title == source1[j].title
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
            if hasattr(source1[i], 'eid') and hasattr(source2[j], 'eid'):
                if (
                    (source1[i].author == source2[j].author or (source1[i].author in source2[j].author) or (source2[j].author in source1[i].author))
                    and source1[i].title == source2[j].title and source1[i].eid == source2[j].eid
                ):
                    copy = True
                    break
            else:
                if (
                    (source1[i].author == source2[j].author or (source1[i].author in source2[j].author) or (source2[j].author in source1[i].author))
                    and source1[i].title == source2[j].title
                ):
                    copy = True
                    break
        if copy == False:
            remove_new_list.append(source1[i])
            
    list_new_tuple = []
    list_ident_tuple = []
    list_remove_tuple = []
    
    for i in range(len(add_new_list)):
        list_new_tuple.append((add_new_list[i].author,add_new_list[i].title, add_new_list[i].year, add_new_list[i].link ))
    
    for i in range(len(identical_new_list)):
        list_ident_tuple.append((identical_new_list[i].author,identical_new_list[i].title, identical_new_list[i].year, identical_new_list[i].link ))
        
    for i in range(len(remove_new_list)):
        list_remove_tuple.append((remove_new_list[i].author, remove_new_list[i].title, remove_new_list[i].year, remove_new_list[i].link ))

    add_new_list, identical_new_list, remove_new_list = sort(add_new_list, identical_new_list, remove_new_list)
    return list_new_tuple, list_ident_tuple, list_remove_tuple, add_new_list, identical_new_list, remove_new_list


def different_source_equals(source1, source2):
    #листы новых данных и лист удалённых данных
    add_new_list = []
    remove_new_list = []
    identical_new_list = []

    #проверяем данные на факт добавления (+ на повторки)
    for i in range(len(source2)):
        copy = False
        for j in range(len(source1)):
            if (
                (source2[i].clear_author == source1[j].clear_author or (source2[i].clear_author in source1[j].clear_author) or (source1[j].clear_author in source2[i].clear_author))
                and source2[i].clear_title == source1[j].clear_title
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
                (source1[i].clear_author == source2[j].clear_author or (source1[i].clear_author in source2[j].clear_author) or (source2[j].clear_author in source1[i].clear_author))
                and source1[i].clear_title == source2[j].clear_title
            ):
                copy = True
                break
        if copy == False:
            remove_new_list.append(source1[i])

    list_new_tuple = []
    list_ident_tuple = []
    list_remove_tuple = []
    
    for i in range(len(add_new_list)):
        list_new_tuple.append((add_new_list[i].author,add_new_list[i].title, add_new_list[i].year, add_new_list[i].link ))
    
    for i in range(len(identical_new_list)):
        list_ident_tuple.append((identical_new_list[i].author,identical_new_list[i].title, identical_new_list[i].year, identical_new_list[i].link ))
        
    for i in range(len(remove_new_list)):
        list_remove_tuple.append((remove_new_list[i].author, remove_new_list[i].title, remove_new_list[i].year, remove_new_list[i].link ))
        
    add_new_list, identical_new_list, remove_new_list = sort(add_new_list, identical_new_list, remove_new_list)
    return list_new_tuple, list_ident_tuple, list_remove_tuple, add_new_list, identical_new_list, remove_new_list