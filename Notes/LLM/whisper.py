from transformers import pipeline

transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large-v2")

#file_path = 'https://huggingface.co/datasets/Narsil/asr_dummy/resolve/main/mlk.flac'
file_path = '/home/cacc/Documents/CodeNotes/Notes/Huggingface/13630134228757034767.wav'

result = transcriber(
    file_path,
    generate_kwargs={"language": "zh", "task": "transcribe"},    
)



print(result)
