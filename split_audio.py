import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_audio_with_silence(file_path, output_folder, target_length=15000, min_silence_len=500, silence_thresh=-40):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Split audio based on silence
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,  # Minimum length of silence to consider as a break (in ms)
        silence_thresh=silence_thresh,     # Silence threshold (in dBFS)
        keep_silence=200                   # Keep some silence at the start/end of each chunk (in ms)
    )

    # Merge chunks to approximate target_length (15 seconds)
    merged_chunks = []
    current_chunk = AudioSegment.empty()
    
    for chunk in chunks:
        if len(current_chunk) + len(chunk) <= target_length:
            current_chunk += chunk
        else:
            if len(current_chunk) > 0:
                merged_chunks.append(current_chunk)
            current_chunk = chunk
    
    # Append the last chunk if it exists
    if len(current_chunk) > 0:
        merged_chunks.append(current_chunk)

    # Save the merged chunks
    for i, chunk in enumerate(merged_chunks, start=1):
        chunk_name = f"chunk_{i}.wav"
        chunk_path = os.path.join(output_folder, chunk_name)
        chunk.export(chunk_path, format="wav")
        print(f"Saved {chunk_name} ({len(chunk)} ms)")

    # Handle any remaining audio that didn't fit into chunks
    total_length = sum(len(chunk) for chunk in merged_chunks)
    if total_length < len(audio):
        remaining = audio[total_length:]
        if len(remaining) > 0:
            chunk_name = f"chunk_{len(merged_chunks) + 1}.wav"
            chunk_path = os.path.join(output_folder, chunk_name)
            remaining.export(chunk_path, format="wav")
            print(f"Saved {chunk_name} ({len(remaining)} ms)")

if __name__ == "__main__":
    # Path to your audio file (inside the "audio" folder)
    audio_file = os.path.join("audio", "audio11.mp3")  # Replace with your file name

    # Output folder to store the chunks (inside the "audio" folder)
    output_folder = os.path.join("audio", "audio_chunks")

    # Split the audio into chunks with silence detection
    split_audio_with_silence(
        audio_file,
        output_folder,
        target_length=15000,      # Target chunk length (15 seconds)
        min_silence_len=500,     # Minimum silence length to split (adjustable)
        silence_thresh=-40       # Silence threshold (adjustable)
    )