import json
from fast_bitrix24 import Bitrix
from user_management.constants import get_list_fields, get_list_params

bx24 = Bitrix('your_webhook')


def create_dep_list():
	'''
	метод создает список всех департаментов
	:return: возвращает словарь с ID списка, типом списка и ID каждого поля в списке, дополнительно записывает данные
	в файл json
	'''
	list_params = get_list_params()
	list_fields = get_list_fields()
	list_id = bx24.call('lists.add', list_params)
	bx24.call('lists.field.update', get_params_name_field(list_id))
	fields = {'title': 'NAME'}
	for field in list_fields:
		field_id = bx24.call('lists.field.add',
							 {'IBLOCK_TYPE_ID': 'lists', 'IBLOCK_ID': list_id, 'FIELDS': list_fields[field]})
		fields[field] = field_id
	list_data = {
		'id': list_id,
		'type': list_params['IBLOCK_TYPE_ID'],
		'fields': fields
	}
	with open('list_structure.json', 'w') as file:
		json.dumps(json.dump(list_data, file, indent=4))
	return list_data


def get_params_name_field(list_id):
	'''
	метод собирает параметр для изменения поля "Название"
	:param list_id: принимает ID списка департаментов
	:return: возвращает словарь с параметрами для метода lists.field.update для изменения наименования поля "Название"
	'''
	return {
		'IBLOCK_TYPE_ID': 'lists',
		'IBLOCK_ID': list_id,
		'FIELD_ID': 'NAME',
		'FIELDS': {
			'NAME': 'Название подразделения',
			'TYPE': 'NAME'
		}
	}


def fill_in_list(list_data):
	'''
	Метод заполняет список департаментов. Поле группа не заполняется. Если в подразделении нет сотрудников, то в поле
	сотрудник будет указан руководитель подразделения
	:param list_data: принимает словарь с ID списка, типом списка и ID каждого поля в списке
	:return:
	'''
	departments = bx24.get_all('department.get')
	i = 1
	for dep in departments:
		dep_name = dep['NAME']
		dep_id = dep['ID']
		leader_id = get_leader_id(dep)
		users = bx24.call('user.get', {'FILTER': {'ACTIVE': 'Y', 'UF_DEPARTMENT': dep_id}})
		emploees_id = [user['ID'] for user in users if user['ID'] != leader_id]
		if not emploees_id:
			emploees_id = [leader_id]
		parent_id = dep['PARENT'] if 'PARENT' in dep else ''
		list_elem = bx24.call('lists.element.add',
							  {
								  'IBLOCK_TYPE_ID': list_data['type'],
								  'IBLOCK_ID': list_data['id'],
								  'ELEMENT_CODE': str(i),
								  'FIELDS': {
									  list_data['fields']['title']: dep_name,
									  list_data['fields']['id']: dep_id,
									  list_data['fields']['leader']: leader_id,
									  list_data['fields']['employees']: emploees_id,
									  list_data['fields']['group']: '',
									  list_data['fields']['parent']: parent_id
								  }
							  }
							  )
		i += 1
	return True


def get_leader_id(dep):
	'''
	метод определяет руководителя подразделения. Если в подразделении нет руководителя, в качестве руководителя будет
	выбран руководитель ближайшего родительского департамента, в котором имеется руководитель
	:param dep: принимает словарь с полями департамента
	:return: возвращает ID руководителя департамента
	'''
	leader_id = dep.get('UF_HEAD')
	if leader_id is None:
		dep_parent = bx24.get_all('department.get', {'FILTER': {'ID': dep['PARENT']}})
		return get_leader_id(*dep_parent)
	return leader_id


if __name__ == '__main__':
	list_data = create_dep_list()
	result = fill_in_list(list_data)
	print(result)
