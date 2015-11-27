{% assign category_images = "sensnode|sensnet|senshub" | split: "|" %}
{% if category_images contains page.category %}
  <div>
    <img class="responsive-img" src="/images/categories/{{ page.category }}.png">
  </div>
{% endif %}
