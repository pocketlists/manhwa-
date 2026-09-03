import os
import glob
import base64

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from src.extract_zip import find_zip_file, extract_input_zip
from src.sequence_selector import SequenceSelector
from src.video_renderer import render_video


def find_audio_file(directory="assets"):
    extensions = ['*.mp3', '*.wav', '*.m4a', '*.flac', '*.aac', '*.ogg']
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, ext)))
    if not files:
        raise FileNotFoundError("No audio file found in 'assets' folder. Please add your audio file.")
    return files[0]


def main():
    print("--- AI MANHWA VIDEO RENDERER ---")

    # Step 1: Auto-Detect ZIP
    zip_path = find_zip_file("assets")
    print(f"Found ZIP: {zip_path}")

    # Step 2: Auto-Detect Audio
    audio_path = find_audio_file("assets")
    print(f"Found Audio: {audio_path}")

    # Step 3: Extract Images from ZIP
    extract_input_zip(zip_path)

    # Step 4: Load Transcript (or use Whisper)
    transcript_lines = []
    transcript_path = "assets/transcript.txt"
    if os.path.exists(transcript_path):
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_lines = [line.strip() for line in f.readlines() if line.strip()]
    else:
        print("Transcript not found. Using Whisper to generate...")
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        transcript_lines = result["text"].split(".")

    # Step 5: API Key from GitHub Secret
    api_key = os.environ.get("OPENAI_API_KEY")

    # Step 6: Choose Method
    selector = SequenceSelector("assets/images", transcript_lines)
    print("\nChoose Sequence Method:")
    print("1. OpenAI Text Matching (Fastest)")
    print("2. OpenAI Vision AI (Most Accurate)")
    print("3. Local CLIP (Free/Private)")

    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        if not api_key:
            print("Error: OPENAI_API_KEY missing in Secrets!")
            return
        ordered_images = selector.method_text_matching(api_key)
    elif choice == "2":
        if not api_key:
            print("Error: OPENAI_API_KEY missing in Secrets!")
            return
        ordered_images = selector.method_vision_ai(api_key)
    else:
        ordered_images = selector.method_local_clip()

    print(f"Sequence decided: {ordered_images}")

    # Step 7: Render Final Video
    render_video(ordered_images, audio_path)


if __name__ == "__main__":
    main()
