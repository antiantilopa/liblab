import threading, socket
from typing import Any

class SerializationTypes:
    END = 0
    CHAR = 1
    SHORT = 2
    INT = 3
    LONG = 4
    S_CHAR = 5
    S_SHORT = 6
    S_INT = 7
    S_LONG = 8

    integer_types = (CHAR, S_CHAR, SHORT, S_SHORT, INT, S_INT, LONG, S_LONG)
    signed_types = (S_CHAR, S_SHORT, S_INT, S_LONG)

    FLOAT = 9
    DOUBLE = 10

    size_dict = {
        CHAR: 1,
        S_CHAR: 1,
        SHORT: 2,
        S_SHORT: 2,
        INT: 4,
        S_INT: 4,
        LONG: 8,
        S_LONG: 8,
        FLOAT: 4,
        DOUBLE: 8
    }

    # In array every element has identical type
    ARRAY_BEGIN = 11

    # In list there can be different types of elements
    LIST_BEGIN = 12

    STRING_BEGIN = 13

    names = (
        "END", 
        "CHAR",
        "SHORT",
        "INT",
        "LONG",
        "S_CHAR",
        "S_SHORT",
        "S_INT",
        "S_LONG",
        "FLOAT",
        "DOUBLE",
        "ARRAY_BEGIN",
        "LIST_BEGIN",
        "STRING_BEGIN",
    )

def abs(x):
    if x < 0: x*=-1
    return x

def binary(x):
    return "0" * ((2 - len(bin(x))) % 8) + bin(x).removeprefix("0b") 



