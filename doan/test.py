import io
import unittest
from doan.dataset import Dataset, _get_iterator, r_num
from doan.util import chunk
from doan.stat import mean, stat


class DatasetTest(unittest.TestCase):
    def test_dataset_iterator(self):
        dts = Dataset('test_dataset')
        N = 10
        for i in range(N):
            dts.add_row([i])
        for i in range(2):
            self.assertEqual(N, len([i for i in dts]))

    def test_column(self):
        dts = Dataset('test_dataset')
        [dts.add_row(i) for i in chunk(range(6), 3)]        
        self.assertEquals([0, 3], list(dts.column(0)))
        self.assertEquals([(1, 2), (4, 5)], list(dts.column(1,2)))


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


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.dataset = r_num(
            io.StringIO('\n'.join([str(i) for i in range(11)])))
        
    def test_calc_mean(self):
        self.assertEquals(5., mean(self.dataset))

    def test_stat(self):
        st = stat(self.dataset)
        self.assertEqual(5., st.mean)
