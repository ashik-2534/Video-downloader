# downloader/tasks.py
import os
import yt_dlp
from django.conf import settings
from celery import shared_task

@shared_task(bind=True)
def download_video_task(self, urls, format_choice, audio_only):
    output_path = os.path.join(settings.MEDIA_ROOT, 'downloads')
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp3' if audio_only else format_choice
        }],
    }
    downloaded_files = []
    for url in urls:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                downloaded_files.append(filename)
        except Exception as e:
            downloaded_files.append(f"Error downloading {url}: {str(e)}")
    
    # Build a list of download link data:
    file_links = []
    for file_path in downloaded_files:
        if file_path.startswith("Error downloading"):
            file_links.append({'name': file_path, 'url': None})
        else:
            from os.path import basename
            file_name = basename(file_path)
            file_url = settings.MEDIA_URL + 'downloads/' + file_name
            file_links.append({'name': file_name, 'url': file_url})
    return file_links

@shared_task
def cleanup_downloads():
    downloads_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
    if not os.path.exists(downloads_dir):
        return "No downloads directory found."
    import time
    now = time.time()
    removed_files = []
    for filename in os.listdir(downloads_dir):
        file_path = os.path.join(downloads_dir, filename)
        if os.path.isfile(file_path) and now - os.path.getmtime(file_path) > 7 * 24 * 3600:
            os.remove(file_path)
            removed_files.append(filename)
    return f"Removed files: {removed_files}"
