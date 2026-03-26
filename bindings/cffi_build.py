from subprocess import run
import cffi
from cffi_mkstub import write_type_stub

ffi = cffi.FFI()
src = run('clang -E -DWIN32 -D_WIN32 ../synthDrivers/eloquence/eci.h', shell=True, check=True, capture_output=True, text=True).stdout
ffi.cdef(src, pack=True)
ffi.set_source(mod_name := '_eci_cffi', None)
ffi.compile(verbose=True, debug=False)
write_type_stub(mod_name)

ffi = cffi.FFI()
src = run('clang -E -DWIN32 -D_WIN32 ../docs/syn_abi.h', shell=True, check=True, capture_output=True, text=True).stdout
ffi.cdef(src)
ffi.set_source(mod_name := '_syn_cffi', None)
ffi.compile(verbose=True, debug=False)
write_type_stub(mod_name)
