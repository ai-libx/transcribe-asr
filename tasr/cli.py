import argparse
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import soundfile as sf
import subprocess
import os
import torch

def denoise_audio_with_demucs(input_audio_file, output_audio_file):
    print("Starting audio denoising...")
    output_dir = "separated/htdemucs"
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "demucs",
        "--two-stems=vocals",
        input_audio_file
    ]
    subprocess.run(command, check=True)

    base_name = os.path.splitext(os.path.basename(input_audio_file))[0]
    vocals_file = os.path.join(output_dir, base_name, "vocals.wav")

    if os.path.exists(vocals_file):
        os.rename(vocals_file, output_audio_file)
        print(f"Denoising completed. Denoised audio saved to: {output_audio_file}")
    else:
        raise FileNotFoundError("Could not find the separated vocal file. Please check Demucs output.")

def recognize_audio(audio_file, language="auto"):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = AutoModel(
        model="danieldong/sensevoice-small-onnx-quant",
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device=device,
        disable_update=True
    )
    
    print("Starting speech recognition...")
    result = model.generate(
        input=audio_file,
        cache={},
        language=language,
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        merge_length_s=15,
    )
    
    text_with_punc = rich_transcription_postprocess(result[0]["text"])
    return text_with_punc

def save_text_to_file(text, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Recognition result saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Perform speech recognition using FunASR and SenseVoice-Small-ONNX-Quant model, and save the result to a text file.")
    parser.add_argument("--input", required=True, help="Path to the input audio file")
    parser.add_argument("--output", required=False, help="Path to the output text file")
    parser.add_argument("--language", default="auto", help="Specify the language (e.g., 'en', 'zh', 'yue', 'ja', 'ko'). Default is auto-detection.")
    parser.add_argument("--denoise", action="store_true", help="Whether to perform audio denoising")
    args = parser.parse_args()

    input_audio_file = args.input
    if args.output:
        output_text_file = args.output
    else:
        output_text_file = input_audio_file.rsplit('.', 1)[0] + ".txt"

    try:
        if args.denoise:
            denoised_audio_file = input_audio_file.rsplit('.', 1)[0] + "_denoised.wav"
            denoise_audio_with_demucs(input_audio_file, denoised_audio_file)
            audio_file_to_recognize = denoised_audio_file
        else:
            audio_file_to_recognize = input_audio_file

        recognized_text = recognize_audio(audio_file_to_recognize, language=args.language)
        print("Recognition result:", recognized_text)

        save_text_to_file(recognized_text, output_text_file)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()