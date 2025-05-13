async function uploadAndCompress(endpoint, file, fileField = "file", isImageCompression = false) {
  const formData = new FormData()
  formData.append(fileField, file)

  try {
    // Show loading indicator
    const loadingDiv = document.createElement("div")
    loadingDiv.className = "loading-indicator"
    loadingDiv.innerHTML = `
      <div class="spinner"></div>
      <p>Processing... This may take a while for large files.</p>
    `
    document.body.appendChild(loadingDiv)

    const response = await fetch(endpoint, {
      method: "POST",
      body: formData,
    })

    // Remove loading indicator
    document.body.removeChild(loadingDiv)

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || "Compression failed")
    }

    // For image compression, we expect a JSON response with stats and file path
    if (isImageCompression) {
      const data = await response.json()

      // Display compression statistics
      const statsDiv = document.createElement("div")
      statsDiv.className = "compression-stats"
      statsDiv.innerHTML = `
        <h3>Compression Results</h3>
        <p>Original size: ${(data.original_size_bits / 8 / 1024).toFixed(2)} KB (${data.original_size_bits} bits)</p>
        <p>Compressed size: ${(data.compressed_size_bits / 8 / 1024).toFixed(2)} KB (${data.compressed_size_bits} bits)</p>
        <p>Compression ratio: ${(data.compression_ratio * 100).toFixed(2)}%</p>
      `

      // Create a modal or append to a results area
      const resultsArea = document.getElementById("compression-results") || document.body
      resultsArea.innerHTML = ""
      resultsArea.appendChild(statsDiv)

      // Create download link for the compressed image
      const downloadLink = document.createElement("a")
      downloadLink.href = data.path
      downloadLink.textContent = "Download Compressed Image"
      downloadLink.className = "download-button"
      downloadLink.download = data.path.split("/").pop()
      resultsArea.appendChild(downloadLink)

      return
    }

    // For other compression types, download the blob directly
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url

    // Set filename based on content disposition header, if available
    const contentDisposition = response.headers.get("Content-Disposition")
    const fileNameMatch = contentDisposition && contentDisposition.match(/filename="(.+)"/)
    const fileName = fileNameMatch ? fileNameMatch[1] : "compressed_output.bin"

    link.download = fileName
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    alert("Compression failed: " + err.message)
    console.error("Compression error:", err)
  }
}

document.getElementById("compress-text").addEventListener("click", () => {
  const file = document.getElementById("text-file").files[0]
  const algorithm = document.getElementById("algorithm").value

  if (file) {
    uploadAndCompress(`/compress/text?method=${algorithm}`, file)
  } else {
    alert("Please upload a text file.")
  }
})

document.getElementById("compress-image").addEventListener("click", () => {
  const file = document.getElementById("image-file").files[0]

  if (file) {
    uploadAndCompress("/compress/image", file, "file", true) // Pass true for isImageCompression
  } else {
    alert("Please upload an image file.")
  }
})

document.getElementById("compress-video").addEventListener("click", () => {
  const file = document.getElementById("video-file").files[0]

  if (file) {
    uploadAndCompress("/compress/video", file)
  } else {
    alert("Please upload a video file.")
  }
})

// Add this to make sure the compression results area exists
document.addEventListener("DOMContentLoaded", () => {
  if (!document.getElementById("compression-results")) {
    const resultsDiv = document.createElement("div")
    resultsDiv.id = "compression-results"
    resultsDiv.className = "results-container"
    document.body.appendChild(resultsDiv)
  }

  // Add CSS for loading indicator
  const style = document.createElement("style")
  style.textContent = `
    .loading-indicator {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 9999;
      color: white;
    }
    
    .spinner {
      border: 5px solid #f3f3f3;
      border-top: 5px solid #3498db;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      animation: spin 2s linear infinite;
      margin-bottom: 20px;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    .download-button {
      display: inline-block;
      background-color: #4CAF50;
      color: white;
      padding: 10px 15px;
      text-decoration: none;
      border-radius: 4px;
      margin-top: 15px;
    }
    
    .compression-stats {
      margin-top: 20px;
      padding: 15px;
      border: 1px solid #ddd;
      border-radius: 4px;
      background-color: #f9f9f9;
    }
  `
  document.head.appendChild(style)
})
