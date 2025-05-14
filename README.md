# 🗜️ Flask Compression App

A web-based compression tool built with **Flask** that allows users to compress **Text**, **Images**, and **Videos** using a variety of algorithms like **Huffman**, **LZW**, and **DCT-based compression**. This app offers a unified interface for file compression and visual feedback on compression efficiency.

---

## 🚀 Features

- 🔤 **Text Compression**  
  Supports:
  - **Huffman Encoding**
  - **Lempel–Ziv–Welch (LZW)**

- 🖼️ **Image Compression**  
  - Uses **Huffman encoding** on image data
  - Image manipulation powered by **Pillow (PIL)**

- 🎞️ **Video Compression**  
  - Extracts frames using **FFmpeg**
  - Applies **DCT (Discrete Cosine Transform)**-based lossy compression to individual frames
  - Reconstructs the compressed video using **FFmpeg**
  - Provides **compression ratio**, **original vs compressed sizes**, and **frame statistics**

---

## 🧠 Algorithms Used

### ✅ Huffman Encoding
A lossless algorithm for text and image data that builds a binary tree to assign shorter codes to frequently occurring symbols.

### ✅ LZW (Lempel–Ziv–Welch)
Another lossless compression algorithm commonly used for text, effective on repetitive sequences.

### ✅ DCT (for Video)
Used for reducing spatial redundancy in video frames by transforming images into frequency components.

---

## 📂 Folder Structure

```
Project/
│
├── app.py                # Flask backend
├── static/
│   ├── style.css         # Your improved CSS
│   └── script.js         # JS file for 
├── templates/
│   └── index.html        # Your HTML file
├── compression_algos/
│   ├──all the algos, text ,image and video compression
```

---

## ⚙️ Requirements

- Python 3.7+
- Flask
- Pillow
- OpenCV
- FFmpeg (installed and accessible via system path)

 ---

## 📽️ How Video Compression Works

1. Save the uploaded video to a temporary location.
2. Extract all video frames using **FFmpeg**.
3. Compress each frame using **DCT thresholding**.
4. Re-encode compressed frames back into a video using **FFmpeg**.
5. Report compression statistics.
-

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Anshdeep Bansal**  
_3rd-year B.Tech CSE student, Graphic Era University_  
💼 [LinkedIn](https://www.linkedin.com/in/anshdeep-bansal-53327b24b) 
