# stego/container.py
import struct
import zlib

MAGIC = b'STG1'
VERSION = 0x01

def pack_container(payload: bytes) -> bytes:
    """Упаковка зашифрованных данных в контейнер."""
    header = MAGIC + bytes([VERSION]) + struct.pack('>I', len(payload))
    body = header + payload
    crc = struct.pack('>I', zlib.crc32(body) & 0xFFFFFFFF)
    return body + crc

def unpack_container(data: bytes) -> bytes:
    """Распаковка и проверка целостности."""
    if len(data) < 13:
        raise ValueError('Данные слишком короткие')
    
    if data[:4] != MAGIC:
        raise ValueError('Неверная сигнатура — это не наш контейнер')
    
    version = data[4]
    if version != VERSION:
        raise ValueError(f'Неподдерживаемая версия: {version}')
    
    length = struct.unpack('>I', data[5:9])[0]
    payload = data[9:9 + length]
    crc_stored = struct.unpack('>I', data[9 + length:13 + length])[0]
    
    # Проверка CRC
    crc_calc = zlib.crc32(data[:9 + length]) & 0xFFFFFFFF
    if crc_calc != crc_stored:
        raise ValueError('CRC не совпадает — данные повреждены')
    
    return payload