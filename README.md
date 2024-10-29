# district42 experimental types

[![PyPI](https://img.shields.io/pypi/v/district42-exp-types.svg?style=flat-square)](https://pypi.python.org/pypi/district42-exp-types/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/district42-exp-types?style=flat-square)](https://pypi.python.org/pypi/district42-exp-types/)
[![Python Version](https://img.shields.io/pypi/pyversions/district42-exp-types.svg?style=flat-square)](https://pypi.python.org/pypi/district42-exp-types/)

[district42](https://github.com/d42-schemas/district42) experimental types

## Installation

```sh
pip3 install district42-exp-types
```

## Usage

[numeric](https://github.com/d42-schemas/district42-exp-types/blob/master/district42_exp_types/numeric/__init__.py)

```python
from d42 import schema
from d42.declaration import register_type
from district42_exp_types.numeric import NumericSchema

register_type("numeric", NumericSchema)

print(schema.numeric)
```

[uuid](https://github.com/d42-schemas/district42-exp-types/blob/master/district42_exp_types/uuid/__init__.py)
```python
from d42 import schema
from d42.declaration import register_type
from district42_exp_types.uuid import UUIDSchema

register_type("uuid", UUIDSchema)

print(schema.uuid)
```

[uuid_str](https://github.com/d42-schemas/district42-exp-types/blob/master/district42_exp_types/uuid_str/__init__.py)

```python
from d42 import schema
from d42.declaration import register_type
from district42_exp_types.uuid_str import UUIDStrSchema

register_type("uuid_str", UUIDStrSchema)

print(schema.uuid_str)
```

[sdict](https://github.com/d42-schemas/district42-exp-types/blob/master/district42_exp_types/sdict/__init__.py)

```python
from d42 import schema
from d42.declaration import register_type
from district42_exp_types.sdict import SDictSchema

register_type("sdict", SDictSchema)

print(schema.sdict)
```

[unordered](https://github.com/d42-schemas/district42-exp-types/blob/master/district42_exp_types/unordered/__init__.py)

```python
from d42 import schema
from d42.declaration import register_type
from district42_exp_types.unordered import UnorderedSchema

register_type("unordered", UnorderedSchema)

print(schema.unordered)
```
