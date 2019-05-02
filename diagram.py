import os
from eralchemy import render_er

render_er(os.environ.get('DB_CONNECTION_STRING'), 'diagram.png')