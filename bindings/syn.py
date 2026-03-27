import codecs
from ._syn_cffi import ffi
import weakref
from . import _syn_intermediate as wrappers
import os.path
_dirname = os.path.dirname(__file__)
ENGINE_PATH = os.path.join(_dirname, r'..\synthDrivers\eloquence')

from typing import TYPE_CHECKING, Callable, cast
if TYPE_CHECKING:
	from ._syn_cffi import types, _CDataBase, PointerBase # pyright: ignore[reportPrivateUsage]

__all__ = ['SynthEngine', 'Synth', 'SynthDict']

def _check(x: int):
	assert not x, f'unsuccessful: {x}'

class SynthEngine:
	def __init__(self, basename: str, engine_path: str=ENGINE_PATH):
		self.lib = ffi.dlopen(os.path.join(engine_path, basename))

class CallbackProp[Ptr: _CDataBase, R, *P]:
	type CallbackSetter = Callable[[Ptr, 'PointerBase[object]'], None]
	type StoredValue = Callable[[*P], R] | None

	def __init__(self,
		setter_accessor: Callable[[wrappers.Synth], CallbackSetter],
		decorator: Callable[[ Callable[[*tuple[*P, 'PointerBase[object]']], R] ], Ptr],
	):
		self.setter_accessor = setter_accessor
		def trampoline(*all_args: *tuple[*P, 'PointerBase[object]']) -> R:
			*args, cookie = all_args
			obj = cast(weakref.ref[Synth], ffi.from_handle(cookie))()
			assert obj, 'weakref is stale. this should never happen.'
			return obj.__dict__[self.attr_name](*args)
		self.trampoline = decorator(trampoline)

	def __set_name__(self, _owner: type['Synth'], name: str):
		if hasattr(self, 'attr_name'):
			assert self.attr_name == name
		self.attr_name = name

	def __get__(self, obj: 'Synth', objtype: type['Synth']) -> StoredValue:
		return obj.__dict__.get(self.attr_name)

	def __set__(self, obj: 'Synth', value: StoredValue):
		prev = obj.__dict__.get(self.attr_name)
		if prev and not value:
			self.setter_accessor(obj.obj)(ffi.NULL, ffi.NULL)
		obj.__dict__[self.attr_name] = value
		if value and not prev:
			self.setter_accessor(obj.obj)(self.trampoline, obj.cb_cookie)

class Synth:
	def __init__(self, engine: SynthEngine):
		outPtr = ffi.new('struct Synth * *')
		engine.lib.getObject(2, outPtr)
		assert outPtr[0], f'failed to allocate engine'
		self.obj = wrappers.Synth(outPtr[0])
		self.engine = engine # keep alive
		self.cb_cookie = ffi.new_handle(weakref.ref(self))

		_check(self.obj.init())

	def __del__(self):
		#self.obj.preDestruct()
		self.obj.destroy()
		del self.obj

	def preDestruct(self):
		''' called by ECI just before `destroy` (?) '''
		self.obj.preDestruct()

	def setFlushing(self, value: bool):
		''' ECI sets this to false when switching to an engine (on the new engine) and toggles it momentarily as part of `eciStop` '''
		_check(self.obj.setFlushing(value))

	def prepare(self):
		''' ECI calls this when switching to an engine (on the new engine) so presumably it resets some internal state or prepares for synthesis in some way? '''
		_check(self.obj.prepare())

	def pushText(self, text: str | bytes, alt: bool = False):
		_text = text.encode('latin-1') if isinstance(text, str) else text
		_check((self.obj.pushText2 if alt else self.obj.pushText)(_text))

	def pushEvent(self, id: int, at: int | None = None):
		if at != None:
			_check(self.obj.pushEventAt(id, at))
		else:
			_check(self.obj.pushEvent(id))

	def readPhonemes(self, n: int = -1) -> bytes:
		if n == -1:
			raise NotImplementedError
		buf = ffi.new('char[]', n)
		size = ffi.new('int *', n)
		for i in range(n): buf[i] = b'\xFF'
		_check(self.obj.readPhonemes(buf, n-1, size)) # FIXME: remove the -1
		assert all(x == b'\xFF' for x in buf[size[0]:])
		return ffi.string(buf[:size[0]])

	def setWantWordIndices(self, value: bool):
		self.obj.setWantWordIndices(value)

	callbackAudio = CallbackProp(lambda obj: obj.setCallbackAudio, ffi.callback('SynthAudioCb'))
	callbackTextIndex = CallbackProp(lambda obj: obj.setCallbackTextIndex, ffi.callback('SynthTextIndexCb'))
	callbackEvent = CallbackProp(lambda obj: obj.setCallbackEvent, ffi.callback('SynthEventCb'))
	callbackPhoneme = CallbackProp(lambda obj: obj.setCallbackPhoneme, ffi.callback('SynthPhonemeCb'))
	callbackParam = CallbackProp(lambda obj: obj.setCallbackParam, ffi.callback('SynthParamCb'))
	callbackWordIndex = CallbackProp(lambda obj: obj.setCallbackWordIndex, ffi.callback('SynthWordIndexCb'))
	callbackUserIndex = CallbackProp(lambda obj: obj.setCallbackUserIndex, ffi.callback('SynthUserIndexCb'))

	def deactivateDict(self):
		self.obj.dictSetActive(ffi.NULL)

class SynthDict:
	def __init__(self, synth: Synth):
		''' creates an empty dictionary '''
		assert (obj := synth.obj.dictNew()), 'failed to allocate dict'
		self.obj = wrappers.SynthDict(synth.obj, obj)
		self.synth = synth # keep alive

	def __del__(self):
		self.obj.delete()
		del self.obj

	def setActive(self):
		self.obj.setActive()

	def __getitem__(self, volume: 'types.SynthDictVolume'):
		self.Volume(self, volume)

	class Volume:
		def __init__(self, dict: 'SynthDict', volume: 'types.SynthDictVolume'):
			self.obj = wrappers.SynthDictVolume(dict.obj, volume)
			self.dict = dict # keep alive

		@staticmethod
		def _tostr(x: str | bytes) -> bytes:
			if isinstance(x, str):
				return codecs.encode(x, 'utf-8')
			return x
		@staticmethod
		def _fromstr(x: 'types.SynthDictStr') -> str:
			assert x
			return codecs.decode(ffi.buffer(x), 'utf-8')

		def __contains__(self, key: str | bytes) -> bool:
			return bool(self.obj.lookup(self._tostr(key)))

		def __getitem__(self, key: str | bytes) -> str:
			if translation := self.obj.lookup(self._tostr(key)):
				return self._fromstr(translation)
			raise KeyError(key)

		def __setitem__(self, key: str | bytes, translation: str | bytes):
			_check(self.obj.update(self._tostr(key), self._tostr(translation)))

		def __delitem__(self, key: str | bytes):
			_check(self.obj.update(self._tostr(key), ffi.NULL))

		def __iter__(self):
			key, translation = ffi.new('char * *'), ffi.new('char * *')
			self.obj.getFirstEntry(key, translation)
			while key:
				yield self._fromstr(key[0]), self._fromstr(translation[0])
				self.obj.getNextEntry(key, translation)
			assert not translation

		def load(self, filename: bytes):
			self.obj.load(filename)
		def save(self, filename: bytes):
			self.obj.save(filename)
