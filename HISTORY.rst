
History
=======

1.2
--------

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
