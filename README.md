## Project Story

I recently attended a workshop where we were introduced to the Huffman Coding algorithm and guided through building a simple text compressor.

After the workshop, I wanted to see whether I had actually understood the ideas or was simply following along. So I started over with a blank Jupyter Notebook and rebuilt the compressor from scratch, experimenting with different implementations and refactoring parts of the code as I learned more about the algorithm.

Once the compressor was working, I decided to take the project a step further and build a Streamlit application around it. This repository contains both the original notebook used for experimentation and the final web application built on top of the refactored Huffman engine.

## How I Approached the Problem

Before writing the compressor itself, I tried to break the problem into smaller pieces.

My initial thought process was:

1. Count how frequently each character appears in the text.
2. Build a Huffman tree from those frequencies.
3. Generate a unique binary code for every character by traversing the tree.
4. Replace the original characters with their corresponding binary codes.
5. Store the resulting bitstream efficiently as bytes.
6. Reconstruct the original text by reversing the process during decompression.

Once the overall workflow was clear, I started implementing each stage independently and testing it with small text samples before connecting everything together.

### Compression Pipeline

The compressor follows the workflow below:

```text
Input Text
    ↓
Character Frequency Analysis
    ↓
Min-Heap Construction
    ↓
Huffman Tree Generation
    ↓
Code Generation
    ↓
Binary Encoding
    ↓
Padding & Byte Conversion
    ↓
Compressed Binary File
```

The frequency table is first converted into a min-heap. The two least frequent nodes are repeatedly merged until a single Huffman tree remains.

After the tree is built, a recursive traversal assigns binary codes to each character. Characters closer to the root receive shorter codes, while less frequent characters receive longer ones.

The resulting bitstream cannot be written directly to a file because files operate on bytes rather than individual bits. To solve this, the bitstream is padded to the nearest multiple of eight bits, and the padding information is stored as metadata so it can be removed correctly during decompression.

### Decompression Pipeline

Decompression simply reverses the process:

```text
Compressed File
    ↓
Read Padding Metadata
    ↓
Recover Original Bitstream
    ↓
Decode Using Huffman Tree
    ↓
Restore Original Text
```

Using the stored Huffman structure and encoded bitstream, the application traverses the tree until complete characters are recovered, eventually reconstructing the original text exactly.

Since Huffman Coding is a lossless compression algorithm, the decompressed output matches the original input character-for-character.

## Application Features

### Flexible Text Input

The application supports two ways of providing input:

- Upload a `.txt` file directly.
- Type or paste text into the built-in text area.

This made it easier to test the compressor on both small examples and larger text files during development.

### Compression & Verification

After compression, the application immediately decompresses the generated binary data and displays the restored text.

This acts as a quick correctness check, ensuring that the decompressed output matches the original input exactly.

### Downloadable Binary Output

Compressed data can be downloaded as a `.bin` file, allowing the encoded byte stream to be saved and inspected outside the application.

### Compression Statistics

The app calculates several useful metrics:

- Original file size
- Compressed file size
- Compression factor
- Percentage reduction in storage size

These metrics help visualize how effective Huffman Coding is on different types of text.

### Huffman Code Visualization

The generated Huffman codes are displayed in a tabular format, showing the binary representation assigned to each character.

Special characters such as spaces, tabs, and newlines are displayed using human-readable labels for easier inspection.

### Character Frequency Analysis

The application exposes the frequency table used to construct the Huffman tree.

Viewing the frequency distribution helps explain why certain characters receive shorter codes than others.

### Huffman Tree Inspection

A text-based visualization of the generated Huffman tree is included for debugging and learning purposes.

This makes it possible to inspect the structure of the tree directly and understand how the encoding scheme was derived from the character frequencies.

### Persistent Session State

The application uses Streamlit session state to preserve generated data across interactions, preventing compression results from being lost when users interact with different widgets or download files.

## Interesting Challenges & Lessons Learned

Beyond Huffman Coding itself, this project taught me a lot about software development and debugging.

- Understanding why a min-heap is the natural data structure for efficiently constructing Huffman trees.
- Implementing bit-level padding and metadata handling so compressed binary files can be reconstructed correctly.
- Refactoring notebook code into reusable modules for a production-style application.
- Managing `st.session_state` in Streamlit to preserve data across user interactions.
- Debugging recursive functions and learning how small mistakes in recursion logic can produce completely unexpected results.
- Handling binary data correctly when integrating the compression engine with Streamlit's file download system.
- Iteratively redesigning the tree visualization to make the generated Huffman structure easier to inspect and understand.

Many of the challenges in this project were not algorithmic at all—they were related to debugging, state management, and turning a working prototype into a usable application.
