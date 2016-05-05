#!/usr/bin/python
#encoding-utf8

"""
**A summary on programs documentation.**

Module docstring.

It should list the classes, exceptions and functions that are exported by
the module, with a one-line summary of each. The docstring for a package
should also list the modules and subpackages exported by the package.

Script (a stand-alone program) docstring.

It should be usable as its *usage* message, printed when the script is
invoked with incorrect or missing arguments (or perhaps with a "-h" option,
for "help"). Such a docstring should document the script's function and
command line syntax, environment variables, and files. Usage messages can
be fairly elaborate (several screens full) and should be sufficient for a
new user to use the command properly, as well as a complete quick reference
to all options and arguments for the sophisticated user.
"""

class ClassDefinition():
    """
    Class docstring.

    It should summarize its behavior as well as enlist its public methods
    and instance variables.
    """

    def __init__(self):
        """
        Constructor docstring.
        """

    def class_method(self):
        """
        Function/method docstring.

        It should summarize its behavior and document its arguments, return
        values, side effects, exceptions raised and restrictions on when it
        can be called. Also, it should be documented whether keyword
        arguments are part of its interface.
        """

def func_definition(myNum, myString):
    """
    Function/method docstring.

    :param myNum: The number to be returned
    :type myNum: float
    :param myString: The input string
    :type myString: String

    It should summarize its behavior and document its arguments, return
    values, side effects, exceptions raised and restrictions on when it
    can be called. Also, it should be documented whether keyword
    arguments are part of its interface.
    """

    return(float(myNum))

def main():
    """
    The main program.

    """

    isRreal = float(func_definition(6.0))


"""
The main sentinel.

Without it, the code would be executed even if the script is imported as a
module.
"""
if __name__ == "__main__":
    import sys
    import numpy as np
    import matplotlib.pyplot as plt
    main()