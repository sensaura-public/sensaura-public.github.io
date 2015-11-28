<div class="widget blue-grey lighten-5">
  <div class="title">Recent Posts</div>
{% assign counter = 0 %}
{% for post in site.posts %}
  {% if counter < 3 %}
  {% assign counter = counter | plus:1 %}
  <div>
    <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
    <div class="byline">
      {{ post.date | date_to_string }} |
      <a href="{{ post.url }}#disqus_thread" data-disqus-identifier="{{ post.url }}">Comments</a>
    </div>
    <p>{{ post.excerpt | markdownify }}</p>
  </div>
  {% endif %}
{% endfor %}
</div>
