import heapq
import os
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left =None
        self.right = None
    # special method to compare nodes in heapq based on frequency
    def __lt__(self, other):
        return self.freq < other.freq
    
def freq_counter(text):
    return Counter(text)
#print("Frequency Table: ", freq_counter(text))

def build_hf_tree(freq_table):
    heap = []
    for char, freq in freq_table.items():
        heapq.heappush(heap, Node(char, freq)) # creat initial nodes
        # iteratively travel bottom to top while merging lowest two nodes
    while len(heap)>1:   
        first = heapq.heappop(heap) # get 1st smallest node
        second = heapq.heappop(heap) # get 2nd smallest node
        
        merged = Node(None, first.freq + second.freq)
        merged.left = first # assign left child
        merged.right = second # assign right child
        
        heapq.heappush(heap, merged) # # push the new parent back into the heap
    return heap[0]

# generate the hf codes using hf tree we just built        
def get_codes(node, current_code="", codes=None):
    if codes is None:  # initialize code dict in first call
        codes = {}
    if node is None: # base case: if node is empty, return current code dict
        return codes
    # leaf node is reached - assign current code to char
    if node.char is not None: 
        codes[node.char] = current_code
        return codes
        
    # recursive calls
    get_codes(node.left, current_code+"0", codes)
    get_codes(node.right, current_code+"1", codes)
    return codes

def compress_text(text, codes):
    # text characters --> string of bits
    bit_str = "".join(codes[ch] for ch in text) # encoded the text
    
    # string of bits --> padded string of bits
    padded_amt = 8 - (len(bit_str) % 8)
    if padded_amt == 8:
        padded_amt = 0
    bit_str += "0" * padded_amt
    # store the padding amount as the very first byte
    compressed_bytes = bytearray()
    compressed_bytes.append(padded_amt)
    
    # string of bits --> 1 byte (8 bit) chunks
    for i in range(0, len(bit_str), 8):
        byte_chunk = bit_str[i:i+8]
        compressed_bytes.append(int(byte_chunk, 2))
    return bytes(compressed_bytes) # convert bytearray to immutable bytes object so streamlit won't complain

def decompress_bytes(compressed_bytes, root):
    if not root:
        return ""
    padded_amt = compressed_bytes[0]
    
    # 1 byte (8 bit) chunks --> padded string of bits
    bit_str = ""
    for byte in compressed_bytes[1:]:
        bit_str += f"{byte:08b}" # convert each byte to its 8-bit binary representation and concatenate to bit_str
    
    # padded string of bits --> string of bits
    if padded_amt>0:
        bit_str = bit_str[:-padded_amt]
    
    # string of bits --> text characters
    decoded_text = ""
    current_node = root
    # traverse the hf tree from root to leaf according to the bits in bit_str
    for bit in bit_str:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right
        
        if current_node.char is not None: # leaf node reached
            decoded_text += current_node.char
            current_node = root # reset to root for next char
    return decoded_text

def print_tree_structure(node, level=0, prefix="Root: "):
    if node is None:
        return []

    indent = "    " * level
    lines = []
    if node.char is not None:
        lines.append(f"{indent}{prefix}[Char: {repr(node.char)} | Freq: {node.freq}]")
    else:
        lines.append(f"{indent}{prefix}(Internal Freq: {node.freq})")

    lines.extend(print_tree_structure(node.left, level + 1, prefix="0 -> "))
    lines.extend(print_tree_structure(node.right, level + 1, prefix="1 -> "))

    if level == 0:
        return "\n".join(lines)  # Return the full tree structure as a string at the root level
    return lines  # Return list of lines for recursive calls