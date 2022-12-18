import sys
import tempfile
from os.path import join

from django.conf import settings

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

# DEFAULTS
VITE_BUNDLE_KEYWORD_DEFAULT = "vite"
VITE_EXTENSION_MAP_DEFAULT = {
    ".js": [".js", ".mjs", ".ts", ".jsx", ".tsx"],
    ".css": [".css", ".sass", ".scss"],
}
VITE_PORT_DEFAULT = 6555
VITE_TSCONFIG_PATH_DEFAULT = None
VITE_TSCONFIG_EXTENDS_DEFAULT = {
    "compilerOptions": {
        "paths": {},
    },
    "include": [],
}
VITE_IGNORE_EXCLUDE_DEFAULT = []
VITE_OUT_DIR_DEFAULT = join(tempfile.mkdtemp())

# SETTINGS
VITE_BUNDLE_KEYWORD = getattr(
    settings, "VITE_BUNDLE_KEYWORD", VITE_BUNDLE_KEYWORD_DEFAULT
)
VITE_EXTENSION_MAP = getattr(settings, "VITE_EXTENSION_MAP", VITE_EXTENSION_MAP_DEFAULT)
VITE_OUT_DIR = getattr(settings, "VITE_OUT_DIR", VITE_OUT_DIR_DEFAULT)
VITE_PORT = getattr(settings, "VITE_PORT", VITE_PORT_DEFAULT) + (1 if TESTING else 0)
VITE_TSCONFIG_PATH = getattr(settings, "VITE_TSCONFIG_PATH", VITE_TSCONFIG_PATH_DEFAULT)
VITE_IGNORE_EXCLUDE = getattr(
    settings, "VITE_IGNORE_EXCLUDE", VITE_IGNORE_EXCLUDE_DEFAULT
)
VITE_TSCONFIG_EXTENDS = getattr(
    settings, "VITE_TSCONFIG_EXTENDS", VITE_TSCONFIG_EXTENDS_DEFAULT
)

# VALUES
VITE_ROOT = str(settings.BASE_DIR)
VITE_URL = str(settings.STATIC_URL)
CSS_EXTENSIONS = VITE_EXTENSION_MAP[".css"]
JS_EXTENSIONS = VITE_EXTENSION_MAP[".js"]
