import pyttsx3

from web.blowhole.data import bass


def sound_get(words, path):
    print(path, "doodfgh")
    file = "recog_audio.wav"
    print(file)
    engine = pyttsx3.init(

    )
    engine.setProperty("rate", 178)
    engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0")

    engine.save_to_file(words, (path + file))
    # engine.say("i am blessed")
    engine.runAndWait()
    bass.main((path + file), "audio_data")
