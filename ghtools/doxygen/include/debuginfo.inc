<!--- Just display the contents of docItem -->
% if docItem is None:
  No 'docItem' instance.
% else:
<h1>Item Details</h1>
<table>
  <thead>
    <tr>
      <th data-field="id">Name</th>
      <th data-field="name">Value</th>
    </tr>
  </thead>
  <tbody>
  % for key in docItem.__dict__.keys():
    <tr>
      <td>${key}</td>
      <td>${docItem.__dict__[key]}</td>
    </tr>
  % endfor
  </tbody>
</table>
  % if docItem.parent is not None:
  <h1>Parent Details</h1>
  <table>
    <thead>
      <tr>
        <th data-field="id">Name</th>
        <th data-field="name">Value</th>
      </tr>
    </thead>
    <tbody>
    % for key in docItem.parent.__dict__.keys():
      <tr>
        <td>${key}</td>
        <td>${docItem.parent.__dict__[key]}</td>
      </tr>
    % endfor
    </tbody>
  </table>
  % endif
% endif

