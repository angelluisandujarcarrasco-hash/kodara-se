"""Compone el video promo final."""
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, vfx
import os

FPS = 30

# Timing (segundos)
# Total: 2 + 5*1.6 + 4 + 2 = 16s
APERTURA_DUR = 2.0
POSTER_DUR = 1.6
OFERTA_DUR = 4.0
CIERRE_DUR = 2.0

def make_clip(img_path, duration, fade_in=0.3, fade_out=0.3):
    clip = ImageClip(img_path).with_duration(duration)
    # subtle zoom para que no sea estatico
    return clip.with_effects([
        vfx.CrossFadeIn(fade_in),
        vfx.CrossFadeOut(fade_out),
    ])

clips = [
    make_clip('video-promo/frames/01-apertura.png', APERTURA_DUR, 0.4, 0.4),
    make_clip('video-promo/frames/02-poster.png', POSTER_DUR),
    make_clip('video-promo/frames/03-poster.png', POSTER_DUR),
    make_clip('video-promo/frames/04-poster.png', POSTER_DUR),
    make_clip('video-promo/frames/05-poster.png', POSTER_DUR),
    make_clip('video-promo/frames/06-poster.png', POSTER_DUR),
    make_clip('video-promo/frames/07-oferta.png', OFERTA_DUR, 0.5, 0.3),
    make_clip('video-promo/frames/08-cierre.png', CIERRE_DUR, 0.5, 0.3),
]

video = concatenate_videoclips(clips, method='compose')
print(f'Duracion total: {video.duration}s')

# Audio: usar el del video brand previo (acoustic latina)
try:
    audio = AudioFileClip('marketing/brand-video/kodarase-brand-15s.mp4')
    if audio.duration < video.duration:
        # loop
        from moviepy.audio.fx import AudioLoop
        audio = audio.with_effects([AudioLoop(duration=video.duration)])
    else:
        audio = audio.subclipped(0, video.duration)
    # Fade out audio al final
    from moviepy.audio.fx import AudioFadeOut
    audio = audio.with_effects([AudioFadeOut(0.5)])
    video = video.with_audio(audio)
    print('Audio agregado desde video brand previo')
except Exception as e:
    print(f'Sin audio: {e}')

os.makedirs('marketing/video-promo', exist_ok=True)
output = 'marketing/video-promo/kodarase-promo-15s.mp4'

print('Renderizando...')
video.write_videofile(
    output,
    codec='libx264',
    audio_codec='aac',
    fps=FPS,
    preset='medium',
    threads=4,
    logger=None,
)

print(f'OK: {output}')
print(f'Tamano: {os.path.getsize(output):,} bytes')
