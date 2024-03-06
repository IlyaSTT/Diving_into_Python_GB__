import argparse
import os
from collections import namedtuple
from typing import List
import pytest
import shutil

#
def parse_path(path: str) -> List[namedtuple]:
    Object = namedtuple('Object', ['name_file', 'ext', 'full_path', 'directory'])
    return [Object(
        name_file=file.split('.')[0] if not os.path.isdir(os.path.join(path, file)) else file,
        ext=file.split('.')[-1] if not os.path.isdir(os.path.join(path, file)) else 'no',
        full_path=os.path.abspath(path),
        directory=os.path.abspath(path).split(os.path.sep)[-1]) for file in os.listdir(path)]

#
def gen_file_data(dir_path):
    pass
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line args parser')
    parser.add_argument('dir_path', default='.', type=str,
                        help="path to dir to collect data from")
    line_args = parser.parse_args()
    res = gen_file_data(line_args.dir_path)
    print(res)

####
@pytest.fixture
def temp_dir():
    os.mkdir('test_dir')
    d_name = 'test_dir'
    os.makedirs(os.path.join(d_name, 'a'))
    os.makedirs(os.path.join(d_name, 'b'))
    with open(os.path.join(d_name, 'c.py'), 'w', encoding='UTF-8') as f1:
        f1.write('# test1')
    with open(os.path.join(d_name, 'd.txt'), 'w', encoding='UTF-8') as f1:
        f1.write('test2')
    yield d_name
    shutil.rmtree(d_name)

#
@pytest.fixture
def file_data():
    return namedtuple('Object',
                      ['name_file', 'ext', 'full_path', 'directory'])

####
def test_gen_file_data_correct_file_name(temp_dir, file_data):
    res = parse_path(temp_dir)
    expected = file_data(name_file='a', ext='', full_path=True, directory='test_dir')
    assert res[0].name_file == expected.name_file

####
def test_gen_file_data_correct_parent_dir(temp_dir, file_data):
    res = parse_path(temp_dir)
    expected = file_data(name_file='b', ext='', full_path=True, directory='test_dir')
    assert res[1].directory == expected.directory

#####
def test_gen_file_data_correct_size(temp_dir, file_data):
    assert len(parse_path(temp_dir)) == 4
