import unittest
from .. import myinterval


class TestIntervalOperations(unittest.TestCase):

    def test_equal(self):
        lst1 = [myinterval.Interval(0,3)]
        lst2 = [myinterval.Interval(0,3)]
        self.assertEqual(lst1, lst2);

    def test_sort(self):
        lst = [myinterval.Interval(0, 3),
               myinterval.Interval(4, 5),
               myinterval.Interval(1, 3),
               myinterval.Interval(0, 4)]

        result = sorted(lst)
        expect = [myinterval.Interval(0, 3),
                  myinterval.Interval(0, 4),
                  myinterval.Interval(1, 3),
                  myinterval.Interval(4, 5)]
        self.assertEqual(result, expect)

    def test_intersection(self):
        lst1 = [myinterval.Interval(0, 3, '1-1'),
                myinterval.Interval(1, 4, '1-2'),
                myinterval.Interval(5, 7, '1-3')]
        lst2 = [myinterval.Interval(1, 4, '2-1'),
                myinterval.Interval(4, 9, '2-2')]

        result = myinterval.intersection(lst1, lst2)
        expect = [myinterval.Interval(1, 3),
                  myinterval.Interval(1, 4),
                  myinterval.Interval(5, 7)]
        self.assertEqual(result, expect)
        self.assertEqual(result[0].id1, "1-1")
        self.assertEqual(result[0].id2, "2-1")

        result = myinterval.intersection(lst1, lst2, setid=True)
        self.assertEqual(result, expect)

    def test_complement(self):
        lst1 = [myinterval.Interval(0, 3, '1-1'),
                myinterval.Interval(1, 4, '1-2'),
                myinterval.Interval(5, 7, '1-3'),
                myinterval.Interval(9, 10, '1-3')]

        result = myinterval.complement(lst1, 0, 8);
        expect = [myinterval.Interval(4, 5),
                  myinterval.Interval(7, 8)]
        self.assertEqual(result, expect)


        lst1 = [myinterval.Interval(0, 3, '1-1')]
        result = myinterval.complement(lst1, 5, 10);
        expect = [myinterval.Interval(5, 10)]
        self.assertEqual(result, expect)

