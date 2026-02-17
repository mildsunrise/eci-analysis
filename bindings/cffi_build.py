from subprocess import run
import cffi
ffi = cffi.FFI()
src = run('clang -E -DWIN32 -D_WIN32 ../synthDrivers/eloquence/eci.h', shell=True, check=True, capture_output=True, text=True).stdout
ffi.cdef(src, pack=True)
ffi.set_source('_eloquence_cffi', None, library=['../synthDrivers/eloquence/ECI'])
ffi.compile(verbose=True, debug=False)
