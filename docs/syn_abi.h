/**
   ABI for synth engines (.SYN).

   Typical usage (without runtime loading) looks like this:

   ~~~ c
   SynthPtr synth = NULL;
   getObject(2, &synth);
   if (!synth)
	 return FAIL;

   if (!synth->vtable->init(synth))
	 goto cleanup;

   synth->vtable->methodName(synth, ...);
   // ...

   cleanup:
   synth->vtable->preDestruct(synth);
   synth->vtable->destroy(synth);
   synth = NULL;
   ~~~
 */

// just so my language server doesn't complain
#ifndef WIN32
#define __cdecl
#define __stdcall
#endif

// ENTRY POINT

typedef struct Synth *SynthPtr;

/**
 * this exported symbol is the entry point for the synth DLL.
 * it allocates a new `Synth` object and, if successful, places it in `outObject`.
 * `param` must be 2.
 */
extern void __stdcall getObject(int param, SynthPtr *outObject);

/**
 * @brief an instance of the synth engine.
 *
 * only a vtable seems to be exposed. note that unlike in a usual C++ object, here the vtable methods use `__stdcall` instead of `__thiscall`, e.g. `this` is passed as a normal arg in the stack rather than in ECX.
 *
 * unlike otherwise stated, methods that return `int` use 0 to signal successful operation.
 *
 * methods whose name starts with `setCallback` set a particular callback (which uses `__cdecl`, not `__stdcall`) and associated cookie (which is passed as the last argument). passing `callback = NULL` disables it.
 *
 * IMPORTANT: engines seem to vary a bit in which callbacks they support, see documentation for `CallbackFlag` in `ECI.INI`.
 */
struct Synth {
	struct Synth_vtable *vtable;
};


// CALLBACKS

/**
 * identifies a parameter which changed in the synthesizer, see `SynthParamCb`.
 * for more information about what the parameters mean, see the relevant
 * annotation in ECI docs (`tts.pdf`). note that for some voice parameters
 * (vb, vs, vv I think) ECI will rewrite the annotations with a units-converted
 * value before handing them over to the synth engine.
 */
enum SynthParamId {
	SynthParam_Global_TextMode, /** set via `` `ts `` [0..3] */
	SynthParam_Global_NumberMode, /** set via `` `ty `` (boolean) */
	SynthParam_Global2, /** i believe synths will not actually use this, as it stores the LangDialect in ECI */
	SynthParam_Global_DictionaryAbbr, /** set via `` `da `` (boolean) */
	SynthParam_Global_WantWordIndices, /** ECI stores here the value passed to `setWantWordIndices`, but i've never seen it actually passed to the callback */

	SynthParam_Voice_Gender, /** set via `` `vg `` (boolean) (FIXME) */
	SynthParam_Voice_HeadSize, /** set via `` `vh `` [0..64] */
	SynthParam_Voice_PitchBaseline, /** set via `` `vb `` [0..64] */
	SynthParam_Voice_PitchFluctuation, /** set via `` `vf `` [0..64] */
	SynthParam_Voice_Roughness, /** set via `` `vr `` [0..64] */
	SynthParam_Voice_Breathiness, /** set via `` `vy `` [0..64] */
	SynthParam_Voice_Speed, /** set via `` `vs `` [0..250] */
	SynthParam_Voice_Volume, /** set via `` `vv `` [0..64] */

	SynthParam_Global_UnkEci11, /** set via `` `pp `` (boolean) */
	SynthParam_Global14,
	SynthParam_Global15,
	SynthParam_Unk16,
	SynthParam_Unk17,
	SynthParam_Unk18,
	SynthParam_Global19,
};

/** phoneme names are passed as 4-character NUL-padded latin-1 strings */
union SynthPhonemeName {
	unsigned int word;
	char str [4];
};
// but cffi does not support composite types as callback parameters, so use unsigned int instead
#ifdef _IS_CFFI
typedef unsigned int SynthPhonemeName;
#else
typedef union SynthPhonemeName SynthPhonemeName;
#endif

/**
 * a chunk of output audio is available.
 * the engine keeps ownership of the passed buffer, which is no longer valid once the callback returns.
 * the audio is 16-bit signed mono (the values are in the range of a 16-bit int even if they're 32-bit) at the sample rate set up with the `` `esr `` annotation.
 */
