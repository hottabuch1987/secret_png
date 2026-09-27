# stego/embedder.py
import hashlib
import struct
import numpy as np
from PIL import Image

MAGIC = b'STG1'
HEADER_SIZE = 13  # 4 (MAGIC) + 1 (VERSION) + 4 (LENGTH) + 4 (CRC)


def _derive_seed(password: str, salt: bytes = b'stego-salt-v1') -> int:
    """Детерминированный seed из пароля."""
    digest = hashlib.sha256(salt + password.encode()).digest()
    return int.from_bytes(digest[:8], 'big')


def _permutation(seed: int, total: int) -> np.ndarray:
    """
    Полная перестановка индексов, детерминированная по seed.
    Первые N элементов одинаковы при любом N — это ключ к тому,
    чтобы embed и extract использовали одни и те же позиции.
    """
    rng = np.random.default_rng(seed)
    return rng.permutation(total)


def _bits_to_bytes(flat: np.ndarray, positions: np.ndarray, count_bits: int) -> bytes:
    """Собирает байты из младших битов по заданным позициям."""
    bits = np.array([flat[positions[i]] & 1 for i in range(count_bits)], dtype=np.uint8)
    result = bytearray()
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte |= int(bits[i + j]) << j
        result.append(byte)
    return bytes(result)


def embed_from_pil(img: Image.Image, container_bytes: bytes, password: str) -> Image.Image:
    """Внедряет контейнер в пиксели картинки (работает с PIL.Image)."""
    arr = np.array(img.convert('RGB'))
    flat = arr.flatten().astype(np.int16)

    bits_needed = len(container_bytes) * 8
    if bits_needed > len(flat):
        raise ValueError(
            f'Картинка слишком мала: нужно {bits_needed} бит, доступно {len(flat)}'
        )

    seed = _derive_seed(password)
    perm = _permutation(seed, len(flat))
    positions = perm[:bits_needed]

    bit_idx = 0
    for byte in container_bytes:
        for shift in range(8):
            bit = (byte >> shift) & 1
            pos = positions[bit_idx]
            flat[pos] = (flat[pos] & 0xFE) | bit
            bit_idx += 1

    return Image.fromarray(flat.astype(np.uint8).reshape(arr.shape))


def extract_from_pil(img: Image.Image, password: str) -> bytes:
    """
    Извлекает контейнер из картинки:
    1. Читает заголовок (13 байт) теми же позициями, что при внедрении.
    2. Проверяет сигнатуру и версию.
    3. Узнаёт длину payload из заголовка.
    4. Читает весь контейнер (заголовок + payload + CRC).
    """
    flat = np.array(img.convert('RGB')).flatten()
    seed = _derive_seed(password)
    perm = _permutation(seed, len(flat))

    # 1) Читаем заголовок (13 байт)
    header_bits = HEADER_SIZE * 8
    if header_bits > len(flat):
        raise ValueError('Картинка слишком мала')

    header = _bits_to_bytes(flat, perm, header_bits)

    # 2) Проверяем сигнатуру
    if header[:4] != MAGIC:
        raise ValueError('Неверная сигнатура — это не наш контейнер')

    version = header[4]
    if version != 0x01:
        raise ValueError(f'Неподдерживаемая версия: {version}')

    # 3) Читаем длину payload
    length = struct.unpack('>I', header[5:9])[0]

    total_bytes = HEADER_SIZE + length
    total_bits = total_bytes * 8

    if total_bits > len(flat):
        raise ValueError('Картинка слишком мала для этого контейнера')

    # 4) Читаем весь контейнер
    return _bits_to_bytes(flat, perm, total_bits)


# --- Старые функции для работы с путями (оставлены для совместимости) ---

def embed(image_path: str, container_bytes: bytes, password: str) -> Image.Image:
    """Внедряет контейнер в пиксели картинки по пути к файлу."""
    img = Image.open(image_path)
    return embed_from_pil(img, container_bytes, password)


def extract(image_path: str, password: str) -> bytes:
    """Извлекает контейнер из картинки по пути к файлу."""
    img = Image.open(image_path)
    return extract_from_pil(img, password)