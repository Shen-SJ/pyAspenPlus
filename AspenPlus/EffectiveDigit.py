def Efdi(mynum, effdi):
    """Get the number at specified effective digit.

    :param mynum: the number you want to be operated.
    :param effdi: the number of effective digit you want on the number.
    :return: String.
    """
    ## 確認mynum資料型態
    if (type(mynum) is not int) and (type(mynum) is not float):
        raise TypeError("mynum must be a 'Number'!!!")
    if type(effdi) is not int:
        raise TypeError("effdi must be a 'Integer'!!!")

    if mynum < 1 and str(mynum).find('0.99') != -1:
        mynew = ""
        index = 0
        for s in str(mynum):
            mynew += s
            index += 1
            if index - 2 == effdi:
                break
        return mynew

    S = "{:." + str(effdi) + "f}"
    return S.format(mynum)

# Test.
if __name__ == "__main__":
    #####我的原始資料
    temp = 316.54132
    pres = 2.253412365
    mol = 239.0122
    x = 1

    print(Efdi(0.2367891,2))
    print(Efdi(1,2))
    print(Efdi(0.2,4))
    print(Efdi(0.99999999,4))
