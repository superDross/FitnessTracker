''' Custom model validators.'''

def youtube_url_prep(link):
    embed = 'embed/'
    watch = 'watch?v='

    if not embed in link:
        if 'youtu.be' in link:
            link = link.replace('youtu.be/', f'youtube.com/{embed}')
        elif watch in link:
            link = link.replace(watch, embed)

    return link
