from typing import TypeAlias, Self, Iterator, Union, Any, Literal, Callable, overload
from types import TracebackType
import _cffi_backend
# needed for conditional definitions in FFI, see below
import sys

class _CDataBase:
	def __enter__(self) -> Self: ...
	def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None, /) -> None: ...

	def __bool__(self) -> bool: ...
	def __hash__(self) -> int: ...

class IntPrimitive(_CDataBase):
	def __int__(self) -> int: ...
	# FIXME
	def __eq__(self, other: IntPrimitive, /) -> bool: ...
	def __ne__(self, other: IntPrimitive, /) -> bool: ...
	def __ge__(self, other: IntPrimitive, /) -> bool: ...
	def __gt__(self, other: IntPrimitive, /) -> bool: ...
	def __le__(self, other: IntPrimitive, /) -> bool: ...
	def __lt__(self, other: IntPrimitive, /) -> bool: ...

class PointerBase[T](_CDataBase):
	""" Used for all pointers, including those pointing to unsized types, which have restricted operations. """
	def __eq__(self, other: PointerBase[Any], /) -> bool: ...
	def __ne__(self, other: PointerBase[Any], /) -> bool: ...
	def __ge__(self, other: PointerBase[Any], /) -> bool: ...
	def __gt__(self, other: PointerBase[Any], /) -> bool: ...
	def __le__(self, other: PointerBase[Any], /) -> bool: ...
	def __lt__(self, other: PointerBase[Any], /) -> bool: ...

class Pointer[T](PointerBase[T]):
	""" Pointer to a sized type. """
	def __add__(self, other: int, /) -> Pointer[T]: ...
	def __radd__(self, other: int, /) -> Pointer[T]: ...
	@overload
	def __sub__(self, other: int, /) -> Pointer[T]: ...
	@overload
	def __sub__(self, other: Pointer[T], /) -> int: ...
	# FIXME: make cffi actually raise in the unsized case
	@overload
	def __getitem__(self, index: int) -> T: ...
	@overload
	def __getitem__(self, index: slice) -> Array[T]: ...
	@overload
	def __setitem__(self, index: int, value: T) -> None: ...
	@overload
	def __setitem__(self, index: slice, value: Array[T]) -> None: ...

class Array[T](Pointer[T]):
	def __len__(self) -> int: ...
	def __iter__(self) -> Iterator[T]: ...

VarArg: TypeAlias = Union[_CDataBase, bool, TODO, complex, bytes, str]
ErrorCallback: TypeAlias = Callable[[Exception, Any, TracebackType], Any]


