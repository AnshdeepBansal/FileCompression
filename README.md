# 🗜️ Text Compression Web App

This project is a **Flask-based web application** that allows users to compress and decompress text files using two popular lossless compression algorithms:

* **Huffman Encoding**
* **LZW (Lempel–Ziv–Welch)**

---

## 🔧 Features

* 📄 Upload plain text files (`.txt`)
* 🧠 Choose between **Huffman** or **LZW** compression
* 💾 Download the compressed `.bin` file
* 📤 Decompress uploaded `.bin` files back to original text
* 🗂️ Compressed files are saved in the `compressed_files/` folder

---

## 🚀 How It Works

### Huffman Compression

1. Builds a frequency table and binary tree
2. Generates unique binary codes per character
3. Stores the compressed data along with the tree using `pickle`

### LZW Compression

1. Initializes dictionary with ASCII characters
2. Iteratively builds sequences and maps them to codes
3. Stores 16-bit codes in a `.bin` file using `struct`

---

## 📁 Project Structure

```
Project/
│
├── app.py                # Flask backend
├── static/
│   ├── style.css         # Your improved CSS
│   └── script.js         # JS file for interactivity (optional for now)
├── templates/
│   └── index.html        # Your HTML file
├── compression_algos/
│   ├── huffman.py        # Your Huffman logic
│   └── lzw.py            # Your LZW logic
```

---

## ▶️ Getting Started

### 1. Install Dependencies

```bash
pip install flask
```
- install all other also if not installed!!

### 2. Run the App

```bash
python app.py
```

### 3. Open in Browser

Visit: [http://localhost:5000](http://localhost:5000)

---

## 📦 Sample Usage

* Upload `sample.txt`
* Choose `Huffman` or `LZW` compression
  
---

## ⚙️ To Do

* Add file size statistics
* Show compression ratio
* Support other file types (e.g., `.csv`, `.json`)
* Add drag-and-drop UI

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---
