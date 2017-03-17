from .. import lambda_function


def test_get_something():
    test_ref = "I say whatever I please"
    res = lambda_function.get_something()
    assert res == test_ref


def test_get_coolest():
    subject = "movie"
    test_ref = ["Lord of the rings", "Batman, the dark knight", "Indiana Jones"]
    res = lambda_function.get_coolest(subject)
    assert res in test_ref


def test_get_coolest2():
    subject = "space shuttles"
    test_ref = "I don't know much about " + str(subject) + " yet"
    res = lambda_function.get_coolest(subject)
    assert res in test_ref


def test_get_person_fact():
    person = 'catherine'
    test_ref = 'catherine works at amazon building models for alexa'
    res = lambda_function.get_person_fact(person)
    assert res == test_ref


def test_get_person_fact2():
    person = "Johnny Depp"
    test_ref = 'i don\'t know much about ' + person
    res = lambda_function.get_person_fact(person)
    assert res == test_ref
