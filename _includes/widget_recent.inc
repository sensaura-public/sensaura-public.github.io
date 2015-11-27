<div class="widget blue-grey lighten-5">
  <div class="title">Recent Posts</div>
{% assign counter = 0 %}
{% for post in site.posts %}
  {% if counter < 4 %}
  {% assign counter = counter | plus:1 %}
  <div>
    <h3>{{ post.title }}</h3>
    <div class="byline">
      {{ post.date | date_to_string }} |
      <a href="{{ post.url }}#disqus_thread" data-disqus-identifier="{{ post.url }}">Comments</a> |
      <a href="{{ post.url }}">Read more ...</a>
    </div>
    <p>{{ post.excerpt }}</p>
  </div>
  {% endif %}
{% endfor %}
</div>
