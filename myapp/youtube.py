from pytube import YouTube

def search_on_youtube(query, max_results=5):
    video_results = []

    try:
        search_results = YouTube.search(query, max_results=max_results)

        for video in search_results:
            video_title = video.title
            video_url = video.url
            video_results.append({'title': video_title, 'url': video_url})

        return video_results
    except Exception as e:
        print(f"Error searching on YouTube: {e}")
        return None