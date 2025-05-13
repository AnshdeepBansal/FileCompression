import os
import subprocess
import cv2
import tempfile
import shutil
import uuid
import logging
from .compress_utils import apply_dct_compression

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def compress_video(video_data, threshold=10, quality=28):
    """
    Compress a video using DCT compression on individual frames
    
    Args:
        video_data: Video data as bytes
        threshold: DCT coefficient threshold (higher = more compression)
        quality: Output video quality (higher = lower quality)
        
    Returns:
        tuple: (compressed_video_path, compression_stats)
    """
    # Check if FFmpeg is installed
    if not check_ffmpeg():
        raise RuntimeError("FFmpeg is not installed or not in PATH. Please install FFmpeg to use video compression.")
    
    # Create unique ID for this compression job
    job_id = str(uuid.uuid4())
    
    # Create temporary directories
    temp_dir = tempfile.mkdtemp()
    logger.info(f"Created temporary directory: {temp_dir}")
    
    input_video = os.path.join(temp_dir, f"input_{job_id}.mp4")
    frames_dir = os.path.join(temp_dir, "frames")
    compressed_dir = os.path.join(temp_dir, "compressed_frames")
    output_video = os.path.join(temp_dir, f"output_{job_id}.mp4")
    
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(compressed_dir, exist_ok=True)
    
    try:
        # Write input video data to file
        with open(input_video, 'wb') as f:
            f.write(video_data)
        
        logger.info(f"Saved input video to {input_video}")
        
        # Get video properties
        cap = cv2.VideoCapture(input_video)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video file: {input_video}")
            
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        
        logger.info(f"Video properties: {width}x{height}, {fps} fps, {frame_count} frames")
        
        if fps <= 0:
            fps = 30  # Default FPS if unable to determine
            logger.warning(f"Could not determine FPS, using default: {fps}")
        
        # Extract frames using FFmpeg
        extract_cmd = ["ffmpeg", "-i", input_video, f"{frames_dir}/frame_%04d.png"]
        logger.info(f"Extracting frames with command: {' '.join(extract_cmd)}")
        
        extract_result = subprocess.run(
            extract_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if extract_result.returncode != 0:
            logger.error(f"FFmpeg frame extraction failed: {extract_result.stderr}")
            raise RuntimeError(f"FFmpeg frame extraction failed: {extract_result.stderr}")
        
        # Check if frames were extracted
        extracted_frames = sorted(os.listdir(frames_dir))
        if not extracted_frames:
            raise RuntimeError("No frames were extracted from the video")
        
        logger.info(f"Extracted {len(extracted_frames)} frames")
        
        # Apply DCT compression on frames
        for i, frame_file in enumerate(extracted_frames):
            path = os.path.join(frames_dir, frame_file)
            image = cv2.imread(path)
            if image is None:
                logger.warning(f"Could not read frame: {path}")
                continue
                
            compressed = apply_dct_compression(image, threshold=threshold)
            output_path = os.path.join(compressed_dir, frame_file)
            cv2.imwrite(output_path, compressed)
            
            if i % 10 == 0:  # Log progress every 10 frames
                logger.info(f"Compressed {i+1}/{len(extracted_frames)} frames")
        
        # Check if compressed frames exist
        compressed_frames = sorted(os.listdir(compressed_dir))
        if not compressed_frames:
            raise RuntimeError("No compressed frames were generated")
        
        logger.info(f"Compressed {len(compressed_frames)} frames")
        
        # Combine compressed frames into video using FFmpeg
        combine_cmd = [
            "ffmpeg", 
            "-framerate", str(fps), 
            "-i", f"{compressed_dir}/frame_%04d.png",
            "-c:v", "libx264", 
            "-preset", "medium", 
            "-crf", str(quality), 
            "-pix_fmt", "yuv420p",  # Ensure compatibility
            output_video
        ]
        
        logger.info(f"Combining frames with command: {' '.join(combine_cmd)}")
        
        combine_result = subprocess.run(
            combine_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if combine_result.returncode != 0:
            logger.error(f"FFmpeg video creation failed: {combine_result.stderr}")
            raise RuntimeError(f"FFmpeg video creation failed: {combine_result.stderr}")
        
        # Check if output video was created
        if not os.path.exists(output_video) or os.path.getsize(output_video) == 0:
            raise RuntimeError("Output video was not created or is empty")
        
        # Calculate compression statistics
        original_size = os.path.getsize(input_video)
        compressed_size = os.path.getsize(output_video)
        compression_ratio = compressed_size / original_size if original_size > 0 else 0
        
        logger.info(f"Compression stats: original={original_size}, compressed={compressed_size}, ratio={compression_ratio}")
        
        # Read the compressed video into memory
        with open(output_video, 'rb') as f:
            compressed_video_data = f.read()
        
        stats = {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'frame_count': frame_count,
            'fps': fps
        }
        
        return compressed_video_data, stats
        
    except Exception as e:
        logger.error(f"Error during video compression: {str(e)}")
        raise
    finally:
        # Clean up temporary files
        try:
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            logger.warning(f"Failed to clean up temporary directory {temp_dir}: {str(e)}")
