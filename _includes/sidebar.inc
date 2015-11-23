{% for widget in page.widgets %}
  {% include {{ widget | prepend:'widget_' | append: '.inc' }} %}
{% endfor %}
