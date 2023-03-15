''' Этот файл содержит хелперы для различных assertions '''

def assert_record_contain_values(record, expected_record_attributes, comparator):
  ''' Для заданной записи модели данных сверяет атрибуты по списку '''
  for key in expected_record_attributes:
    comparator(record.get(key), expected_record_attributes.get(key))
