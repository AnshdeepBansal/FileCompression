from flask import Flask, request, jsonify, render_template, send_file
import io
import os
import logging
from compression_algos import huffman, lzw, image_huffman, video_compression

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.route('/compress/image', methods=['POST'])
def compress_image():
    file = request.files.get('file')
    
    if not file:
        return jsonify({'error': 'Image file required'}), 400
    
    # Check if the file is an image
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        return jsonify({'error': 'File must be an image'}), 400
    
    # Read the image file
    image_data = file.read()
    
    try:
        # Compress the image
        compressed_bytes, stats = image_huffman.compress_image(image_data)
        
        # Generate a filename based on the original filename
        original_name = os.path.splitext(file.filename)[0]
        filename = f"{original_name}_compressed.jpg"
        filepath = os.path.join(COMPRESSED_DIR, filename)
        
        # Save the compressed image
        with open(filepath, 'wb') as f:
            f.write(compressed_bytes)
        
        # Return the compression statistics and file path
        return jsonify({
            'message': 'Image compressed and saved',
            'path': filepath,
            'original_size_bits': stats['original_size'],
            'compressed_size_bits': stats['compressed_size'],
            'compression_ratio': stats['compression_ratio']
        })
    
    except Exception as e:
        logger.error(f"Image compression failed: {str(e)}")
        return jsonify({'error': f'Compression failed: {str(e)}'}), 500

@app.route('/compress/video', methods=['POST'])
def compress_video():
    file = request.files.get('file')
    
    if not file:
        return jsonify({'error': 'Video file required'}), 400
    
    # Check if the file is a video
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
        return jsonify({'error': 'File must be a video'}), 400
    
    # Get compression parameters from request (or use defaults)
    threshold = request.args.get('threshold', default=10, type=int)
    quality = request.args.get('quality', default=28, type=int)
    
    # Read the video file
    video_data = file.read()
    
    try:
        # Check if FFmpeg is installed
        if not video_compression.check_ffmpeg():
            return jsonify({'error': 'FFmpeg is not installed. Please install FFmpeg to use video compression.'}), 500
        
        # Compress the video
        logger.info(f"Starting video compression for {file.filename}")
        compressed_video_data, stats = video_compression.compress_video(
            video_data, 
            threshold=threshold,
            quality=quality
        )
        
        # Generate a filename based on the original filename
        original_name = os.path.splitext(file.filename)[0]
        filename = f"{original_name}_compressed.mp4"
        filepath = os.path.join(COMPRESSED_DIR, filename)
        
        # Save the compressed video
        with open(filepath, 'wb') as f:
            f.write(compressed_video_data)
        
        logger.info(f"Video compression completed. Saved to {filepath}")
        
        # Return the compressed video as a downloadable file
        return send_file(
            io.BytesIO(compressed_video_data),
            mimetype='video/mp4',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        logger.error(f"Video compression failed: {str(e)}")
        return jsonify({'error': f'Video compression failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
