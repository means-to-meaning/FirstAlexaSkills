from FirstAlexaSkills import lambda_utils


def test_replace_nested_dict_val():
    test_in1 = {"a": "1", "b": {"aa": "11", "bb": {"aaa": "333"}},
                "c": ["3", "4"]}
    test_in2 = {"a": "1", "b": {"aa": "11", "bb": {"aaa": "333"}},
                "c": ["3", "4"]}
    test_in3 = {"a": "1", "b": {"aa": "11", "bb": {"aaa": "333"}},
                "c": ["3", "4"]}
    test_in4 = {"a": "1", "b": {"aa": "11", "bb": {"aaa": "333"}},
                "c": ["3", "4"]}
    test_in5 = {"a": "1", "b": {"aa": "11", "bb": {"aaa": "333"}},
                "c": ["3", "4"]}
    test_in6 = {"a": "1", "b": {"aa": "11", "bb": {"aaa": "333"}},
                "c": ["3", "4"]}
    test_in7 = {"a": "1", "b": {"aa": "11", "bb": {"aaa": "333"}},
                "c": ["3", "4"]}
    test_in8 = {"a": "1", "b": {"aa": "11", "bb": {"aaa": "333"}},
                "c": ["3", "4"]}
    test_1ref = {"a": "test", "b": {"aa": "11", "bb": {"aaa": "333"}},
                 "c": ["3", "4"]}
    test_2ref = {"a": "1", "b": "test", "c": ["3", "4"]}
    test_3ref = {"a": "1", "b": {"aa": "11", "bb": {"aaa": "333"}},
                 "c": "test"}
    test_4ref = {"a": "1", "b": {"aa": "test", "bb": {"aaa": "333"}},
                 "c": ["3", "4"]}
    test_5ref = {"a": "1", "b": {"aa": "11", "bb": "test"},
                 "c": ["3", "4"]}
    test_6ref = {"a": "1", "b": {"aa": "11", "bb": {"aaa": "test"}},
                 "c": ["3", "4"]}
    test_7ref = {"a": {"test": "test"},
                 "b": {"aa": "11", "bb": {"aaa": "333"}},
                 "c": ["3", "4"]}
    test_8ref = {"a": "1", "b": {"aa": "11", "bb": {"aa": "bb"}},
                 "c": ["3", "4"]}
    test_data = [[test_in1, "a", "test", test_1ref],
                 [test_in2, "b", "test", test_2ref],
                 [test_in3, "c", "test", test_3ref],
                 [test_in4, "aa", "test", test_4ref],
                 [test_in5, "bb", "test", test_5ref],
                 [test_in6, "aaa", "test", test_6ref],
                 [test_in7, "a", {"test": "test"}, test_7ref],
                 [test_in8, "bb", {"aa": "bb"}, test_8ref],
                 ]
    for inp, k, v, ref in test_data:
        yield check_replace_nested_dict_val, inp, k, v, ref,


def check_replace_nested_dict_val(test_in, k, v, test_ref):
    test_res = lambda_utils.replace_nested_dict_val(test_in, k, v)
    print(test_res)
    print(test_ref)
    assert test_ref == test_res
