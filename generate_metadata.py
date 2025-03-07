import os
import csv
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def generate_metadata(dataset_dir, wavs_dir, transcripts_dir, output_csv):
    speakers = ['adnan', 'meena']
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_NONE, escapechar='\\')
        
        for speaker in speakers:
            wav_folder = os.path.join(wavs_dir, speaker)
            transcript_folder = os.path.join(transcripts_dir, speaker)
            
            wav_files = [f for f in os.listdir(wav_folder) if f.endswith('.wav')]
            wav_files.sort(key=natural_sort_key)
            
            for wav_file in wav_files:
                base_name = os.path.splitext(wav_file)[0]
                txt_file = f"{base_name}.txt"
                # Use forward slashes for the path
                wav_path = f"wavs/{speaker}/{wav_file}"  # Force forward slashes
                txt_path = os.path.join(transcript_folder, txt_file)
                
                if os.path.exists(txt_path):
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        transcript = f.read().strip()
                else:
                    print(f"Warning: Transcript not found for {wav_path}. Using empty string.")
                    transcript = ""
                
                writer.writerow([wav_path, transcript, speaker])
                print(f"Added: {wav_path}|{transcript}|{speaker}")

if __name__ == "__main__":
    dataset_dir = "dataset"
    wavs_dir = os.path.join(dataset_dir, "wavs")
    transcripts_dir = os.path.join(dataset_dir, "transcripts")
    output_csv = os.path.join(dataset_dir, "metadata.csv")
    
    generate_metadata(dataset_dir, wavs_dir, transcripts_dir, output_csv)
    print(f"Metadata CSV generated at: {output_csv}")