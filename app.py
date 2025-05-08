from flask import Flask, request, jsonify, render_template
import io
import os
from compression_algos import huffman, lzw

app = Flask(__name__)
COMPRESSED_DIR = os.path.join(os.getcwd(), 'compressed_files')
os.makedirs(COMPRESSED_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compress/text', methods=['POST'])
def compress_text():
    method = request.args.get('method')
    file = request.files.get('file')

    if not file or not method:
        return jsonify({'error': 'File and method required'}), 400

    text = file.read().decode('utf-8')

    if method == 'huffman':
        compressed_data, tree = huffman.compress(text)
        filename = "compressed_huffman.bin"
        filepath = os.path.join(COMPRESSED_DIR, filename)
        with open(filepath, 'wb') as f:
            huffman.save_to_bytes(f, compressed_data, tree)

    elif method == 'lzw':
        compressed_codes = lzw.compress(text)
        filename = "compressed_lzw.bin"
        filepath = os.path.join(COMPRESSED_DIR, filename)
        with open(filepath, 'wb') as f:
            lzw.save_to_bytes(f, compressed_codes)

    else:
        return jsonify({'error': 'Invalid method'}), 400

    return jsonify({'message': 'File compressed and saved', 'path': filepath})

if __name__ == '__main__':
    app.run(debug=True)
