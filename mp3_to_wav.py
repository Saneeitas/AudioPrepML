from pydub import AudioSegment
import os

def convert_audio(input_path, output_path, from_format, to_format):
    # Validate input file existence
    if not os.path.exists(input_path):
        print(f"Error: The file {input_path} does not exist.")
        return
    
    # Validate formats
    supported_formats = ["wav", "mp3"]
    from_format = from_format.lower()
    to_format = to_format.lower()
    
    if from_format not in supported_formats or to_format not in supported_formats:
        print(f"Error: Supported formats are {supported_formats}. Got from_format='{from_format}' and to_format='{to_format}'.")
        return
    
    # Check if input file matches the specified from_format
    if not input_path.lower().endswith(f".{from_format}"):
        print(f"Error: Input file {input_path} does not match the specified from_format '{from_format}'.")
        return
    
    # Ensure output path has the correct extension
    if not output_path.lower().endswith(f".{to_format}"):
        output_path = output_path.rsplit('.', 1)[0] + f".{to_format}"
    
    try:
        # Load the audio file based on the from_format
        if from_format == "wav":
            audio = AudioSegment.from_wav(input_path)
        elif from_format == "mp3":
            audio = AudioSegment.from_mp3(input_path)
        
        # Export to the specified to_format
        audio.export(output_path, format=to_format)
        print(f"Successfully converted {input_path} ({from_format}) to {output_path} ({to_format})")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Example 1: WAV to MP3
    convert_audio(
        input_path="audio/audio13.wav",
        output_path="audio13.mp3",
        from_format="wav",
        to_format="mp3"
    )

    # Example 2: MP3 to WAV
    convert_audio(
        input_path="audio11.mp3",
        output_path="output_audio.wav",
        from_format="mp3",
        to_format="wav"
    )