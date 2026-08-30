

# %% ../notebooks/01_data_contracts_provenance.ipynb #identity-code-01
import hashlib
from pathlib import Path as IdentityPath

__all__ = ["sha256_bytes", "sha256_file"]


def sha256_bytes(content: bytes) -> str:
    """Return the lowercase SHA-256 digest of bytes."""

    return hashlib.sha256(content).hexdigest()


def sha256_file(path: IdentityPath) -> str:
    """Return the lowercase SHA-256 digest of a file without loading it whole."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()