typedef void (__cdecl *SynthAudioCb)(int nSamples, int *samples, void *cookie);

/**
 * informs you of the position increment in the text stream, e.g. amount of characters processed since last callback dispatch.
 * note that an escaped character is 1 character, e.g. the `\` does not count.
 */
typedef void (__cdecl *SynthTextIndexCb)(int index, void *cookie);

/**
 * audio production has reached an event registered with `pushEvent` or `pushEventAt`.
 * this callback appears NOT to be synchronized with `SynthAudioCb`, `SynthTextIndexCb`, `SynthUserIndexCb`, `SynthWordIndexCb` or `SynthPhonemeCb`?
 */
typedef void (__cdecl *SynthEventCb)(int eventId, void *cookie);

/**
 * a phoneme has been uttered. see `ECI.INI` for remarks on phoneme names.
 * FIXME: `streamPosition` could be some position in the text or audio, or it could be some sort of internal phoneme ID.
 */
typedef void (__cdecl *SynthPhonemeCb)(SynthPhonemeName phoneme, int streamPosition, void *cookie);

/** an engine parameter has a new value; see SynthParamId. */
typedef void (__cdecl *SynthParamCb)(enum SynthParamId param, int value, void *cookie);

/** informs you of the word position in the text stream, e.g. amount of words uttered. */
typedef void (__cdecl *SynthWordIndexCb)(int index, void *cookie);

/** a `` `ui `` annotation has been reached. */
typedef void (__cdecl *SynthUserIndexCb)(void *cookie);


// METHODS

/** opaque handle for a dictionary set belonging to an engine instance */
typedef struct _SynthDict *SynthDict;

/**
 * a NUL-terminated string (FIXME: encoding?) holding a dictionary key / translation.
 * when returned by the engine, the string is presumed to be read-only and owned by the dictionary. should be safe to use at least until the dictionary is mutated.
 * return value of NULL means entry not found.
 */
typedef const char *SynthDictStr;

/** identifies a dictionary within a dictionary set. */
enum SynthDictVolume {
	dictMain = 0,
	dictRoot = 1,
	dictAbbv = 2,
};

typedef enum SynthDictVolume SynthDictVolume;

struct Synth_vtable {
	void (__stdcall *__method0)(SynthPtr _obj);
	void (__stdcall *__method1)(SynthPtr _obj);

	/** destroy and free the instance (no methods may be called after this) */
	void (__stdcall *destroy)(SynthPtr _obj);
	/** called once before anything else */
	int (__stdcall *init)(SynthPtr _obj);

	void (__stdcall *__method4)(SynthPtr _obj);

	/**
	 * push input text with annotations. unless the string ends with a space, one seems to be inserted implicitly (we know this because we see an extra char processed according to TextIndex, and because words are split across pushText boundaries).
	 * in addition to the annotations explained in ECI documentation, some others have been seen:
	 *   - `` `esr<N> `` sets sample rate (0 = 8kHz, 1 = 11kHz)
	 *   - `` `espr<Bool> `` enables/disables phoneme generation (this includes both `SynthPhonemeCb` and annotated-form output that can be consumed with `readPhonemes`). Note that this annotation only has an effect if `setWantWordIndices` is set.
	 *   - `` `einp<Bool> `` like `espr` but generates Pinyin phonemes instead? untested
	 *   - `` `ui `` dispatches `SynthUserIndexCb`
	 */
	int (__stdcall *pushText)(SynthPtr _obj, const char *annotatedText);
	/** like `pushText`, but also flushes the synthesizer (dispatching all the phoneme, audio and index callbacks). NULL can be passed if just a flush is desired. */
	int (__stdcall *pushTextSync)(SynthPtr _obj, const char *annotatedText);

	void (__stdcall *__method7)(SynthPtr _obj);
	void (__stdcall *__method8)(SynthPtr _obj);

	/**
	 * reads output phonemes into a buffer.
	 *
	 * attempts to read up to `capacity` 8-bit characters (including a terminating NUL) into `buffer`, and if successful, places the amount of characters read (including the NUL) in `outLength`.
	 * if there are no remaining characters to read, the method still returns successful, but places 0 in `outLength` (even though the NUL is still written).
	 * warning: if called while flushing, it returns successfully *without* setting `outLength` or writing anything.
	 */
	int (__stdcall *readPhonemes)(SynthPtr _obj, char *buffer, int capacity, int *outLength);

