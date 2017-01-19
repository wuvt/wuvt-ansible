#!/usr/bin/python3

import json
import re
import textwrap


def process_content(content, indent=4):
    content = content.replace(" | replace('\n', '\\n')", " | indent({}, false)".format(indent))
    content = content.replace("'\\n'", "'\\\\n'")
    content = content.replace("'\n'", "'\\n'")
    return content


data = open('ignition.json.j2').read()

replace_re = re.compile(r'{%.*%}')
data = replace_re.sub('', data)
data = data.replace('{{ ssh_authorized_keys | to_json }}', '[]')

replace2_re = re.compile(',\n\s+{{ ignition_extra.* }}')
data = replace2_re.sub('', data)

d = json.loads(data)

print("""\
#cloud-config

ssh_authorized_keys:
{% for key in ssh_authorized_keys -%}
- {{ key }}
{% endfor %}
""")

print('write_files:')
for f in d['storage']['files']:
    contents = process_content(f['contents']['source'][6:])

    if 'user' in f and len(f['user']) > 0:
        owner = f['user']
        if 'group' in f and len(f['group']) > 0:
            owner += ':{}'.format(f['group'])
    else:
        owner = "root"

    print("""\
- path: {path}
  permissions: {permissions}
  owner: {owner}
  content: |
{content}""".format(
        path=f['path'],
        permissions=oct(f['mode'])[2:],
        owner=owner,
        content=textwrap.indent(contents, ' ' * 4)))
print("""\
{% for f in ignition_extra_files -%}
- path: {{ f.path }}
  permissions: {{ "%o" | format(f.mode | default(420)) }}
  {% if 'user' in f -%}
  owner: {{ f.user }}{% if 'group' in f %}:{{ f.group }}{% endif %}
  {% endif -%}
  content: |
    {{ f.contents.source | replace('data:,', '', 1) | replace('\\\\n', '\\n') | indent(4, false) }}
{% endfor %}""")

print('\ncoreos:\n  units:')
for unit in d['systemd']['units']:
    print('  - name: {}'.format(unit['name']))
    if unit['enable']:
        print('    enable: true\n    command: start')

    if unit['name'] == "locksmithd.service":
        print('{% if locksmith_window_start != "" and locksmith_window_length != "" %}')
    if 'dropins' in unit and len(unit['dropins']) > 0:
        print('    drop-ins:')
        for dropin in unit['dropins']:
            print("""\
    - name: {name}
      content: |
{content}""".format(
                name=dropin['name'],
                content=textwrap.indent(process_content(dropin['contents'], 8), ' ' * 8)))
    if unit['name'] == "locksmithd.service":
        print('{% endif %}')

    if 'contents' in unit:
        print('    content: |\n{}'.format(
            textwrap.indent(process_content(unit['contents'], 6), ' ' * 6)))
print("""\
{% for unit in ignition_extra_services %}
  - name: {{ unit.name }}
{% if 'enable' in unit and unit.enable %}
    enable: true
    command: start
{% endif %}
{% if 'contents' in unit %}
    content: |
      {{ unit.contents | replace('\\\\n', '\\n') | indent(6, false) }}
{% endif %}
{% if 'dropins' in unit and unit.dropins | length > 0 %}
    drop-ins:
{% for dropin in unit.dropins %}
    - name: {{ dropin.name }}
      content: |
        {{ dropin.contents | replace('\\\\n', '\\n') | indent(8, false) }}
{% endfor %}
{% endif %}
{% endfor %}""")
