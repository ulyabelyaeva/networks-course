import socket


class CRC:
    def __init__(self):
        self.cdw = ''

    def xor(self,a,b):
        result = []
        for i in range(1,len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')
        return ''.join(result)


    def crc(self, message, key):
        size = len(key)

        tmp = message[:size]

        while size < len(message):
            if tmp[0] == '1':
                tmp = self.xor(key, tmp) + message[size]
            else:
                tmp = self.xor('0' * size, tmp) + message[size]

            size+=1

        if tmp[0] == "1":
            tmp = self.xor(key, tmp)
        else:
            tmp = self.xor('0' * size, tmp)

        checkword = tmp
        return checkword

    def encodeData(self, data, key):
        append_data = data + '0' * (len(key) - 1)
        remainder = self.crc(append_data, key)
        codeword = data + remainder
        self.cdw += codeword
        print("Remainder: ", remainder)
        print("Data: ", codeword)
        return codeword

    def reciverSide(self, key, data):
        checkword = self.crc(data, key)
        size = len(key) - 1
        print(checkword)
        if checkword == '0' * (len(data) - 1):
            print("Success")
            return True
        else:
            print("Error")
            return False


def test_success():
    c = CRC()

    data = '1001000'
    key = '1101'
    codeword = c.encodeData(data,key)
    print('---------------')
    success = c.reciverSide(codeword, data)
    print('---------------')
    print(c.cdw)

    assert success
    print('test_success passed')
    print('===============')


def test_error():
    c = CRC()

    data = '1001000'
    key = '1101'
    codeword = c.encodeData(data,key)
    print('---------------')
    data = '1001100'
    error = c.reciverSide(codeword, data)
    print('---------------')
    print(c.cdw)

    assert (not error)
    print('test_error passed')
    print('===============')


test_success()
test_error()
