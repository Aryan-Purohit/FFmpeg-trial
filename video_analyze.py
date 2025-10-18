# a branch change
import ffmpeg
import yt_dlp
import json

def get_youtube_video_metadata(youtube_url):
    """
    Extracts metadata from a YouTube video by first getting its
    direct stream URL using yt-dlp.
    """
    ydl_opts = {
        'format': 'best', # Get the best quality stream
        'quiet': True,    # Suppress console output from yt-dlp
    }

    try:
        # Get video info from yt-dlp
        print(f"Fetching stream URL from: {youtube_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
        
        # Get the direct URL to the video stream
        stream_url = info_dict['url']

        # Now, use ffprobe on the direct stream URL
        print("Probing stream with FFmpeg...")
        probe = ffmpeg.probe(stream_url)
        
        # Find the video stream
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

        if video_stream is None:
            print("No video stream found.")
            return
            
        # Extract and display metadata
        width = video_stream.get('width', 'N/A')
        height = video_stream.get('height', 'N/A')
        duration = float(info_dict.get('duration', 0)) # Get duration from yt-dlp info
        codec = video_stream.get('codec_name', 'N/A')
        frame_rate_str = video_stream.get('avg_frame_rate', '0/1')
        frame_rate = eval(frame_rate_str) if frame_rate_str != '0/1' else 0

        print("\n--- YouTube Video Metadata ---")
        print(f"Title: {info_dict.get('title')}")
        print(f"Uploader: {info_dict.get('uploader')}")
        print(f"Resolution: {width}x{height}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Codec: {codec}")
        print(f"Frame Rate: {frame_rate:.2f} fps")

    except yt_dlp.utils.DownloadError as e:
        print(f"yt-dlp Error: {e}")
    except ffmpeg.Error as e:
        print("FFmpeg Error:")
        print(e.stderr.decode())

# --- Main execution ---
if __name__ == "__main__":
    # Paste any YouTube video link here
    youtube_link = "https://www.youtube.com/watch?v=havARbP7Fyk" 
    get_youtube_video_metadata(youtube_link)