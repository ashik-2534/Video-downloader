# downloader/forms.py
from django import forms

class DownloadForm(forms.Form):
    urls = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        help_text="Enter YouTube URLs (one per line)"
    )
    format_choice = forms.ChoiceField(
        choices=[('mp4', 'mp4'), ('mkv', 'mkv'), ('webm', 'webm')],
        initial='mp4',
        label="Select Video Format"
    )
    audio_only = forms.BooleanField(
        required=False,
        label="Download Audio Only (MP3)"
    )
