import argparse
import os
from collections import namedtuple
from typing import List
import pytest
import shutil


# Пишем функцию для получения директории на вход, собираем информацию в объект namedtuple
def parse_path(path: str) -> List[namedtuple]:
    Object = namedtuple('Object', ['name_file', 'ext', 'full_path', 'directory'])
    return [Object(
        name_file=file.split('.')[0] if not os.path.isdir(os.path.join(path, file)) else file,
        ext=file.split('.')[-1] if not os.path.isdir(os.path.join(path, file)) else 'no',
        full_path=os.path.abspath(path),
        directory=os.path.abspath(path).split(os.path.sep)[-1]) for file in os.listdir(path)]

### def gen_file_data(dir_path):
###     pass

#Создаем временную директорию для проверки и так же ее удаляем
@pytest.fixture
def temporary_directory():
    os.mkdir('test_directory')
    d_name = 'test_directory'
    os.makedirs(os.path.join(d_name, 'a'))
    os.makedirs(os.path.join(d_name, 'b'))
    with open(os.path.join(d_name, 'c.py'), 'w', encoding='UTF-8') as f1:
        f1.write('test1')
    with open(os.path.join(d_name, 'd.txt'), 'w', encoding='UTF-8') as f1:
        f1.write('test2')
    yield d_name
    shutil.rmtree(d_name)

###
@pytest.fixture
def file_data():
    return namedtuple('Object',
                      ['name_file', 'ext', 'full_path', 'directory'])

### Имя файла
def test_file_name(temporary_directory, file_data):
    res = parse_path(temporary_directory)
    expected = file_data(name_file='a', ext='', full_path=True, directory='test_directory')
    assert res[0].name_file == expected.name_file
### директория
def test_directory(temporary_directory, file_data):
    res = parse_path(temporary_directory)
    expected = file_data(name_file='b', ext='', full_path=True, directory='test_directory')
    assert res[1].directory == expected.directory
### Размер
def test_correct_size(temporary_directory, file_data):
    assert len(parse_path(temporary_directory)) == 4




