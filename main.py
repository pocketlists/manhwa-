import os
from src.extract_zip import extract_input_zip
from src.sequence_selector import SequenceSelector
from src.video_renderer import render_video

def main():
    print("--- AI MANHWA VIDEO RENDERER ---")
    zip_path = "assets/input.zip"
    audio_path = "assets/audio.mp3"  # <-- Apni audio file yahan rakhein

    # Step 1: Extract Zip
    if not os.path.exists("assets/images"):
        extract_input_zip(zip_path)
    else:
        print("Images already extracted.")

    # Step 2: Load Transcript (Agar transcript.txt nahi hai, toh Whisper use hoga)
    transcript_lines = []
    if os.path.exists("assets/transcript.txt"):
        with open("assets/transcript.txt", "r", encoding="utf-8") as f:
            transcript_lines = [line.strip() for line in f.readlines() if line.strip()]
    else:
        print("Transcript not found. Using Whisper to generate...")
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        transcript_lines = result["text"].split(".")

    # Step 3: Choose Method
    selector = SequenceSelector("assets/images", transcript_lines)
    print("\nChoose Sequence Method:")
    print("1. OpenAI Text Matching (Fastest)")
    print("2. OpenAI Vision AI (Most Accurate)")
    print("3. Local CLIP (Free/Private)")
    
    choice = input("Enter 1, 2, or 3: ")
    
    api_key = "YOUR_OPENAI_API_KEY"  # Yahan apni key daalein
    
    if choice == "1":
        ordered_images = selector.method_text_matching(api_key)
    elif choice == "2":
        ordered_images = selector.method_vision_ai(api_key)
    elif choice == "3":
        ordered_images = selector.method_local_clip()
    else:
        print("Invalid choice, defaulting to Local CLIP.")
        ordered_images = selector.method_local_clip()

    print(f"📸 Sequence decided: {ordered_images}")

    # Step 4: Render Video
    render_video(ordered_images, audio_path)

if __name__ == "__main__":
    main()
