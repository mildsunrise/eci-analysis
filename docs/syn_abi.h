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
 * a chunk of output audio is available.
 * the engine keeps ownership of the passed buffer, which is no longer valid once the callback returns.
 * the audio is 16-bit signed mono, at the sample rate set up with the `` `sr `` annotation.
 */
typedef void __cdecl (*SynthAudioCb)(int nSamples, short *audiobuf, void *cookie);

/**
 * informs you of the position in the text stream, e.g. amount of characters processed (note that an escaped character is 1 character, e.g. the `\` does not count).
 * ECI unsets this while calling `pushText2`.
 */
typedef void __cdecl (*SynthTextIndexCb)(int index, void *cookie);

/**
 * audio production has reached an event registered with `pushEvent` or `pushEventAt`.
 * ECI usage seems to suggest that, unlike `SynthTextIndexCb`, `SynthUserIndexCb`, `SynthWordIndexCb` or `SynthPhonemeCb`, this callback is synchronized with `SynthAudioCb`. but it could be different semantics (FIXME)
 */
typedef void __cdecl (*SynthEventCb)(int eventId, void *cookie);

/**
 * a phoneme has been uttered. see `ECI.INI` for remarks on phoneme names.
 * FIXME: `streamPosition` could be some position in the text or audio, or it could be some sort of internal phoneme ID.
 */
typedef void __cdecl (*SynthPhonemeCb)(char phonemeName [4], int streamPosition, void *cookie);

/** an engine parameter has a new value; see SynthParamId. */
typedef void __cdecl (*SynthParamCb)(enum SynthParamId param, int value, void *cookie);

/** informs you of the word position in the text stream, e.g. amount of words uttered. */
typedef void __cdecl (*SynthWordIndexCb)(int index, void *cookie);

/**
 * a `` `ui `` annotation has been reached.
 * ECI unsets this while calling `pushText2`.
 */
typedef void __cdecl (*SynthUserIndexCb)(void *cookie);


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
	void __stdcall (*__method0)(SynthPtr _obj);
	void __stdcall (*__method1)(SynthPtr _obj);

	/** destroy and free the instance (no methods may be called after this) */
	void __stdcall (*destroy)(SynthPtr _obj);
	/** called before anything else */
	int __stdcall (*init)(SynthPtr _obj);

	void __stdcall (*__method4)(SynthPtr _obj);

	/** push input text with annotations. unless the string ends with a space, one seems to be inserted implicitly (we know this because we see an extra char processed according to TextIndex, and because words are split across pushText boundaries). */
	int __stdcall (*pushText)(SynthPtr _obj, const char *annotatedText);
	/** like pushText, but this version seems to be used only for setting parameters */
	int __stdcall (*pushText2)(SynthPtr _obj, const char *annotatedText);

	void __stdcall (*__method7)(SynthPtr _obj);
	void __stdcall (*__method8)(SynthPtr _obj);

	/**
	 * reads output phonemes into a buffer.
	 *
	 * attempts to read up to `capacity` 8-bit characters into `buffer`, and if successful, places the amount of characters read in `outLength`. no NUL terminator is written (FIXME: verify this is the case, and not that it's written but not included in `capacity` and `outLength`).
	 */
	int __stdcall (*readPhonemes)(SynthPtr _obj, char *buffer, int capacity, int *outLength);

	void __stdcall (*__method10)(SynthPtr _obj);

	/** ECI sets this to false when switching to an engine (on the new engine) and toggles it momentarily as part of `eciStop` */
	int __stdcall (*setFlushing)(SynthPtr _obj, bool value);
	/** ECI calls this when switching to an engine (on the new engine) so presumably it resets some internal state or prepares for synthesis in some way? */
	int __stdcall (*prepare)(SynthPtr _obj);

	void __stdcall (*__method13)(SynthPtr _obj);
	void __stdcall (*__method14)(SynthPtr _obj);
	void __stdcall (*__method15)(SynthPtr _obj);
	void __stdcall (*__method16)(SynthPtr _obj);

	int __stdcall (*setCallbackAudio)(SynthPtr _obj, SynthAudioCb callback, void *cookie);

	void __stdcall (*__method18)(SynthPtr _obj);

	void __stdcall (*setCallbackTextIndex)(SynthPtr _obj, SynthTextIndexCb callback, void *cookie);
	void __stdcall (*setCallbackEvent)(SynthPtr _obj, SynthEventCb callback, void *cookie);
	void __stdcall (*setCallbackPhoneme)(SynthPtr _obj, SynthPhonemeCb callback, void *cookie);
	void __stdcall (*setCallbackParam)(SynthPtr _obj, SynthParamCb callback, void *cookie);

	/** register an event ID at the current point in the stream (`SynthEventCb` will be dispatched with that ID once production has gotten to it) */
	int __stdcall (*pushEvent)(SynthPtr _obj);
	/** like pushEvent but with a mysterious extra argument, which ECI passes as the last argument of `SynthPhonemeCb`, so it could be a {text, audio} position to register the event in, or an internal phoneme ID to associate the event with... assuming the former for now (FIXME) */
	int __stdcall (*pushEventAt)(SynthPtr _obj, int eventId, int streamPosition);

	void __stdcall (*setWantWordIndices)(SynthPtr _obj, bool enabled);

	/** called by ECI just before `destroy` (?) */
	void __stdcall (*preDestruct)(SynthPtr _obj);

	/** create a new, empty dictionary set in the instance. returns NULL if allocation fails. */
	SynthDict __stdcall (*dictNew)(SynthPtr _obj);
	void __stdcall (*__method28)(SynthPtr _obj);
	/** set the active user dictionary set (pass NULL to remove the active user dictionary set) */
	void __stdcall (*dictSetActive)(SynthPtr _obj, SynthDict dict);
	/** deallocates a user dictionary set, deactivating it if needed */
	void __stdcall (*dictDelete)(SynthPtr _obj, SynthDict dict);
	/** populate a dictionary with entries read from the passed file */
	void __stdcall (*dictLoad)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, const char *filename);
	/** write dictionary entries to the passed file */
	void __stdcall (*dictSave)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, const char *filename);
	/** add or update an entry in a dictionary (if translation != NULL), or remove it (if NULL) */
	int __stdcall (*dictUpdate)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, SynthDictStr key, SynthDictStr translation);
	/** fetch the first entry in a dictionary */
	void __stdcall (*dictGetFirstEntry)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, SynthDictStr *key, SynthDictStr *translation);
	/** fetch the entry following the last returned entry */
	void __stdcall (*dictGetNextEntry)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, SynthDictStr *key, SynthDictStr *translation);
	/** fetch the entry for a key in a dictionary, returning the translation */
	SynthDictStr __stdcall (*dictLookup)(SynthPtr _obj, SynthDict dict, SynthDictVolume volume, SynthDictStr key);

	void __stdcall (*setCallbackWordIndex)(SynthPtr _obj, SynthWordIndexCb callback, void *cookie);
	void __stdcall (*setCallbackUserIndex)(SynthPtr _obj, SynthUserIndexCb callback, void *cookie);
};

// FIXME: check if getObject really allocates a new object every time or if you'd have to load many instances of the DLL (I'd hope not)
// FIXME: check callback return values
