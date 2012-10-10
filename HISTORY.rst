
History
=======

2.0
---

- Fix default help text.
  [rnix, 2012-10-10]

- fixed bug in factory returned wrong renderes on call of display_renderers
  [jensens, 2012-10-09]

- renamed plans to macros.
  [rnix, jensens]

- custom chains can be passed as dictionary to the factory.
  [rnix, 2012-09-28]

- introduce ``display_proxy`` property for mode ``display``.
  [rnix, 2012-08-08]

- add generic ``tag`` blueprint.
  [rnix, 2012-08-08]

- adopt to ``plumber`` 1.2.
  [rnix, 2012-07-29]

- adopt to ``node`` 0.9.8.
  [rnix, 2012-07-29]

- pep8ify
  [jensens, 2012-06-08]

- make TBSupplement compatible with both: ```zExceptions``` and
  ```zope.exceptions```. Major change: html output is no longer default and
  the kwarg of getInfo is now ```as_html``` (was ```html```).
  Also added blueprints to the supplement as info to make it easier to identify
  the form part.
  [jensens, 2012-06-07]

1.3.2
-----

- Check with 'if not value' instead of 'if value is None' in
  ``generic_display_renderer``.
  [thet, 2012-05-23]

- Add a title attribute to the label blueprint.
  [thet, 2012-05-02]

- Fix file extractor.
  [rnix, 2012-04-21]

- Avoid rendering of value attribute in file blueprint.
  [rnix, 2012-04-21]

1.3.1
-----

- Label property can be callable.
  [rnix, 2012-02-19]

1.3
---

- Loading resources is done more explicit and in a pluggable way
  using entry-points. Thus yafowil extensions such as widgets
  can define an entry point.
  [jensens, 2012-02-14]

- Add size attribute for ``select`` edit renderer.
  [jensens, 2012-01-20]

- fix number extractor
  [jensens, 2012-01-20]

- Add default css class for ``select`` blueprint.
  [rnix, 2011-12-18]

- Register ``number`` blueprint display renderer.
  [rnix, 2011-12-18]

- Consider ``expression`` in ``submit`` blueprint renderer.
  [rnix, 2011-12-18]

- ``checked`` attribute can be set explicitly in ``checkbox`` blueprint.
  [rnix, 2011-11-21]

- Fix Bug in ``yafowil.common.select_edit_renderer``. Crashed with empty
  vocabularies.
  [rnix, 2011-11-16]

- Add ``lines`` blueprint. Renders a textarea and extracts lines as list.
  [rnix, 2011-11-11]

- Added concept of *plans* to the factory, which is a named set of blueprints.
  Plans are registered to the factory and can be addressed with the ``#`` sign.
  [jensens, 2011-09-29]

- ``td`` blueprint can be used as compound or part of leaf widget now.
  [rnix, 2011-09-28]

- Accept value property on compounds.
  [rnix, 2011-09-27]

- Make ``data.extracted`` available as ``odict`` with values of children on
  compounds.
  [rnix, 2011-09-27]

- Pass ``blueprints`` and ``custom`` arguments to Widget constructor in factory
  for debugging and duplication purposes.
  [rnix, 2011-09-26]

- Rename ``yafowil.base.Widget._properties`` to
  ``yafowil.base.Widget.properties``.
  [rnix, 2011-09-26]

- Add ``div`` blueprint. Renders within '<div>' element. Can be used for
  compound and leaf widgets.
  [rnix, 2011-09-23]

1.2
---

- naming makes a difference between blueprints and widgets
  [jensens, 2011-09-20]

- fix traceback test
  [rnix, 2011-09-15]

1.1.3
-----

- traceback supplement now with html support. test for html part is missing for now.
  [jensens, 2011-09-01]

1.1.2
-----

- traceback supplement is now better formatted.
  [jensens, 2011-08-30]

1.1.1
-----

- Bugfix: mode ``display`` did eat up all previous renderings. This made error
  widget fail in display mode to show the value. Fixed: empty_display_renderer
  proxies now all previous rendered.
  [jensens, 2011-08-11]

1.1
---

- Extend select widget for better UI control of selections and multi selections
  [rnix, 2011-08-05]

- Plumb ``node.parts.Order`` to widget node
  [rnix, 2011-07-28]

- define label and field renderer as display renderer as well
  [rnix, 2011-07-25]

- deprecate use of mode widget
  [rnix, 2011-07-08]

- now mode is a central element: each Widget instance has a mode now: edit,
  display or skip. edit is default and works as usal. Display renders the new
  display_renderer chain. Skip just renders an empty Unicode string.
  [jensens, 2011-07-07]

1.0.4
-----

- clean up html5 handling, we believe in novalidate now...
  [jensens, 2011-06-11]

- add ``disabled`` attribute for select widget.
  [jensens, 2011-06-01]

- add ``novalidate`` property for form
  [rnix, 2011-05-23]

- return empty string in mode renderer if value is UNSET
  [rnix, 2011-05-23]

1.0.3
-----

- test coverage
  [rnix, 2011-05-07]

- add widget value validation checking 'multivalued' property against 'value'
  length.
  [rnix, 2011-05-07]

- remove outdated ``_value``. user ``fetch_value`` instead.
  [rnix, 2011-05-07]

- add optional ``for`` property for label widget.
  [rnix, 2011-04-23]

- select extractor - fix required behavior
  [rnix, 2011-04-19]

- compound renderer - consider 'structural' property on widget node
  [rnix, 2011-04-19]

- number extractor - return val if UNSET
  [rnix, 2011-04-14]

- textarea renderer - check value against None and render empty string instead
  [rnix, 2011-04-14]

1.0.2
-----

- Add ``html5type`` property for email widget
  [rnix, 2011-03-16]

1.0.1
-----

- Add ``html5required`` property
  [rnix, 2011-03-16]

1.0
---

- adopt to node 0.9 [rnix]

- documentation [jensens, rnix]

1.0-beta
--------

- made it work [jensens, rnix, et al, 2010-12-27]
