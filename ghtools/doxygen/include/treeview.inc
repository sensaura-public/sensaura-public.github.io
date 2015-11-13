<!-- Generate the tree view of all items -->
<ul id="nav-mobile" class="side-nav fixed" style="position: relative;">
  <!-- TODO: Fixed items here -->
  <li class="bold"><a href="index.html" class="waves-effect waves-teal">Overview</a></li>
  <!-- Collapsible menus -->
% for kind in ("file", "enum", "typedef", "struct", "class", "function"):
  % if docItemsByKind.has_key(kind):
  <li class="no-padding">
    <ul class="collapsible collapsible-accordion">
      % if (docItem is not None) and (kind == docItem.kind):
      <li class="bold"><a class="collapsible-header  waves-effect waves-teal active">${getPlural(kind)}</a>
      % else:
      <li class="bold"><a class="collapsible-header  waves-effect waves-teal">${getPlural(kind)}</a>
      % endif
        <div class="collapsible-body">
          <ul>
            % for item in docItemsByKind[kind]:
            % if (docItem is not None) and (docItem.refid == item.refid):
            <li class="active"><a href="${item.refid + '.html'}">${item.name}</a></li>
            % else:
            <li><a href="${item.refid + '.html'}">${item.name}</a></li>
            % endif
            % endfor
          </ul>
        </div>
      </li>
    </ul>
  </li>
  % endif
% endfor
