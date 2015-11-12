<!-- Generate the tree view of all items -->
<ul id="nav-mobile" class="side-nav fixed">
  <!-- TODO: Fixed items here -->
  <li class="bold"><a href="about.html" class="waves-effect waves-teal">About</a></li>
  <li class="bold"><a href="getting-started.html" class="waves-effect waves-teal">Getting Started</a></li>
  <!-- Collapsible menus -->
% for kind in ("file", "enum", "typedef", "struct", "function"):
  % if docItemsByKind.has_key(kind):
  <li class="no-padding">
    <ul class="collapsible collapsible-accordion">
      <li class="bold"><a class="collapsible-header  waves-effect waves-teal">${kind.capitalize() + "s"}</a>
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
</ul>

