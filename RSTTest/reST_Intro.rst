A brief introduction to *re*\ Structured\ *Text*
************************************************

This is a brief introduction to *re*\ Structured\ *Text*\ . A more complete
description may be found on the
`reST <http://docutils.sourceforge.net/rst.html>`_,
`Sphinx <http://www.sphinx-doc.org>`_ and
`Python <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`_,
`zh-sphinx <http://zh-sphinx-doc.readthedocs.io/en/latest/contents.html>`_,
web pages of, as well as the notes of
`thomas cokelaer <http://thomas-cokelaer.info/tutorials/sphinx/index.html>`_
.

Introduction
============

*re*\ Structured\ *Text* syntax provides an easy-to-read,
what-you-see-is-what-you-get plaintext markup syntax and parser system.

Text Formatting
===============

Special characters and inline markups
-------------------------------------

There are two special text formating characters: ``*`` and `````. The former
is used to produce *italics* and **bold** text and the latter is used to
define ``verbatim`` text as well as to create both internal and external links.
The proper use of these special characters is summarized on the following table

=========== ================================== ==============================
Usage       Syntax                             HTML rendering
=========== ================================== ==============================
italic      ``*italic*``                       *italic*
bold        ``**bold**``                       **bold**
link        ```Python <www.python.org>`_``     `Python`_
verbatim    ````*````                          ``*``
=========== ================================== ==============================

There are, however, some restrictions on the use of ``*`` and `````. They:

    * can not be nested,
    * content may not start or end with whitespace: \* text\* is wrong,
    * it must be separated from surrounding text by non-word characters, like
        a space.

The use of the escape character, ``\``, fixes the last two restrictions.

Headings
--------

Headers are used to break longer text up into sections. These are a single
line of text with an underline (alone), or an underline and an overline
of the same length (which should match the header length). The non-alphanumeric
characters allowed in the declaration of headers are
``= - ` : ' " ~ ^ _ * + # < >``

Internal and external links
---------------------------

In `Sphinx`_ there are 3 types of links:

+----------+----------------------------------------+------------------------------------+
| Type     | Declaration                            | Reference                          |
+==========+========================================+====================================+
| External | ```google <https://www.google.com>`_`` | ```google`_``                      |
|          |                                        |                                    |
+----------+----------------------------------------+------------------------------------+
| Implicit | | ``Internal and external links``      | ```Internal and external links`_`` |
|          | | ``---------------------------``      |                                    |
+----------+----------------------------------------+------------------------------------+
| Explicit | ``.. _myLabel:``                       | ``myLabel_``                       |
|          |                                        | Goes to the location where the     |
|          |                                        | label was declared                 |
|          |                                        |                                    |
|          |                                        | ``:ref: `myLabel```                |
|          |                                        | Goes to the 1st header after the   |
|          |                                        | label declaration                  |
+----------+----------------------------------------+------------------------------------+

Directives
==========

Sphinx and reST directives are the primary syntax extension mechanism. All
directives have a common syntax: ::

    .. Type:: Directive
       block

Directives are used to include specific formated text. For example, the
combination ``Type = code`` and ``Directive = python`` will highly python syntax

.. code:: python

    class MyClass():
        def __init__(self,myNum=1):
            self.myNum=myNum

Boxes
=====

Literal Blocks
--------------

Beside specific directives, there are simples ways to introduce literal
code-blocks, that is to end a paragraph with the double colon marker ``::``
and then insert the desired literal block (which should be indented). For
example::

    ::

        import math
        print 'import math'

produces::

    import math
    print 'import math'

Boxes
-----

Simple directives such as ``note``, ``seealso`` and ``warning``
create nice colored boxes:

note syntax::

    .. note:: This is a **note** box

.. note:: This is a simple **note** box

seealso syntax::

    .. seealso:: This is a **seealso** box

.. seealso:: This is a **seealso** box

warning syntax::

    .. warning:: This is a **warning** box

.. warning:: This is a **warning** box

Topic
-----

This directive allows to write a title and a text within a box. The topic syntax
is as follows::

    .. topic:: Title of you topic

        The rest of the text goes here

.. topic:: Title of you topic

    The rest of the text goes here

Sidebar
-------

The syntax is pretty similar to that of ``topic``::

    .. sidebar:: Here goes the tile

        And the rest goes here

.. sidebar:: Here goes the tile

    And the rest goes here

Miscellaneous
=============

Comments
--------

Comments can made by adding two dots to the beginning of the line::

    .. This will be a comment

Substitutions
-------------

The syntax to define a substitution is::

    .. _Java: http://www.java.com

.. _Java: http://www.java.com

Then, references to them are done by inserting the ``_``-suffixed alias in the
text, i.e., ``Java_`` yields Java_ in this case.

A second way to use substitutions is the following::

    .. |myText| replace:: This is a very long text that will appear over and
        over, better to use a label!!!

.. |myText| replace:: "a very long text that will appear over and
    over, better to use a label!!!"

Now ``|myText|`` will yield |myText|

field list
----------

The syntax to create a new field is::

    :newField: This is the declaration of a new field

:newField: This is the declaration of a new field

glossary
--------

The syntax to create a glossary is::

    .. glossary::
        iconoclast
            A person that does not believe in images of symbols

.. glossary::

    iconoclast
        A person that does not believe in images of symbols.

    apical
        At the top of the plant.

download
--------

If you want to create a link to a file to be downloaded you simply need::

    :download:`download myFile <myFile.py>`

please :download:`download thisFile <reST_Intro.rst>`

hlist
-----

``hlist`` can be used to set a list in several columns::

    .. hlist::
        :columns: 3

        * first item
        * second item
        * 3d item
        * 4th item
        * 5th item

.. hlist::
    :columns: 3

    * first item
    * second item
    * 3d item
    * 4th item
    * 5th item

footnote
--------

For footnotes, use ``[#name]_`` to mark the footnote location, and add the
footnote body at the bottom of the document, after a \`\`Footnotes\`\` rubric
heading, like so::

    Some text that requires a footnote [#f1]_ .

    .. rubric:: Footnotes

    .. [#f1] Text to the first footnote.

Here is an example of how to use auto-numbered footnotes [#]_ [#]_

Including Maths and Equations with Latex
----------------------------------------

The inclusion of latex equations is achieved with the directive ``.. math::``,
however, before doing so, the extension ``sphinx.ext.pngmath`` has to be added
in the ``config.py`` file::

    extensions.append('sphinx.ext.pngmath')

Then, latex-math expressions can be included as:

.. math::

    n_{\mathrm{offset}} = \sum_{k=0}^{N-1} s_k n_k

.. warning::

    The math markup can be used within RST files (to be parsed by Sphinx) but
    within your python\'s docstring, the slashes need to be escaped !

    ``:math:`\alpha``` should therefore be written ``:math:`\\alpha``` or put
    an \"r\" before the docstring




.. rubric:: Footnotes

.. [#] This should be the 1st footnote

.. [#] This should be the 2nd footnote
