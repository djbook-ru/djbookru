#!/usr/bin/env python

# htmlentitydecode: Decode html entities
# Copyright (C) 2010  Niels Serup

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Do What The Fuck You Want To Public
# License as published by Sam Hocevar, either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the Do
# What The Fuck You Want To Public License for more details.
#
# You should have received a copy of the Do What The Fuck You Want To
# Public License along with this program. If not, see
# <http://sam.zoy.org/wtfpl/>.

# Version:...... 0.1.1
# Maintainer:... Niels Serup <ns@metanohi.org>
# Website:...... http://metanohi.org/projects/htmlentitiesdecode/
# Development:.. http://gitorious.org/htmlentitiesdecode

# This is a Python module.
import re
from htmlentitydefs import name2codepoint
try:
    # Using functools requires Python 2.5+
    from functools import partial
    _PARTIAL_EXISTS = True
except ImportError:
    _PARTIAL_EXISTS = False

if _PARTIAL_EXISTS:
    _int16 = partial(int, base=16)
else:
    _int16 = lambda i: int(i, 16)

_entity_text = re.compile('&(%s);' % '|'.join(name2codepoint))
_entity_base10 = re.compile('&#(\d+);')
_entity_base16 = re.compile('&#x([0-9a-fA-F]+);')

_entity_text_decode = lambda m: unichr(name2codepoint[m.group(1)])
_entity_base10_decode = lambda m: unichr(int(m.group(1)))
_entity_base16_decode = lambda m: unichr(_int16(m.group(1)))

if _PARTIAL_EXISTS:
    _entity_text_sub = partial(_entity_text.sub, _entity_text_decode)
    _entity_base10_sub = partial(_entity_base10.sub,
                                 _entity_base10_decode)
    _entity_base16_sub = partial(_entity_base16.sub,
                                 _entity_base16_decode)
else:
    _entity_text_sub = lambda t: _entity_text.sub(
        _entity_text_decode, t)
    _entity_base10_sub = lambda t: _entity_base10.sub(
        _entity_base10_decode, t)
    _entity_base16_sub = lambda t: _entity_base16.sub(
        _entity_base16_decode, t)

# The core function of the module
def decode(text):
    """Decode html entities."""
    return _entity_base10_sub(_entity_base16_sub(_entity_text_sub(text)))
