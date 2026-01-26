{ pkgs ? import <nixpkgs> {} }: with pkgs; pkgs.mkShell {
	nativeBuildInputs = [ clang wine ];

	PYWIN32 = fetchzip {
		name = "python-3.14.2-embed-win32";
		url = "https://www.python.org/ftp/python/3.14.2/python-3.14.2-embed-win32.zip";
		hash = "sha256-WeoHXMZbh14CtJKRYZuAzvgj7giaSf6rrkkROShB3qI=";
		stripRoot = false;
	};

	PYWIN32_CFFI = fetchzip {
		name = "cffi-2.0.0-cp314-cp314-win32";
		url = "https://files.pythonhosted.org/packages/3e/aa/df335faa45b395396fcbc03de2dfcab242cd61a9900e914fe682a59170b1/cffi-2.0.0-cp314-cp314-win32.whl";
		hash = "sha256-syDLryeJxHsskbg9zLRw+02SH2jV1AoXwGkYVPpPRJw=";
		stripRoot = false;
		extension = "zip";
	};
}
