from abc import ABC, abstractmethod

import hashlib


class HandleFileAbstract(ABC):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.hash_chunk_dict = {}

    @abstractmethod
    def break_file_into_chunks(self, chunk_size=256 * 1024): ...

    @abstractmethod
    def hash_chunk(self, chunk, hash_algorithm='sha1'): ...


class TXTHandleFile(HandleFileAbstract):
    def break_file_into_chunks(self, chunk_size=256 * 1024):
        with open(self.file_path, 'rb') as file:
            index = 1
            chunk = file.read(chunk_size)
            while chunk:
                yield chunk
                self.hash_chunk_dict.update({f'{index}:{self.hash_chunk(chunk)}': chunk})
                index += 1
                chunk = file.read(chunk_size)

    def hash_chunk(self, chunk, hash_algorithm='sha1'):
        hash_obj = hashlib.new(hash_algorithm)
        hash_obj.update(chunk)
        return hash_obj.hexdigest()
