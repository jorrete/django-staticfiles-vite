import sys
from os.path import abspath, dirname, join

from django.conf import settings

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

# DEFAULTS
VITE_BUNDLE_KEYWORD_DEFAULT = "vite"
VITE_CONFIG_DEFAULT = str(settings.BASE_DIR / ".." / "vite.config.js")
VITE_EXTENSION_MAP_DEFAULT = {
    ".js": [".mjs", ".ts", ".tsx", ".jsx"],
    ".css": [".sass", ".scss"],
}
VITE_IMPORT_KEYWORD_DEFAULT = "import"
VITE_NODE_MODULES_DEFAULT = str(settings.BASE_DIR / ".." / "node_modules")
VITE_PORT_DEFAULT = 5555
VITE_ROOT_DEFAULT = str(settings.BASE_DIR / "..")


# SETTINGS
VITE_BUNDLE_KEYWORD = getattr(
    settings, "VITE_BUNDLE_KEYWORD", VITE_BUNDLE_KEYWORD_DEFAULT
)  # noqa: E261
VITE_CONFIG = getattr(settings, "VITE_CONFIG", VITE_CONFIG_DEFAULT)  # noqa: E261
VITE_EXTENSION_MAP = getattr(
    settings, "VITE_EXTENSION_MAP", VITE_EXTENSION_MAP_DEFAULT
)  # noqa: E261
VITE_IMPORT_KEYWORD = getattr(
    settings, "VITE_IMPORT_KEYWORD", VITE_IMPORT_KEYWORD_DEFAULT
)  # noqa: E261
VITE_NODE_MODULES = getattr(
    settings, "VITE_NODE_MODULES", VITE_NODE_MODULES_DEFAULT
)  # noqa: E261
VITE_OUT_DIR = str(settings.STATIC_ROOT)
VITE_PORT = getattr(settings, "VITE_PORT", VITE_PORT_DEFAULT) + (
    1 if TESTING else 0
)  # noqa: E261
VITE_ROOT = getattr(settings, "VITE_ROOT", VITE_ROOT_DEFAULT)  # noqa: E261
VITE_URL = settings.STATIC_URL

# VALUES
NODE_SCRIPTS_PATH = abspath(join(dirname(__file__), "node"))  # noqa: E261
BUILD_PATH = join(NODE_SCRIPTS_PATH, "build.js")
CSS_EXTENSIONS = [".css"] + VITE_EXTENSION_MAP[".css"]
JS_EXTENSIONS = [".js"] + VITE_EXTENSION_MAP[".js"]
POSTCSS_PATH = join(NODE_SCRIPTS_PATH, "postcss.js")
SERVE_PATH = join(NODE_SCRIPTS_PATH, "serve.js")
