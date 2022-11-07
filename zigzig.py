from math import floor


def _calc_dev(base_price, price):
    return 100 * (price - base_price) / base_price


def zigzag(highs, lows, depth=10, dev_threshold=5):
    def pivots(src_raw, length, isHigh):
        src = list(reversed(src_raw))
        bar_index = list(range(len(src)))
        for start in range(0, len(src)):
            if start + 2 * length + 1 > len(src) - 1:
                return
            p = 0
            if length < len(src) - start:
                p = src[start + length]
            if length == 0:
                yield 0, p
            else:
                isFound = True
                for i in range(start, start + length):
                    if isHigh and src[i] > p:
                        isFound = False
                    if not isHigh and src[i] < p:
                        isFound = False
                for i in range(start + length + 1, start + 2 * length + 1):
                    if isHigh and src[i] >= p:
                        isFound = False
                    c = not isHigh and src[i] <= p
                    if c:
                        isFound = False
                if isFound:
                    yield (bar_index[start + length], p)
                else:
                    yield None, None
    
    def pivotFound(dev, isHigh, price, isHighLast, pLast, dev_threshold, lineLast):
        if isHighLast == isHigh and lineLast:
            if (isHighLast==True and price > pLast) or (not isHighLast==True and price < pLast):
                return lineLast ,isHighLast, False
            else:
                return False, False, False
        else:
            if lineLast:
                return True ,isHigh, True
            else:
                if dev >= dev_threshold:
                    return True ,isHigh, True
                else:
                    return False,False, False

    data_highs = [x for x in pivots(highs, floor(depth / 2), True) if x[0]]
    data_lows = [x for x in pivots(lows, floor(depth / 2), False) if x[0]]
    data_highs.reverse()
    data_lows.reverse()
    raw_pairs = []
    isHighLast = False
    pLast = data_highs[0][-1]
    lineLast = False
    new_i = False
    for i, (ind, p) in enumerate(data_highs):
        lows_d = sorted([(ind_l, p_l) for ind_l, p_l in data_lows if ind >= ind_l], key=lambda x: x[0])
        if lows_d:
            lows = lows_d[-1]

            dev1 = abs(_calc_dev(pLast, p))
            id2, isHigh2, status = pivotFound(dev1, True, p, isHighLast, pLast, dev_threshold, lineLast)
            lineLast = id2
            isHighLast = isHigh2
            pLast = p
            #print(pLast, lows[1])
            #print(_calc_dev(pLast, p))
            dev2 = abs(_calc_dev(pLast, lows[1]))
            print(pLast)
            id1, isHigh1, status  = pivotFound(dev2, False, lows[-1], isHighLast, pLast, dev_threshold, lineLast)
            if status:
                if dev2 < dev_threshold:
                    if len(raw_pairs) > 1:
                        if abs(_calc_dev(raw_pairs[-1][1][1], p)) < dev_threshold:
                            if lows[1] < raw_pairs[-1][1][1] and not new_i:
                                ind2, p2 = raw_pairs[-1][0]
                                raw_pairs = raw_pairs[:-1]
                                raw_pairs.append(
                                    ((ind2, p2),
                                    lows)
                                )
                        else:
                            new_i = True
                        
                else:
                    
                    if len(raw_pairs) > 0 and ind > raw_pairs[-1][1][0]:
                        if lows[1] < raw_pairs[-1][1][1]:
                            highr = raw_pairs[-1][0]
                            raw_pairs.append(
                                (highr,
                                lows)
                            )
                    else:
                        new_i = False
                        raw_pairs.append(
                            ((ind, p),
                            (lows[0], lows[1]))
                        )
                        if len(raw_pairs) > 0:
                            if len(raw_pairs) == 1:
                                index1 = len(highs)
                            else:
                                index1 = raw_pairs[-2][1][0]
                            index2 = raw_pairs[-1][0][0]
                            
                            try:
                                highest_l = sorted([(ind_h, p_h) for ind_h, p_h in data_highs if index1 > ind_h and index2 < ind_h], key=lambda x: x[1])
                                highest_p = highest_l[-1]
                                if raw_pairs[-1][0][1] == 20329.9:
                                    print(index1, index2)
                                    print(highest_l)
                                #print(highest_p, raw_pairs[-1][0])
                                if highest_p[1] > raw_pairs[-1][0][1]:
                                    lowr = raw_pairs[-1][1]
                                    raw_pairs = raw_pairs[:-1]
                                    raw_pairs.append(
                                        (highest_p,
                                        lowr)
                                    )
                                #print("True")
                            except:
                                pass
            lineLast = id1
            isHighLast = isHigh1
            pLast = lows[-1]
            

    result = []
    try:
        lastp = raw_pairs[-1][1][0]
        print(raw_pairs)
        print(lastp)
        highest_l = sorted([(ind_h, p_h) for ind_h, p_h in data_highs if lastp > ind_h], key=lambda y: y[1])[-1]
        lowest_l = sorted([(ind_l, p_l) for ind_l, p_l in data_lows if lastp > ind_l], key=lambda x: x[1])[0]
        dev3 = abs(_calc_dev(highest_l[1], lowest_l[1]))
        if dev3 >= dev_threshold:
            raw_pairs.append(
                (highest_l,
                lowest_l)
            )
    except:
        pass
    for (i_h, p_h),(i_l, p_l) in raw_pairs:
        if not result:
            result.append(((i_h, p_h),(i_l, p_l)))
            continue

        if i_l == result[-1][1][0]:
            if p_h > result[-1][0][1]:
                result = result[:-1]
            else:
                continue

        result.append(((i_h, p_h),(i_l, p_l)))

    return result