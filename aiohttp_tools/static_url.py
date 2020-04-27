import hashlib
import logging
import functools


SETTINGS = {
    "filename_to_url": lambda filename, hash: "/{}?v={}".format(filename, hash)
}
log = logging.getLogger(__name__)


def setup(**settings):
    SETTINGS.update(settings)


def static_url(filename):
    hash = file_version(filename)
    return SETTINGS["filename_to_url"](filename, hash)


@functools.lru_cache()
def file_version(filename):
    log.debug("Calculate version hash for file: %s", filename)
    return file_hash(filename)[-5:]


def file_hash(filename):
    md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b""):
            md5.update(chunk)
    return md5.hexdigest()
