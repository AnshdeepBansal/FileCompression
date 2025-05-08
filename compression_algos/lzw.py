import struct

def compress(text):
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []

    for c in text:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])

    return result  # Return list of codes

def save_to_bytes(output_io, codes):
    for code in codes:
        output_io.write(struct.pack('>H', code))  # 2 bytes per code

def load_from_bytes(input_io):
    byte_data = input_io.read()
    codes = []
    for i in range(0, len(byte_data), 2):
        (code,) = struct.unpack('>H', byte_data[i:i+2])
        codes.append(code)
    return codes

def decompress_codes(codes):
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    result = []

    w = chr(codes[0])
    result.append(w)

    for k in codes[1:]:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError("Bad compressed k: %s" % k)
        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry

    return ''.join(result)
