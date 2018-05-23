from flask import Flask, jsonify, request

from blockchain.chain import BlockChain

from argparse import ArgumentParser

app = Flask(__name__)

blockchain = BlockChain()


@app.route('/chain', methods=['GET'])
def get_chain():
    result = {
        'id': blockchain.chain_id,
        'chain': [blk.to_json() for blk in blockchain.chain.values()],
        'length': len(blockchain)
    }
    return jsonify(result)


@app.route('/chain/block', methods=['POST'])
def add_block():
    transaction = request.get_json()
    try:
        blk_id = blockchain.append(transaction)
    except:
        print('got an exception.')
    result = {'block_id': blk_id}
    return jsonify(result)


@app.route('/chain/block/<string:block_id>', methods=['GET'])
def get_block(block_id):
    blk = blockchain[block_id]
    result = {
        'chain_id': blockchain.chain_id,
        'block_id': blk.block_id,
        'block': blk.to_json()
    }
    return jsonify(result)

def parse_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-H', '--host', default='127.0.0.1', type=str, help='host name')
    arg_parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    arg_parser.add_argument('-d', '--debug', action='store_true', help='debug mode')
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    app.debug = args.debug
    app.testing = args.debug
    app.run(host=args.host, port=args.port)