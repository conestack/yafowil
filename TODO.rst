TODO
====

Rendering after extraction
--------------------------

Rules, to be verified for every widget:

1. A missing request parameter extracts ``UNSET``.
2. An empty request parameter raises an extraction error if the widget is
   required. Otherwise it extracts ``emptyvalue`` if set, else the empty value
   of the widget, see below.
3. The initial rendering renders the preset value. Every rendering after the
   extraction renders the input from the request. A missing parameter renders
   the preset value, e.g. for disabled inputs, which are not submitted.
4. ``emptyvalue`` only affects the extraction, it is not rendered. Undecided,
   see open decisions.

Rule 3 is not met literally today: after a successful extraction
``fetch_value`` renders the extracted, converted value (``10,0`` renders as
``10.0``), after a failed extraction the value before the failing extractor
(``number`` with ``min`` renders the converted value).


Empty value
~~~~~~~~~~~

What "empty" is depends on the widget, ``''`` does not fit e.g. ``datetime``.
yafowil core has a concept for this:

- ``yafowil.utils.EMPTY_VALUE`` (since 2.2.2) identifies empty values in
  conjunction with datatype conversion. It is falsy, renders as ``''``, has
  length 0 and compares ``False``. The required extractor applies to it.
- ``convert_value_to_datatype`` converts ``None`` and ``''`` to
  ``empty_value``, which defaults to ``EMPTY_VALUE``, even for the ``str``
  datatype. ``generic_datatype_extractor`` passes ``emptyvalue`` if set,
  otherwise ``EMPTY_VALUE``.
- Convention by ``test_datatypes.py``: a missing parameter extracts
  ``UNSET``, an empty input ``''`` without ``datatype`` and ``EMPTY_VALUE``
  with ``datatype``, ``emptyvalue`` overrides it (also ``None``, ``-1`` or
  ``UNSET``).
- yafowil.documentation (``usage.rst``): use ``emptyvalue`` for non required
  fields with ``datatype``.

Resulting empty value per widget: ``''`` for string widgets without
``datatype``, ``[]`` for multivalued widgets, ``EMPTY_VALUE`` for typed
widgets (``datetime``, ``time``, ``number``, ``slider``, ...), each
overridable by ``emptyvalue``.

Deviations:

