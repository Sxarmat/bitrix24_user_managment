import json
from fast_bitrix24 import Bitrix

bx24 = Bitrix('your_webhook')


def invite_user(user_fields):
    '''
    Метод приглашает пользователя на портал. Пользователь получает стандартное уведомление со ссылкой для авторизации
    :param user_fields: принимает словарь с полями из карточки пользователя
    :return: возвращает ID пользователя
    '''
    return bx24.call('user.add', user_fields)


def add_to_group(user_id, group_id):
    '''
    Добавляет пользователя в группу (без приглашения и подтверждения его принятия)
    :param user_id: ID пользователя
    :param group_id: ID группы
    :return: ID группы в случае успеха. В противном случае False
    '''
    try:
        bx24.call('sonet_group.user.add', {'GROUP_ID': group_id, 'USER_ID': user_id})
        return group_id
    except RuntimeError:
        return False


def add_to_deps_list(user_id, department_id, leader=False):
    '''
    Добавляет пользователя в элемент списка подразделений, соответствующий его подразделению
    :param user_id: ID пользователя
    :param department_id: ID департамента
    :param leader: Булева величина, говорящая о том, является ли пользователь руководителем подразделения
    :return: ID элемента списка подразделений, в который добавлен пользователь в случае успеха, иначе False
    '''
    params = generate_params_to_department_list(user_id, department_id, leader)
    try:
        bx24.call('lists.element.update', params)
        return params['ELEMENT_ID']
    except Exception:
        return False


def generate_params_to_department_list(user_id, department_id, leader):
    '''
    Генерирует параметры для метода add_to_deps_list для добавления нового пользователя в список подразделений
    :param user_id: ID пользователя
    :param department_id: ID подразделения
    :param leader: Булева величина, говорящая о том, является ли пользователь руководителем подразделения
    :return: Славарь с параметрами
    '''
    with open('list_structure.json') as file:
        list_structure = json.load(file)
    list_type = list_structure['type']
    list_id = list_structure['id']
    fields = list_structure['fields']
    filter_key = fields['id']
    list_data = bx24.call('lists.element.get', {'IBLOCK_TYPE_ID': list_type, 'IBLOCK_ID': list_id,
                                                'FILTER': {f'={filter_key}': department_id}})[0]
    leader_id = user_id if leader else list_data[fields['leader']].popitem()[1]
    employees_id = list(list_data[fields['employees']].values())
    employees_id.append(user_id) if not leader else None
    employees_id.remove(leader_id) if leader_id in employees_id and len(employees_id) > 1 else None
    params = {
        'IBLOCK_TYPE_ID': list_type,
        'IBLOCK_ID': list_id,
        'ELEMENT_ID': list_data['ID'],
        'FIELDS': {
            fields['title']: list_data['NAME'],
            fields['id']: list_data[fields['id']].popitem()[1],
            fields['leader']: leader_id,
            fields['employees']: employees_id,
            fields['group']: list_data[fields['group']].popitem()[1],
            fields['parent']: list_data[fields['parent']].popitem()[1]
        }
    }
    return params
