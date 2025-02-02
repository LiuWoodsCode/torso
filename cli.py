import argparse
import torso

def main():
    parser = argparse.ArgumentParser(
        description="Generates a slideshow video with randomly placed geometric shapes and synthesized audio, inspired by Webdriver Torso."
    )
    
    parser.add_argument("-w", "--width", type=int, default=640, help="Width of the generated slides in pixels (default: 640)")
    parser.add_argument("-t", "--height", type=int, default=360, help="Height of the generated slides in pixels (default: 360)")
    parser.add_argument("-n", "--num_slides", type=int, default=10, help="Number of slides to generate (default: 10)")
    parser.add_argument("-d", "--slide_duration", type=float, default=1.0, help="Duration of each slide in seconds (default: 1.0)")
    parser.add_argument("--font", type=str, default="arial.ttf", help="Path to the font file used for slide text (default: arial.ttf)")
    parser.add_argument("--font_size", type=int, default=24, help="Font size for the slide text (default: 24)")
    parser.add_argument("-f", "--displayed_file_name", type=str, default="aqua.flv", help="File name displayed on the slides (default: aqua.flv)")
    parser.add_argument("--min_freq", type=int, default=400, help="Minimum frequency for generated tones in Hz (default: 400)")
    parser.add_argument("--max_freq", type=int, default=1000, help="Maximum frequency for generated tones in Hz (default: 1000)")
    parser.add_argument("-o", "--file_name", type=str, default="torso_output.mp4", help="Name of the output video file (default: torso_output.mp4)")
    parser.add_argument("--fps", type=int, default=25, help="Frames per second for the generated video (default: 25)")
    
    args = parser.parse_args()
    
    torso.generate_video(
        width=args.width,
        height=args.height,
        num_slides=args.num_slides,
        slide_duration=args.slide_duration,
        font=args.font,
        font_size=args.font_size,
        displayed_file_name=args.displayed_file_name,
        min_freq=args.min_freq,
        max_freq=args.max_freq,
        file_name=args.file_name,
        fps=args.fps
    )
    
    print(f"Video saved as {args.file_name}")

if __name__ == "__main__":
    main()
