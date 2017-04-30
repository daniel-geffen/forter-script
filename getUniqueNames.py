from csv import DictReader
from itertools import combinations
from fuzzywuzzy import fuzz
import unittest


def remove_nickname(name):
    first_name = name.split(" ")[0]
    with open("nicknames.csv") as f:
        nickname_list = DictReader(f)
        original_name = " ".join(row["name"] for row in nickname_list if is_equal(row["nickname"], first_name))
        return original_name + " ".join(name.split(" ")[1:]) if original_name else name


def equal_middle_name(name1, name2):
    name1_list, name2_list = name1.split(" "), name2.split(" ")
    shorter_len = min(len(name1_list), len(name2_list))
    name1 = " ".join(name1_list[:shorter_len - 1]) + " " + name1_list[-1]
    name2 = " ".join(name2_list[:shorter_len - 1]) + " " + name2_list[-1]
    return name1, name2


def full_name_equal(name1, name2):
    name1, name2 = equal_middle_name(name1, name2)
    return is_equal(name1, name2)


def is_equal(name1, name2):
    return fuzz.token_sort_ratio(name1, name2) > 90


def count_unique_names(bill_first_name, bill_last_name, ship_first_name, ship_last_name, bill_name_on_card):
    bill_name = remove_nickname(bill_first_name) + " " + bill_last_name
    ship_name = remove_nickname(ship_first_name) + " " + ship_last_name
    bill_name_on_card = remove_nickname(bill_name_on_card.split(" ")[0]) + " " + " ".join(bill_name_on_card.split(" ")[1:])

    num_of_equals = sum(map(lambda x: int(full_name_equal(x[0], x[1])), combinations([bill_name, ship_name, bill_name_on_card], 2)))
    return 3 - min(2, num_of_equals)


class UnitTesting(unittest.TestCase):
    def test1(self):
        self.assertEqual(1, count_unique_names("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli"))

    def test2(self):
        self.assertEqual(1, count_unique_names("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli"))

    def test3(self):
        self.assertEqual(1, count_unique_names("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli"))

    def test4(self):
        self.assertEqual(1, count_unique_names("Deborah s", "Egli", "Deborah", "Egli", "Egli Deborah"))

    def test5(self):
        self.assertEqual(2, count_unique_names("Michele", "Egli", "Deborah", "Egli", "Michele Egli"))

unittest.main()
