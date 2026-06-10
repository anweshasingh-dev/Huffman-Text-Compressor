import streamlit as st
import pandas as pd
from huffman_engine import *

st.title("Huffman Text Compressor")

# UPLOAD FILE
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
user_input_text = st.text_area("Or type/paste your text here:", height=150)
text = ""  

if uploaded_file is not None:   
    text = uploaded_file.read().decode("utf-8")
    
    text = st.text_area(
        "File Contents", 
        text,
        height=150
    )
elif user_input_text:
    text = user_input_text

if text:
    # COMPRESS AND DECOMPRESS
    if st.button("Compress"):
        freq_table = freq_counter(text)
        root = build_hf_tree(freq_table)
        codes = get_codes(root)
        compressed_data = compress_text(text, codes)
        restored_text = decompress_bytes(compressed_data, root)
        hf_tree = print_tree_structure(root)
        
        st.success("Compression successful!")
        
        # show the text inside a read-only text box
        st.text_area(
            label="Restored Text:", 
            value=restored_text, 
            height=150, 
            disabled=True
        )

        # SESSION STATES    
        st.session_state['freq_table'] = freq_table
        st.session_state['codes'] = codes
        st.session_state['compressed_data'] = compressed_data
        st.session_state['restored_text'] = restored_text
        st.session_state['hf_tree'] = hf_tree

if 'compressed_data' in st.session_state:
    compressed_data = st.session_state['compressed_data']
    freq_table = st.session_state['freq_table']
    codes = st.session_state['codes']
    hf_tree = st.session_state['hf_tree']
    restored_text = st.session_state['restored_text']
    #st.write(type(compressed_data))

# DOWNLOAD COMPRESSED FILE
    st.download_button(
        label="Download Compressed File",
        data=compressed_data,
        file_name="compressed.bin",
        mime="application/octet-stream" # Set MIME type for binary data
    )

# SHOW STATISTICS
    st.subheader("Compression Statistics")
    original_size = len(text.encode('utf-8')) # in bytes
    compressed_size = len(compressed_data) # in bytes

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Original Size (bytes)", original_size)
    c2.metric("Compressed Size (bytes)", compressed_size)
    c3.metric("Compression Factor", f"{original_size / compressed_size:.2f}x")
    c4.metric("Data Shrunk By", f"{(1 - (compressed_size / original_size)) * 100:.2f}%")

# SHOW HUFFMAN CODES
    st.subheader("Huffman Codes")
    #.json(codes)
    readable_codes = []
    for char, code in codes.items():
        if char == " ":    
            display_char = "Space"
        elif char == "\n":
            display_char = "Newline"
        elif char == "\t":
            display_char = "Tab"
        else:
            display_char = char
        readable_codes.append((display_char, code))

    codes_df = pd.DataFrame(readable_codes, columns=['Character', 'Huffman Code'])
    st.dataframe(codes_df)

# SHOW FREQUENCY CHART
    st.subheader("Character Frequency Table")

    # 1. Map the invisible characters for frequencies into a separate list
    readable_freqs = []
    for char, freq in freq_table.items():
        if char == " ":
            display_char = "Space"
        elif char == "\n":
            display_char = "Newline"
        elif char == "\t":
            display_char = "Tab"
        else:
            display_char = char
        readable_freqs.append((display_char, freq))

    freq_df = pd.DataFrame(readable_freqs, columns=['Character', 'Frequency'])
    st.dataframe(freq_df)
    
# SHOW HUFFMAN TREE STRUCTURE
    st.subheader("Huffman Tree Structure")
    st.text_area(
            label="Tree Visualization:",
            value=st.session_state['hf_tree'], 
            height=300, 
            disabled=True
        )    

    st.markdown(""" *Built using Python, Heap queues, Huffman coding, and Streamlit* """)