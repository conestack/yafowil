Table rendering
---------------

Table elements are available as blueprints, often one wanta to organize
form elements inside a table, providing pretty looking forms::

    >>> from yafowil.base import factory
    >>> import yafowil.common
    >>> import yafowil.compound
    >>> import yafowil.table
    >>> factory(
    ...     'table',
    ...     name='foo')()
    u'<table></table>'

    >>> factory(
    ...     'table',
    ...     name='foo_table',
    ...     props={
    ...         'id': 'id',
    ...         'class': 'css'
    ...     })()
    u'<table class="css" id="id"></table>'

    >>> factory(
    ...     'table',
    ...     name='foo',
    ...     mode='display')()
    u'<table></table>'

    >>> factory(
    ...     'thead',
    ...     name='foo')()
    u'<thead></thead>'

    >>> factory(
    ...     'thead',
    ...     name='foo',
    ...     mode='display')()
    u'<thead></thead>'

    >>> factory(
    ...     'tbody',
    ...     name='foo')()
    u'<tbody></tbody>'

    >>> factory(
    ...     'tbody',
    ...     name='foo',
    ...     mode='display')()
    u'<tbody></tbody>'

    >>> factory(
    ...     'tr',
    ...     name='foo')()
    u'<tr></tr>'

    >>> factory(
    ...     'tr',
    ...     name='foo',
    ...     mode='display')()
    u'<tr></tr>'

    >>> factory(
    ...     'tr',
    ...     name='foo',
    ...     props={
    ...         'id': 'id',
    ...         'class': 'css'
    ...     })()
    u'<tr class="css" id="id"></tr>'

    >>> factory(
    ...     'th',
    ...     name='foo')()
    u'<th></th>'

    >>> factory(
    ...     'th',
    ...     name='foo',
    ...     mode='display')()
    u'<th></th>'
    
    >>> factory(
    ...     'th',
    ...     name='foo',
    ...     props={
    ...         'id': 'id',
    ...         'class': 'css',
    ...         'colspan': 2,
    ...         'rowspan': 2,
    ...     })()
    u'<th class="css" colspan="2" id="id" rowspan="2"></th>'

    >>> factory(
    ...     'td',
    ...     name='foo')()
    u'<td></td>'

    >>> factory(
    ...     'td',
    ...     name='foo',
    ...     mode='display')()
    u'<td></td>'

    >>> factory(
    ...     'td',
    ...     name='foo',
    ...     props={
    ...         'id': 'id',
    ...         'class': 'css',
    ...         'colspan': 2,
    ...         'rowspan': 2,
    ...     })()
    u'<td class="css" colspan="2" id="id" rowspan="2"></td>'

    >>> form = factory(
    ...     'form',
    ...     name='myform',
    ...     props={
    ...         'action': 'myaction',
    ...     })
    >>> form['table'] = factory('table')
    >>> form['table']['row1'] = factory('tr')
    >>> form['table']['row1']['field1'] = factory(
    ...     'td:text',
    ...     name='field1')
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" 
      method="post" novalidate="novalidate">
      <table>
        <tr>
          <td>
            <input class="text" id="input-myform-table-row1-field1" 
              name="myform.table.row1.field1" type="text" value=""/>
          </td>
        </tr>
      </table>
    </form>
    <BLANKLINE>

Build same table again but set some nodes structural. This is considered in
``Widget.dottedpath``::

    >>> form = factory(
    ...     'form',
    ...     name='mytableform',
    ...     props={
    ...         'action': 'mytableaction',
    ...     })
    >>> form['table'] = factory(
    ...     'table',
    ...     props={
    ...         'structural': True
    ...     })
    >>> form['table']['row1'] = factory(
    ...     'tr',
    ...     props={
    ...         'structural': True
    ...     })
    >>> form['table']['row1']['field1'] = factory(
    ...     'td:error:text',
    ...     props={
    ...         'required': 'Field 1 is required',
    ...     }
    ... )
    >>> pxml(form())
    <form action="mytableaction" enctype="multipart/form-data" 
      id="form-mytableform" method="post" novalidate="novalidate">
      <table>
        <tr>
          <td>
            <input class="required text" id="input-mytableform-field1" 
              name="mytableform.field1" required="required" type="text" 
              value=""/>
          </td>
        </tr>
      </table>
    </form>
    <BLANKLINE>

    >>> data = form.extract({})
    >>> data.printtree()
    <RuntimeData mytableform, value=<UNSET>, 
      extracted=odict([('field1', <UNSET>)]) at ...>
      <RuntimeData mytableform.field1, value=<UNSET>, extracted=<UNSET> at ...>

    >>> data = form.extract({'mytableform.field1': ''})
    >>> data.printtree()
    <RuntimeData mytableform, value=<UNSET>, extracted=odict([('field1', '')]) 
      at ...>
      <RuntimeData mytableform.field1, value=<UNSET>, extracted='', 
        1 error(s) at ...>

    >>> pxml(form(data))
    <form action="mytableaction" enctype="multipart/form-data" 
      id="form-mytableform" method="post" novalidate="novalidate">
      <table>
        <tr>
          <td>
            <div class="error">
              <div class="errormessage">Field 1 is required</div>
              <input class="required text" id="input-mytableform-field1" 
                name="mytableform.field1" required="required" type="text" 
                value=""/>
            </div>
          </td>
        </tr>
      </table>
    </form>
    <BLANKLINE>

Create table with 'td' as compound::

    >>> form = factory(
    ...     'form',
    ...     name='mytableform',
    ...     props={
    ...         'action': 'mytableaction',
    ...     })
    >>> form['table'] = factory(
    ...     'table',
    ...     props={
    ...         'structural': True
    ...     })
    >>> form['table']['row1'] = factory(
    ...     'tr',
    ...     props={
    ...         'structural': True
    ...     })
    >>> form['table']['row1']['td1'] = factory(
    ...     'td',
    ...     props={
    ...         'structural': True
    ...     })
    >>> form['table']['row1']['td1']['field1'] = factory(
    ...     'error:text',
    ...     props={
    ...         'required': 'Field 1 is required',
    ...     }
    ... )
    >>> pxml(form())
    <form action="mytableaction" enctype="multipart/form-data" 
      id="form-mytableform" method="post" novalidate="novalidate">
      <table>
        <tr>
          <td>
            <input class="required text" id="input-mytableform-field1" 
              name="mytableform.field1" required="required" type="text" 
              value=""/>
          </td>
        </tr>
      </table>
    </form>
    <BLANKLINE>

    >>> data = form.extract({})
    >>> data.printtree()
    <RuntimeData mytableform, value=<UNSET>, 
      extracted=odict([('field1', <UNSET>)]) at ...>
      <RuntimeData mytableform.field1, value=<UNSET>, extracted=<UNSET> at ...>

    >>> data = form.extract({'mytableform.field1': ''})
    >>> data.printtree()
    <RuntimeData mytableform, value=<UNSET>, 
      extracted=odict([('field1', '')]) at ...>
      <RuntimeData mytableform.field1, value=<UNSET>, 
        extracted='', 1 error(s) at ...>

    >>> pxml(form(data))
    <form action="mytableaction" enctype="multipart/form-data" 
      id="form-mytableform" method="post" novalidate="novalidate">
      <table>
        <tr>
          <td>
            <div class="error">
              <div class="errormessage">Field 1 is required</div>
              <input class="required text" id="input-mytableform-field1" 
                name="mytableform.field1" required="required" type="text" 
                value=""/>
            </div>
          </td>
        </tr>
      </table>
    </form>
    <BLANKLINE>
