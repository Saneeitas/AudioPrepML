import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_audio_with_silence(file_path, audio_folder, text_folder, speaker_name, start_number, max_length=15000, min_silence_len=500, silence_thresh=-40):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Convert to 24 kHz, 16-bit, mono (XTTS-v2 standard)
    audio = audio.set_frame_rate(24000).set_sample_width(2).set_channels(1)

    # Create the audio and text folders if they don't exist
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)
    if not os.path.exists(text_folder):
        os.makedirs(text_folder)

    # Split audio based on silence
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=200
    )

    # Merge chunks and enforce max_length
    merged_chunks = []
    current_chunk = AudioSegment.empty()
    
    for chunk in chunks:
        if len(current_chunk) + len(chunk) <= max_length:
            current_chunk += chunk
        else:
            if len(current_chunk) > 0:
                while len(current_chunk) > max_length:
                    merged_chunks.append(current_chunk[:max_length])
                    current_chunk = current_chunk[max_length:]
                merged_chunks.append(current_chunk)
            current_chunk = chunk
    
    if len(current_chunk) > 0:
        while len(current_chunk) > max_length:
            merged_chunks.append(current_chunk[:max_length])
            current_chunk = current_chunk[max_length:]
        merged_chunks.append(current_chunk)

    # Handle remaining audio
    total_length = sum(len(chunk) for chunk in merged_chunks)
    if total_length < len(audio):
        remaining = audio[total_length:]
        while len(remaining) > max_length:
            merged_chunks.append(remaining[:max_length])
            remaining = remaining[max_length:]
        if len(remaining) > 0:
            merged_chunks.append(remaining)

    # Save chunks and create text files with speaker name
    for i, chunk in enumerate(merged_chunks, start=start_number):
        audio_name = f"{speaker_name}_{i}.wav"
        audio_path = os.path.join(audio_folder, audio_name)
        chunk.export(audio_path, format="wav")
        print(f"Saved {audio_name} ({len(chunk)} ms)")

        text_name = f"{speaker_name}_{i}.txt"
        text_path = os.path.join(text_folder, text_name)
        with open(text_path, 'w') as f:
            f.write("")
        print(f"Created {text_name} for transcript")

    return len(merged_chunks) + start_number

if __name__ == "__main__":
    audio_file = os.path.join("audio", "audio11.mp3")
    audio_folder = os.path.join("audio", "audio_chunks")
    text_folder = os.path.join("audio", "text_chunks")

    # Prompt user for the speaker name
    speaker_name = input("Enter the speaker name (e.g., adnan, meena): ").strip().lower()
    if not speaker_name:
        print("Speaker name cannot be empty. Using 'unknown'.")
        speaker_name = "unknown"

    # Prompt user for the starting number
    while True:
        try:
            start_number = int(input(f"Enter the starting number for {speaker_name}'s audio split (e.g., 1): "))
            if start_number < 1:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    # Split audio with speaker-specific naming
    next_number = split_audio_with_silence(
        audio_file,
        audio_folder,
        text_folder,
        speaker_name=speaker_name,
        start_number=start_number,
        max_length=15000,
        min_silence_len=500,
        silence_thresh=-40
    )

    print(f"Next available number for {speaker_name}'s next audio split: {next_number}")