
# Enums

*8th October 2018*, by Dave Willmer


This lesson is about using enums to improve the code. We will use python as an example,
but the main point applies to any programming language - explicitly enumerate the options
available in one place, and your code will be cleaner.

### Basic Usage

To define a simple enum in python, import the `Enum` class from the standard library:

```python
from enum import Enum
```

This has been part of the standard library since 3.4, but is available via `pip` for
earlier language versions.

After this, you can define a standard enum by adding class-side attributes:

```python
class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
```

The usual way to select an enum value is like `Direction.NORTH`, however the python
`Enum` class has some nice extra properties.

Firstly, if you are accepting user input
or selections, you can pass a string directly to the class, and it will either
return the enum value, or raise a ValueError:

```bash
>>> Direction('NORTH')
<Direction.North: 1>
>>> Direction('SOUTH_EAST')
Traceback (most recent call last):
...
ValueError: 'SOUTH_EAST' is not a valid Direction
```

You can also iterate over an enum:

```python
for item in Direction:
    print(item)
```

Allowing you to get the string values:

```python
names = [x.name for x in Direction]
```

As of Python 3.6, you can also have python create the enum values automatically:

```python
from enum import auto, Enum


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
```

This is incredibly useful in case you may have developers add options later, as it
prevents mistakes with the numbering.

There is also an `@unique` decorator to ensure that values aren't
duplicated (a common enum-related error in large programming teams):

```python
from enum import Enum, unique


@unique
class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 3  # This number is wrong (duplicated)
```

In the case above, the `@unique` decorator will raise an error when it
is parsed (effectively at 'compile' time), to warn that the values
are not unique.

In large projects you do see cases of multiple identical attributes
being addded to an enum because later developers missed the original
declaration, so `@unique` is extremely useful.

The style of enum shown above is similar to C++/old-Java
enums, and whilst it is better than not using an enum, it still has
major issues.

When we associate a label with an integer or string value, as shown in
the simple examples above, we have removed a number of potential bugs
from mistyped string labels, however we still need huge amounts of
control flow logic all over the codebase to use them.

Taking the `Direction` example above, if we took a user input to move
a character around in a game, our code may look like this:

```python
def move(self, user_input):
    value = Direction(user_input)
    if value == Direction.NORTH:
        self.move_north()
    elif value == Direction.SOUTH:
        self.move_south()
    elif value == Direction.EAST:
        self.move_east()
    elif value == Direction.WEST:
        self.move_west()
```

As you can see, we have to have large control flow blocks to denote the
appropriate logic for each enum value, at each place the enum is used.

Having many places where we need to update the code in order to add an
option is a major cause of software errors.

The fix is to use Enums in a slightly more sophisticated way, so that
the logic required is contained within the enum definition. This is
demonstrated in the next section. If this is implemented correctly,
you should never need to use an `if` statement to compare an enum value.

> **Note:** This is important enough to repeat; you should *never* need
  to use an `if` statement to compare an enum value.

### Rich objects as Enum values

