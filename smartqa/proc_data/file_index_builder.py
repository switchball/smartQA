class FileIndexBuilder:
    def __init__(self):
        self.index = 0
        self.index_map = {}

    def build_index(self, text_list):
        index_file_path = f'index_{self.index}.dat'
        with open(index_file_path, 'wb') as index_file:
            offsets_lengths = []
            for text in text_list:
                text_bytes = text.encode('utf-8')
                offset = index_file.tell()
                length = len(text_bytes)
                offsets_lengths.append((offset, length))
                index_file.write(length.to_bytes(4, byteorder='big'))
                index_file.write(text_bytes)
            index_file.flush()
            self.index_map[self.index] = (index_file_path, offsets_lengths)
            self.index += 1

    def search_index(self, index):
        index_file_path, offsets_lengths = self.index_map[index]
        with open(index_file_path, 'rb') as index_file:
            offset, length = offsets_lengths[index]
            index_file.seek(offset + 4)  # 跳过长度信息
            text_bytes = index_file.read(length)
            return text_bytes.decode('utf-8')

import unittest

class TestFileIndexBuilder(unittest.TestCase):
    def test_build_and_search(self):
        texts = ['Hello, world!', 'Python is awesome!', 'This is a test.']
        f = FileIndexBuilder()
        f.build_index(texts)
        for i in range(3):
            self.assertEqual(f.search_index(i), texts[i])