from celery_app import app

from apps.youtube.utils import YouTube


@app.task(queue='youtube_default')
def sync_youtube_videos():
    youtube = YouTube()
    youtube.save_responses()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Syncing youtube videos every 10 seconds.
    sender.add_periodic_task(30.0, sync_youtube_videos.si(), name='sync youtube videos')
