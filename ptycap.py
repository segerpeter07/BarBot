"""
Party captain dashboard
"""

import os
from flask import Flask, render_template, request

app = Flask('flaskapp')


@app.route('/pcdash', methods=['GET', 'POST'])
def pcdashboard():
    return render_template('pcdash.html')


if __name__ == '__main__':
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
