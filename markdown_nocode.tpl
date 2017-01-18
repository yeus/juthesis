{% extends 'markdown.tpl' %}

{% block input %}
{#```{% if nb.metadata.language_info %}{{ nb.metadata.language_info.name }}{% endif %}
{{ cell.source}}
```#}
{% endblock input %}
