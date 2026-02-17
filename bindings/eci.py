import os
from ._eci_cffi import ffi

_dirname = os.path.dirname(__file__)
ENGINE_PATH = os.path.join(_dirname, r'..\synthDrivers\eloquence')

def load_ffi():
	with open(os.path.join(ENGINE_PATH, 'ECI.INI.orig'), 'r') as f:
		ini_orig = f.read()
	with open(os.path.join(ENGINE_PATH, 'ECI.INI'), 'w') as f:
		f.write(ini_orig.replace('ENGINE_PATH', ENGINE_PATH))
	return ffi.dlopen(os.path.join(ENGINE_PATH, 'ECI.DLL'))
lib = load_ffi()

from enum import IntFlag

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

def version():
	version = ffi.new('char[]', 20)
	lib.eciVersion(version)
	return ffi.string(version)

def availableLanguages():
	langs_num = ffi.new('int*')
	assert not (ret := lib.eciGetAvailableLanguages(ffi.NULL, langs_num)), f'eciGetAvailableLanguages failed: {ret:#x}'
	langs = ffi.new('enum ECILanguageDialect[]', langs_num[0])
	assert not (ret := lib.eciGetAvailableLanguages(langs, langs_num)) and langs_num[0] == len(langs), f'eciGetAvailableLanguages failed: {ret:#x}'
	return [ ffi.cast("enum ECILanguageDialect", x) for x in langs ]

class ECI:
	def __init__(self, langDialect) -> None:
		self.eci = lib.eciNewEx(langDialect)
		assert self.eci, f'failed creating engine'
		self.err_msg_buf = ffi.new('char[]', 100)

	def __del__(self):
		lib.eciDelete(self.eci)
		self.eci = None

	def check_err(self, b: bool):
		if b: return
		bits = ErrorCode(lib.eciProgStatus(self.eci))
		lib.eciErrorMessage(self.eci, self.err_msg_buf)
		msg = ffi.string(self.err_msg_buf)
		lib.eciClearErrors(self.eci)
		raise AssertionError(f'failed {bits} {msg!r}')

	def setOutputBuffer(self, buf):
		check_err(lib.eciSetOutputBuffer(self.eci, len(buf), buf))

	def addText(self, text: str):
		check_err(lib.eciAddText(self.eci, text.encode('mbcs')))
	def synthesize(self):
		check_err(lib.eciSynthesize(self.eci))
	def synchronize(self):
		check_err(lib.eciSynchronize(self.eci))
