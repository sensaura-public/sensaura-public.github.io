<!-- Generate the tree view of all items -->
  <!-- Collapsible menus -->
  <ul class="collapsible collapsible-accordion">
    <!-- TODO: Fixed items here -->
    <li>
      <div class="collapsible-header">
        <a class="waves-effect waves-teal" href="index.html">Overview</a>
      </div>
    </li>
% for kind in getDocumentedKinds():
  % if docItemsByKind.has_key(kind):
    <li>
    % if (docItem is not None) and (kind == docItem.kind):
      <div class="collapsible-header waves-effect waves-teal active">${getPlural(kind)}</div>
    % else:
      <div class="collapsible-header waves-effect waves-teal">${getPlural(kind)}</div>
    % endif
      <div class="collapsible-body">
        <div class="collection">
          % for item in docItemsByKind[kind]:
          % if (docItem is not None) and (docItem.refid == item.refid):
          <a class="collection-item active" href="${item.refid + '.html'}">${item.getShortName()}</a>
          % else:
          <a class="collection-item" href="${item.refid + '.html'}">${item.getShortName()}</a>
          % endif
          % endfor
        </div>
      </div>
    </li>
  % endif
% endfor
  </ul>
