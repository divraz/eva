import random
random.seed(10)
from decimal import Decimal

class qualean (object):

    def __init__ (self, real_num : 'an integer from [-1, 0, 1]'):
        '''
        Inspired by Boolean + Quantum concepts. 
        We can assign it only 3 possible real states. True, False, and Maybe (1, 0, -1).
        But it internally picks an imaginary state, an imaginary number random.uniform(-1, 1).
        It multiplies real number with imaginary number and stores that 'magic' number internally after using Bankers rounding to 10th decimal place.
        '''
        if real_num not in [-1, 0, 1]:
            raise ValueError ("Number not in [-1, 0, 1]")
        self._real_num = real_num
        try:
            self._img_num = Decimal (random.uniform (-1, 1))
        except:
            raise ImportError ("Can't find module random")
 
        self._num = 0
        self.magic_number ()

    def magic_number (self):
        '''
        It multiplies the real with imaginary number.
        It uses python math.round function which internally uses banker's algorithm for rounding.
        '''
        self._num = round (self._real_num * self._img_num, 10)

    @property
    def imag (self):
        '''
        The randomly generated imaginary number
        '''
        return self._img_num

    @property
    def real (self):
        '''
        The real number as per input
        '''
        return self._real_num

    @property
    def qual (self):
        '''
        The qualean number
        '''
        return self._num

    def __invertsign__ (self):
        '''
        Invert the sign of Qualean number
        '''
        self._real_num *= -1
        self.magic_number ()

    def __invert__ (self):
        self.__invertsign__ ()
        return self._num
 
    def __mul__ (self, value):
        if isinstance (value, qualean):
            return self._num * value._num
        return self._num * Decimal (value)

    def __add__ (self, value):
        if isinstance (value, qualean):
            return self._num + value._num
        return self._num + Decimal (value)

    def __sqrt__ (self):
        return self._num.sqrt ()

    def __eq__ (self, value):
        if isinstance (value, qualean):
            return self._num == value._num
        return self._num == Decimal (value)

    def __float__ (self):
        return float (self._num)

    def __Decimal__ (self):
        return Decimal (self._num)

    def _cmp (self, value):
        '''
        Compare the two non-NaN decimal instances self and other.
        Returns -1 if self < other, 0 if self == other and 1
        if self > other.    This routine is for internal use only.
        '''
        if isinstance (value, qualean):
            if self._num == value._num:
                return 0
            elif self._num < value._num:
                return -1
            else:
                return 1
        else:
            if self._num == Decimal (value):
                return 0
            elif self._num < Decimal (value):
                return -1
            else:
                return 1

    def __gt__ (self, value):
        return self._cmp (value) > 0

    def __ge__ (self, value):
        return self._cmp (value) >= 0

    def __lt__ (self, value):
        return self._cmp (value) < 0

    def __le__ (self, value):
        return self._cmp (value) <= 0

    def __bool__ (self):
        if self._num == 0:
            return False
        return True

    def __and__ (self, value):
        if not isinstance (value, qualean):
            return False
        if self._num == 0 or value._num == 0:
            return False
        return True

    def __or__ (self, value):
        if self._num != 0:
            return True
        if isinstance (value, qualean) and value._num != 0:
            return True
        return False

    def __repr__ (self):
        return '{0}'.format (self._num)

    def __str__ (self):
        return '{0}'.format (self._num)
