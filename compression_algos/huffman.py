import heapq
from collections import Counter
import pickle

class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(text):
    freq = Counter(text)
    heap = [HuffmanNode(ch, fr) for ch, fr in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, prefix='', codebook=None):
    if codebook is None:
        codebook = {}
    if node.char is not None:
        codebook[node.char] = prefix
    if node.left:
        generate_codes(node.left, prefix + '0', codebook)
    if node.right:
        generate_codes(node.right, prefix + '1', codebook)
    return codebook

def compress(text):
    tree = build_tree(text)
    codebook = generate_codes(tree)
    encoded = ''.join(codebook[ch] for ch in text)
    return encoded, tree

import struct

def save_to_bytes(output_io, bit_data, tree):
    # Convert bit string to bytes
    extra_padding = 8 - len(bit_data) % 8
    bit_data += '0' * extra_padding
    b = int(bit_data, 2)
    byte_data = b.to_bytes(len(bit_data) // 8, byteorder='big')

    # Save padding info + tree + compressed data
    output_io.write(struct.pack('B', extra_padding))  # 1 byte padding info
    pickle.dump(tree, output_io)  # still using pickle for now, could optimize later
    output_io.write(byte_data)


def decompress(bit_data, tree):
    result = []
    node = tree
    for bit in bit_data:
        node = node.left if not bit else node.right
        if node.char:
            result.append(node.char)
            node = tree
    return ''.join(result)
