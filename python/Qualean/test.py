import subprocess
import sys

try:
    import memory_profiler
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'memory-profiler'])
finally:
    import memory_profiler
    
from memory_profiler import memory_usage
import pytest
import Qualean
from Qualean import qualean
from decimal import Decimal
import time
import os.path
import re
import inspect 
import random
random.seed(10)
import math

README_CONTENT_CHECK_FOR = [
'__and__',
'__or__',
'__repr__',
'__str__',
'__add__',
'__eq__',
'__float__',
'__ge__',
'__gt__',
'__invert__',
'__le__',
'__lt__',
'__mul__',
'__sqrt__',
'__bool__'
]

def test_qualean_values():
    with pytest.raises(ValueError) as e_info:
        r = qualean (3)

def test_bankers_rounding ():
    q = qualean (1)
    x = str (q.qual)
    x = x.split ('.')[1]
    assert len (x) == 10, x + " 10 decimal places not present"

def test_float_conversion ():
    q = qualean (1)
    x = float (q)
    assert type (x) == type (float ()), "unable to convert to float"

def test_n_times_addition ():
    q = qualean (1)
    x = 0
    for i in range (100):
        x = q + x
    y = q * 100
    assert x==y, "q + q + q ... 100 times = 100 * q"

def test_sqrt_func ():
    q = qualean (1)
    if float (q) < 0:
        ~q
    assert q.__sqrt__() == Decimal(str(q)).sqrt(), "q.__sqrt__() = Decimal(q).sqrt"

def test_one_million_qs_add ():
    x = 0
    for i in range (1000000):
        x = qualean (random.randint(-1, 1)) + x
    assert math.isclose (x, 0, rel_tol = 1), str (x) + " not nearing to 0"

def test_one_million_qs_mul ():
    x = 1
    for i in range (1000000):
        x = qualean (random.randint(-1, 1)) * x
    assert math.isclose (x, 0), "not nearing to 0"

def test_bool_False ():
    q1 = qualean (0)
    assert bool (q1) == False, "bool False operator not working"

def test_bool_True ():
    q1 = qualean (1)
    assert bool (q1) == True, "bool True operator not working"

def test_and_False ():
    q1 = qualean (0)
    q2 = 0
    assert (bool (q1) and q2) == False, "and False not working" 

def test_and_True ():
    q1 = qualean (1)
    q2 = qualean (-1)
    assert (bool (q1) and bool (q2)) == True, "and True not working" 

def test_or_True ():
    q1 = qualean (1)
    q2 = 0
    assert (bool (q1) or q2) == True, "or True not working" 

def test_or_False ():
    q1 = qualean (0)
    q2 = 0
    assert (q2 or bool (q1)) == False, "and False not working" 

def test_invert ():
    q1 = qualean (1)
    y = q1.qual
    ~q1
    x = q1.qual
    assert x + y == 0, "Invert not working"

def test_repr():
    r = qualean (1)
    num = r.qual
    assert r.__repr__() == f'{num}', 'The representation of the Qualean object does not meet expectations'

def test_srt():
    r = qualean (1)
    num = r.qual
    assert r.__str__() == f'{num}', 'The print of the Qualean object does not meet expectations'

def test_eq ():
    q = qualean (1)
    assert q == q, "equality function not working"

def test_ge ():
    q1 = qualean (1)
    q2 = qualean (-1)
    x1 = q1.qual
    x2 = q2.qual
    if x1 >= x2:
    	assert q1 >= q2, "greater than equal to not working"
    else:
    	assert q2 >= q1, "greater than equal to not working"

def test_lt ():
    q1 = qualean (1)
    q2 = qualean (-1)
    x1 = q1.qual
    x2 = q2.qual
    if x1 < x2:
    	assert q1 < q2, "less than not working"
    else:
    	assert q2 < q1, "less than not working"

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 100, "Make your README.md file interesting! Add atleast 500 words"

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    f = open("README.md", "r")
    content = f.read()
    f.close()
    assert content.count("#") >= 3

def test_fourspace():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(Qualean)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert re.search('[a-zA-Z#@\'\"]', space), "Your code intentation does not follow PEP8 guidelines"
        assert len(re.sub(r'[a-zA-Z#@\n\"\']', '', space)) % 4 == 0, \
        "Your code intentation does not follow PEP8 guidelines" 

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(Qualean, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

if __name__ ==  '__main__':
    test_clear_memory()