class Serializator:

    @staticmethod
    def encode_to(obj: int|float|tuple|list|set|str, serialization_type: int, *args: list[int]):
        if serialization_type in (SerializationTypes.S_CHAR, SerializationTypes.S_SHORT, SerializationTypes.S_INT, SerializationTypes.S_LONG):
            if not isinstance(obj, int):
                raise TypeError(f"{obj} is not integer to be serialized as {SerializationTypes.names[serialization_type]}")
            if obj < 0 or  obj > 256 ** SerializationTypes.size_dict[serialization_type]:
                raise ValueError(f"{obj} can not be serialized as {SerializationTypes.names[serialization_type]}")
            return bytes([serialization_type] + [(obj // (256 ** (SerializationTypes.size_dict[serialization_type] - i - 1))) % 256 for i in range(SerializationTypes.size_dict[serialization_type])])
        elif serialization_type in (SerializationTypes.CHAR, SerializationTypes.SHORT, SerializationTypes.INT, SerializationTypes.LONG):
            if abs(obj) > 256 ** SerializationTypes.size_dict[serialization_type] / 2:
                raise TypeError(f"{obj} can not be serialized as {SerializationTypes.names[serialization_type]}")
            obj %= 256 ** SerializationTypes.size_dict[serialization_type]
            return bytes([serialization_type] + [(obj // (256 ** (SerializationTypes.size_dict[serialization_type] - i - 1))) % 256 for i in range(SerializationTypes.size_dict[serialization_type])])
        elif serialization_type in (SerializationTypes.FLOAT, SerializationTypes.DOUBLE):
            if not isinstance(obj, float|int):
                raise TypeError(f"{obj} is not a real number to be serialized as {SerializationTypes.names[serialization_type]}")
            if obj == 0:
                return bytes(SerializationTypes.size_dict[serialization_type])
            result = bytearray(SerializationTypes.size_dict[serialization_type] + 1)
            result[0] = serialization_type
            exp = 127
            sign = obj > 0
            obj = abs(obj)
            if abs(obj) >= 2:
                exp += int(abs(obj)).bit_length() - 1
                obj /= (2 ** (int(abs(obj)).bit_length() - 1))
            elif abs(obj) < 1:
                exp -= int(abs(1/obj)).bit_length()
                obj *= 2 ** int(abs(1/obj)).bit_length()
                
            if exp > 255 or exp < 0:
                raise ValueError(f"{obj} is too big or too small to be serialized... wtf are you doing?")
            result[1] = exp
            obj -= 1
            obj /= 2
            for i in range(1, SerializationTypes.size_dict[serialization_type]):
                result[i + 1] = int((obj * (256 ** i))) % 256
            result[2] = (128 * int(not sign)) + (result[2] % 128)
            return bytes(result)
        elif serialization_type == SerializationTypes.ARRAY_BEGIN:
            if not isinstance(obj, tuple|list|set):
                raise TypeError(f"{obj} is not a set nor tuple nor list to be serialized as {SerializationTypes.names[serialization_type]}")
            result = bytearray((serialization_type, args[0]))
            for inner in obj:
                result.extend(Serializator.encode_to(inner, args[0], args[1:])[1:])
            result.append(SerializationTypes.END)
            return result
        elif serialization_type == SerializationTypes.LIST_BEGIN:
            if not isinstance(obj, tuple|list|set):
                raise TypeError(f"{obj} is not a set nor tuple nor list to be serialized as {SerializationTypes.names[serialization_type]}")
            result = bytearray(serialization_type.to_bytes())
            for inner in obj:
                result.extend(Serializator.encode(inner))
            result.append(SerializationTypes.END)
            return result
        elif serialization_type == SerializationTypes.STRING_BEGIN:
            if not isinstance(obj, tuple|list|set|str):
                raise TypeError(f"{obj} is not a set nor tuple nor list to be serialized as {SerializationTypes.names[serialization_type]}")
            result = bytearray(serialization_type.to_bytes())
            if isinstance(obj, str):
                result.extend(obj.encode())
            else:
                for inner in obj:
                    result.extend(Serializator.encode_to(inner, SerializationTypes.S_CHAR)[1:])
            result.append(SerializationTypes.END)
            return result

    @staticmethod    
    def encode(obj: Any):
        if isinstance(obj, int):
            if obj > 0:
                if obj < 256:
                    return Serializator.encode_to(obj, SerializationTypes.S_CHAR)
                elif obj < 256**2:
                    return Serializator.encode_to(obj, SerializationTypes.S_SHORT)
                elif obj < 256**4:
                    return Serializator.encode_to(obj, SerializationTypes.S_INT)
                elif obj < 256**8:
                    return Serializator.encode_to(obj, SerializationTypes.S_LONG)
                else:
                    raise ValueError(f"{obj} is too big to be serialized... wtf are you doing?")
            else:
                if abs(obj) < 256**1 / 2:
                    return Serializator.encode_to(obj, SerializationTypes.CHAR)
                elif abs(obj) < 256**2 / 2:
                    return Serializator.encode_to(obj, SerializationTypes.SHORT)
                elif abs(obj) < 256**4 / 2:
                    return Serializator.encode_to(obj, SerializationTypes.INT)
                elif abs(obj) < 256**8 / 2:
                    return Serializator.encode_to(obj, SerializationTypes.LONG)
                else:
                    raise ValueError(f"{obj} is too big or too small to be serialized... wth are you doing?")
        if isinstance(obj, float):
            return Serializator.encode_to(obj, SerializationTypes.FLOAT)
        if isinstance(obj, tuple|list|set):
            return Serializator.encode_to(obj, SerializationTypes.LIST_BEGIN)
        if isinstance(obj, str):
            return Serializator.encode_to(obj, SerializationTypes.STRING_BEGIN)

    @staticmethod
    def decode(obj: bytes|bytearray):
        if int(obj[0]) in SerializationTypes.integer_types:
            result = 0
            for i in range(len(obj[1:])):
                print(len(obj[1:]) - i)
                result += int(obj[len(obj[1:]) - i]) * 256 ** i
            if not (int(obj[0]) in SerializationTypes.signed_types):
                if result >= 256 ** SerializationTypes.size_dict[int(obj[0])] / 2:
                    result -= 256 ** SerializationTypes.size_dict[int(obj[0])]
            return result
        if int(obj[0]) in (SerializationTypes.FLOAT, SerializationTypes.DOUBLE):
            exp = int(obj[1]) - 127
            
            sign = int(obj[2]) // 128
            result = 0

            for i in range(len(obj[2:])):
                result += int(obj[len(obj[2:]) - i + 1]) * 256 ** i
            
            if sign:
                result -= 256 ** (SerializationTypes.size_dict[int(obj[0])] - 1) / 2
                result *= -1
            result *= 2
            result /= 256 ** (SerializationTypes.size_dict[int(obj[0])] - 1)
            result += 1
            result *= 2 ** exp
            return result
        if int(obj[0]) in (SerializationTypes.ARRAY_BEGIN, SerializationTypes.LIST_BEGIN, SerializationTypes.STRING_BEGIN):
            result = []
            i = 1
            if int(obj[0]) == SerializationTypes.ARRAY_BEGIN:
                i += 1
            while obj[i] != SerializationTypes.END:
                if int(obj[0]) == SerializationTypes.LIST_BEGIN:
                    serialization_type = obj[i]
                    i += 1
                elif int(obj[0]) == SerializationTypes.ARRAY_BEGIN:
                    serialization_type = obj[1]
                elif int(obj[0]) == SerializationTypes.STRING_BEGIN:
                    serialization_type = SerializationTypes.S_CHAR
                
                if serialization_type in (SerializationTypes.ARRAY_BEGIN, SerializationTypes.LIST_BEGIN, SerializationTypes.STRING_BEGIN) :
                    result.append(Serializator.decode(serialization_type.to_bytes() + obj[i:]))
                    i = obj.find(0, i) + 1
                else:
                    result.append(Serializator.decode(serialization_type.to_bytes() + obj[i : i + SerializationTypes.size_dict[serialization_type]]))
                    i += SerializationTypes.size_dict[serialization_type]
                
            if int(obj[0]) == SerializationTypes.STRING_BEGIN:
                return bytes(result).decode()
            else:
                print(result)
                return result
class Connection:
    ipv4: str
    port: int
    conn: socket.socket
    
    def __init__(self, ipv4: str, port: int):
        self.ipv4 = ipv4
        self.port = port
x = Serializator.encode([1, 2, 3, 5.665, 228.007, "333", [34, 43, "abc"]])
print(x)
for i in x:
    print(str(int(i))+"\t"+binary(int(i)))

print(Serializator.decode(b'\x0c\x05\x01\x05\x02\x05\x03\t\x815G\xae\t\x86d\x01\xca\r333\x00\x0c\x05"\x05+\rabc\x00\x00\x00'))