async function uploadAndCompress(endpoint, file, fileField = 'file') {
  const formData = new FormData();
  formData.append(fileField, file);

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error("Compression failed");

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;

    // Set filename based on content disposition header, if available
    const contentDisposition = response.headers.get('Content-Disposition');
    const fileNameMatch = contentDisposition && contentDisposition.match(/filename="(.+)"/);
    const fileName = fileNameMatch ? fileNameMatch[1] : 'compressed_output.bin';
    
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (err) {
    alert("Compression failed: " + err.message);
  }
}

document.getElementById('compress-text').addEventListener('click', () => {
  const file = document.getElementById('text-file').files[0];
  const algorithm = document.getElementById('algorithm').value;

  if (file) {
    alert('Uploading for Text Compression...');
    uploadAndCompress(`/compress/text?method=${algorithm}`, file);
  } else {
    alert('Please upload a text file.');
  }
});

document.getElementById('compress-image').addEventListener('click', () => {
  const file = document.getElementById('image-file').files[0];

  if (file) {
    alert('Image Compression in Progress...');
    uploadAndCompress('/compress/image', file);
  } else {
    alert('Please upload an image file.');
  }
});

document.getElementById('compress-video').addEventListener('click', () => {
  const file = document.getElementById('video-file').files[0];

  if (file) {
    alert('Video Compression in Progress...');
    uploadAndCompress('/compress/video', file);
  } else {
    alert('Please upload a video file.');
  }
});
