import io
import unittest
from doan.dataset import Dataset, LinesIterator, r_num
from doan.util import chunk, fixed_width, num_list_equal
from doan.stat import mean, stat


class DatasetTest(unittest.TestCase):
    def test_dataset_iterator(self):
        """Dataset must correctly work as iterable object."""
        dts = Dataset()
        N = 10
        for i in range(N):
            dts.add_row([i])
        for i in range(2):
            self.assertEqual(N, len([i for i in dts]))

    def test_get_dataset_columns(self):
        """Test column splitting correctness.

        | 0 | 1 | 2 |
        | 3 | 4 | 5 |
        """
        dts = Dataset()
        [dts.add_row(i) for i in chunk(range(6), 3)]
        for i in range(3):
            self.assertEqual([i, i + 3], list(dts.column(i)))
        # test multiple
        self.assertEqual([(0, 1), (3, 4)], list(dts.column(0,1)))
        self.assertEqual([(1, 2), (4, 5)], list(dts.column(1,2)))

    def test_load_invalid_date_type(self):
        """Test invalid data for dataset fails with verbose message."""
        dts = Dataset([Dataset.DATE])
        try:
            dts.load([['aa-bb-cc']])
            self.fail('dataset has loaded invalid data')
        except dts.ParseError as exc:
            self.assertEqual('Invalid value "aa-bb-cc" in line 1 '
                             'for "d" column type (index: 0)',
                             str(exc))


class ReaderTest(unittest.TestCase):

    def setUp(self):
        self.N = 10
        self.str = '1\n' * self.N

    def test_lines_iterator_stringio(self):
        sio = io.StringIO(self.str)
        self.assertEqual(self.N, len([i for i in LinesIterator(sio)]))

    def test_lines_iterator_file(self):
        fname = '/tmp/doan-test-generator'
        with open(fname, 'w') as f:
            f.write(self.str)
        self.assertEqual(self.N, len([i for i in LinesIterator(fname)]))
        self.assertEqual(fname, LinesIterator(fname).name)


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.dataset = r_num(
            io.StringIO('\n'.join([str(i) for i in range(11)])))

    def test_calc_mean(self):
        self.assertEqual(5., mean(self.dataset))

    def test_stat(self):
        st = stat(self.dataset)
        self.assertEqual(5., st.mean)


class UtilTest(unittest.TestCase):
    def test_fixed_width(self):
        N = 10
        self.assertEqual(N, len(fixed_width('1', N)))
        self.assertEqual(N, len(fixed_width('1' * (N + 1), N)))
        self.assertEqual(N, len(fixed_width(1.1, N)))
        self.assertEqual(N, len(fixed_width(1.1 * 1e11, N)))

    def test_num_list_equal(self):
        self.assertTrue(num_list_equal([1] * 5, [0.9] * 5, 0.1))
