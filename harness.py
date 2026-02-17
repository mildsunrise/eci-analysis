import sys
sys.path.append(os.getenv('PYWIN32_CFFI'))

from bindings import eci
from bindings.eci import ffi, lib
import hashlib

print('eciVersion:', eci.version())

langs = eci.availableLanguages()
print(f'found {len(langs)} languages:')
for lang in langs:
    print(f' - {ffi.string(lang)}')

engine = eci.ECI(lib.eciGeneralAmericanEnglish)

@ffi.callback('ECICallback')
def callback(_engine, msg, param, _data):
    if msg == lib.eciWaveformBuffer:
        audio = audio_buf[0:param]
        with open('/tmp/audio.bin', 'wb') as f:
            f.write(ffi.buffer(audio))
        hash = hashlib.sha256(ffi.buffer(audio)).digest()
        print(f'waveform buffer ({param} samples): {hash.hex()}')
    else:
        print('message:', ffi.string(ffi.cast('enum ECIMessage', msg)), param)
    return lib.eciDataProcessed
lib.eciRegisterCallback(engine.eci, callback, ffi.NULL)

engine.setOutputBuffer(audio_buf := ffi.new('short[]', 48000 * 60))

engine.addText('Hello, does this work?')
engine.synthesize()
engine.synchronize()
