
History
=======

2.2.4 (2017-11-13)
------------------

- Do not set ``persist`` property for ``proxy`` blueprint in factory defaults.
  [rnix]

- Translate datatype label used to generate extraction error in
  ``generic_datatype_extractor`` if datatype conversion fails.
  [rnix]

- Add ``generic_datatype_extractor`` to ``email`` blueprint. Allowed datatypes
  are ``str`` and ``unicode``.
  [rnix]

- Prevent ``KeyError`` in ``select_display_renderer`` if multivalued selection
  and a value no longer available in vocab.
  [rnix]


2.2.3 (2017-06-12)
------------------

- Fix ``number_extractor``. Return ``UNSET`` if extracted value is ``UNSET``.
  Check ``min`` and ``max`` for ``None`` explicitely to ensure ``0`` bounds
  get considered.
  [rnix]


2.2.2 (2017-06-07)
------------------

- ``yafowil.common.generic_datatype_extractor`` considers ``emptyvalue`` used
  as default empty value for datatype conversion.
  [rnix]

- Improve ``yafowil.common.select_edit_renderer``. Split up code and consider
  ``datatype`` and ``emptyvalue`` when dealing with vocabularies.
  [rnix]

- ``yafowil.utils.convert_values_to_datatype`` and
  ``yafowil.utils.convert_value_to_datatype`` considers empty value handling
  and accept default ``empty_value`` keyword argument.
  [rnix]

- Introduce ``yafowil.utils.EMPTY_VALUE`` marker.
  [rnix]


2.2.1 (2017-05-15)
------------------

- Introduce ``hybrid_renderer`` and ``leaf`` widget property which gets
  considered in ``hybrid_renderer`` and ``hybrid_extractor``. Use
  ``hybrid_renderer`` in ``div`` blueprint.
  [rnix]

- Consider data attributes in div renderer.
  [rnix]

- Fix rendering of empty div renderer.
  [rnix]

- Explicitely check for ``None`` and ``UNSET`` before rendering empty value in
  ``generic_display_renderer``.
  [rnix]


2.2 (2016-10-06)
----------------

- No changes.


2.2b2 (2016-09-08)
------------------

- Add ``yafowil.utils.entry_point`` decorator to control order of entry point
  loading.
  [rnix, 2016-06-27]


2.2b1 (2016-03-01)
------------------

- Fix typo in ``setup.py``, fixes #26
  [saily, 2016-03-01]

- Improve ``yafowil.base.WidgetAttributes`` to check attribute containment with
  ``__iter__`` instead of ``__getitem__`` catching a ``KeyError``. Speeds up
  whole yafowil test suite (including official addon widgets) by approximately
  18 percent.
  [rnix, 2016-02-07]

- Fix ``yafowil.utils.cssid``. CSS ID's must not contain special characters
  which get normalized now and should not contain whitespaces which get
  replaced by underscore.
  [rnix, 2015-11-30]

- Set ``persist`` factory default to ``True`` for ``hidden``, ``proxy``,
  ``text``, ``textarea``, ``lines``, ``password``, ``checkbox``, ``select``,
  ``email``, ``url`` and ``number`` blueprints.
  [rnix, 2015-11-26]

- Introduce ``yafowil.persistence``, ``RuntimeData.write`` and
  ``RuntimeData.has_errors``.
  [rnix, 2015-11-26]

- Add default ``class`` property to ``lines`` blueprint.
  [rnix, 2015-11-20]

- Use ``generic_emptyvalue_extractor`` in ``hidden``, ``proxy``, ``text``,
  ``textarea``, ``lines``, ``select``, ``file``, ``password``, ``email``,
  ``url``, ``search`` and ``number`` blueprints.
  [rnix, 2015-11-20]

- Use ``generic_datatype_extractor`` in ``hidden``, ``proxy``, ``text``,
  ``lines``, ``select`` and ``number`` blueprints.
  [rnix, 2015-11-19]

- Introduce ``generic_emptyvalue_extractor``.
  [rnix, 2015-11-19]

- Instroduce ``generic_datatype_extractor``.
  [rnix, 2015-11-18]

