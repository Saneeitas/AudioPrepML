import os
from pydub import AudioSegment

# Set the path to ffmpeg explicitly

def split_audio(file_path, output_folder, min_length=15000, max_length=15000):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Calculate the number of chunks
    total_length = len(audio)
    start = 0
    chunk_number = 1

    while start < total_length:
        # Calculate the end of the chunk
        end = start + min_length
        if end > total_length:
            end = total_length

        # Ensure the chunk is within the max_length
        if end - start > max_length:
            end = start + max_length

        # Extract the chunk
        chunk = audio[start:end]

        # Save the chunk to the output folder
        chunk_name = f"chunk_{chunk_number}.wav"
        chunk_path = os.path.join(output_folder, chunk_name)
        chunk.export(chunk_path, format="wav")

        # Print the chunk information
        print(f"Saved {chunk_name} ({len(chunk)} ms)")

        # Update the start time and chunk number
        start = end
        chunk_number += 1

if __name__ == "__main__":
    # Path to your audio file (inside the "audio" folder)
    audio_file = os.path.join("audio", "2.mp3")  # Replace "your_audio_file.mp3" with your file name

    # Output folder to store the chunks (inside the "audio" folder)
    output_folder = os.path.join("audio", "audio_chunks")

    # Split the audio into chunks
    split_audio(audio_file, output_folder)