class types:
    long: TypeAlias = int

    unsigned_char: TypeAlias = bytes
    ''' bytes of length 1 '''

    unsigned_short: TypeAlias = int

    char: TypeAlias = bytes
    ''' bytes of length 1 '''

    unsigned_int: TypeAlias = int

    short: TypeAlias = int

    Boolean: TypeAlias = int

    enum_ECICallbackReturn: TypeAlias = int

    class struct__ECI(_CDataBase):
        ''' struct _ECI '''

    ECIHand: TypeAlias = PointerBase[types.struct__ECI]

    enum_ECIMessage: TypeAlias = int

    ECIint32: TypeAlias = types.long

    ECIDictHand: TypeAlias = PointerBase[object]

    ECIFilterHand: TypeAlias = PointerBase[object]

    ECIInputText: TypeAlias = PointerBase[object]

    class ECICallback(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECICallbackReturn(*)(struct _ECI *, enum ECIMessage, long, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: types.enum_ECIMessage, arg2: types.long, arg3: PointerBase[object], /) -> types.enum_ECICallbackReturn: ...

    class anon_union_1(_CDataBase):
        ''' union $1 (size = 10) '''
        sz: Array[types.unsigned_char]
        ''' 
        .. code-block:: c
            unsigned char sz[5]; '''
        wsz: Array[types.unsigned_short]
        ''' 
        .. code-block:: c
            unsigned short wsz[5]; '''

    enum_ECILanguageDialect: TypeAlias = int

    class ECIMouthData(_CDataBase):
        ''' ECIMouthData (size = 22) '''
        phoneme: types.anon_union_1
        ''' 
        .. code-block:: c
            union $1 phoneme; '''
        eciLanguageDialect: types.enum_ECILanguageDialect
        ''' 
        .. code-block:: c
            enum ECILanguageDialect eciLanguageDialect; '''
        mouthHeight: types.unsigned_char
        ''' 
        .. code-block:: c
            unsigned char mouthHeight; '''
        mouthWidth: types.unsigned_char
        ''' 
        .. code-block:: c
            unsigned char mouthWidth; '''
        mouthUpturn: types.unsigned_char
        ''' 
        .. code-block:: c
            unsigned char mouthUpturn; '''
        jawOpen: types.unsigned_char
        ''' 
        .. code-block:: c
            unsigned char jawOpen; '''
        teethUpperVisible: types.unsigned_char
        ''' 
        .. code-block:: c
            unsigned char teethUpperVisible; '''
        teethLowerVisible: types.unsigned_char
        ''' 
        .. code-block:: c
            unsigned char teethLowerVisible; '''
        tonguePosn: types.unsigned_char
        ''' 
        .. code-block:: c
            unsigned char tonguePosn; '''
        lipTension: types.unsigned_char
        ''' 
        .. code-block:: c
            unsigned char lipTension; '''

    class struct_ECIVoiceAttrib(_CDataBase):
        ''' struct ECIVoiceAttrib (size = 8) '''
        eciSampleRate: int
        ''' 
        .. code-block:: c
            int eciSampleRate; '''
        languageID: types.enum_ECILanguageDialect
        ''' 
        .. code-block:: c
            enum ECILanguageDialect languageID; '''

    ECIVoiceAttrib: TypeAlias = types.struct_ECIVoiceAttrib

    ECIsystemChar: TypeAlias = types.char

    enum_ECIDialogBox: TypeAlias = int

    enum_ECIDictError: TypeAlias = int

    enum_ECIDictVolume: TypeAlias = int

    enum_ECIFilterError: TypeAlias = int

    enum_ECIParam: TypeAlias = int

    enum_ECIPartOfSpeech: TypeAlias = int

    enum_ECIVoiceError: TypeAlias = int

    enum_ECIVoiceParam: TypeAlias = int

    class anon_funcptr_1(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIFilterError(*)(struct _ECI *, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], /) -> types.enum_ECIFilterError: ...

    class anon_funcptr_2(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(struct _ECI *, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], /) -> int: ...

    class sym_eciClearErrors(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            void(*)(struct _ECI *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], /) -> None: ...

    class anon_funcptr_3(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(struct _ECI *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], /) -> int: ...

    class sym_eciCopyVoice(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(struct _ECI *, int, int) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: int, arg2: int, /) -> int: ...

    class sym_eciDelete(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            struct _ECI *(*)(struct _ECI *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], /) -> PointerBase[types.struct__ECI]: ...

    class anon_funcptr_4(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            void *(*)(struct _ECI *, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], /) -> PointerBase[object]: ...

    class anon_funcptr_5(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], arg2: types.enum_ECIDictVolume, arg3: Pointer[PointerBase[object]], arg4: Pointer[PointerBase[object]], /) -> types.enum_ECIDictError: ...

    class anon_funcptr_6(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *, enum ECIPartOfSpeech *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], arg2: types.enum_ECIDictVolume, arg3: Pointer[PointerBase[object]], arg4: Pointer[PointerBase[object]], arg5: Pointer[types.enum_ECIPartOfSpeech], /) -> types.enum_ECIDictError: ...

    class sym_eciDictLookup(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            char *(*)(struct _ECI *, void *, enum ECIDictVolume, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], arg2: types.enum_ECIDictVolume, arg3: PointerBase[object], /) -> Pointer[types.char]: ...

    class sym_eciDictLookupA(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *, void * *, enum ECIPartOfSpeech *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], arg2: types.enum_ECIDictVolume, arg3: PointerBase[object], arg4: Pointer[PointerBase[object]], arg5: Pointer[types.enum_ECIPartOfSpeech], /) -> types.enum_ECIDictError: ...

    class sym_eciErrorMessage(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            void(*)(struct _ECI *, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], /) -> None: ...

    class anon_funcptr_7(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(struct _ECI *, int, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: int, arg2: PointerBase[object], /) -> int: ...

    class sym_eciGetAvailableLanguages(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(enum ECILanguageDialect *, int *) '''
        def __call__(self, arg0: Pointer[types.enum_ECILanguageDialect], arg1: Pointer[int], /) -> int: ...

    class sym_eciGetDefaultParam(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(enum ECIParam) '''
        def __call__(self, arg0: types.enum_ECIParam, /) -> int: ...

    class anon_funcptr_8(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            void *(*)(struct _ECI *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], /) -> PointerBase[object]: ...

    class sym_eciGetFilteredText(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIFilterError(*)(struct _ECI *, void *, void *, void * *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], arg2: PointerBase[object], arg3: Pointer[PointerBase[object]], /) -> types.enum_ECIFilterError: ...

    class sym_eciGetParam(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(struct _ECI *, enum ECIParam) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: types.enum_ECIParam, /) -> int: ...

    class sym_eciGetVoiceParam(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(struct _ECI *, int, enum ECIVoiceParam) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: int, arg2: types.enum_ECIVoiceParam, /) -> int: ...

    class anon_funcptr_9(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(struct _ECI *, int) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: int, /) -> int: ...

    class anon_funcptr_10(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], arg2: types.enum_ECIDictVolume, arg3: PointerBase[object], /) -> types.enum_ECIDictError: ...

    class sym_eciNew(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            struct _ECI *(*)() '''
        def __call__(self, /) -> PointerBase[types.struct__ECI]: ...

    class sym_eciNewEx(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            struct _ECI *(*)(enum ECILanguageDialect) '''
        def __call__(self, arg0: types.enum_ECILanguageDialect, /) -> PointerBase[types.struct__ECI]: ...

    class sym_eciNewFilter(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            void *(*)(struct _ECI *, unsigned int, int) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: types.unsigned_int, arg2: int, /) -> PointerBase[object]: ...

    class sym_eciRegisterCallback(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            void(*)(struct _ECI *, enum ECICallbackReturn(*)(struct _ECI *, enum ECIMessage, long, void *), void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: types.ECICallback, arg2: PointerBase[object], /) -> None: ...

    class sym_eciRegisterVoice(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIVoiceError(*)(struct _ECI *, int, void *, struct ECIVoiceAttrib *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: int, arg2: PointerBase[object], arg3: Pointer[types.struct_ECIVoiceAttrib], /) -> types.enum_ECIVoiceError: ...

    class sym_eciSetDefaultParam(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(enum ECIParam, int) '''
        def __call__(self, arg0: types.enum_ECIParam, arg1: int, /) -> int: ...

    class sym_eciSetDict(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIDictError(*)(struct _ECI *, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], /) -> types.enum_ECIDictError: ...

    class sym_eciSetOutputBuffer(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(struct _ECI *, int, short *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: int, arg2: Pointer[types.short], /) -> int: ...

    class sym_eciSetParam(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(struct _ECI *, enum ECIParam, int) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: types.enum_ECIParam, arg2: int, /) -> int: ...

    class sym_eciSetVoiceParam(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(struct _ECI *, int, enum ECIVoiceParam, int) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: int, arg2: types.enum_ECIVoiceParam, arg3: int, /) -> int: ...

    class sym_eciSpeakText(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(void *, int) '''
        def __call__(self, arg0: PointerBase[object], arg1: int, /) -> int: ...

    class sym_eciSpeakTextEx(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            int(*)(void *, int, enum ECILanguageDialect) '''
        def __call__(self, arg0: PointerBase[object], arg1: int, arg2: types.enum_ECILanguageDialect, /) -> int: ...

    class sym_eciUnregisterVoice(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIVoiceError(*)(struct _ECI *, int, struct ECIVoiceAttrib *, void * *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: int, arg2: Pointer[types.struct_ECIVoiceAttrib], arg3: Pointer[PointerBase[object]], /) -> types.enum_ECIVoiceError: ...

    class sym_eciUpdateDict(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], arg2: types.enum_ECIDictVolume, arg3: PointerBase[object], arg4: PointerBase[object], /) -> types.enum_ECIDictError: ...

    class sym_eciUpdateDictA(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *, void *, enum ECIPartOfSpeech) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], arg2: types.enum_ECIDictVolume, arg3: PointerBase[object], arg4: PointerBase[object], arg5: types.enum_ECIPartOfSpeech, /) -> types.enum_ECIDictError: ...

    class sym_eciUpdateFilter(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            enum ECIFilterError(*)(struct _ECI *, void *, void *, void *) '''
        def __call__(self, arg0: PointerBase[types.struct__ECI], arg1: PointerBase[object], arg2: PointerBase[object], arg3: PointerBase[object], /) -> types.enum_ECIFilterError: ...

    class sym_eciVersion(_CDataBase):
        ''' function pointer type:
        .. code-block:: c
            void(*)(char *) '''
        def __call__(self, arg0: Pointer[types.char], /) -> None: ...

class Lib:
    DictAccessError: types.enum_ECIDictError = 6
    ''' enum ECIDictError (value 6) '''

    DictErrLookUpKey: types.enum_ECIDictError = 5
    ''' enum ECIDictError (value 5) '''

    DictFileNotFound: types.enum_ECIDictError = 1
    ''' enum ECIDictError (value 1) '''

    DictInternalError: types.enum_ECIDictError = 3
    ''' enum ECIDictError (value 3) '''

    DictInvalidVolume: types.enum_ECIDictError = 7
    ''' enum ECIDictError (value 7) '''

    DictNoEntry: types.enum_ECIDictError = 4
    ''' enum ECIDictError (value 4) '''

    DictNoError: types.enum_ECIDictError = 0
    ''' enum ECIDictError (value 0) '''

    DictOutOfMemory: types.enum_ECIDictError = 2
    ''' enum ECIDictError (value 2) '''

    FilterAccessError: types.enum_ECIFilterError = 4
    ''' enum ECIFilterError (value 4) '''

    FilterFileNotFound: types.enum_ECIFilterError = 1
    ''' enum ECIFilterError (value 1) '''

    FilterInternalError: types.enum_ECIFilterError = 3
    ''' enum ECIFilterError (value 3) '''

    FilterNoError: types.enum_ECIFilterError = 0
    ''' enum ECIFilterError (value 0) '''

    FilterOutOfMemory: types.enum_ECIFilterError = 2
    ''' enum ECIFilterError (value 2) '''

    NODEFINEDCODESET: types.enum_ECILanguageDialect = 0
    ''' enum ECILanguageDialect (value 0) '''

    VoiceInvalidFileFormatError: types.enum_ECIVoiceError = 3
    ''' enum ECIVoiceError (value 3) '''

    VoiceNoError: types.enum_ECIVoiceError = 0
    ''' enum ECIVoiceError (value 0) '''

    VoiceNotRegisteredError: types.enum_ECIVoiceError = 2
    ''' enum ECIVoiceError (value 2) '''

    VoiceSystemError: types.enum_ECIVoiceError = 1
    ''' enum ECIVoiceError (value 1) '''

    eciAbbvDict: types.enum_ECIDictVolume = 2
    ''' enum ECIDictVolume (value 2) '''

    eciAboutDB: types.enum_ECIDialogBox = 1
    ''' enum ECIDialogBox (value 1) '''

    @property
    def eciActivateFilter(self) -> types.anon_funcptr_1:
        ''' function:
        .. code-block:: c
            enum ECIFilterError eciActivateFilter(struct _ECI *, void *); '''
        ...

    @property
    def eciAddText(self) -> types.anon_funcptr_2:
        ''' function:
        .. code-block:: c
            int eciAddText(struct _ECI *, void *); '''
        ...

    eciAudioIndexReply: types.enum_ECIMessage = 6
    ''' enum ECIMessage (value 6) '''

    eciBrazilianPortuguese: types.enum_ECILanguageDialect = 458752
    ''' enum ECILanguageDialect (value 458752) '''

    eciBreathiness: types.enum_ECIVoiceParam = 5
    ''' enum ECIVoiceParam (value 5) '''

    eciBritishEnglish: types.enum_ECILanguageDialect = 65537
    ''' enum ECILanguageDialect (value 65537) '''

    eciCanadianFrench: types.enum_ECILanguageDialect = 196609
    ''' enum ECILanguageDialect (value 196609) '''

    eciCastilianSpanish: types.enum_ECILanguageDialect = 131072
    ''' enum ECILanguageDialect (value 131072) '''

    @property
    def eciClearErrors(self) -> types.sym_eciClearErrors:
        ''' function:
        .. code-block:: c
            void eciClearErrors(struct _ECI *); '''
        ...

    @property
    def eciClearInput(self) -> types.anon_funcptr_3:
        ''' function:
        .. code-block:: c
            int eciClearInput(struct _ECI *); '''
        ...

    @property
    def eciCopyVoice(self) -> types.sym_eciCopyVoice:
        ''' function:
        .. code-block:: c
            int eciCopyVoice(struct _ECI *, int, int); '''
        ...

    eciDataAbort: types.enum_ECICallbackReturn = 2
    ''' enum ECICallbackReturn (value 2) '''

    eciDataNotProcessed: types.enum_ECICallbackReturn = 0
    ''' enum ECICallbackReturn (value 0) '''

    eciDataProcessed: types.enum_ECICallbackReturn = 1
    ''' enum ECICallbackReturn (value 1) '''

    @property
    def eciDeactivateFilter(self) -> types.anon_funcptr_1:
        ''' function:
        .. code-block:: c
            enum ECIFilterError eciDeactivateFilter(struct _ECI *, void *); '''
        ...

    @property
    def eciDelete(self) -> types.sym_eciDelete:
        ''' function:
        .. code-block:: c
            struct _ECI *eciDelete(struct _ECI *); '''
        ...

    @property
    def eciDeleteDict(self) -> types.anon_funcptr_4:
        ''' function:
        .. code-block:: c
            void *eciDeleteDict(struct _ECI *, void *); '''
        ...

    @property
    def eciDeleteFilter(self) -> types.anon_funcptr_4:
        ''' function:
        .. code-block:: c
            void *eciDeleteFilter(struct _ECI *, void *); '''
        ...

    @property
    def eciDictFindFirst(self) -> types.anon_funcptr_5:
        ''' function:
        .. code-block:: c
            enum ECIDictError eciDictFindFirst(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *); '''
        ...

    @property
    def eciDictFindFirstA(self) -> types.anon_funcptr_6:
        ''' function:
        .. code-block:: c
            enum ECIDictError eciDictFindFirstA(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *, enum ECIPartOfSpeech *); '''
        ...

    @property
    def eciDictFindNext(self) -> types.anon_funcptr_5:
        ''' function:
        .. code-block:: c
            enum ECIDictError eciDictFindNext(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *); '''
        ...

    @property
    def eciDictFindNextA(self) -> types.anon_funcptr_6:
        ''' function:
        .. code-block:: c
            enum ECIDictError eciDictFindNextA(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *, enum ECIPartOfSpeech *); '''
        ...

    @property
    def eciDictLookup(self) -> types.sym_eciDictLookup:
        ''' function:
        .. code-block:: c
            char *eciDictLookup(struct _ECI *, void *, enum ECIDictVolume, void *); '''
        ...

    @property
    def eciDictLookupA(self) -> types.sym_eciDictLookupA:
        ''' function:
        .. code-block:: c
            enum ECIDictError eciDictLookupA(struct _ECI *, void *, enum ECIDictVolume, void *, void * *, enum ECIPartOfSpeech *); '''
        ...

    eciDictionary: types.enum_ECIParam = 3
    ''' enum ECIParam (value 3) '''

    @property
    def eciErrorMessage(self) -> types.sym_eciErrorMessage:
        ''' function:
        .. code-block:: c
            void eciErrorMessage(struct _ECI *, void *); '''
        ...

    eciFutsuuMeishi: types.enum_ECIPartOfSpeech = 1
    ''' enum ECIPartOfSpeech (value 1) '''

    eciGender: types.enum_ECIVoiceParam = 0
    ''' enum ECIVoiceParam (value 0) '''

    eciGeneralAmericanEnglish: types.enum_ECILanguageDialect = 65536
    ''' enum ECILanguageDialect (value 65536) '''

    eciGeneralDB: types.enum_ECIDialogBox = 0
    ''' enum ECIDialogBox (value 0) '''

    @property
    def eciGeneratePhonemes(self) -> types.anon_funcptr_7:
        ''' function:
        .. code-block:: c
            int eciGeneratePhonemes(struct _ECI *, int, void *); '''
        ...

    @property
    def eciGetAvailableLanguages(self) -> types.sym_eciGetAvailableLanguages:
        ''' function:
        .. code-block:: c
            int eciGetAvailableLanguages(enum ECILanguageDialect *, int *); '''
        ...

    @property
    def eciGetDefaultParam(self) -> types.sym_eciGetDefaultParam:
        ''' function:
        .. code-block:: c
            int eciGetDefaultParam(enum ECIParam); '''
        ...

    @property
    def eciGetDict(self) -> types.anon_funcptr_8:
        ''' function:
        .. code-block:: c
            void *eciGetDict(struct _ECI *); '''
        ...

    @property
    def eciGetFilteredText(self) -> types.sym_eciGetFilteredText:
        ''' function:
        .. code-block:: c
            enum ECIFilterError eciGetFilteredText(struct _ECI *, void *, void *, void * *); '''
        ...

    @property
    def eciGetIndex(self) -> types.anon_funcptr_3:
        ''' function:
        .. code-block:: c
            int eciGetIndex(struct _ECI *); '''
        ...

    @property
    def eciGetParam(self) -> types.sym_eciGetParam:
        ''' function:
        .. code-block:: c
            int eciGetParam(struct _ECI *, enum ECIParam); '''
        ...

    @property
    def eciGetVoiceName(self) -> types.anon_funcptr_7:
        ''' function:
        .. code-block:: c
            int eciGetVoiceName(struct _ECI *, int, void *); '''
        ...

    @property
    def eciGetVoiceParam(self) -> types.sym_eciGetVoiceParam:
        ''' function:
        .. code-block:: c
            int eciGetVoiceParam(struct _ECI *, int, enum ECIVoiceParam); '''
        ...

    eciHeadSize: types.enum_ECIVoiceParam = 1
    ''' enum ECIVoiceParam (value 1) '''

    eciHongKongCantonese: types.enum_ECILanguageDialect = 720897
    ''' enum ECILanguageDialect (value 720897) '''

    eciHongKongCantoneseBig5: types.enum_ECILanguageDialect = 720897
    ''' enum ECILanguageDialect (value 720897) '''

    eciHongKongCantoneseUCS: types.enum_ECILanguageDialect = 722945
    ''' enum ECILanguageDialect (value 722945) '''

    eciIndexReply: types.enum_ECIMessage = 2
    ''' enum ECIMessage (value 2) '''

    eciInputType: types.enum_ECIParam = 1
    ''' enum ECIParam (value 1) '''

    @property
    def eciInsertIndex(self) -> types.anon_funcptr_9:
        ''' function:
        .. code-block:: c
            int eciInsertIndex(struct _ECI *, int); '''
        ...

    @property
    def eciIsBeingReentered(self) -> types.anon_funcptr_3:
        ''' function:
        .. code-block:: c
            int eciIsBeingReentered(struct _ECI *); '''
        ...

    eciKoyuuMeishi: types.enum_ECIPartOfSpeech = 2
    ''' enum ECIPartOfSpeech (value 2) '''

    eciLanguageDialect: types.enum_ECIParam = 9
    ''' enum ECIParam (value 9) '''

    @property
    def eciLoadDict(self) -> types.anon_funcptr_10:
        ''' function:
        .. code-block:: c
            enum ECIDictError eciLoadDict(struct _ECI *, void *, enum ECIDictVolume, void *); '''
        ...

    eciMainDict: types.enum_ECIDictVolume = 0
    ''' enum ECIDictVolume (value 0) '''

    eciMainDictExt: types.enum_ECIDictVolume = 3
    ''' enum ECIDictVolume (value 3) '''

    eciMainDictionaryDB: types.enum_ECIDialogBox = 4
    ''' enum ECIDialogBox (value 4) '''

    eciMandarinChinese: types.enum_ECILanguageDialect = 393216
    ''' enum ECILanguageDialect (value 393216) '''

    eciMandarinChineseGB: types.enum_ECILanguageDialect = 393216
    ''' enum ECILanguageDialect (value 393216) '''

    eciMandarinChinesePinYin: types.enum_ECILanguageDialect = 393472
    ''' enum ECILanguageDialect (value 393472) '''

    eciMandarinChineseUCS: types.enum_ECILanguageDialect = 395264
    ''' enum ECILanguageDialect (value 395264) '''

    eciMexicanSpanish: types.enum_ECILanguageDialect = 131073
    ''' enum ECILanguageDialect (value 131073) '''

    eciMingCi: types.enum_ECIPartOfSpeech = 4
    ''' enum ECIPartOfSpeech (value 4) '''

    @property
    def eciNew(self) -> types.sym_eciNew:
        ''' function:
        .. code-block:: c
            struct _ECI *eciNew(); '''
        ...

    @property
    def eciNewDict(self) -> types.anon_funcptr_8:
        ''' function:
        .. code-block:: c
            void *eciNewDict(struct _ECI *); '''
        ...

    @property
    def eciNewEx(self) -> types.sym_eciNewEx:
        ''' function:
        .. code-block:: c
            struct _ECI *eciNewEx(enum ECILanguageDialect); '''
        ...

    @property
    def eciNewFilter(self) -> types.sym_eciNewFilter:
        ''' function:
        .. code-block:: c
            void *eciNewFilter(struct _ECI *, unsigned int, int); '''
        ...

    eciNumDeviceBlocks: types.enum_ECIParam = 13
    ''' enum ECIParam (value 13) '''

    eciNumDialogBoxes: types.enum_ECIDialogBox = 6
    ''' enum ECIDialogBox (value 6) '''

    eciNumParams: types.enum_ECIParam = 17
    ''' enum ECIParam (value 17) '''

    eciNumPrerollDeviceBlocks: types.enum_ECIParam = 15
    ''' enum ECIParam (value 15) '''

    eciNumVoiceParams: types.enum_ECIVoiceParam = 8
    ''' enum ECIVoiceParam (value 8) '''

    eciNumberMode: types.enum_ECIParam = 10
    ''' enum ECIParam (value 10) '''

    @property
    def eciPause(self) -> types.anon_funcptr_9:
        ''' function:
        .. code-block:: c
            int eciPause(struct _ECI *, int); '''
        ...

    eciPhonemeBuffer: types.enum_ECIMessage = 1
    ''' enum ECIMessage (value 1) '''

    eciPhonemeIndexReply: types.enum_ECIMessage = 3
    ''' enum ECIMessage (value 3) '''

    eciPitchBaseline: types.enum_ECIVoiceParam = 2
    ''' enum ECIVoiceParam (value 2) '''

    eciPitchFluctuation: types.enum_ECIVoiceParam = 3
    ''' enum ECIVoiceParam (value 3) '''

    @property
    def eciProgStatus(self) -> types.anon_funcptr_3:
        ''' function:
        .. code-block:: c
            int eciProgStatus(struct _ECI *); '''
        ...

    eciReadingDB: types.enum_ECIDialogBox = 3
    ''' enum ECIDialogBox (value 3) '''

    eciRealWorldUnits: types.enum_ECIParam = 8
    ''' enum ECIParam (value 8) '''

    @property
    def eciRegisterCallback(self) -> types.sym_eciRegisterCallback:
        ''' function:
        .. code-block:: c
            void eciRegisterCallback(struct _ECI *, enum ECICallbackReturn(*)(struct _ECI *, enum ECIMessage, long, void *), void *); '''
        ...

    @property
    def eciRegisterVoice(self) -> types.sym_eciRegisterVoice:
        ''' function:
        .. code-block:: c
            enum ECIVoiceError eciRegisterVoice(struct _ECI *, int, void *, struct ECIVoiceAttrib *); '''
        ...

    @property
    def eciReset(self) -> types.anon_funcptr_3:
        ''' function:
        .. code-block:: c
            int eciReset(struct _ECI *); '''
        ...

    eciRootDict: types.enum_ECIDictVolume = 1
    ''' enum ECIDictVolume (value 1) '''

    eciRootDictionaryDB: types.enum_ECIDialogBox = 5
    ''' enum ECIDialogBox (value 5) '''

    eciRoughness: types.enum_ECIVoiceParam = 4
    ''' enum ECIVoiceParam (value 4) '''

    eciSahenMeishi: types.enum_ECIPartOfSpeech = 3
    ''' enum ECIPartOfSpeech (value 3) '''

    eciSampleRate: types.enum_ECIParam = 5
    ''' enum ECIParam (value 5) '''

    @property
    def eciSaveDict(self) -> types.anon_funcptr_10:
        ''' function:
        .. code-block:: c
            enum ECIDictError eciSaveDict(struct _ECI *, void *, enum ECIDictVolume, void *); '''
        ...

    @property
    def eciSetDefaultParam(self) -> types.sym_eciSetDefaultParam:
        ''' function:
        .. code-block:: c
            int eciSetDefaultParam(enum ECIParam, int); '''
        ...

    @property
    def eciSetDict(self) -> types.sym_eciSetDict:
        ''' function:
        .. code-block:: c
            enum ECIDictError eciSetDict(struct _ECI *, void *); '''
        ...

    @property
    def eciSetOutputBuffer(self) -> types.sym_eciSetOutputBuffer:
        ''' function:
        .. code-block:: c
            int eciSetOutputBuffer(struct _ECI *, int, short *); '''
        ...

    @property
    def eciSetOutputDevice(self) -> types.anon_funcptr_9:
        ''' function:
        .. code-block:: c
            int eciSetOutputDevice(struct _ECI *, int); '''
        ...

    @property
    def eciSetOutputFilename(self) -> types.anon_funcptr_2:
        ''' function:
        .. code-block:: c
            int eciSetOutputFilename(struct _ECI *, void *); '''
        ...

    @property
    def eciSetParam(self) -> types.sym_eciSetParam:
        ''' function:
        .. code-block:: c
            int eciSetParam(struct _ECI *, enum ECIParam, int); '''
        ...

    @property
    def eciSetVoiceName(self) -> types.anon_funcptr_7:
        ''' function:
        .. code-block:: c
            int eciSetVoiceName(struct _ECI *, int, void *); '''
        ...

    @property
    def eciSetVoiceParam(self) -> types.sym_eciSetVoiceParam:
        ''' function:
        .. code-block:: c
            int eciSetVoiceParam(struct _ECI *, int, enum ECIVoiceParam, int); '''
        ...

    eciSizeDeviceBlocks: types.enum_ECIParam = 14
    ''' enum ECIParam (value 14) '''

    eciSizePrerollDeviceBlocks: types.enum_ECIParam = 16
    ''' enum ECIParam (value 16) '''

    @property
    def eciSpeakText(self) -> types.sym_eciSpeakText:
        ''' function:
        .. code-block:: c
            int eciSpeakText(void *, int); '''
        ...

    @property
    def eciSpeakTextEx(self) -> types.sym_eciSpeakTextEx:
        ''' function:
        .. code-block:: c
            int eciSpeakTextEx(void *, int, enum ECILanguageDialect); '''
        ...

    @property
    def eciSpeaking(self) -> types.anon_funcptr_3:
        ''' function:
        .. code-block:: c
            int eciSpeaking(struct _ECI *); '''
        ...

    eciSpeed: types.enum_ECIVoiceParam = 6
    ''' enum ECIVoiceParam (value 6) '''

    eciStandardCantonese: types.enum_ECILanguageDialect = 720896
    ''' enum ECILanguageDialect (value 720896) '''

    eciStandardCantoneseGB: types.enum_ECILanguageDialect = 720896
    ''' enum ECILanguageDialect (value 720896) '''

    eciStandardCantoneseUCS: types.enum_ECILanguageDialect = 722944
    ''' enum ECILanguageDialect (value 722944) '''

    eciStandardDanish: types.enum_ECILanguageDialect = 983040
    ''' enum ECILanguageDialect (value 983040) '''

    eciStandardDutch: types.enum_ECILanguageDialect = 786432
    ''' enum ECILanguageDialect (value 786432) '''

    eciStandardFinnish: types.enum_ECILanguageDialect = 589824
    ''' enum ECILanguageDialect (value 589824) '''

    eciStandardFrench: types.enum_ECILanguageDialect = 196608
    ''' enum ECILanguageDialect (value 196608) '''

    eciStandardGerman: types.enum_ECILanguageDialect = 262144
    ''' enum ECILanguageDialect (value 262144) '''

    eciStandardItalian: types.enum_ECILanguageDialect = 327680
    ''' enum ECILanguageDialect (value 327680) '''

    eciStandardJapanese: types.enum_ECILanguageDialect = 524288
    ''' enum ECILanguageDialect (value 524288) '''

    eciStandardJapaneseSJIS: types.enum_ECILanguageDialect = 524288
    ''' enum ECILanguageDialect (value 524288) '''

    eciStandardJapaneseUCS: types.enum_ECILanguageDialect = 526336
    ''' enum ECILanguageDialect (value 526336) '''

    eciStandardKorean: types.enum_ECILanguageDialect = 655360
    ''' enum ECILanguageDialect (value 655360) '''

    eciStandardKoreanUCS: types.enum_ECILanguageDialect = 657408
    ''' enum ECILanguageDialect (value 657408) '''

    eciStandardKoreanUHC: types.enum_ECILanguageDialect = 655360
    ''' enum ECILanguageDialect (value 655360) '''

    eciStandardNorwegian: types.enum_ECILanguageDialect = 851968
    ''' enum ECILanguageDialect (value 851968) '''

    eciStandardReserved: types.enum_ECILanguageDialect = 1048576
    ''' enum ECILanguageDialect (value 1048576) '''

    eciStandardSwedish: types.enum_ECILanguageDialect = 917504
    ''' enum ECILanguageDialect (value 917504) '''

    eciStandardThai: types.enum_ECILanguageDialect = 1114112
    ''' enum ECILanguageDialect (value 1114112) '''

    eciStandardThaiTIS: types.enum_ECILanguageDialect = 1114112
    ''' enum ECILanguageDialect (value 1114112) '''

    @property
    def eciStop(self) -> types.anon_funcptr_3:
        ''' function:
        .. code-block:: c
            int eciStop(struct _ECI *); '''
        ...

    eciStringIndexReply: types.enum_ECIMessage = 5
    ''' enum ECIMessage (value 5) '''

    @property
    def eciSynchronize(self) -> types.anon_funcptr_3:
        ''' function:
        .. code-block:: c
            int eciSynchronize(struct _ECI *); '''
        ...

    eciSynthMode: types.enum_ECIParam = 0
    ''' enum ECIParam (value 0) '''

    eciSynthesisBreak: types.enum_ECIMessage = 7
    ''' enum ECIMessage (value 7) '''

    @property
    def eciSynthesize(self) -> types.anon_funcptr_3:
        ''' function:
        .. code-block:: c
            int eciSynthesize(struct _ECI *); '''
        ...

    @property
    def eciSynthesizeFile(self) -> types.anon_funcptr_2:
        ''' function:
        .. code-block:: c
            int eciSynthesizeFile(struct _ECI *, void *); '''
        ...

    eciTaiwaneseMandarin: types.enum_ECILanguageDialect = 393217
    ''' enum ECILanguageDialect (value 393217) '''

    eciTaiwaneseMandarinBig5: types.enum_ECILanguageDialect = 393217
    ''' enum ECILanguageDialect (value 393217) '''

    eciTaiwaneseMandarinPinYin: types.enum_ECILanguageDialect = 393729
    ''' enum ECILanguageDialect (value 393729) '''

    eciTaiwaneseMandarinUCS: types.enum_ECILanguageDialect = 395265
    ''' enum ECILanguageDialect (value 395265) '''

    eciTaiwaneseMandarinZhuYin: types.enum_ECILanguageDialect = 393473
    ''' enum ECILanguageDialect (value 393473) '''

    @property
    def eciTestPhrase(self) -> types.anon_funcptr_3:
        ''' function:
        .. code-block:: c
            int eciTestPhrase(struct _ECI *); '''
        ...

    eciTextMode: types.enum_ECIParam = 2
    ''' enum ECIParam (value 2) '''

    eciUndefinedPOS: types.enum_ECIPartOfSpeech = 0
    ''' enum ECIPartOfSpeech (value 0) '''

    @property
    def eciUnregisterVoice(self) -> types.sym_eciUnregisterVoice:
        ''' function:
        .. code-block:: c
            enum ECIVoiceError eciUnregisterVoice(struct _ECI *, int, struct ECIVoiceAttrib *, void * *); '''
        ...

    @property
    def eciUpdateDict(self) -> types.sym_eciUpdateDict:
        ''' function:
        .. code-block:: c
            enum ECIDictError eciUpdateDict(struct _ECI *, void *, enum ECIDictVolume, void *, void *); '''
        ...

    @property
    def eciUpdateDictA(self) -> types.sym_eciUpdateDictA:
        ''' function:
        .. code-block:: c
            enum ECIDictError eciUpdateDictA(struct _ECI *, void *, enum ECIDictVolume, void *, void *, enum ECIPartOfSpeech); '''
        ...

    @property
    def eciUpdateFilter(self) -> types.sym_eciUpdateFilter:
        ''' function:
        .. code-block:: c
            enum ECIFilterError eciUpdateFilter(struct _ECI *, void *, void *, void *); '''
        ...

    @property
    def eciVersion(self) -> types.sym_eciVersion:
        ''' function:
        .. code-block:: c
            void eciVersion(char *); '''
        ...

    eciVoicesDB: types.enum_ECIDialogBox = 2
    ''' enum ECIDialogBox (value 2) '''

    eciVolume: types.enum_ECIVoiceParam = 7
    ''' enum ECIVoiceParam (value 7) '''

    eciWantPhonemeIndices: types.enum_ECIParam = 7
    ''' enum ECIParam (value 7) '''

    eciWantWordIndex: types.enum_ECIParam = 12
    ''' enum ECIParam (value 12) '''

    eciWaveformBuffer: types.enum_ECIMessage = 0
    ''' enum ECIMessage (value 0) '''

    eciWordIndexReply: types.enum_ECIMessage = 4
    ''' enum ECIMessage (value 4) '''

class FFI(_cffi_backend.FFI):
    CData: TypeAlias = _CDataBase

    def dlclose(self, lib: Lib, /) -> None: ...
    if sys.platform == "win32":
        def dlopen(self, libpath: str | FFI.CData, flags: int = ..., /) -> Lib: ...
    else:
        def dlopen(self, libpath: str | FFI.CData | None = ..., flags: int = ..., /) -> Lib: ...

    def gc[T: CData](self, cdata: T, destructor: Callable[[T], Any], size: int = ...) -> T: ...

    @overload
    def new(self, ctype: Literal['int *'], init: int = ..., /) -> Pointer[int]: ...
    @overload
    def new(self, ctype: Literal['int[]'], init: Union[int, tuple[int, ...]], /) -> Array[int]: ...
    @overload
    def new(self, ctype: Literal['enum ECICallbackReturn *'], init: types.enum_ECICallbackReturn = ..., /) -> Pointer[types.enum_ECICallbackReturn]: ...
    @overload
    def new(self, ctype: Literal['enum ECICallbackReturn[]'], init: Union[int, tuple[types.enum_ECICallbackReturn, ...]], /) -> Array[types.enum_ECICallbackReturn]: ...
    @overload
    def new(self, ctype: Literal['struct _ECI * *'], init: PointerBase[types.struct__ECI] = ..., /) -> Pointer[PointerBase[types.struct__ECI]]: ...
    @overload
    def new(self, ctype: Literal['struct _ECI *[]'], init: Union[int, tuple[PointerBase[types.struct__ECI], ...]], /) -> Array[PointerBase[types.struct__ECI]]: ...
    @overload
    def new(self, ctype: Literal['enum ECIMessage *'], init: types.enum_ECIMessage = ..., /) -> Pointer[types.enum_ECIMessage]: ...
    @overload
    def new(self, ctype: Literal['enum ECIMessage[]'], init: Union[int, tuple[types.enum_ECIMessage, ...]], /) -> Array[types.enum_ECIMessage]: ...
    @overload
    def new(self, ctype: Literal['long *'], init: types.long = ..., /) -> Pointer[types.long]: ...
    @overload
    def new(self, ctype: Literal['long[]'], init: Union[int, tuple[types.long, ...]], /) -> Array[types.long]: ...
    @overload
    def new(self, ctype: Literal['void * *'], init: PointerBase[object] = ..., /) -> Pointer[PointerBase[object]]: ...
    @overload
    def new(self, ctype: Literal['void *[]'], init: Union[int, tuple[PointerBase[object], ...]], /) -> Array[PointerBase[object]]: ...
    @overload
    def new(self, ctype: Literal['enum ECICallbackReturn(* *)(struct _ECI *, enum ECIMessage, long, void *)'], init: types.ECICallback = ..., /) -> Pointer[types.ECICallback]: ...
    @overload
    def new(self, ctype: Literal['enum ECICallbackReturn(*[])(struct _ECI *, enum ECIMessage, long, void *)'], init: Union[int, tuple[types.ECICallback, ...]], /) -> Array[types.ECICallback]: ...
    @overload
    def new(self, ctype: Literal['unsigned char *'], init: types.unsigned_char = ..., /) -> Pointer[types.unsigned_char]: ...
    @overload
    def new(self, ctype: Literal['unsigned char[]'], init: Union[int, Union[bytes, tuple[types.unsigned_char, ...]]], /) -> Array[types.unsigned_char]: ...
    @overload
    def new(self, ctype: Literal['unsigned char[5]'], init: tuple[types.unsigned_char, types.unsigned_char, types.unsigned_char, types.unsigned_char, types.unsigned_char] = ..., /) -> Array[types.unsigned_char]: ...
    @overload
    def new(self, ctype: Literal['unsigned char(*)[5]'], init: Array[types.unsigned_char] = ..., /) -> Pointer[Array[types.unsigned_char]]: ...
    @overload
    def new(self, ctype: Literal['unsigned char[][5]'], init: Union[int, tuple[Array[types.unsigned_char], ...]], /) -> Array[Array[types.unsigned_char]]: ...
    @overload
    def new(self, ctype: Literal['unsigned short *'], init: types.unsigned_short = ..., /) -> Pointer[types.unsigned_short]: ...
    @overload
    def new(self, ctype: Literal['unsigned short[]'], init: Union[int, tuple[types.unsigned_short, ...]], /) -> Array[types.unsigned_short]: ...
    @overload
    def new(self, ctype: Literal['unsigned short[5]'], init: tuple[types.unsigned_short, types.unsigned_short, types.unsigned_short, types.unsigned_short, types.unsigned_short] = ..., /) -> Array[types.unsigned_short]: ...
    @overload
    def new(self, ctype: Literal['unsigned short(*)[5]'], init: Array[types.unsigned_short] = ..., /) -> Pointer[Array[types.unsigned_short]]: ...
    @overload
    def new(self, ctype: Literal['unsigned short[][5]'], init: Union[int, tuple[Array[types.unsigned_short], ...]], /) -> Array[Array[types.unsigned_short]]: ...
    @overload
    def new(self, ctype: Literal['union $1 *'], init: types.anon_union_1 = ..., /) -> Pointer[types.anon_union_1]: ...
    @overload
    def new(self, ctype: Literal['union $1[]'], init: Union[int, tuple[types.anon_union_1, ...]], /) -> Array[types.anon_union_1]: ...
    @overload
    def new(self, ctype: Literal['enum ECILanguageDialect *'], init: types.enum_ECILanguageDialect = ..., /) -> Pointer[types.enum_ECILanguageDialect]: ...
    @overload
    def new(self, ctype: Literal['enum ECILanguageDialect[]'], init: Union[int, tuple[types.enum_ECILanguageDialect, ...]], /) -> Array[types.enum_ECILanguageDialect]: ...
    @overload
    def new(self, ctype: Literal['ECIMouthData *'], init: types.ECIMouthData = ..., /) -> Pointer[types.ECIMouthData]: ...
    @overload
    def new(self, ctype: Literal['ECIMouthData[]'], init: Union[int, tuple[types.ECIMouthData, ...]], /) -> Array[types.ECIMouthData]: ...
    @overload
    def new(self, ctype: Literal['struct ECIVoiceAttrib *'], init: types.struct_ECIVoiceAttrib = ..., /) -> Pointer[types.struct_ECIVoiceAttrib]: ...
    @overload
    def new(self, ctype: Literal['struct ECIVoiceAttrib[]'], init: Union[int, tuple[types.struct_ECIVoiceAttrib, ...]], /) -> Array[types.struct_ECIVoiceAttrib]: ...
    @overload
    def new(self, ctype: Literal['char *'], init: types.char = ..., /) -> Pointer[types.char]: ...
    @overload
    def new(self, ctype: Literal['char[]'], init: Union[int, Union[bytes, tuple[types.char, ...]]], /) -> Array[types.char]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDialogBox *'], init: types.enum_ECIDialogBox = ..., /) -> Pointer[types.enum_ECIDialogBox]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDialogBox[]'], init: Union[int, tuple[types.enum_ECIDialogBox, ...]], /) -> Array[types.enum_ECIDialogBox]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError *'], init: types.enum_ECIDictError = ..., /) -> Pointer[types.enum_ECIDictError]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError[]'], init: Union[int, tuple[types.enum_ECIDictError, ...]], /) -> Array[types.enum_ECIDictError]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictVolume *'], init: types.enum_ECIDictVolume = ..., /) -> Pointer[types.enum_ECIDictVolume]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictVolume[]'], init: Union[int, tuple[types.enum_ECIDictVolume, ...]], /) -> Array[types.enum_ECIDictVolume]: ...
    @overload
    def new(self, ctype: Literal['enum ECIFilterError *'], init: types.enum_ECIFilterError = ..., /) -> Pointer[types.enum_ECIFilterError]: ...
    @overload
    def new(self, ctype: Literal['enum ECIFilterError[]'], init: Union[int, tuple[types.enum_ECIFilterError, ...]], /) -> Array[types.enum_ECIFilterError]: ...
    @overload
    def new(self, ctype: Literal['enum ECIParam *'], init: types.enum_ECIParam = ..., /) -> Pointer[types.enum_ECIParam]: ...
    @overload
    def new(self, ctype: Literal['enum ECIParam[]'], init: Union[int, tuple[types.enum_ECIParam, ...]], /) -> Array[types.enum_ECIParam]: ...
    @overload
    def new(self, ctype: Literal['enum ECIPartOfSpeech *'], init: types.enum_ECIPartOfSpeech = ..., /) -> Pointer[types.enum_ECIPartOfSpeech]: ...
    @overload
    def new(self, ctype: Literal['enum ECIPartOfSpeech[]'], init: Union[int, tuple[types.enum_ECIPartOfSpeech, ...]], /) -> Array[types.enum_ECIPartOfSpeech]: ...
    @overload
    def new(self, ctype: Literal['enum ECIVoiceError *'], init: types.enum_ECIVoiceError = ..., /) -> Pointer[types.enum_ECIVoiceError]: ...
    @overload
    def new(self, ctype: Literal['enum ECIVoiceError[]'], init: Union[int, tuple[types.enum_ECIVoiceError, ...]], /) -> Array[types.enum_ECIVoiceError]: ...
    @overload
    def new(self, ctype: Literal['enum ECIVoiceParam *'], init: types.enum_ECIVoiceParam = ..., /) -> Pointer[types.enum_ECIVoiceParam]: ...
    @overload
    def new(self, ctype: Literal['enum ECIVoiceParam[]'], init: Union[int, tuple[types.enum_ECIVoiceParam, ...]], /) -> Array[types.enum_ECIVoiceParam]: ...
    @overload
    def new(self, ctype: Literal['enum ECIFilterError(* *)(struct _ECI *, void *)'], init: types.anon_funcptr_1 = ..., /) -> Pointer[types.anon_funcptr_1]: ...
    @overload
    def new(self, ctype: Literal['enum ECIFilterError(*[])(struct _ECI *, void *)'], init: Union[int, tuple[types.anon_funcptr_1, ...]], /) -> Array[types.anon_funcptr_1]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(struct _ECI *, void *)'], init: types.anon_funcptr_2 = ..., /) -> Pointer[types.anon_funcptr_2]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(struct _ECI *, void *)'], init: Union[int, tuple[types.anon_funcptr_2, ...]], /) -> Array[types.anon_funcptr_2]: ...
    @overload
    def new(self, ctype: Literal['void(* *)(struct _ECI *)'], init: types.sym_eciClearErrors = ..., /) -> Pointer[types.sym_eciClearErrors]: ...
    @overload
    def new(self, ctype: Literal['void(*[])(struct _ECI *)'], init: Union[int, tuple[types.sym_eciClearErrors, ...]], /) -> Array[types.sym_eciClearErrors]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(struct _ECI *)'], init: types.anon_funcptr_3 = ..., /) -> Pointer[types.anon_funcptr_3]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(struct _ECI *)'], init: Union[int, tuple[types.anon_funcptr_3, ...]], /) -> Array[types.anon_funcptr_3]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(struct _ECI *, int, int)'], init: types.sym_eciCopyVoice = ..., /) -> Pointer[types.sym_eciCopyVoice]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(struct _ECI *, int, int)'], init: Union[int, tuple[types.sym_eciCopyVoice, ...]], /) -> Array[types.sym_eciCopyVoice]: ...
    @overload
    def new(self, ctype: Literal['struct _ECI *(* *)(struct _ECI *)'], init: types.sym_eciDelete = ..., /) -> Pointer[types.sym_eciDelete]: ...
    @overload
    def new(self, ctype: Literal['struct _ECI *(*[])(struct _ECI *)'], init: Union[int, tuple[types.sym_eciDelete, ...]], /) -> Array[types.sym_eciDelete]: ...
    @overload
    def new(self, ctype: Literal['void *(* *)(struct _ECI *, void *)'], init: types.anon_funcptr_4 = ..., /) -> Pointer[types.anon_funcptr_4]: ...
    @overload
    def new(self, ctype: Literal['void *(*[])(struct _ECI *, void *)'], init: Union[int, tuple[types.anon_funcptr_4, ...]], /) -> Array[types.anon_funcptr_4]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *)'], init: types.anon_funcptr_5 = ..., /) -> Pointer[types.anon_funcptr_5]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(*[])(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *)'], init: Union[int, tuple[types.anon_funcptr_5, ...]], /) -> Array[types.anon_funcptr_5]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *, enum ECIPartOfSpeech *)'], init: types.anon_funcptr_6 = ..., /) -> Pointer[types.anon_funcptr_6]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(*[])(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *, enum ECIPartOfSpeech *)'], init: Union[int, tuple[types.anon_funcptr_6, ...]], /) -> Array[types.anon_funcptr_6]: ...
    @overload
    def new(self, ctype: Literal['char *(* *)(struct _ECI *, void *, enum ECIDictVolume, void *)'], init: types.sym_eciDictLookup = ..., /) -> Pointer[types.sym_eciDictLookup]: ...
    @overload
    def new(self, ctype: Literal['char *(*[])(struct _ECI *, void *, enum ECIDictVolume, void *)'], init: Union[int, tuple[types.sym_eciDictLookup, ...]], /) -> Array[types.sym_eciDictLookup]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void *, void * *, enum ECIPartOfSpeech *)'], init: types.sym_eciDictLookupA = ..., /) -> Pointer[types.sym_eciDictLookupA]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(*[])(struct _ECI *, void *, enum ECIDictVolume, void *, void * *, enum ECIPartOfSpeech *)'], init: Union[int, tuple[types.sym_eciDictLookupA, ...]], /) -> Array[types.sym_eciDictLookupA]: ...
    @overload
    def new(self, ctype: Literal['void(* *)(struct _ECI *, void *)'], init: types.sym_eciErrorMessage = ..., /) -> Pointer[types.sym_eciErrorMessage]: ...
    @overload
    def new(self, ctype: Literal['void(*[])(struct _ECI *, void *)'], init: Union[int, tuple[types.sym_eciErrorMessage, ...]], /) -> Array[types.sym_eciErrorMessage]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(struct _ECI *, int, void *)'], init: types.anon_funcptr_7 = ..., /) -> Pointer[types.anon_funcptr_7]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(struct _ECI *, int, void *)'], init: Union[int, tuple[types.anon_funcptr_7, ...]], /) -> Array[types.anon_funcptr_7]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(enum ECILanguageDialect *, int *)'], init: types.sym_eciGetAvailableLanguages = ..., /) -> Pointer[types.sym_eciGetAvailableLanguages]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(enum ECILanguageDialect *, int *)'], init: Union[int, tuple[types.sym_eciGetAvailableLanguages, ...]], /) -> Array[types.sym_eciGetAvailableLanguages]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(enum ECIParam)'], init: types.sym_eciGetDefaultParam = ..., /) -> Pointer[types.sym_eciGetDefaultParam]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(enum ECIParam)'], init: Union[int, tuple[types.sym_eciGetDefaultParam, ...]], /) -> Array[types.sym_eciGetDefaultParam]: ...
    @overload
    def new(self, ctype: Literal['void *(* *)(struct _ECI *)'], init: types.anon_funcptr_8 = ..., /) -> Pointer[types.anon_funcptr_8]: ...
    @overload
    def new(self, ctype: Literal['void *(*[])(struct _ECI *)'], init: Union[int, tuple[types.anon_funcptr_8, ...]], /) -> Array[types.anon_funcptr_8]: ...
    @overload
    def new(self, ctype: Literal['enum ECIFilterError(* *)(struct _ECI *, void *, void *, void * *)'], init: types.sym_eciGetFilteredText = ..., /) -> Pointer[types.sym_eciGetFilteredText]: ...
    @overload
    def new(self, ctype: Literal['enum ECIFilterError(*[])(struct _ECI *, void *, void *, void * *)'], init: Union[int, tuple[types.sym_eciGetFilteredText, ...]], /) -> Array[types.sym_eciGetFilteredText]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(struct _ECI *, enum ECIParam)'], init: types.sym_eciGetParam = ..., /) -> Pointer[types.sym_eciGetParam]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(struct _ECI *, enum ECIParam)'], init: Union[int, tuple[types.sym_eciGetParam, ...]], /) -> Array[types.sym_eciGetParam]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(struct _ECI *, int, enum ECIVoiceParam)'], init: types.sym_eciGetVoiceParam = ..., /) -> Pointer[types.sym_eciGetVoiceParam]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(struct _ECI *, int, enum ECIVoiceParam)'], init: Union[int, tuple[types.sym_eciGetVoiceParam, ...]], /) -> Array[types.sym_eciGetVoiceParam]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(struct _ECI *, int)'], init: types.anon_funcptr_9 = ..., /) -> Pointer[types.anon_funcptr_9]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(struct _ECI *, int)'], init: Union[int, tuple[types.anon_funcptr_9, ...]], /) -> Array[types.anon_funcptr_9]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void *)'], init: types.anon_funcptr_10 = ..., /) -> Pointer[types.anon_funcptr_10]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(*[])(struct _ECI *, void *, enum ECIDictVolume, void *)'], init: Union[int, tuple[types.anon_funcptr_10, ...]], /) -> Array[types.anon_funcptr_10]: ...
    @overload
    def new(self, ctype: Literal['struct _ECI *(* *)()'], init: types.sym_eciNew = ..., /) -> Pointer[types.sym_eciNew]: ...
    @overload
    def new(self, ctype: Literal['struct _ECI *(*[])()'], init: Union[int, tuple[types.sym_eciNew, ...]], /) -> Array[types.sym_eciNew]: ...
    @overload
    def new(self, ctype: Literal['struct _ECI *(* *)(enum ECILanguageDialect)'], init: types.sym_eciNewEx = ..., /) -> Pointer[types.sym_eciNewEx]: ...
    @overload
    def new(self, ctype: Literal['struct _ECI *(*[])(enum ECILanguageDialect)'], init: Union[int, tuple[types.sym_eciNewEx, ...]], /) -> Array[types.sym_eciNewEx]: ...
    @overload
    def new(self, ctype: Literal['unsigned int *'], init: types.unsigned_int = ..., /) -> Pointer[types.unsigned_int]: ...
    @overload
    def new(self, ctype: Literal['unsigned int[]'], init: Union[int, tuple[types.unsigned_int, ...]], /) -> Array[types.unsigned_int]: ...
    @overload
    def new(self, ctype: Literal['void *(* *)(struct _ECI *, unsigned int, int)'], init: types.sym_eciNewFilter = ..., /) -> Pointer[types.sym_eciNewFilter]: ...
    @overload
    def new(self, ctype: Literal['void *(*[])(struct _ECI *, unsigned int, int)'], init: Union[int, tuple[types.sym_eciNewFilter, ...]], /) -> Array[types.sym_eciNewFilter]: ...
    @overload
    def new(self, ctype: Literal['void(* *)(struct _ECI *, enum ECICallbackReturn(*)(struct _ECI *, enum ECIMessage, long, void *), void *)'], init: types.sym_eciRegisterCallback = ..., /) -> Pointer[types.sym_eciRegisterCallback]: ...
    @overload
    def new(self, ctype: Literal['void(*[])(struct _ECI *, enum ECICallbackReturn(*)(struct _ECI *, enum ECIMessage, long, void *), void *)'], init: Union[int, tuple[types.sym_eciRegisterCallback, ...]], /) -> Array[types.sym_eciRegisterCallback]: ...
    @overload
    def new(self, ctype: Literal['enum ECIVoiceError(* *)(struct _ECI *, int, void *, struct ECIVoiceAttrib *)'], init: types.sym_eciRegisterVoice = ..., /) -> Pointer[types.sym_eciRegisterVoice]: ...
    @overload
    def new(self, ctype: Literal['enum ECIVoiceError(*[])(struct _ECI *, int, void *, struct ECIVoiceAttrib *)'], init: Union[int, tuple[types.sym_eciRegisterVoice, ...]], /) -> Array[types.sym_eciRegisterVoice]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(enum ECIParam, int)'], init: types.sym_eciSetDefaultParam = ..., /) -> Pointer[types.sym_eciSetDefaultParam]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(enum ECIParam, int)'], init: Union[int, tuple[types.sym_eciSetDefaultParam, ...]], /) -> Array[types.sym_eciSetDefaultParam]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *)'], init: types.sym_eciSetDict = ..., /) -> Pointer[types.sym_eciSetDict]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(*[])(struct _ECI *, void *)'], init: Union[int, tuple[types.sym_eciSetDict, ...]], /) -> Array[types.sym_eciSetDict]: ...
    @overload
    def new(self, ctype: Literal['short[]'], init: Union[int, tuple[types.short, ...]], /) -> Array[types.short]: ...
    @overload
    def new(self, ctype: Literal['short *'], init: types.short = ..., /) -> Pointer[types.short]: ...
    @overload
    def new(self, ctype: Literal['short * *'], init: Pointer[types.short] = ..., /) -> Pointer[Pointer[types.short]]: ...
    @overload
    def new(self, ctype: Literal['short *[]'], init: Union[int, tuple[Pointer[types.short], ...]], /) -> Array[Pointer[types.short]]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(struct _ECI *, int, short *)'], init: types.sym_eciSetOutputBuffer = ..., /) -> Pointer[types.sym_eciSetOutputBuffer]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(struct _ECI *, int, short *)'], init: Union[int, tuple[types.sym_eciSetOutputBuffer, ...]], /) -> Array[types.sym_eciSetOutputBuffer]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(struct _ECI *, enum ECIParam, int)'], init: types.sym_eciSetParam = ..., /) -> Pointer[types.sym_eciSetParam]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(struct _ECI *, enum ECIParam, int)'], init: Union[int, tuple[types.sym_eciSetParam, ...]], /) -> Array[types.sym_eciSetParam]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(struct _ECI *, int, enum ECIVoiceParam, int)'], init: types.sym_eciSetVoiceParam = ..., /) -> Pointer[types.sym_eciSetVoiceParam]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(struct _ECI *, int, enum ECIVoiceParam, int)'], init: Union[int, tuple[types.sym_eciSetVoiceParam, ...]], /) -> Array[types.sym_eciSetVoiceParam]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(void *, int)'], init: types.sym_eciSpeakText = ..., /) -> Pointer[types.sym_eciSpeakText]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(void *, int)'], init: Union[int, tuple[types.sym_eciSpeakText, ...]], /) -> Array[types.sym_eciSpeakText]: ...
    @overload
    def new(self, ctype: Literal['int(* *)(void *, int, enum ECILanguageDialect)'], init: types.sym_eciSpeakTextEx = ..., /) -> Pointer[types.sym_eciSpeakTextEx]: ...
    @overload
    def new(self, ctype: Literal['int(*[])(void *, int, enum ECILanguageDialect)'], init: Union[int, tuple[types.sym_eciSpeakTextEx, ...]], /) -> Array[types.sym_eciSpeakTextEx]: ...
    @overload
    def new(self, ctype: Literal['enum ECIVoiceError(* *)(struct _ECI *, int, struct ECIVoiceAttrib *, void * *)'], init: types.sym_eciUnregisterVoice = ..., /) -> Pointer[types.sym_eciUnregisterVoice]: ...
    @overload
    def new(self, ctype: Literal['enum ECIVoiceError(*[])(struct _ECI *, int, struct ECIVoiceAttrib *, void * *)'], init: Union[int, tuple[types.sym_eciUnregisterVoice, ...]], /) -> Array[types.sym_eciUnregisterVoice]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void *, void *)'], init: types.sym_eciUpdateDict = ..., /) -> Pointer[types.sym_eciUpdateDict]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(*[])(struct _ECI *, void *, enum ECIDictVolume, void *, void *)'], init: Union[int, tuple[types.sym_eciUpdateDict, ...]], /) -> Array[types.sym_eciUpdateDict]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void *, void *, enum ECIPartOfSpeech)'], init: types.sym_eciUpdateDictA = ..., /) -> Pointer[types.sym_eciUpdateDictA]: ...
    @overload
    def new(self, ctype: Literal['enum ECIDictError(*[])(struct _ECI *, void *, enum ECIDictVolume, void *, void *, enum ECIPartOfSpeech)'], init: Union[int, tuple[types.sym_eciUpdateDictA, ...]], /) -> Array[types.sym_eciUpdateDictA]: ...
    @overload
    def new(self, ctype: Literal['enum ECIFilterError(* *)(struct _ECI *, void *, void *, void *)'], init: types.sym_eciUpdateFilter = ..., /) -> Pointer[types.sym_eciUpdateFilter]: ...
    @overload
    def new(self, ctype: Literal['enum ECIFilterError(*[])(struct _ECI *, void *, void *, void *)'], init: Union[int, tuple[types.sym_eciUpdateFilter, ...]], /) -> Array[types.sym_eciUpdateFilter]: ...
    @overload
    def new(self, ctype: Literal['void(* *)(char *)'], init: types.sym_eciVersion = ..., /) -> Pointer[types.sym_eciVersion]: ...
    @overload
    def new(self, ctype: Literal['void(*[])(char *)'], init: Union[int, tuple[types.sym_eciVersion, ...]], /) -> Array[types.sym_eciVersion]: ...

    @overload
    def callback(self, ctype: Literal['enum ECICallbackReturn(*)(struct _ECI *, enum ECIMessage, long, void *)', 'ECICallback'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], types.enum_ECIMessage, types.long, PointerBase[object]], types.enum_ECICallbackReturn]], types.ECICallback]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIFilterError(*)(struct _ECI *, void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object]], types.enum_ECIFilterError]], types.anon_funcptr_1]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(struct _ECI *, void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object]], int]], types.anon_funcptr_2]: ...
    @overload
    def callback(self, ctype: Literal['void(*)(struct _ECI *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI]], None]], types.sym_eciClearErrors]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(struct _ECI *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI]], int]], types.anon_funcptr_3]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(struct _ECI *, int, int)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], int, int], int]], types.sym_eciCopyVoice]: ...
    @overload
    def callback(self, ctype: Literal['struct _ECI *(*)(struct _ECI *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI]], PointerBase[types.struct__ECI]]], types.sym_eciDelete]: ...
    @overload
    def callback(self, ctype: Literal['void *(*)(struct _ECI *, void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object]], PointerBase[object]]], types.anon_funcptr_4]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object], types.enum_ECIDictVolume, Pointer[PointerBase[object]], Pointer[PointerBase[object]]], types.enum_ECIDictError]], types.anon_funcptr_5]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *, enum ECIPartOfSpeech *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object], types.enum_ECIDictVolume, Pointer[PointerBase[object]], Pointer[PointerBase[object]], Pointer[types.enum_ECIPartOfSpeech]], types.enum_ECIDictError]], types.anon_funcptr_6]: ...
    @overload
    def callback(self, ctype: Literal['char *(*)(struct _ECI *, void *, enum ECIDictVolume, void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object], types.enum_ECIDictVolume, PointerBase[object]], Pointer[types.char]]], types.sym_eciDictLookup]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *, void * *, enum ECIPartOfSpeech *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object], types.enum_ECIDictVolume, PointerBase[object], Pointer[PointerBase[object]], Pointer[types.enum_ECIPartOfSpeech]], types.enum_ECIDictError]], types.sym_eciDictLookupA]: ...
    @overload
    def callback(self, ctype: Literal['void(*)(struct _ECI *, void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object]], None]], types.sym_eciErrorMessage]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(struct _ECI *, int, void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], int, PointerBase[object]], int]], types.anon_funcptr_7]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(enum ECILanguageDialect *, int *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[Pointer[types.enum_ECILanguageDialect], Pointer[int]], int]], types.sym_eciGetAvailableLanguages]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(enum ECIParam)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[types.enum_ECIParam], int]], types.sym_eciGetDefaultParam]: ...
    @overload
    def callback(self, ctype: Literal['void *(*)(struct _ECI *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI]], PointerBase[object]]], types.anon_funcptr_8]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIFilterError(*)(struct _ECI *, void *, void *, void * *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object], PointerBase[object], Pointer[PointerBase[object]]], types.enum_ECIFilterError]], types.sym_eciGetFilteredText]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(struct _ECI *, enum ECIParam)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], types.enum_ECIParam], int]], types.sym_eciGetParam]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(struct _ECI *, int, enum ECIVoiceParam)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], int, types.enum_ECIVoiceParam], int]], types.sym_eciGetVoiceParam]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(struct _ECI *, int)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], int], int]], types.anon_funcptr_9]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object], types.enum_ECIDictVolume, PointerBase[object]], types.enum_ECIDictError]], types.anon_funcptr_10]: ...
    @overload
    def callback(self, ctype: Literal['struct _ECI *(*)()'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[], PointerBase[types.struct__ECI]]], types.sym_eciNew]: ...
    @overload
    def callback(self, ctype: Literal['struct _ECI *(*)(enum ECILanguageDialect)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[types.enum_ECILanguageDialect], PointerBase[types.struct__ECI]]], types.sym_eciNewEx]: ...
    @overload
    def callback(self, ctype: Literal['void *(*)(struct _ECI *, unsigned int, int)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], types.unsigned_int, int], PointerBase[object]]], types.sym_eciNewFilter]: ...
    @overload
    def callback(self, ctype: Literal['void(*)(struct _ECI *, enum ECICallbackReturn(*)(struct _ECI *, enum ECIMessage, long, void *), void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], types.ECICallback, PointerBase[object]], None]], types.sym_eciRegisterCallback]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIVoiceError(*)(struct _ECI *, int, void *, struct ECIVoiceAttrib *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], int, PointerBase[object], Pointer[types.struct_ECIVoiceAttrib]], types.enum_ECIVoiceError]], types.sym_eciRegisterVoice]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(enum ECIParam, int)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[types.enum_ECIParam, int], int]], types.sym_eciSetDefaultParam]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object]], types.enum_ECIDictError]], types.sym_eciSetDict]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(struct _ECI *, int, short *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], int, Pointer[types.short]], int]], types.sym_eciSetOutputBuffer]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(struct _ECI *, enum ECIParam, int)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], types.enum_ECIParam, int], int]], types.sym_eciSetParam]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(struct _ECI *, int, enum ECIVoiceParam, int)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], int, types.enum_ECIVoiceParam, int], int]], types.sym_eciSetVoiceParam]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(void *, int)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[object], int], int]], types.sym_eciSpeakText]: ...
    @overload
    def callback(self, ctype: Literal['int(*)(void *, int, enum ECILanguageDialect)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[object], int, types.enum_ECILanguageDialect], int]], types.sym_eciSpeakTextEx]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIVoiceError(*)(struct _ECI *, int, struct ECIVoiceAttrib *, void * *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], int, Pointer[types.struct_ECIVoiceAttrib], Pointer[PointerBase[object]]], types.enum_ECIVoiceError]], types.sym_eciUnregisterVoice]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *, void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object], types.enum_ECIDictVolume, PointerBase[object], PointerBase[object]], types.enum_ECIDictError]], types.sym_eciUpdateDict]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *, void *, enum ECIPartOfSpeech)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object], types.enum_ECIDictVolume, PointerBase[object], PointerBase[object], types.enum_ECIPartOfSpeech], types.enum_ECIDictError]], types.sym_eciUpdateDictA]: ...
    @overload
    def callback(self, ctype: Literal['enum ECIFilterError(*)(struct _ECI *, void *, void *, void *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[PointerBase[types.struct__ECI], PointerBase[object], PointerBase[object], PointerBase[object]], types.enum_ECIFilterError]], types.sym_eciUpdateFilter]: ...
    @overload
    def callback(self, ctype: Literal['void(*)(char *)'], error: Any = ..., onerror: ErrorCallback = ...) -> Callable[[Callable[[Pointer[types.char]], None]], types.sym_eciVersion]: ...

    @overload
    def cast(self, cdata: Literal['uintptr_t', 'intptr_t', 'size_t'], value: Union[int, PointerBase[Any]], /) -> IntPrimitive: ...
    @overload
    def cast(self, ctype: Literal['int *'], value: Union[int, PointerBase[Any]], /) -> Pointer[int]: ...
    @overload
    def cast(self, ctype: Literal['enum ECICallbackReturn *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECICallbackReturn]: ...
    @overload
    def cast(self, ctype: Literal['struct _ECI *', 'ECIHand'], value: Union[int, PointerBase[Any]], /) -> PointerBase[types.struct__ECI]: ...
    @overload
    def cast(self, ctype: Literal['struct _ECI * *'], value: Union[int, PointerBase[Any]], /) -> Pointer[PointerBase[types.struct__ECI]]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIMessage *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECIMessage]: ...
    @overload
    def cast(self, ctype: Literal['long *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.long]: ...
    @overload
    def cast(self, ctype: Literal['void *', 'ECIDictHand', 'ECIFilterHand', 'ECIInputText'], value: Union[int, PointerBase[Any]], /) -> PointerBase[object]: ...
    @overload
    def cast(self, ctype: Literal['void * *'], value: Union[int, PointerBase[Any]], /) -> Pointer[PointerBase[object]]: ...
    @overload
    def cast(self, ctype: Literal['enum ECICallbackReturn(*)(struct _ECI *, enum ECIMessage, long, void *)', 'ECICallback'], value: Union[int, PointerBase[Any]], /) -> types.ECICallback: ...
    @overload
    def cast(self, ctype: Literal['enum ECICallbackReturn(* *)(struct _ECI *, enum ECIMessage, long, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.ECICallback]: ...
    @overload
    def cast(self, ctype: Literal['unsigned char *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.unsigned_char]: ...
    @overload
    def cast(self, ctype: Literal['unsigned char(*)[5]'], value: Union[int, PointerBase[Any]], /) -> Pointer[Array[types.unsigned_char]]: ...
    @overload
    def cast(self, ctype: Literal['unsigned short *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.unsigned_short]: ...
    @overload
    def cast(self, ctype: Literal['unsigned short(*)[5]'], value: Union[int, PointerBase[Any]], /) -> Pointer[Array[types.unsigned_short]]: ...
    @overload
    def cast(self, ctype: Literal['union $1 *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_union_1]: ...
    @overload
    def cast(self, ctype: Literal['enum ECILanguageDialect *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECILanguageDialect]: ...
    @overload
    def cast(self, ctype: Literal['ECIMouthData *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.ECIMouthData]: ...
    @overload
    def cast(self, ctype: Literal['struct ECIVoiceAttrib *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.struct_ECIVoiceAttrib]: ...
    @overload
    def cast(self, ctype: Literal['char *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.char]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDialogBox *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECIDialogBox]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECIDictError]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictVolume *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECIDictVolume]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIFilterError *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECIFilterError]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIParam *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECIParam]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIPartOfSpeech *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECIPartOfSpeech]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIVoiceError *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECIVoiceError]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIVoiceParam *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.enum_ECIVoiceParam]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIFilterError(*)(struct _ECI *, void *)'], value: Union[int, PointerBase[Any]], /) -> types.anon_funcptr_1: ...
    @overload
    def cast(self, ctype: Literal['enum ECIFilterError(* *)(struct _ECI *, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_funcptr_1]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(struct _ECI *, void *)'], value: Union[int, PointerBase[Any]], /) -> types.anon_funcptr_2: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(struct _ECI *, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_funcptr_2]: ...
    @overload
    def cast(self, ctype: Literal['void(*)(struct _ECI *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciClearErrors: ...
    @overload
    def cast(self, ctype: Literal['void(* *)(struct _ECI *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciClearErrors]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(struct _ECI *)'], value: Union[int, PointerBase[Any]], /) -> types.anon_funcptr_3: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(struct _ECI *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_funcptr_3]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(struct _ECI *, int, int)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciCopyVoice: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(struct _ECI *, int, int)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciCopyVoice]: ...
    @overload
    def cast(self, ctype: Literal['struct _ECI *(*)(struct _ECI *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciDelete: ...
    @overload
    def cast(self, ctype: Literal['struct _ECI *(* *)(struct _ECI *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciDelete]: ...
    @overload
    def cast(self, ctype: Literal['void *(*)(struct _ECI *, void *)'], value: Union[int, PointerBase[Any]], /) -> types.anon_funcptr_4: ...
    @overload
    def cast(self, ctype: Literal['void *(* *)(struct _ECI *, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_funcptr_4]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *)'], value: Union[int, PointerBase[Any]], /) -> types.anon_funcptr_5: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_funcptr_5]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *, enum ECIPartOfSpeech *)'], value: Union[int, PointerBase[Any]], /) -> types.anon_funcptr_6: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void * *, void * *, enum ECIPartOfSpeech *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_funcptr_6]: ...
    @overload
    def cast(self, ctype: Literal['char *(*)(struct _ECI *, void *, enum ECIDictVolume, void *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciDictLookup: ...
    @overload
    def cast(self, ctype: Literal['char *(* *)(struct _ECI *, void *, enum ECIDictVolume, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciDictLookup]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *, void * *, enum ECIPartOfSpeech *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciDictLookupA: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void *, void * *, enum ECIPartOfSpeech *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciDictLookupA]: ...
    @overload
    def cast(self, ctype: Literal['void(*)(struct _ECI *, void *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciErrorMessage: ...
    @overload
    def cast(self, ctype: Literal['void(* *)(struct _ECI *, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciErrorMessage]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(struct _ECI *, int, void *)'], value: Union[int, PointerBase[Any]], /) -> types.anon_funcptr_7: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(struct _ECI *, int, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_funcptr_7]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(enum ECILanguageDialect *, int *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciGetAvailableLanguages: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(enum ECILanguageDialect *, int *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciGetAvailableLanguages]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(enum ECIParam)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciGetDefaultParam: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(enum ECIParam)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciGetDefaultParam]: ...
    @overload
    def cast(self, ctype: Literal['void *(*)(struct _ECI *)'], value: Union[int, PointerBase[Any]], /) -> types.anon_funcptr_8: ...
    @overload
    def cast(self, ctype: Literal['void *(* *)(struct _ECI *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_funcptr_8]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIFilterError(*)(struct _ECI *, void *, void *, void * *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciGetFilteredText: ...
    @overload
    def cast(self, ctype: Literal['enum ECIFilterError(* *)(struct _ECI *, void *, void *, void * *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciGetFilteredText]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(struct _ECI *, enum ECIParam)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciGetParam: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(struct _ECI *, enum ECIParam)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciGetParam]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(struct _ECI *, int, enum ECIVoiceParam)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciGetVoiceParam: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(struct _ECI *, int, enum ECIVoiceParam)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciGetVoiceParam]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(struct _ECI *, int)'], value: Union[int, PointerBase[Any]], /) -> types.anon_funcptr_9: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(struct _ECI *, int)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_funcptr_9]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *)'], value: Union[int, PointerBase[Any]], /) -> types.anon_funcptr_10: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.anon_funcptr_10]: ...
    @overload
    def cast(self, ctype: Literal['struct _ECI *(*)()'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciNew: ...
    @overload
    def cast(self, ctype: Literal['struct _ECI *(* *)()'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciNew]: ...
    @overload
    def cast(self, ctype: Literal['struct _ECI *(*)(enum ECILanguageDialect)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciNewEx: ...
    @overload
    def cast(self, ctype: Literal['struct _ECI *(* *)(enum ECILanguageDialect)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciNewEx]: ...
    @overload
    def cast(self, ctype: Literal['unsigned int *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.unsigned_int]: ...
    @overload
    def cast(self, ctype: Literal['void *(*)(struct _ECI *, unsigned int, int)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciNewFilter: ...
    @overload
    def cast(self, ctype: Literal['void *(* *)(struct _ECI *, unsigned int, int)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciNewFilter]: ...
    @overload
    def cast(self, ctype: Literal['void(*)(struct _ECI *, enum ECICallbackReturn(*)(struct _ECI *, enum ECIMessage, long, void *), void *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciRegisterCallback: ...
    @overload
    def cast(self, ctype: Literal['void(* *)(struct _ECI *, enum ECICallbackReturn(*)(struct _ECI *, enum ECIMessage, long, void *), void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciRegisterCallback]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIVoiceError(*)(struct _ECI *, int, void *, struct ECIVoiceAttrib *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciRegisterVoice: ...
    @overload
    def cast(self, ctype: Literal['enum ECIVoiceError(* *)(struct _ECI *, int, void *, struct ECIVoiceAttrib *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciRegisterVoice]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(enum ECIParam, int)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciSetDefaultParam: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(enum ECIParam, int)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciSetDefaultParam]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciSetDict: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciSetDict]: ...
    @overload
    def cast(self, ctype: Literal['short *'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.short]: ...
    @overload
    def cast(self, ctype: Literal['short * *'], value: Union[int, PointerBase[Any]], /) -> Pointer[Pointer[types.short]]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(struct _ECI *, int, short *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciSetOutputBuffer: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(struct _ECI *, int, short *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciSetOutputBuffer]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(struct _ECI *, enum ECIParam, int)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciSetParam: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(struct _ECI *, enum ECIParam, int)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciSetParam]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(struct _ECI *, int, enum ECIVoiceParam, int)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciSetVoiceParam: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(struct _ECI *, int, enum ECIVoiceParam, int)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciSetVoiceParam]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(void *, int)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciSpeakText: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(void *, int)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciSpeakText]: ...
    @overload
    def cast(self, ctype: Literal['int(*)(void *, int, enum ECILanguageDialect)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciSpeakTextEx: ...
    @overload
    def cast(self, ctype: Literal['int(* *)(void *, int, enum ECILanguageDialect)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciSpeakTextEx]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIVoiceError(*)(struct _ECI *, int, struct ECIVoiceAttrib *, void * *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciUnregisterVoice: ...
    @overload
    def cast(self, ctype: Literal['enum ECIVoiceError(* *)(struct _ECI *, int, struct ECIVoiceAttrib *, void * *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciUnregisterVoice]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *, void *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciUpdateDict: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void *, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciUpdateDict]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(*)(struct _ECI *, void *, enum ECIDictVolume, void *, void *, enum ECIPartOfSpeech)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciUpdateDictA: ...
    @overload
    def cast(self, ctype: Literal['enum ECIDictError(* *)(struct _ECI *, void *, enum ECIDictVolume, void *, void *, enum ECIPartOfSpeech)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciUpdateDictA]: ...
    @overload
    def cast(self, ctype: Literal['enum ECIFilterError(*)(struct _ECI *, void *, void *, void *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciUpdateFilter: ...
    @overload
    def cast(self, ctype: Literal['enum ECIFilterError(* *)(struct _ECI *, void *, void *, void *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciUpdateFilter]: ...
    @overload
    def cast(self, ctype: Literal['void(*)(char *)'], value: Union[int, PointerBase[Any]], /) -> types.sym_eciVersion: ...
    @overload
    def cast(self, ctype: Literal['void(* *)(char *)'], value: Union[int, PointerBase[Any]], /) -> Pointer[types.sym_eciVersion]: ...

    @overload
    def addressof[T: VarArg](self, cdata: Pointer[T], index: int, /) -> Pointer[T]: ...
    @overload
    def addressof[T: _CDataBase](self, cdata: T, /) -> Pointer[T]: ...
    @overload
    def addressof(self, cdata: types.anon_union_1, field: Literal['sz'], /) -> Pointer[Array[types.unsigned_char]]: ...
    @overload
    def addressof(self, cdata: types.anon_union_1, field: Literal['wsz'], /) -> Pointer[Array[types.unsigned_short]]: ...
    @overload
    def addressof(self, cdata: types.ECIMouthData, field: Literal['phoneme'], /) -> Pointer[types.anon_union_1]: ...
    @overload
    def addressof(self, cdata: types.ECIMouthData, field: Literal['eciLanguageDialect'], /) -> Pointer[types.enum_ECILanguageDialect]: ...
    @overload
    def addressof(self, cdata: types.ECIMouthData, field: Literal['mouthHeight'], /) -> Pointer[types.unsigned_char]: ...
    @overload
    def addressof(self, cdata: types.ECIMouthData, field: Literal['mouthWidth'], /) -> Pointer[types.unsigned_char]: ...
    @overload
    def addressof(self, cdata: types.ECIMouthData, field: Literal['mouthUpturn'], /) -> Pointer[types.unsigned_char]: ...
    @overload
    def addressof(self, cdata: types.ECIMouthData, field: Literal['jawOpen'], /) -> Pointer[types.unsigned_char]: ...
    @overload
    def addressof(self, cdata: types.ECIMouthData, field: Literal['teethUpperVisible'], /) -> Pointer[types.unsigned_char]: ...
    @overload
    def addressof(self, cdata: types.ECIMouthData, field: Literal['teethLowerVisible'], /) -> Pointer[types.unsigned_char]: ...
    @overload
    def addressof(self, cdata: types.ECIMouthData, field: Literal['tonguePosn'], /) -> Pointer[types.unsigned_char]: ...
    @overload
    def addressof(self, cdata: types.ECIMouthData, field: Literal['lipTension'], /) -> Pointer[types.unsigned_char]: ...
    @overload
    def addressof(self, cdata: types.struct_ECIVoiceAttrib, field: Literal['eciSampleRate'], /) -> Pointer[int]: ...
    @overload
    def addressof(self, cdata: types.struct_ECIVoiceAttrib, field: Literal['languageID'], /) -> Pointer[types.enum_ECILanguageDialect]: ...

ffi: FFI
