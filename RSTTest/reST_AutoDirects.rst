Code documentation with the `auto` extension
********************************************

The semi-automatic documentation (**autodoc**) is activated by the inclusion of
the ``sphinx.ext.autodoc`` extension in the ``conf.py`` file. Then the following
additional directives will be available (see
`AutoDocs <http://www.sphinx-doc.org/en/stable/ext/autodoc.html#directive-automodule>`_):

    * ``.. automodule::``
    * ``.. autoclass::``
    * ``.. autoexception::``
    * ``.. autofunction::``
    * ``.. autodata::``
    * ``.. automethod::``
    * ``.. autoattribute::``

By default, the ``automodule``, ``autoclass`` and ``autoexception`` directives
only insert the docstring of the object itself. Some of them accept the
following options:

    * ``:members:`` will recursively document **all**/**non-private** document
      members when used in the **automodule**/**autoclass** context.
    * ``:undoc-members:`` will include members without docstring.
    * ``:private-members:`` will include **_private** or **__private** members.
    * ``:special-members:`` will include **__special__** members.
    * ``:inherited-members:`` will include all **inherited** members.
    * ``:noindex:`` no index entries are generated for the documented object.
    * ``:synopsis:`` to describe the module purpose.
    * ``:deprecated:`` to mark a module as deprecated.
    * ``:platform:`` to enlist all platforms on which the module is available.

The rest of directives behave the same way than the ``class`` directive, but
they do not offer options for member documentation.

``autodata`` and ``autoattribute`` support the **annotation** option. Without
this option, the representation of the object will be shown in the
documentation. When the option is given without arguments, only the name of the
object will be printed.

Use of autofunction
-------------------

::

    .. autofunction:: pyRST_ProgDoc1.func1

.. autofunction:: pyRST_ProgDoc1.func1

Use of automethod
-----------------

::

    .. automethod:: pyRST_ProgDoc1.Class2.func1

.. automethod:: pyRST_ProgDoc1.Class2.func1

Use of autoclass without ``:members:`` option
---------------------------------------------

::

    .. autoclass:: pyRST_ProgDoc1.Class2

.. autoclass:: pyRST_ProgDoc1.Class2

Use of autoclass with ``:members:`` option
------------------------------------------

::

    .. autoclass:: pyRST_ProgDoc1.Class2
        :members:

.. autoclass:: pyRST_ProgDoc1.Class2
    :members:

Use of automodule
-----------------

::
    .. automodule:: pyRST_ProgDoc1
        :members:

.. automodule:: pyRST_ProgDoc1
    :members:

Source Code
-----------

