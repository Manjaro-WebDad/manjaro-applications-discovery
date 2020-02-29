from flask import Flask
from discover.templateUtils import truncate_description
app = Flask(__name__)
app.jinja_env.filters['truncate_description'] = truncate_description
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


import discover.views