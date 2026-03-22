#!/usr/bin/env python3

from flask import Flask, jsonify, request
import os
import time

app = Flask(__name__)
SERVER_ID = os.environ.get('SERVER_ID', 'unknown')

@app.route('/v1/models', methods=['GET'])
def list_models():
    return jsonify({
        'object': 'list',
        'data': [
            {
                'id': 'test-model',
                'object': 'model',
                'owned_by': 'test',
                'server_id': SERVER_ID
            }
        ]
    })

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    time.sleep(0.5)
    
    return jsonify({
        'id': f'chatcmpl-{SERVER_ID}',
        'object': 'chat.completion',
        'created': int(time.time()),
        'model': data.get('model', 'test-model'),
        'server_id': SERVER_ID,
        'choices': [
            {
                'index': 0,
                'message': {
                    'role': 'assistant',
                    'content': f'Test response from server {SERVER_ID}'
                },
                'finish_reason': 'stop'
            }
        ],
        'usage': {
            'prompt_tokens': 10,
            'completion_tokens': 10,
            'total_tokens': 20
        }
    })

@app.route('/v1/embeddings', methods=['POST'])
def embeddings():
    data = request.json
    text = data.get('input', [''])[0]
    embedding = [0.1] * 1536
    
    return jsonify({
        'object': 'list',
        'data': [
            {
                'object': 'embedding',
                'embedding': embedding,
                'index': 0
            }
        ],
        'model': 'text-embedding-3-small',
        'usage': {
            'prompt_tokens': len(text.split()),
            'total_tokens': len(text.split())
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
