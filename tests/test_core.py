import contextlib
import io
import sys

import pyset_x


@contextlib.contextmanager
def wrap_stdouterr(new_stdout, new_stderr=None):
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = new_stdout
    if new_stderr:
        sys.stderr = new_stderr
    yield
    sys.stdout = old_stdout
    sys.stderr = old_stderr


def get_stdout(func, *args, **kwargs):
    with io.StringIO() as stdout, wrap_stdouterr(stdout):
        rv = func(*args, **kwargs)
        return rv, stdout.getvalue()


def test_basic():
    @pyset_x.annotate_function
    def basic():
        a = 1 + 1
        return a

    rv, stdout = get_stdout(basic)
    assert rv == 2
    assert stdout.strip() == '''a = 1 + 1\nreturn a'''


def test_nonlocal():
    a = 1

    @pyset_x.annotate_function
    def with_nonlocal():
        return a + a

    rv, stdout = get_stdout(with_nonlocal)
    assert rv == 2
    assert stdout.strip() == '''return a + a'''


def test_calls():
    def foo():
        return 1

    @pyset_x.annotate_function
    def bar():
        return foo() + foo()

    rv, stdout = get_stdout(bar)
    assert rv == 2
    assert stdout.strip() == '''return foo() + foo()'''
