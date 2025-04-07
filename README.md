# TranscribeASR

TranscribeASR (TASR, pronounced "Tay-ser") is a simple CLI based on ASR technology, focused on quickly and accurately converting audio files into text, helping users improve their work efficiency.

## Installation

Install via pip:

```bash
pip install tasr
```

## Dependencies

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Demucs (Optional, only required for noise reduction):

```bash
pip install demucs
```

## Usage

### Basic Usage

```bash
tasr --input <audio_file_path> [--output <output_text_file_path>] [--language <language>] [--denoise]
```

| Parameter    | Required | Description                                                                                                                      |
| ------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `--input`    | Yes      | Path to the input audio file.                                                                                                    |
| `--output`   | No       | Path to the output text file. If not specified, it defaults to the same name as the input audio file with a `.txt` extension.    |
| `--language` | No       | Specify the language for recognition (e.g., `'en'`, `'zh'`, `'yue'`, `'ja'`, `'ko'`). Default is `'auto'` (automatic detection). |
| `--denoise`  | No       | Whether to perform noise reduction on the audio. Disabled by default.                                                            |

## Examples

### Basic Speech Recognition

Perform speech recognition on the audio file `example.wav` and save the result as `example.txt`:

```bash
tasr --input example.wav
```

### Specify Output File

Perform speech recognition on the audio file `example.wav` and save the result as `output.txt`:

```bash
python cli.py --input example.wav --output output.txt
```

## Notes

Supported audio formats depend on the capabilities of `soundfile` and `demucs`, typically including `.wav`, `.flac`, `.mp3`, etc.
For best results with noise reduction, it is recommended to use `.wav` format.
