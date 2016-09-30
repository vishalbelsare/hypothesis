# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis-python
#
# Most of this work is copyright (C) 2013-2016 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import division, print_function, absolute_import

from hypothesis import given
from hypothesis.stateful import GenericStateMachine
from hypothesis.strategies import integers
from hypothesis.internal.detection import is_given, is_hypothesis_test


def test_functions_default_to_not_tests():
    def foo():
        pass
    assert not is_hypothesis_test(foo)
    assert not is_given(foo)


def test_methods_default_to_not_tests():
    class Foo(object):

        def foo():
            pass
    assert not is_hypothesis_test(Foo().foo)
    assert not is_given(Foo().foo)


def test_detection_of_functions():
    @given(integers())
    def test(i):
        pass

    assert is_hypothesis_test(test)
    assert is_given(test)


def test_detection_of_methods():
    class Foo(object):

        @given(integers())
        def test(self, i):
            pass

    assert is_hypothesis_test(Foo().test)
    assert is_given(Foo().test)


def test_detection_of_stateful_tests():
    class Stuff(GenericStateMachine):

        def steps(self):
            return integers()

        def execute_step(self, step):
            pass

    assert is_hypothesis_test(Stuff.TestCase().runTest)
    assert not is_given(Stuff.TestCase().runTest)
