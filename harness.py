import sys
import os
sys.path.append(_dirname := os.path.dirname(__file__))
sys.path.append(os.getenv('PYWIN32_CFFI'))
from _eloquence_cffi import ffi

ENGINE_PATH = os.path.join(_dirname, 'synthDrivers\\eloquence')
with open(os.path.join(ENGINE_PATH, 'ECI.INI.orig'), 'r') as f:
    ini_orig = f.read()
with open(os.path.join(ENGINE_PATH, 'ECI.INI'), 'w') as f:
    f.write(ini_orig.replace('ENGINE_PATH', ENGINE_PATH))
lib = ffi.dlopen(os.path.join(ENGINE_PATH, 'ECI.DLL'))

from enum import IntFlag
import hashlib

ECI_PRESET_VOICES  = 8
ECI_USER_DEFINED_VOICES  = 8

ECI_VOICE_NAME_LENGTH  = 30

class ErrorCode(IntFlag):
    SYSTEMERROR			= 0x00000001
    MEMORYERROR			= 0x00000002
    MODULELOADERROR		= 0x00000004
    DELTAERROR			= 0x00000008
    SYNTHERROR			= 0x00000010
    DEVICEERROR			= 0x00000020
    DICTERROR			= 0x00000040
    PARAMETERERROR		= 0x00000080
    SYNTHESIZINGERROR	= 0x00000100
    DEVICEBUSY			= 0x00000200
    SYNTHESISPAUSED		= 0x00000400
    REENTRANTCALL		= 0x00000800
    ROMANIZERERROR		= 0x00001000
    SYNTHESIZING		= 0x00002000

eciPhonemeLength = 4

version = ffi.new('char[]', 20)
lib.eciVersion(version)
version = ffi.string(version)
print('eciVersion:', version)

langs_num = ffi.new('int*')
assert not (ret := lib.eciGetAvailableLanguages(ffi.NULL, langs_num)), f'eciGetAvailableLanguages failed: {ret:#x}'
langs = ffi.new('enum ECILanguageDialect[]', langs_num[0])
assert not (ret := lib.eciGetAvailableLanguages(langs, langs_num)) and langs_num[0] == len(langs), f'eciGetAvailableLanguages failed: {ret:#x}'
langs = [ ffi.cast("enum ECILanguageDialect", x) for x in langs ]
print(f'found {len(langs)} languages:')
for lang in langs:
    print(f' - {ffi.string(lang)}')

engine = lib.eciNewEx(lib.eciGeneralAmericanEnglish)
assert engine, f'failed creating engine'

err_msg_buf = ffi.new('char[]', 100)
def check_err(b: bool):
    if b: return
    bits = ErrorCode(lib.eciProgStatus(engine))
    lib.eciErrorMessage(engine, err_msg_buf)
    msg = ffi.string(err_msg_buf)
    lib.eciClearErrors(engine)
    raise AssertionError(f'failed {bits} {msg!r}')

@ffi.callback('ECICallback')
def callback(_engine, msg, param, _data):
    if msg == lib.eciWaveformBuffer:
        audio = audio_buf[0:param]
        hash = hashlib.sha256(ffi.buffer(audio)).digest()
        print(f'waveform buffer ({param} samples): {hash.hex()}')
    else:
        print('message:', ffi.string(ffi.cast('enum ECIMessage', msg)), param)
    return lib.eciDataProcessed
lib.eciRegisterCallback(engine, callback, ffi.NULL)

audio_buf = ffi.new('short[]', 48000 * 60)
check_err(lib.eciSetOutputBuffer(engine, len(audio_buf), audio_buf))

def eciAddText(text: str):
    check_err(lib.eciAddText(engine, text.encode('mbcs')))
def eciSynthesize():
    check_err(lib.eciSynthesize(engine))
def eciSynchronize():
    check_err(lib.eciSynchronize(engine))

eciAddText('Hello, does this work?')
eciSynthesize()
eciSynchronize()
