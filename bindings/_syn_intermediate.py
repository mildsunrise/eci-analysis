# pyright: reportPrivateUsage=false

from abc import abstractmethod
from typing import Callable, Any, TYPE_CHECKING, cast
if TYPE_CHECKING:
	from ._syn_cffi import types

class ObjBase[Obj, VT]:
	''' wrapper to make vtable calls less verbose '''
	def __init__(self, obj: Obj):
		self._obj = obj

	@property
	@abstractmethod
	def _vtable(self) -> VT: ...

	class FnWrap[R, *P]:
		def __init__(self, accessor: Callable[[VT], Callable[[Obj, *P], R]]):
			self.accessor = accessor
		def __get__(self, _obj: 'ObjBase[Any, Any]', _objtype: type) -> Callable[[*P], R]:
			obj = cast('ObjBase[Obj, VT]', _obj)
			assert obj != None
			fn = self.accessor(obj._vtable)
			def wrapped(*args: *P):
				return fn(obj._obj, *args)
			return wrapped

	@classmethod
	def _wrap_function[R, *P](cls, accessor: Callable[[VT], Callable[[Obj, *P], R]]):
		return cls.FnWrap(accessor)

class Synth(_base := ObjBase['types.SynthPtr', 'types.struct_Synth_vtable']):
	_wrap = _base._wrap_function
	@property
	def _vtable(self):
		return self._obj[0].vtable[0]

	__method0 = _wrap(lambda vt: vt.__method0)
	'''
	.. code-block:: c
		void __method0(); '''
	__method1 = _wrap(lambda vt: vt.__method1)
	'''
	.. code-block:: c
		void __method1(); '''
	destroy = _wrap(lambda vt: vt.destroy)
	'''
	.. code-block:: c
		void destroy(); '''
	init = _wrap(lambda vt: vt.init)
	'''
	.. code-block:: c
		int init(); '''
	__method4 = _wrap(lambda vt: vt.__method4)
	'''
	.. code-block:: c
		void __method4(); '''
	pushText = _wrap(lambda vt: vt.pushText)
	'''
	.. code-block:: c
		int pushText(char *); '''
	pushText2 = _wrap(lambda vt: vt.pushText2)
	'''
	.. code-block:: c
		int pushText2(char *); '''
	__method7 = _wrap(lambda vt: vt.__method7)
	'''
	.. code-block:: c
		void __method7(); '''
	__method8 = _wrap(lambda vt: vt.__method8)
	'''
	.. code-block:: c
		void __method8(); '''
	readPhonemes = _wrap(lambda vt: vt.readPhonemes)
	'''
	.. code-block:: c
		int readPhonemes(char *, int, int *); '''
	__method10 = _wrap(lambda vt: vt.__method10)
	'''
	.. code-block:: c
		void __method10(); '''
	setFlushing = _wrap(lambda vt: vt.setFlushing)
	'''
	.. code-block:: c
		int setFlushing(_Bool); '''
	prepare = _wrap(lambda vt: vt.prepare)
	'''
	.. code-block:: c
		int prepare(); '''
	__method13 = _wrap(lambda vt: vt.__method13)
	'''
	.. code-block:: c
		void __method13(); '''
	__method14 = _wrap(lambda vt: vt.__method14)
	'''
	.. code-block:: c
		void __method14(); '''
	__method15 = _wrap(lambda vt: vt.__method15)
	'''
	.. code-block:: c
		void __method15(); '''
	__method16 = _wrap(lambda vt: vt.__method16)
	'''
	.. code-block:: c
		void __method16(); '''
	setCallbackAudio = _wrap(lambda vt: vt.setCallbackAudio)
	'''
	.. code-block:: c
		int setCallbackAudio(void(*)(int, short *, void *), void *); '''
	__method18 = _wrap(lambda vt: vt.__method18)
	'''
	.. code-block:: c
		void __method18(); '''
	setCallbackTextIndex = _wrap(lambda vt: vt.setCallbackTextIndex)
	'''
	.. code-block:: c
		void setCallbackTextIndex(void(*)(int, void *), void *); '''
	setCallbackEvent = _wrap(lambda vt: vt.setCallbackEvent)
	'''
	.. code-block:: c
		void setCallbackEvent(void(*)(int, void *), void *); '''
	setCallbackPhoneme = _wrap(lambda vt: vt.setCallbackPhoneme)
	'''
	.. code-block:: c
		void setCallbackPhoneme(void(*)(char *, int, void *), void *); '''
	setCallbackParam = _wrap(lambda vt: vt.setCallbackParam)
	'''
	.. code-block:: c
		void setCallbackParam(void(*)(enum SynthParamId, int, void *), void *); '''
	pushEvent = _wrap(lambda vt: vt.pushEvent)
	'''
	.. code-block:: c
		int pushEvent(int); '''
	pushEventAt = _wrap(lambda vt: vt.pushEventAt)
	'''
	.. code-block:: c
		int pushEventAt(int, int); '''
	setWantWordIndices = _wrap(lambda vt: vt.setWantWordIndices)
	'''
	.. code-block:: c
		void setWantWordIndices(_Bool); '''
	preDestruct = _wrap(lambda vt: vt.preDestruct)
	'''
	.. code-block:: c
		void preDestruct(); '''
	dictNew = _wrap(lambda vt: vt.dictNew)
	'''
	.. code-block:: c
		struct _SynthDict * dictNew(); '''
	__method28 = _wrap(lambda vt: vt.__method28)
	'''
	.. code-block:: c
		void __method28(); '''
	dictSetActive = _wrap(lambda vt: vt.dictSetActive)
	'''
	.. code-block:: c
		void dictSetActive(struct _SynthDict *); '''
	dictDelete = _wrap(lambda vt: vt.dictDelete)
	'''
	.. code-block:: c
		void dictDelete(struct _SynthDict *); '''
	dictLoad = _wrap(lambda vt: vt.dictLoad)
	'''
	.. code-block:: c
		void dictLoad(struct _SynthDict *, enum SynthDictVolume, char *); '''
	dictSave = _wrap(lambda vt: vt.dictSave)
	'''
	.. code-block:: c
		void dictSave(struct _SynthDict *, enum SynthDictVolume, char *); '''
	dictUpdate = _wrap(lambda vt: vt.dictUpdate)
	'''
	.. code-block:: c
		int dictUpdate(struct _SynthDict *, enum SynthDictVolume, char *, char *); '''
	dictGetFirstEntry = _wrap(lambda vt: vt.dictGetFirstEntry)
	'''
	.. code-block:: c
		void dictGetFirstEntry(struct _SynthDict *, enum SynthDictVolume, char * *, char * *); '''
	dictGetNextEntry = _wrap(lambda vt: vt.dictGetNextEntry)
	'''
	.. code-block:: c
		void dictGetNextEntry(struct _SynthDict *, enum SynthDictVolume, char * *, char * *); '''
	dictLookup = _wrap(lambda vt: vt.dictLookup)
	'''
	.. code-block:: c
		char * dictLookup(struct _SynthDict *, enum SynthDictVolume, char *); '''
	setCallbackWordIndex = _wrap(lambda vt: vt.setCallbackWordIndex)
	'''
	.. code-block:: c
		void setCallbackWordIndex(void(*)(int, void *), void *); '''
	setCallbackUserIndex = _wrap(lambda vt: vt.setCallbackUserIndex)
	'''
	.. code-block:: c
		void setCallbackUserIndex(void(*)(void *), void *); '''

