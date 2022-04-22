'''
Параметры для создания списка и полей списка департаментов
'''

list_params = {
    'IBLOCK_TYPE_ID': 'lists',
    'IBLOCK_CODE': 'deps',
    'FIELDS': {
        'NAME': 'Departments',
        'DESCRIPTION': 'Содержит актуальную и обновляемую информацию о департаментах'
    }
}

list_fields = {
    'id':
        {
            'NAME': 'ID подразделения',
            'IS_REQUIRED': 'N',
            'MULTIPLE': 'N',
            'TYPE': 'N',
            'SORT': 20,
            'CODE': 'DEP_ID',
            'SETTINGS': {
                'SHOW_ADD_FORM': 'Y',
                'SHOW_EDIT_FORM': 'Y',
                'ADD_READ_ONLY_FIELD': 'N',
                'EDIT_READ_ONLY_FIELD': 'N',
                'SHOW_FIELD_PREVIEW': 'N'
            },
        },
    'leader':
        {
            'NAME': 'Руководитель подразделения',
            'IS_REQUIRED': 'N',
            'MULTIPLE': 'N',
            'TYPE': 'S:employee',
            'SORT': 30,
            'CODE': 'DEP_LEADER',
            'SETTINGS': {
                'SHOW_ADD_FORM': 'Y',
                'SHOW_EDIT_FORM': 'Y',
                'ADD_READ_ONLY_FIELD': 'N',
                'EDIT_READ_ONLY_FIELD': 'N',
                'SHOW_FIELD_PREVIEW': 'N'
            },
        },
    'employees':
        {
            'NAME': 'Сотрудники подразделения',
            'IS_REQUIRED': 'N',
            'MULTIPLE': 'Y',
            'TYPE': 'S:employee',
            'SORT': 40,
            'CODE': 'DEP_EMPLOYEES',
            'SETTINGS': {
                'SHOW_ADD_FORM': 'Y',
                'SHOW_EDIT_FORM': 'Y',
                'ADD_READ_ONLY_FIELD': 'N',
                'EDIT_READ_ONLY_FIELD': 'N',
                'SHOW_FIELD_PREVIEW': 'N'
            }
        },
    'group':
        {
            'NAME': 'Группа подразделения',
            'IS_REQUIRED': 'N',
            'MULTIPLE': 'N',
            'TYPE': 'N',
            'SORT': 50,
            'CODE': 'DEP_GROUP',
            'SETTINGS': {
                'SHOW_ADD_FORM': 'Y',
                'SHOW_EDIT_FORM': 'Y',
                'ADD_READ_ONLY_FIELD': 'N',
                'EDIT_READ_ONLY_FIELD': 'N',
                'SHOW_FIELD_PREVIEW': 'N'
            }
        },
    'parent':
        {
            'NAME': 'Вышестоящее подразделение',
            'IS_REQUIRED': 'N',
            'MULTIPLE': 'N',
            'TYPE': 'N',
            'SORT': 60,
            'CODE': 'DEP_PARENT',
            'SETTINGS': {
                'SHOW_ADD_FORM': 'Y',
                'SHOW_EDIT_FORM': 'Y',
                'ADD_READ_ONLY_FIELD': 'N',
                'EDIT_READ_ONLY_FIELD': 'N',
                'SHOW_FIELD_PREVIEW': 'N'
            }
        }
}


def get_list_params():
    '''
    Возвращает параметры для создаваемого списка
    :return: словарь с параметрами
    '''
    return list_params

def get_list_fields():
    '''
    Возвращает параметры для полей по каждому полю создаваемого списка
    :return: словарь с параметрами
    '''
    return list_fields