- ``number``: ``number.emptyvalue`` defaults to ``UNSET``, from 2014 ("Return
  ``UNSET`` in number extractor if received extracted value is empty
  string"), before ``EMPTY_VALUE`` existed. Empty and missing are the same.
- ``time`` and ``slider``: an empty input extracts ``UNSET``.
- ``datetime``: an empty and a missing input both extract ``None``.
- ``cron`` uses ``EMPTY_VALUE`` as default ``emptyvalue``, as intended.
- ``select.default`` is ``UNSET``, which "represents both, an empty single
  valued and an empty multi valued selection" (2015). This is the rendering
  default, not the extraction.


Audit
~~~~~

2026-10-26: every widget with a preset value, rendered after the extraction
of an empty input, an empty input with ``emptyvalue`` and a missing
parameter.

Correct:

- ``checkbox``, ``select`` (single, multivalued, radio and checkbox format),
  ``multiselect``, ``chosen``, ``select2`` (all modes), ``dynatree``, ``ace``,
  ``richtext``, ``wysihtml5``, ``array``, ``dict``.
- ``datetime`` and ``time`` with ``is_empty_input`` of
  ``yafowil.widget.datetime`` 2.0.3 (approach A below).
- ``reference`` and ``translation`` of ``cone.app``, by reading the code only.

Open:

- ``number``: an empty input renders the preset value. The fix by approach A
  (``number_edit_renderer``) is postponed.
- ``emptyvalue`` is rendered: ``text``, ``email``, ``url``, ``search``,
  ``hidden``, ``password``, ``textarea``, ``tiptap``, ``color``, ``select``
  (single, no option is selected) and ``lines`` (one character per line).
- Widgets with ``datatype`` and ``emptyvalue=None`` render ``"None"``, after
  the extraction of an empty input and also initially for a preset value
  ``None``, e.g. when editing a record. ``DatatypeConverter.to_form`` converts
  ``None`` to ``'None'``.
- ``select`` with ``datatype`` intends to map ``emptyvalue`` back to the
  ``''`` option by converting the vocabulary keys with
  ``empty_value=emptyvalue``. This fails, the value itself is converted with
  the default ``EMPTY_VALUE``, no option is selected.
- ``slider`` (single): an empty input renders the preset value.
- The extraction of a missing parameter is not ``UNSET`` (rule 1), changing
  this changes extracted values:

  - ``lines``: ``[]``, renders empty instead of the preset value.
  - ``slider`` (range): ``[UNSET, UNSET]``, renders empty instead of the
    preset value.
  - ``autocomplete``: ``{'value': UNSET}``, renders empty instead of the
    preset value.
  - ``datetime``: ``None``, renders the preset value by its own preset logic.

  Check whether these values get persisted, e.g. for disabled inputs.
- ``cron``: rendering after the extraction of an empty input raises a
  ``TypeError`` in ``compound_renderer``, the extracted ``EMPTY_VALUE`` is no
  container. Also without preset value.
- ``location``: the renderer fails if ``emptyvalue`` is neither a dict nor
  ``None``.
- ``proxy`` renders the preset value for an empty request value. It
  transports a value and is no user input, probably intended.
- ``array`` has no exists marker, an empty and a missing input both extract
  ``[]``.
- Not audited: ``file`` and ``image`` (no value rendering) and
  ``yafowil.plone``.


Approaches
~~~~~~~~~~

A. Request lookup in the renderers: an empty request value renders ``''``.
   Implemented for ``datetime`` and ``time`` (``is_empty_input`` in
   ``yafowil.widget.datetime``) and for ``number``, postponed::

       @managedprops(*css_managed_props)
       def number_edit_renderer(widget, data):
           if data.request and data.request.get(widget.dottedpath) == '':
               return input_generic_renderer(
                   widget, data, custom_attrs={'value': ''}
               )
           return input_generic_renderer(widget, data)

   Generalized as a core function used by the renderers of plain inputs only
   (working name ``fetch_input_value``), returning ``''`` if the input was
   submitted empty, otherwise ``fetch_value``. Used in
   ``input_generic_renderer`` (``text``, ``email``, ``url``, ``search``,
   ``hidden``, ``number``), ``textarea``, ``password``, ``lines`` and
   ``select`` (single). ``tiptap``, ``color``, ``datetime`` and ``time`` use
   it as well and require ``yafowil>=4.1.0``, ``is_empty_input`` of
   ``yafowil.widget.datetime`` is dropped. ``slider``, ``cron``, ``location``
   and ``autocomplete`` are fixed in their packages.

B. Request lookup in ``fetch_value``: patching ``fetch_value`` to return
   ``''`` for an empty request value fixes ``text``, ``number`` and ``time``,
   but breaks two tests of the root test run. ``checkbox`` with
   ``display_proxy``: ``''`` means checked with an empty value attribute, the
   patch renders "No". ``select2`` multivalued with ``display_proxy``: ``''``
   means an empty list, the patch renders a hidden input with an empty value.
   The meaning of an empty request value depends on the widget. The
   ``datetime`` renderer does not use ``fetch_value`` at all. Rejected.

C. Correct extraction: if every widget extracts ``UNSET`` for a missing
   parameter and its empty value for an empty input, ``fetch_value`` renders
   correctly without looking at the request. ``EMPTY_VALUE`` renders as
   ``''``, ``UNSET`` falls back to the preset value. Remaining is a set
   ``emptyvalue``: the renderer maps it back to empty, as ``select`` intends.
   This applies to the initial rendering as well: a preset value equal to
   ``emptyvalue`` (e.g. ``0``) renders empty, saving again extracts the same
   value. For ``None`` it fixes the ``"None"`` rendering. Changes extracted
   values (API): ``number`` and ``time`` ``UNSET`` -> ``EMPTY_VALUE``,
   ``datetime`` for a missing parameter ``None`` -> ``UNSET``. A default
   ``datetime.emptyvalue = None`` keeps the extraction of an empty input.
   Without ``emptyvalue``, ``EMPTY_VALUE`` gets persisted, as already for
   typed core widgets. Likely supersedes A.

For every widget, first write a test covering exactly this behavior, e.g.
for ``number`` (postponed with the fix):

- An empty input renders empty, not the preset value.
- A missing input renders the preset value.
- An invalid input renders as entered.
- With ``emptyvalue``, the extracted value is ``emptyvalue`` and it renders
  empty.
- A required empty input renders empty with an extraction error (already
  correct for all widgets).


Open decisions
~~~~~~~~~~~~~~

- ``emptyvalue`` when rendering after the extraction, e.g. after a
  validation error of another field. Rendering it is convenient and matches
  what the next edit of the saved record shows. Rendering empty keeps the
  round trip: submitting the re-rendered form unchanged extracts the same
  value again. A rendered ``emptyvalue`` becomes user input, which does not
  survive the extractor chain unchanged if it is ``None``, an object, a
  converted type or fails validation, the required extractor does not apply
  anymore, and the user sees a value they did not enter. To hint what an
  empty input means, ``placeholder`` can be used. Recommendation: render
  empty.
- Approach A or C.
- With A: core function and ``yafowil>=4.1.0`` for the addons, or fixes per
  package.
- Fix the extraction of missing parameters together with the rendering, or
  separately.


yafowil.widget.array
--------------------

- ``set_row_index`` (``js/src/base/array.js``) derives the base name of the
  array from its css id by replacing ``-`` with ``.``. ``cssid`` replaces
  ``.`` with ``-`` and spaces with ``_`` and drops non ASCII characters, so
  this is lossy. For array names containing ``-``, spaces or umlauts the
  ``name`` attributes are not reindexed after row actions: added rows keep
  ``TEMPLATE``, after removing row 0 the names start at ``.1`` and the
  extractor stops at index 0, all entries are lost on submit.

  Plan: ``array_wrapper_renderer`` renders ``data-name="<dottedpath>"`` on
  the wrapper, ``set_row_index`` reads the base name from it (``attr``, not
  ``data``, jQuery caches data). ``data-name`` of nested arrays is reindexed
  like ``name``, the template contains
  ``data-name="form.outer.TEMPLATE.inner"``. The Python tests with expected
  HTML get the attribute (about 30), JS tests for names with ``-``, spaces and
  umlauts and for nested arrays. Rejected: deriving the base name from
  rendered input names is ambiguous for nested arrays and numbers in names,
  and there is no template with ``add=False``.
