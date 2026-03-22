#!/usr/bin/env python3

from flask import Flask, jsonify, request
import os
import time

app = Flask(__name__)
SERVER_ID = os.environ.get('SERVER_ID', 'unknown')


def model_catalog():
    now = int(time.time())
    return [
        {
            'id': 'general_assistant',
            'object': 'model',
            'created': now,
            'owned_by': 'bsuir-test',
            'server_id': SERVER_ID
        },
        {
            'id': 'test-model',
            'object': 'model',
            'created': now,
            'owned_by': 'bsuir-test',
            'server_id': SERVER_ID
        },
        {
            'id': 'text-embedding-3-small',
            'object': 'model',
            'created': now,
            'owned_by': 'bsuir-test',
            'server_id': SERVER_ID
        }
    ]


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'server_id': SERVER_ID
    })


@app.route('/v1/models', methods=['GET'])
def list_models():
    return jsonify({
        'object': 'list',
        'data': model_catalog()
    })


@app.route('/v1/models/<model_id>', methods=['GET'])
def get_model(model_id):
    for model in model_catalog():
        if model['id'] == model_id:
            return jsonify(model)
    return jsonify({'error': {'message': f'Model {model_id} not found'}}), 404


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json or {}
    time.sleep(0.5)

    messages = data.get('messages', [])
    user_message = ''
    for message in reversed(messages):
        if message.get('role') == 'user':
            user_message = message.get('content', '')
            break

    return jsonify({
        'id': f'chatcmpl-{SERVER_ID}',
        'object': 'chat.completion',
        'created': int(time.time()),
        'model': data.get('model', 'general_assistant'),
        'server_id': SERVER_ID,
        'choices': [
            {
                'index': 0,
                'message': {
                    'role': 'assistant',
                    'content': f'Test response from server {SERVER_ID}. User said: {user_message}'
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


@app.route('/v1/responses', methods=['POST'])
def responses():
    data = request.json or {}
    input_data = data.get('input', '')

    if isinstance(input_data, list):
        text_parts = []
        for item in input_data:
            if isinstance(item, dict):
                content = item.get('content', [])
                if isinstance(content, list):
                    for part in content:
                        if isinstance(part, dict) and part.get('type') == 'input_text':
                            text_parts.append(part.get('text', ''))
        prompt = ' '.join(part for part in text_parts if part)
    else:
        prompt = str(input_data)

    return jsonify({
        'id': f'resp-{SERVER_ID}',
        'object': 'response',
        'created_at': int(time.time()),
        'model': data.get('model', 'general_assistant'),
        'server_id': SERVER_ID,
        'status': 'completed',
        'output': [
            {
                'id': f'msg-{SERVER_ID}',
                'type': 'message',
                'role': 'assistant',
                'content': [
                    {
                        'type': 'output_text',
                        'text': f'Test response from server {SERVER_ID}. Prompt: {prompt}'
                    }
                ]
            }
        ]
    })


@app.route('/v1/embeddings', methods=['POST'])
def embeddings():
    data = request.json or {}
    input_value = data.get('input', [''])
    if isinstance(input_value, list):
        text = str(input_value[0]) if input_value else ''
    else:
        text = str(input_value)
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