- Values in ``Widget.attrs`` can also be ``UNSET``.
  [rnix, 2015-11-18]

- Change ``default`` value of ``select`` blueprint from ``list()`` to
  ``UNSET``. This represents both, an empty single valued and an empty
  multi valued selection.
  [rnix, 2015-11-18]

- Fix URL extractor. Must not raise ExtractionError if not required on empty
  input.
  [rnix, 2015-11-18]


2.1.3 (2015-04-12)
------------------

- Fix email extractor. Must not raise ExtractionError if not required on empty
  input.
  [rnix, 2015-04-11]


2.1.2 (2015-01-23)
------------------

- Fix ``compound_extractor`` case if structural child is structural as well
  and skip extraction if so.
  [rnix, 2014-08-29]

- Introduce ``yafowil.resources.YafowilResources`` class which can be used
  as base for resource publishing specific framework integration code.
  [rnix, 2014-08-07]

- Introduce ``configure`` entry points. They are executed after ``register``
  entry points and are supposed to be used for theme configuration (for which
  it's important that all factory defaults are already set)
  [rnix, 2014-08-02]

- Use ``plumbing`` decorator instead of ``plumber`` metaclass.
  [rnix, 2014-08-01]

- Replace ``"`` with ``&quot`` for input values.
  [rnix, 2014-07-16]


2.1.1 (2014-06-10)
------------------

- Package not ZIP safe.
  [chaoflow, 2014-06-10]


2.1 (2014-06-03)
----------------

- Consider ``YAFOWIL_FORCE_DUMMY_TSF`` os.environ variable which can be used
  to force dummy translation string factory when running tests.
  [rnix, 2014-05-13]

- Add translations.
  [rnix, 2014-04-30]

- Add ``yafowil.tsf`` module, which is used to create yafowil related
  translation string factory.
  [rnix, 2014-04-30]

- Re-add ``yafowil.utils.Unset`` class (import from ``node.utils``) for
  backward compatibility reasons.
  [rnix, 2014-04-30]

- Return ``UNSET`` in number extractor if received extracted value is empty
  string.
  [rnix, 2014-03-20]

- Use ``generic_html5_attrs`` in ``tag_renderer``.
  [jensens, 2013-03-06]

- Add default CSS class for ``checkbox`` and ``textarea`` blueprints.
  [rnix, 2013-03-06]

- Float number input seperator may also be comma.
  [rnix, 2013-12-02]

- Don't generate an id attribute for structural widgets. Fixes #6, where the
  same id for all structural elements in a form was generated.
  [thet, 2013-05-27]

- Blueprints accept ``data`` property for generic HTML5 data attributes.
  [rnix, 2013-04-11]

- Introduce ``yafowil.utils.generic_html5_attrs`` helper function.
  [rnix, 2013-04-11]

- Introduce ``with_label`` property for ``checkbox`` blueprint. Useful for
  cross browser compatible checkbox CSS.
  [rnix, 2013-03-29]

- Use json.dumps for data atrribute values to convert Python types to JSON.
  Enclose data-attribute values in single quotes to meet the JSON requirements.
  Convert camelCase data attribute names into camel-case. Since jQuery 1.6 they
  are automatically converted back to camelCase after calling .data().
  [thet]

- Import ``node.utils.UNSET`` in ``yafowil.utils`` instead of providing own
  unset marker class and instance.
  [rnix, 2013-02-10]

- Add helper function for creating a data-attributes dictionary from a list of
  attribute-keys which can be passed to tag-renderer.
  [thet, 2012-12-05]

- Allow passing of a custom html attributes dictionary to textarea_renderer,
  select_edit_renderer and input_generic_renderer. A dictionary is used instead
  of passing them as function parameters to avoid namespace conflicts.
  [thet]


2.0.2
-----

- Consider ``maxlength`` in ``input_attributes_common``.
  [rnix, 2012-11-03]


2.0.1
-----

- Use ``attr_value`` wherever possible to lookup attribute values.
  [rnix, 2012-10-25]

- Introduce ``attr_value`` utility.
  [rnix, 2012-10-25]

- Textarea can have ``title`` attribute.
  [rnix, 2012-10-25]


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
