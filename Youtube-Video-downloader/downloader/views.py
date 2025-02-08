

# downloader/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from celery.result import AsyncResult
from .forms import DownloadForm
from .tasks import download_video_task

def download_view(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            urls = [url.strip() for url in form.cleaned_data['urls'].splitlines() if url.strip()]
            format_choice = form.cleaned_data['format_choice']
            audio_only = form.cleaned_data['audio_only']
            task = download_video_task.delay(urls, format_choice, audio_only)
            return redirect('download_status', task_id=task.id)
    else:
        form = DownloadForm()
    return render(request, 'downloader/form.html', {'form': form})

def download_status(request, task_id):
    task_result = AsyncResult(task_id)
    if task_result.state == 'SUCCESS':
        file_links = task_result.result
        return render(request, 'downloader/success.html', {'downloaded_files': file_links})
    elif task_result.state == 'FAILURE':
        error = task_result.info or "An error occurred."
        return render(request, 'downloader/error.html', {'error': error})
    else:
        return render(request, 'downloader/status.html', {'task_id': task_id, 'state': task_result.state})

def task_status_json(request, task_id):
    task_result = AsyncResult(task_id)
    return JsonResponse({
        'task_id': task_id,
        'state': task_result.state,
        'result': task_result.result,
    })

