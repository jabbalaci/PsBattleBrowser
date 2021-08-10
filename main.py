#!/usr/bin/env python3

from flask import render_template, request

from common import app
from lib import filters, reddit
from models.battle import Battle
from models.index import Index

app.jinja_env.filters['remove_psbattle'] = filters.remove_psbattle


@app.route('/')
def fn_index():
    after: str = request.args.get('after', '').strip()
    index: Index = reddit.get_index_entries(after)
    return render_template('index.html', index=index)


@app.route('/entry')
def fn_entry():
    permalink: str = request.args.get('permalink', '').strip()
    result: Battle = reddit.get_shopped_entries(permalink)
    return render_template('entry.html', battle=result)


if __name__ == "__main__":
    info = """
+----------------------------------------------------------------------+
| If the images don't appear, then use localhost instead of 127.0.0.1, |
| i.e. open http://localhost:5000 in your browser!                     |
+----------------------------------------------------------------------+
""".strip()
    print(info)
    # app.run()
    app.run(debug=True)    # listen on localhost ONLY
