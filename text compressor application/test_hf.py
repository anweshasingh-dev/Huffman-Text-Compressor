from huffman_engine import *

text = "Hello Huffman Coding"

freq_table = freq_counter(text)

root = build_hf_tree(freq_table)

codes = get_codes(root)

compressed = compress_text(text, codes)

restored = decompress_bytes(compressed, root)

print(restored)