Source code used to study the use of autodocumentation::

    """
    This module illustrates how to write modules' documentation using docstring
    and Sphinx.
    """

    class Class1(object):
        """
        This class docstring shows how to use sphinx and rst syntax

        The first line is a brief explanation, which may be completed with a
        longer one. For instance to discuss about its methods. The only method
        here is :func:`function1`'s. The main idea is to document the class and
        methods's arguments with

        - **parameters**, **types**, **return** and **return types**::

            :param arg1: description
            :param arg2: description
            :type arg1: type description
            :type arg2: type description
            :return: return description
            :rtype: the return type description

        - and to provide section such as **Example** using the double commas
          syntax::

            :Example:

            followed by a blank line!

        which appears as follow:

        :Example:

        followed by a blank line

        - Finally special sections such as **See also**, **Warnings**, **Notes**
          use the sphinx syntax (*paragraph directives*)::

            .. seealso:: seealso bla
            .. warnings also:: warning also bla
            .. note:: note bla
            .. todo:: todo bla

        .. note::
            There are many other Info fields but they may be redundant:
                * param, parameter, arg, argument, key, keyword: Description of
                  parameter.
                * type: Type of a parameter.
                * raises, raises exception, exception: That (and when) a
                  specific exception is raised.
                * var, ivar, cvar: Description of variable.
                * returns, return: Description of the return value.
                * rtype: Return type.

        .. note::
            There are many other directives such as versionadded, versionchange,
            rubric, centered, ... See the sphinx documentation for more details.

        Here below is the results of the :func:`fucntion1`  docstrings.
        """

        def func1(self, arg1, arg2, arg3):
            """
            Returns (arg1/arg2) + arg3

            This is a longer explanation, which may include math with latex
            syntax :math:`\\alpha`.

            Then you need to provide optional section in this order (just to be
            consistent and have a uniform documentation. Nothing prevent you to
            switch the order):

                - parameters using ``:param <name>: <description>``
                - type of the parameters ``:type <name>: <description>``
                - returns using ``:returns: <description>``
                - examples (doctest)
                - seealso using ``.. seealso:: text``
                - notes using ``.. note:: text``
                - warning using ``.. warning:: text``
                - todo ``.. todo:: text``

            **Advantages**:
                - Uses sphinx markups, which will certainly be improved in
                  future version.
                - Nice HTML output with the See Also, Note, Warnings directives.


            **Drawbacks**:
                - Just looking at the docstring, the parameter, type and  return
                  sections do not appear nicely.

            :param arg1: the first value
            :param arg2: the first value
            :param arg3: the first value
            :type arg1: int, float,...
            :type arg2: int, float,...
            :type arg3: int, float,...
            :returns: arg1/arg2 +arg3
            :rtype: int, float

            :Example:

            >>> import template
            >>> a = template.MainClass1()
            >>> a.function1(1,1,1)
            2

            .. note:: can be useful to emphasize important feature
            .. seealso:: :class:`MainClass2`
            .. warning:: arg2 must be non-zero.
            .. todo:: Do do do
            """
            return arg1/arg2 + arg3

        def func2(self, arg1, arg2, arg3):
            """
            Returns arg1 + arg2 + arg3

            This is the 2nd function within the class Class1

            :param arg1: the first value
            :param arg2: the first value
            :param arg3: the first value
            :type arg1: int, float,...
            :type arg2: int, float,...
            :type arg3: int, float,...
            :returns: arg1 + arg2 +arg3
            :rtype: int, float
            """
            return arg1 + arg2 + arg3

    class Class2(object):
        """
        This is the 2nd class of my not very useful module.

        The class implements two methods only.

        :Example:

        Nothing really fancy going on here.

        By the way, this class implements the Object's, null argument
        constructor.
        """

        def func1(self, arg1, arg2, arg3):
            """
            Returns inVar

            This is the 1st function of the class Class2. It returns a instance
            variable.

            :param arg1: the first value
            :param arg2: the first value
            :param arg3: the first value
            :param inVar: the instance variable
            :type arg1: int, float,...
            :type arg2: int, float,...
            :type arg3: int, float,...
            :type inVar: float
            :returns: inVar
            :rtype: float
            """
            inVar = float(10.)
            return inVar

        def func2(self, arg1, arg2, arg3):
            """
            Returns arg1 + arg2 + arg3

            This is the 2nd function within the class Class2. It returns the sum
            of its input parameters.

            :param arg1: the first value
            :param arg2: the first value
            :param arg3: the first value
            :type arg1: int, float,...
            :type arg2: int, float,...
            :type arg3: int, float,...
            :returns: arg1 + arg2 +arg3
            :rtype: int, float
            """
            return arg1 + arg2 + arg3

    def func1(self, arg1, arg2, arg3):
        """
        Returns arg1 + arg2 + arg3

        This is the 1st function of the module. It returns the sum of its input
        parameters.

        :param arg1: the first value
        :param arg2: the first value
        :param arg3: the first value
        :type arg1: int, float,...
        :type arg2: int, float,...
        :type arg3: int, float,...
        :returns: arg1 + arg2 +arg3
        :rtype: int, float
        """
        return arg1 + arg2 + arg3

    if __name__ == "__main__":
        import doctest
        doctest.testmod()
