from PIL import Image
import heapq
from collections import defaultdict
import os
import io

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_table):
    heap = [Node(freq, sym) for sym, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = Node(node1.freq + node2.freq, None, node1, node2)
        heapq.heappush(heap, merged)

    return heap[0]

def generate_huffman_codes(root):
    codes = {}

    def generate_codes_helper(node, current_code):
        if node:
            if node.symbol is not None:
                codes[node.symbol] = current_code
            generate_codes_helper(node.left, current_code + "0")
            generate_codes_helper(node.right, current_code + "1")

    generate_codes_helper(root, "")
    return codes

def huffman_encoding(data):
    freq_table = defaultdict(int)
    for pixel in data:
        freq_table[pixel] += 1

    huffman_tree_root = build_huffman_tree(freq_table)
    huffman_codes = generate_huffman_codes(huffman_tree_root)

    encoded_data = "".join(huffman_codes[pixel] for pixel in data)
    return huffman_codes, encoded_data

def huffman_decoding(encoded_data, huffman_codes):
    reverse_huffman_codes = {v: k for k, v in huffman_codes.items()}
    current_code = ""
    decoded_data = []

    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_huffman_codes:
            decoded_data.append(reverse_huffman_codes[current_code])
            current_code = ""

    return decoded_data

def process_channel(channel):
    flat_channel = list(channel.getdata())
    huffman_codes, encoded_data = huffman_encoding(flat_channel)
    decoded_data = huffman_decoding(encoded_data, huffman_codes)
    return decoded_data, encoded_data, huffman_codes

def compress_image(image_data):
    """
    Compress an image using Huffman encoding
    
    Args:
        image_data: Image data as bytes or file-like object
        
    Returns:
        tuple: (compressed_image_bytes, compression_stats)
    """
    # Open the image from bytes
    img = Image.open(io.BytesIO(image_data))
    width, height = img.size

    # Split into RGB channels
    r, g, b = img.split()

    # Process each channel
    r_decoded, r_encoded, r_codes = process_channel(r)
    g_decoded, g_encoded, g_codes = process_channel(g)
    b_decoded, b_encoded, b_codes = process_channel(b)

    # Calculate compression statistics
    original_size = len(list(r.getdata())) + len(list(g.getdata())) + len(list(b.getdata()))
    encoded_size = len(r_encoded) + len(g_encoded) + len(b_encoded)
    compression_ratio = encoded_size / (original_size * 8)

    # Reconstruct the image
    r_image = Image.new('L', (width, height))
    g_image = Image.new('L', (width, height))
    b_image = Image.new('L', (width, height))

    r_image.putdata(r_decoded)
    g_image.putdata(g_decoded)
    b_image.putdata(b_decoded)

    decoded_img = Image.merge("RGB", (r_image, g_image, b_image))

    # Save as JPEG to bytes
    output_buffer = io.BytesIO()
    decoded_img.save(output_buffer, format='JPEG', quality=90)
    compressed_bytes = output_buffer.getvalue()

    stats = {
        'original_size': original_size * 8,  # in bits
        'compressed_size': encoded_size,     # in bits
        'compression_ratio': compression_ratio
    }

    return compressed_bytes, stats
