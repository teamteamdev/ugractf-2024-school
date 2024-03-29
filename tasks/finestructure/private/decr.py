open("D:\\Izobrahjenie.bmp", "wb").write(bytes((lambda a, b: a ^ b)(a, b) for a, b in zip(open("D:\\Zashifrovannye dannye.bin", "rb").read(), open("D:\\Klych shifrovania.bin", "rb").read())))
