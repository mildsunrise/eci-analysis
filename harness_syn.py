import os
import sys
from array import array
sys.path.append(_dirname := os.path.dirname(__file__))
sys.path.append(os.getenv('PYWIN32_CFFI'))

from typing import Callable, TYPE_CHECKING
import bindings.syn as syn
if TYPE_CHECKING:
	from bindings._syn_cffi import Array, types

# workaround for pyright bug (lambda parameters not inferred when setting an attribute that is descriptor-backed)
def withType[T](_a: T) -> Callable[[T], T]:
	return lambda x: x

from bindings._syn_cffi import ffi
import re
paramNames = { k: re.fullmatch('SynthParam_(.+)', v).group(1) for k, v in ffi.typeof('enum SynthParamId').elements.items() }

engine = syn.SynthEngine('ENG.SYN')
synth = syn.Synth(engine)
print('synth initialized:', synth.obj._obj)

audio = array('h')
wordIndices = True

def log(x: str):
	print(f'[{len(audio):8}] {x}', flush=True)

synth.callbackEvent = withType(synth.callbackEvent)(lambda ev: print('event:', ev))
synth.callbackPhoneme = withType(synth.callbackPhoneme)(lambda p, unk: log(f'phoneme {p!r} {unk or ''}'))
synth.callbackParam = withType(synth.callbackParam)(lambda k, v: log(f'param {paramNames[k]} = {v}'))
synth.callbackTextIndex = withType(synth.callbackTextIndex)(lambda idx: log(f'text index: {idx}'))
synth.callbackAudio = withType(synth.callbackAudio)(lambda buf: audio.extend(buf))
if wordIndices: synth.callbackWordIndex = withType(synth.callbackWordIndex)(lambda idx: log(f'word index: {idx}'))

synth.resetParams()
synth.setFlushing(False)
print('callbacks set up.')

synth.pushText("`v1 `ts0 `da1 `ty1 `pp1 `espr1 `esr1", flush=True)
synth.setWantWordIndices(wordIndices)

print('synthesizing text...')
synth.pushText("Hello world!", flush=True)
log(f'phonemes: {synth.readPhonemes()!r}')

with open(fname := '/tmp/result-audio.raw', 'wb') as f:
	f.write(audio)
print(f'wrote {len(audio)} samples to {fname!r}')
