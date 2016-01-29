import io
import unittest
from doan.dataset import Dataset, _get_iterator


class DatasetTest(unittest.TestCase):
    def test_dataset_iterator(self):
        dts = Dataset('test_dataset')
        N = 10
        for i in range(N):
            dts.add_row([i])
        for i in range(2):
            self.assertEqual(N, len([i for i in dts]))


class ReaderTest(unittest.TestCase):
    def test_get_iterator(self):
        N = 10
        s = '1\n' * N
        sio = io.StringIO(s)
        sio.doan_dataset_name = '10 lines of 1'
        self.assertEqual(N, len([i for i in _get_iterator(sio)]))
        self.assertEqual(sio.doan_dataset_name, _get_iterator(sio).doan_dataset_name)
        fname = '/tmp/doan-test-generator'
        with open(fname, 'w') as f:
            f.write(s)
        self.assertEqual(N, len([i for i in _get_iterator(fname)]))
        self.assertEqual(fname, _get_iterator(fname).doan_dataset_name)