A more advanced use of Enums is to have richer python objects as the
enum values instead of strings/integers. The python docs have a [nice example here](https://docs.python.org/3/library/enum.html#planet),
but we will carry on with the `Direction` example from the previous
section.

As shown previously, we usually want to execute a different piece of
logic depending on which enum value is chosen (if the player selects
`Direction.NORTH`, we want to run the method `self.move_north()`).

To achieve this, we can simply use a python function as the enum value:

```python
from enum import Enum, unique


@unique
class Direction(Enum):
    NORTH = move_north
    SOUTH = move_south
    EAST = move_east
    WEST = move_west
```

> Note that we are not **calling** the functions (there are no
  parentheses). We are just assigning the function objects as the
  enum values.

With a system such as this, instead of getting given an integer, we
get passed the function when we select an enum value. In this case,
the large `if:elif` block above turns into this:

```python
def move(self, user_input):
    value = Direction(user_input)
    value()
```

As you can see, this is much more elegant code, with very little room
for error.

Most importantly, adding a new enum value does **not** require changing
any part of the codebase except the enum definition itself.

For example:

```python
from enum import Enum, unique


@unique
class Direction(Enum):
    NORTH = move_north
    SOUTH = move_south
    EAST = move_east
    WEST = move_west
    SOUTH_EAST = move_south_east
    SOUTH_WEST = move_south_west
```

which significantly reduces both the development time to add new
behaviour, *and* reduces the chance of introducing bugs.

> This is extremely important; correct usage of enums with rich objects
  reduces complexity, development time and the number of possible bugs.

This works well for simple cases, however in reality we tend to use
Enums in multiple places and we perform different tasks with them at
different places in the codebase.

For example, in our hypothetical game we may want to let the user
select the direction in one part of the code (as shown above), but in
another part of the code we might want to reverse the direction
of the character.

In this case we have multiple different pieces of logic that we might
want to execute for each enum value, depending on the situation.

To do this, we need a more sophisticated setup than just assigning
functions.

### Advanced Usage

As you may have guessed by now, one way of achieving multiple pieces of
logic is to use classes as enum values:

```python
from abc import ABC, abstractmethod
from enum import Enum, unique

class AbstractEnumValue(ABC):
    @abstractmethod
    def move(self):
        """ Executed when the user selects move """

    @abstractmethod
    def reverse(self):
        """ Returns the opposite direction """


class North(AbstractEnumValue):
    def move(self):
        move_north()

    def reverse(self):
        return Direction.SOUTH


class South(AbstractEnumValue):
    def move(self):
        move_south()

    def reverse(self):
        return Direction.NORTH


@unique
class Direction(Enum):
    NORTH = North()
    SOUTH = South()

    def __init__(self, item):
        self.item = item
```

This might seem a little complicated, so lets walk through each
component. It's easiest to start with the Enum definition at the
bottom and move upwards:

- We want the enum values to be objects (or classes) which implement
  the behaviours required throughout the codebase. We have chosen to
  have class instances as the values here (ie, `NORTH = North()`).
- With objects as values, we don't get passed the object directly -
  we have to implement an `__init__` (constructor) method which will
  be called implicitly when the enum value is selected. When we execute
  `Direction.NORTH`, the `North()` instance which is created at import
  time is automatically passed to the constructor, and we store it as
  `self.item`.
- In order to access this object, we then have to do
  `Direction.NORTH.item.move()` or `Direction.NORTH.item.reverse()`,
  ie, it is the `.item` access which now returns the raw enum value.
- Moving upwards through the code, we have defined `North` and `South`
  classes which implement the required `move()` and `reverse()`
  interface.
- In order to ensure that the interfaces are implemented, we have used
  an Abstract Base Class for the Enum value base class. This is very
  important: in a changing codebase people will add or modify the
  interface, but may forget to update all subclasses with a new
  implementation. By using an `ABC` along with class instances on the
  Enum, we will get an early import-time error if the interface hasn't
  been implemented properly.

> **Task:** Try this for yourself; add a new function to the `ABC`,
  and only implement it on one of the subclasses. You should get a
  `TypeError: Can't instantiate abstract class` at import time.

You can also implement the `ABC` interface on the Enum class, in order
to avoid having to access the object via `item`:

```python
@unique
class Direction(Enum):
    NORTH = North()
    SOUTH = South()

    def __init__(self, item):
        self._item = item

    def move(self):
        self._item.move()

    def reverse(self):
        self._item.reverse()
```

This removes the need to use the `.item` accessor to call the value
methods, at the expense of needing to update the Enum class when adding
methods to the interface.

With this, you would call move with `Direction.NORTH.move()`.

Unfortunately, due to the use of metaclasses for `ABC`s, you can't
have `Direction` inherit from the `AbstractEnumValue` class, which
could be a potential source of errors.

You don't have to use a class hierarchy to store multiple pieces of
logic; you can do the same using a tuple instead of a class:

```python
from enum import Enum, unique


@unique
class Direction(Enum):
    NORTH = (move_north, reverse_north)
    SOUTH = (move_south, reverse_south)

    def __init__(self, *args):
        self.move = args[0]
        self.reverse = args[1]
```

However, you do lose some of the benefits of the class hierarchy - this
tuple option becomes difficult to maintain as the number of items and
size of the tuple grows.

The class hierarchy version scales much better, although still requires
discipline.


### Conclusion

We have seen that Enums clean up the codebase in multiple ways. For
any concept where there is a well-defined (enumerated) set of options,
you should **always** try to use an `enum`. This will reduce errors from
declaring labels/integer codes in multiple places.

We have also seen that more advanced uses of enums (function / object
values) carry all the benefits of the simple enums, and also help
reduce complex control flow throughout the wider codebase.

If you follow the pattern of having class instances as the enum values,
all of which share the same interface through the `ABC` base class,
then you have:
- A well-defined interface so developers/users know what to expect
- Early `compile-time` warnings of any mistakes.
- Well-separated code for each enum value.
- No changes required to control flow in the wider codebase when
  adding/modifying the Enum values.

> **Task:** Build a class instance-based Enum which solves a coding
  problem you are currently working on. Then try to break it. If you
  use `Enum`, `unique`, `ABC` in the definition, is it possible to
  import an incorrectly defined Enum?
