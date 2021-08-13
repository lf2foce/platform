
from jinja2 import Template

# https://geoffruddock.com/sql-jinja-templating/

# Adding a minus sign (-) tells jinja to strip the whitespace before or after a block.

sql = """
SELECT
    date_,
    {%- for event in events %}
    SUM(CASE WHEN event_type = '{{event}}' THEN 1 END) AS num_{{event}}
    {%- if not loop.last -%}
        , 
    {%- endif -%}
    {%- endfor %}
FROM raw_events
GROUP BY 1
ORDER BY 1 ASC
"""

print(Template(sql).render(events=['send', 'deliver', 'open', 'click']))