	void (__stdcall *__method10)(SynthPtr _obj);

	/** ECI sets this to false when switching to an engine (on the new engine, after calling `prepare`) and toggles it momentarily as part of `eciStop` */
	int (__stdcall *setFlushing)(SynthPtr _obj, int value);
	/** resets parameter state. seems to cover all parameters that can be set through annotations, even if they are not notified via `SynthParamCb`. ECI calls this when switching to an engine (on the new engine) after setting all the callbacks */
	int (__stdcall *resetParams)(SynthPtr _obj);

	void (__stdcall *__method13)(SynthPtr _obj);
	void (__stdcall *__method14)(SynthPtr _obj);
	void (__stdcall *__method15)(SynthPtr _obj);
	void (__stdcall *__method16)(SynthPtr _obj);

	int (__stdcall *setCallbackAudio)(SynthPtr _obj, SynthAudioCb callback, void *cookie);

	void (__stdcall *__method18)(SynthPtr _obj);

	void (__stdcall *setCallbackTextIndex)(SynthPtr _obj, SynthTextIndexCb callback, void *cookie);
	void (__stdcall *setCallbackEvent)(SynthPtr _obj, SynthEventCb callback, void *cookie);
	void (__stdcall *setCallbackPhoneme)(SynthPtr _obj, SynthPhonemeCb callback, void *cookie);
	void (__stdcall *setCallbackParam)(SynthPtr _obj, SynthParamCb callback, void *cookie);

	/** register an event ID at the current point in the stream (`SynthEventCb` will be dispatched with that ID once production has gotten to it) */
	int (__stdcall *pushEvent)(SynthPtr _obj, int eventId);
	/** like pushEvent but with a mysterious extra argument, which ECI passes as the last argument of `SynthPhonemeCb`, so it could be a {text, audio} position to register the event in, or an internal phoneme ID to associate the event with... assuming the former for now (FIXME) */
	int (__stdcall *pushEventAt)(SynthPtr _obj, int eventId, int streamPosition);

	/** presumably controls whether `SynthWordIndexCb` is dispatched */
	void (__stdcall *setWantWordIndices)(SynthPtr _obj, int enabled);

	/** called by ECI just before `destroy` (?) */
	void (__stdcall *preDestruct)(SynthPtr _obj);

	/** create a new, empty dictionary set in the instance. returns NULL if allocation fails. */
	SynthDict (__stdcall *dictNew)(SynthPtr _obj);
	void (__stdcall *__method28)(SynthPtr _obj);
	/** set the active user dictionary set (pass NULL to remove the active user dictionary set) */
	void (__stdcall *dictSetActive)(SynthPtr _obj, SynthDict dict);
	/** deallocates a user dictionary set, deactivating it if needed */
	void (__stdcall *dictDelete)(SynthPtr _obj, SynthDict dict);
	/** populate a dictionary with entries read from the passed file */
	void (__stdcall *dictLoad)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, const char *filename);
	/** write dictionary entries to the passed file */
	void (__stdcall *dictSave)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, const char *filename);
	/** add or update an entry in a dictionary (if translation != NULL), or remove it (if NULL) */
	int (__stdcall *dictUpdate)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, SynthDictStr key, SynthDictStr translation);
	/** fetch the first entry in a dictionary */
	void (__stdcall *dictGetFirstEntry)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, SynthDictStr *key, SynthDictStr *translation);
	/** fetch the entry following the last returned entry */
	void (__stdcall *dictGetNextEntry)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, SynthDictStr *key, SynthDictStr *translation);
	/** fetch the entry for a key in a dictionary, returning the translation */
	SynthDictStr (__stdcall *dictLookup)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, SynthDictStr key);

	void (__stdcall *setCallbackWordIndex)(SynthPtr _obj, SynthWordIndexCb callback, void *cookie);
	void (__stdcall *setCallbackUserIndex)(SynthPtr _obj, SynthUserIndexCb callback, void *cookie);
};

// FIXME: check if getObject really allocates a new object every time or if you'd have to load many instances of the DLL (I'd hope not)
// FIXME: check callback return values
