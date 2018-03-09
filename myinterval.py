class Interval:
    def __init__(self, start, end, id_=None):
        assert start < end
        self.start = start
        self.end = end
        if id_ is not None:
            self.id_ = id_

    def __str__(self):
        return "[{},{})".format(self.start, self.end)

    def __len__(self):
        return self.end - self.start

    def __eq__(self, other):
        if isinstance(other, Interval):
            return (self.start == other.start) and (self.end == other.end)
        else:
            return False

    def __lt__(self, other):
        if self.start < other.start:
            return True
        elif self.start > other.start:
            return False

        if self.end < other.end:
            return True
        elif self.end > other.end:
            return False

        return False

def intersection(lst1, lst2, resetid=False):
    """
    given 2 list of Interval, return intersection.
    input lists need to have unique identifier defined as id_.
    you can access original ids by id1 and id2 respectively.
    """

    # create sorted position list
    pos_lst = [] #(position, id_, isStart, category
    for _, interval in enumerate(lst1):
        if resetid:
            pos_lst.append((interval.start, _, True, 1))
            pos_lst.append((interval.end, _, False, 1))
        else:
            pos_lst.append((interval.start, interval.id_, True, 1))
            pos_lst.append((interval.end, interval.id_, False, 1))
    for _, interval in enumerate(lst2):
        if resetid:
            pos_lst.append((interval.start, _, True, 2))
            pos_lst.append((interval.end, _, False, 2))
        else:
            pos_lst.append((interval.start, interval.id_, True, 2))
            pos_lst.append((interval.end, interval.id_, False, 2))
    pos_lst = sorted(pos_lst, key=lambda x:(x[0],x[2],x[3]))

    # based on sorted position list, extract all the overlap information in overlap_dctdct
    overlap_dctdct = {}
    id1_lst, id2_lst = [], [] # record in-process ids
    for pos in pos_lst:
        if pos[2]:
            key_lst = []
            if pos[3] == 1:
                id1 = pos[1]
                id1_lst.append(id1)
                for id2 in id2_lst:
                    key_lst.append((id1, id2))
            elif pos[3] == 2:
                id2 = pos[1]
                id2_lst.append(id2)
                for id1 in id1_lst:
                    key_lst.append((id1, id2))

            for key in key_lst:
                overlap_dctdct[key] = {}
                overlap_dctdct[key]["start"] = pos[0]
        else:
            key_lst = []
            if pos[3] == 1:
                id1 = pos[1]
                id1_lst.remove(id1)
                for id2 in id2_lst:
                    key_lst.append((id1, id2))
            elif pos[3] == 2:
                id2 = pos[1]
                id2_lst.remove(id2)
                for id1 in id1_lst:
                    key_lst.append((id1, id2))

            for key in key_lst:
                overlap_dctdct[key]["end"] = pos[0]

    # based on overlap_dctdct, created return list of sorted Interval
    ret_lst = []
    for  key, val in overlap_dctdct.items():
        interval = Interval(val["start"], val["end"])
        interval.id1 = key[0]
        interval.id2 = key[1]
        ret_lst.append(interval)
    ret_lst = sorted(ret_lst)
    return ret_lst

def complement(lst, start, end):
    assert start <= end

    pos_lst = [] #(position, isStart)
    for interval in lst:
        pos_lst.append((interval.start, True, 0))
        pos_lst.append((interval.end, False, 0))
    pos_lst.append((start, True, 1))
    pos_lst.append((end, False, 1))
    pos_lst = sorted(pos_lst, key=lambda x:(x[0],x[1])) # end comes before start

    ret_lst = []
    prv = start
    cnt = 0 #count intervals
    id_ = 0
    inProcess = False

    for pos in pos_lst:
        if pos[2] == 1:
            if pos[1]:
                inProcess = True
                prv = pos[0]
            else:
                if cnt == 0 and pos[0] > prv:
                    ret_lst.append(Interval(prv, end, id_))
                break
        elif pos[2] == 0:
            if pos[1]:
                if cnt == 0 and pos[0] > prv and inProcess:
                    ret_lst.append(Interval(prv, pos[0], id_))
                id_ += 1
                cnt += 1
                prv = pos[0]
            else:
                cnt -= 1
                prv = pos[0]
    return ret_lst

def justsum(lst):
    sum = 0
    for interval in lst:
        sum += len(interval)
    return sum

def coverage(lst, start, end):
    assert start <= end
    coverage = (end - start) - justsum(complement(lst, start, end))
    return coverage
