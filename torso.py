import random
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips
from moviepy.audio.AudioClip import AudioArrayClip
from PIL import Image, ImageDraw, ImageFont

# --- Configuration Parameters ---      
SAMPLE_RATE = 500000     # Audio sample rate in Hz

def generate_slide(slide_number, width=1920, height=1080, fontname="arial.ttf", font_size=24, file_name="aqua.flv"):
    # Create a pure white canvas
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    # --- Draw the Blue Rectangle ---
    blue_rect_width = random.randint(50, width // 2)
    blue_rect_height = random.randint(50, height // 2)
    blue_x = random.randint(0, width - blue_rect_width)
    blue_y = random.randint(0, height - blue_rect_height)
    blue_coords = (blue_x, blue_y, blue_x + blue_rect_width, blue_y + blue_rect_height)
    draw.rectangle(blue_coords, fill="blue")
    
    # --- Draw the Red Rectangle (Always on top) ---
    red_rect_width = random.randint(50, width // 2)
    red_rect_height = random.randint(50, height // 2)
    red_x = random.randint(0, width - red_rect_width)
    red_y = random.randint(0, height - red_rect_height)
    red_coords = (red_x, red_y, red_x + red_rect_width, red_y + red_rect_height)
    draw.rectangle(red_coords, fill="red")
    
    # --- Add the Slide Text ---
    # The text follows the pattern: "aqua.flv - slide XXXX"
    text = f"{file_name} - slide {slide_number:04d}"
    font = ImageFont.load_default()

    # Use textbbox to determine the text's dimensions
    # VT323 from Google Fonts (https://fonts.google.com/specimen/VT323)
    font = ImageFont.truetype(fontname, font_size)  # Increase size value
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
        
    margin = 10
    # Placing the text in the bottom-left corner
    text_position = (margin, height - text_height - margin)
    draw.text(text_position, text, fill="black", font=font)
    
    return image



# --- Function to Generate a Tone for Each Slide ---
def generate_tone(duration, sample_rate, min_freq=300, max_freq=1000):
    # Summon a tone of random frequency between 300 Hz and 1000 Hz
    frequency = random.uniform(min_freq, max_freq)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    amplitude = 0.5
    tone = amplitude * np.sin(2 * np.pi * frequency * t)
    # Create a stereo tone (duplicate the channel)
    tone_stereo = np.column_stack((tone, tone))
    return tone_stereo

def generate_sine_wave():
    """
    Generates a random sine wave tone between 330Hz and 1000Hz.

    Returns:
        frequency (float): The generated frequency in Hz.
        sample_rate (int): The sample rate of the audio.
        sine_wave (numpy.ndarray): The generated sine wave audio data.
    """
    # Generate a random frequency between 330Hz and 1000Hz
    frequency = np.random.uniform(330, 1000)

    # Sampling rate and duration
    sample_rate = 44100  # 44.1 kHz standard audio rate
    duration = 2.0  # 2 seconds

    # Generate time values
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Generate sine wave
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # Amplitude scaled to 0.5 to prevent clipping

    return frequency, sample_rate, sine_wave
    
# --- Main Conjuration Routine ---
def generate_video(width=1920, height=1080, num_slides=10, slide_duration=1.0, font="arial.ttf", font_size=24, displayed_file_name="aqua.flv", min_freq=300, max_freq=1000, file_name="torso_output.mp4", fps=25):
    slide_clips = []   # To collect visual clips of each slide
    audio_segments = []  # To collect corresponding audio tones

    # For each slide, create its visual and auditory essence
    for i in range(1, num_slides + 1):
        # Generate and convert slide image into an array for MoviePy
        pil_image = generate_slide(i, width, height, font, font_size, displayed_file_name)
        frame = np.array(pil_image)
        clip = ImageClip(frame).set_duration(slide_duration)
        slide_clips.append(clip)
        
        # Generate the unique tone for this slide
        tone = generate_tone(slide_duration, SAMPLE_RATE, min_freq, max_freq)
        audio_segments.append(tone)
    
    # Conjure the video by concatenating all slide clips
    video = concatenate_videoclips(slide_clips, method="compose")
    
    # Merge the audio tones into a continuous stream
    audio_array = np.concatenate(audio_segments, axis=0)
    audio_clip = AudioArrayClip(audio_array, fps=SAMPLE_RATE)
    
    # Bind the audio to the visual sequence
    video = video.set_audio(audio_clip)
    
    # Output the final spectral creation to a file
    video.write_videofile(file_name, fps=fps, codec="libx264", audio_codec="aac")

if __name__ == '__main__':
    generate_video()
