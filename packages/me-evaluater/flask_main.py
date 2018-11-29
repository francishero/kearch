import flask
import sys
import base64
from flask import jsonify
import kearch_evaluater.evaluater
from kearch_common.requester import KearchRequester

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306
REQUESTER_NAME = 'me-evaluater'

timestamp = dict()
app = flask.Flask(__name__)


def update_param_file(filename):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    ret = db_req.request(path='/me/db/check_binary_file_timestamp',
                         params={'name': filename})
    dt = ret['updated_at']
    print('db:', dt, file=sys.stderr)
    if filename not in timestamp or timestamp[filename] < dt:
        timestamp[filename] = dt
        ret = db_req.request(path='/me/db/pull_binary_file',
                             params={'name': filename})
        body = base64.b64decode(ret['body'].encode())
        with open(filename, 'wb') as f:
            f.write(body)


@app.route('/evaluate', methods=['GET'])
def post():
    print('Start checking parameter files.', file=sys.stderr)
    update_param_file(kearch_evaluater.evaluater.PARAMS_FILE)
    print('End checking parameter files.', file=sys.stderr)

    queries = flask.request.args.get('queries')
    queries = queries.split(' ')

    e = kearch_evaluater.kearch_evaluater.Evaluater()
    e.load_params(kearch_evaluater.kearch_evaluater.PARAMS_FILE)

    return jsonify(e.evaluate(queries))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=10080)  # どこからでもアクセス可能に