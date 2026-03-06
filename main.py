from sys import argv
from pathlib import Path
from mutagen.id3 import ID3
from mutagen.id3._frames import TXXX
from mutagen._file import File
from pydub import AudioSegment


def main():
    dirpath = parse_args()
    print("Trimming clips...")
    trim_silence(dirpath)
    print("Done")


def parse_args():
    # One argument, the path of the folder containing the clips.
    if len(argv) != 2:
        print("There should be only one arg: the dirpath containing the clips.")
        exit(1)

    try:
        dirpath = Path(argv[1])
    except Exception as e:
        print(f"Problem parsing path arg: {str(e)}")
        exit(1)

    if not dirpath.is_dir():
        print(f"Path '{audio_path}' is not a valid directory.")
        exit(1)

    return dirpath


def trim_silence(dirpath):
    clips = set()

    for file in dirpath.iterdir():
        if file.suffix == ".mp3":
            clips.add(file)

    for clip in clips:
        trimmed = check_trimmed(clip)

        if not trimmed:
            sound = AudioSegment.from_file(clip, format="mp3")

            start_trim = detect_leading_silence(sound)
            end_trim = detect_leading_silence(sound.reverse())

            duration = len(sound)
            trimmed_sound = sound[start_trim : duration - end_trim]
            trimmed_sound.export(clip, format="mp3")

            add_trimmed_tag(clip)

    return


def check_trimmed(clip):
    file = File(clip)
    if not file or not file.tags:
        return False
    for frame in file.tags.getall("TXXX"):
        if frame.desc == "silence_trimmed":
            return True

    return False


def add_trimmed_tag(clip):
    mp3_metadata = ID3(clip)
    mp3_metadata.add(TXXX(encoding=3, desc="silence_trimmed", text="True"))
    mp3_metadata.save()


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=5):
    """
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    """
    trim_ms = 0  # ms

    assert chunk_size > 0  # to avoid infinite loop
    while sound[
        trim_ms : trim_ms + chunk_size
    ].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


if __name__ == "__main__":
    main()
