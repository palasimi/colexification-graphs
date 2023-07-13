# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2023 Levi Gruspe
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Compute FNV-1A hashes."""

from argparse import ArgumentParser, Namespace


def fnv_1a(data: bytes, prime: int, offset_basis: int, size: int) -> bytes:
    """Compute the FNV-1a hash of the input.

    size is the number of bytes.
    """
    mask = (1 << (size << 3)) - 1
    hash_ = offset_basis
    for byte in data:
        hash_ ^= byte
        hash_ *= prime
        hash_ &= mask
    return hash_.to_bytes(size)


def fnv_1a_32(data: bytes) -> bytes:
    """Compute the 32-bit FNV-1a hash."""
    return fnv_1a(data, prime=0x01000193, offset_basis=0x811c9dc5, size=4)


def fnv_1a_64(data: bytes) -> bytes:
    """Compute the 64-bit FNV-1a hash."""
    return fnv_1a(
        data,
        prime=0x00000100000001B3,
        offset_basis=0xcbf29ce484222325,
        size=8,
    )


def fnv_1a_128(data: bytes) -> bytes:
    """Compute the 128-bit FNV-1a hash."""
    return fnv_1a(
        data,
        prime=0x0000000001000000000000000000013B,
        offset_basis=0x6c62272e07bb014262b821756295c58d,
        size=16,
    )


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "-b",
        "--bits",
        dest="bits",
        choices=[32, 64, 128],
        default=32,
        type=int,
        help="number of bits",
    )
    parser.add_argument(
        "string",
        type=str,
        help="string to hash",
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    """Script entrypoint."""
    data = args.string.encode()
    match args.bits:
        case 32:
            print(fnv_1a_32(data).hex())
        case 64:
            print(fnv_1a_64(data).hex())
        case 128:
            print(fnv_1a_128(data).hex())


if __name__ == "__main__":
    main(parse_args())


__all__ = ["fnv_1a_32", "fnv_1a_64", "fnv_1a_128"]
