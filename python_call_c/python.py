from ctypes import *


if __name__ == "__main__":
	ll = CDLL("/root/libtest.so")
	string = "hello!!!"
	c = create_string_buffer(len(string))
	c.value = string.encode(encoding="utf-8")
	ll.test(c)
