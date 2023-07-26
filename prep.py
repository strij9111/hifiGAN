import os
import random
import librosa
from scipy.io.wavfile import write

def split_audio_files(input_dir, output_dir_clean, output_dir_wavs, segment_length, train_file, valid_file):
    file_names = [f for f in os.listdir(input_dir) if f.endswith('.wav')]
    base_file_names = set(f[:-8] for f in file_names if f.endswith('_ns1.wav') or f.endswith('_ns2.wav'))    
    train_files = []
    valid_files = []

    for base_file_name in base_file_names:        
        file_name = base_file_name + '.wav'
        file_path = os.path.join(input_dir, file_name)
        audio, _ = librosa.load(file_path, sr=22050)
        print(file_name + " processing")
        segments = [audio[i:i+segment_length] for i in range(0, len(audio), segment_length)]
        
        file_name1 = base_file_name + '_ns1.wav'
        file_path = os.path.join(input_dir, file_name1)
        audio_ns1, _ = librosa.load(file_path, sr=22050)

        file_name2 = base_file_name + '_ns2.wav'
        file_path = os.path.join(input_dir, file_name2)
        audio_ns2, _ = librosa.load(file_path, sr=22050)
            
        for i, segment in enumerate(segments):
            if len(segment) < segment_length:
                continue  # Skip segments that are too short
            segment_file_name = f'{file_name[:-4]}_segment_{i}.wav'
            
            output_dir = output_dir_clean

            segment_file_path = os.path.join(output_dir, segment_file_name)
            write(segment_file_path, 22050, segment)

            segment_file_name1 = f'{file_name[:-4]}_segment_{i}_1.wav'
            segment_file_path = os.path.join(output_dir, segment_file_name1)
            write(segment_file_path, 22050, segment)
            
            output_dir = output_dir_wavs
            
            start_sample = i * segment_length
            end_sample = start_sample + segment_length
            
            segment_ns1 = audio_ns1[start_sample:end_sample]            
            segment_file_path = os.path.join(output_dir, segment_file_name)
            write(segment_file_path, 22050, segment_ns1)

            segment_ns2 = audio_ns2[start_sample:end_sample]
            segment_file_path = os.path.join(output_dir, segment_file_name1)
            write(segment_file_path, 22050, segment_ns2)
            
            if random.random() < 0.8:  # Use 80% of the data for training
                train_files.append(segment_file_name)
            else:  # Use the remaining 20% for validation
                valid_files.append(segment_file_name)

            if random.random() < 0.8:  # Use 80% of the data for training
                train_files.append(segment_file_name1)
            else:  # Use the remaining 20% for validation
                valid_files.append(segment_file_name1)
                
        print(file_name + " complete")
        
        
    with open(train_file, 'w') as f:
        for file_name in train_files:
            f.write(f'{file_name}\n')

    with open(valid_file, 'w') as f:
        for file_name in valid_files:
            f.write(f'{file_name}\n')

# Use the function:
split_audio_files("f:\\dataset_noise", "e:\\hifigan\\data\\clean", "e:\\hifigan\\data\\wavs", 32000, 'train_files.txt', 'valid_files.txt')
