import sys
from os.path import abspath, dirname, join

from django.conf import settings

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

# DEFAULTS
VITE_BUNDLE_KEYWORD_DEFAULT = "vite"
VITE_EXTENSION_MAP_DEFAULT = {
    ".js": [".js", ".mjs", ".ts", ".jsx", ".tsx", ".json"],
    ".css": [".css", ".sass", ".scss"],
}
VITE_PORT_DEFAULT = 5555
VITE_TSCONFIG_GENERATE_DEFAULT = True
VITE_TSCONFIG_PATH_DEFAULT = "/tmp/tsconfig.django.json"

# SETTINGS
VITE_BUNDLE_KEYWORD = getattr(
    settings, "VITE_BUNDLE_KEYWORD", VITE_BUNDLE_KEYWORD_DEFAULT
)
VITE_EXTENSION_MAP = getattr(
    settings, "VITE_EXTENSION_MAP", VITE_EXTENSION_MAP_DEFAULT
)
VITE_OUT_DIR = str(settings.STATIC_ROOT)
VITE_PORT = getattr(settings, "VITE_PORT", VITE_PORT_DEFAULT) + (
    1 if TESTING else 0
)
VITE_TSCONFIG_GENERATE = getattr(
    settings, "VITE_TSCONFIG_GENERATE", VITE_TSCONFIG_GENERATE_DEFAULT
)
VITE_TSCONFIG_PATH = getattr(
    settings, "VITE_TSCONFIG_PATH", VITE_TSCONFIG_PATH_DEFAULT
)

# VALUES
VITE_ROOT = str(settings.BASE_DIR)
VITE_URL = str(settings.STATIC_URL)
CSS_EXTENSIONS = VITE_EXTENSION_MAP[".css"]
JS_EXTENSIONS = VITE_EXTENSION_MAP[".js"]