class SynthDict(_base := ObjBase['types.SynthDict', Synth]):
	_wrap = _base._wrap_function
	def __init__(self, synth: Synth, obj: 'types.SynthDict'):
		super().__init__(obj)
		self.synth = synth
	@property
	def _vtable(self):
		return self.synth

	setActive = _wrap(lambda vt: vt.dictSetActive)
	'''
	.. code-block:: c
		void setActive(); '''
	delete = _wrap(lambda vt: vt.dictDelete)
	'''
	.. code-block:: c
		void delete(); '''
	load = _wrap(lambda vt: vt.dictLoad)
	'''
	.. code-block:: c
		void load(enum SynthDictVolume, char *); '''
	save = _wrap(lambda vt: vt.dictSave)
	'''
	.. code-block:: c
		void save(enum SynthDictVolume, char *); '''
	update = _wrap(lambda vt: vt.dictUpdate)
	'''
	.. code-block:: c
		int update(enum SynthDictVolume, char *, char *); '''
	getFirstEntry = _wrap(lambda vt: vt.dictGetFirstEntry)
	'''
	.. code-block:: c
		void getFirstEntry(enum SynthDictVolume, char * *, char * *); '''
	getNextEntry = _wrap(lambda vt: vt.dictGetNextEntry)
	'''
	.. code-block:: c
		void getNextEntry(enum SynthDictVolume, char * *, char * *); '''
	lookup = _wrap(lambda vt: vt.dictLookup)
	'''
	.. code-block:: c
		char * lookup(enum SynthDictVolume, char *); '''

class SynthDictVolume(_base := ObjBase['types.SynthDictVolume', SynthDict]):
	_wrap = _base._wrap_function
	def __init__(self, dict: SynthDict, obj: 'types.SynthDictVolume'):
		super().__init__(obj)
		self.dict = dict
	@property
	def _vtable(self):
		return self.dict

	load = _wrap(lambda vt: vt.load)
	'''
	.. code-block:: c
		void load(char *); '''
	save = _wrap(lambda vt: vt.save)
	'''
	.. code-block:: c
		void save(char *); '''
	update = _wrap(lambda vt: vt.update)
	'''
	.. code-block:: c
		int update(char *, char *); '''
	getFirstEntry = _wrap(lambda vt: vt.getFirstEntry)
	'''
	.. code-block:: c
		void getFirstEntry(char * *, char * *); '''
	getNextEntry = _wrap(lambda vt: vt.getNextEntry)
	'''
	.. code-block:: c
		void getNextEntry(char * *, char * *); '''
	lookup = _wrap(lambda vt: vt.lookup)
	'''
	.. code-block:: c
		char * lookup(char *); '''
