# downloader/views.py
import os
import yt_dlp
from django.conf import settings
from django.shortcuts import render
from .forms import DownloadForm

# (For testing purposes we keep a global progress_bar variable.)
progress_bar = {}

def update_progress(d):
    """A progress hook for yt_dlp that logs progress.
    (In your tests, you can substitute a mock progress_bar.)
    """
    if d.get('status') == 'downloading':
        percent_str = d.get('_percent_str', '0.0%')
        # Extract numeric percentage (this is similar to your original code)
        percent = ''.join(filter(str.isdigit, percent_str))
        try:
            progress_bar['value'] = float(percent)
            # Here we simply print the progress.
            print(f"Download progress: {percent_str}")
        except ValueError:
            pass

def download_video(urls, output_path, format_choice, audio_only):
    """Download the videos using yt_dlp."""
    os.makedirs(output_path, exist_ok=True)

    # Configure yt_dlp options
    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'progress_hooks': [update_progress]
    }
    
    # Add a postprocessor to convert the file
    if audio_only:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',  # (Note: many use 'FFmpegExtractAudio' for audio-only)
            'preferedformat': 'mp3'
        }]
    else:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': format_choice
        }]

    # Run yt_dlp to download the videos
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

def download_view(request):
    message = ""
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            # Split URLs by lines and remove any empty entries.
            urls_str = form.cleaned_data['urls']
            urls = [line.strip() for line in urls_str.splitlines() if line.strip()]
            format_choice = form.cleaned_data['format_choice']
            audio_only = form.cleaned_data['audio_only']
            
            # Define a fixed output path (for example: MEDIA_ROOT/downloads)
            output_path = os.path.join(settings.MEDIA_ROOT, 'downloads')
            try:
                download_video(urls, output_path, format_choice, audio_only)
                message = "Download completed successfully!"
            except Exception as e:
                message = f"Download failed: {e}"
    else:
        form = DownloadForm()

    return render(request, 'downloader/download_form.html', {'form': form, 'message': message})

