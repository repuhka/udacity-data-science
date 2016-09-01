import operator


def take_one(box, trffl):
    total_trffl = sum(box.values())
    prob = (0. + box[trffl])/total_trffl
    if box[trffl]:
        box[trffl] -=1
    return prob, box


def take_sq(box, sq):
    probs = []
    for trffl in sq:
        p, box = take_one(box, trffl)
        probs.append(p)
        return reduce(operator.mul, probs, 1)


if __name__ == '__main__':
    total_prb = 0
    for sq in ['CCOO', 'OCCO', 'OOCC', 'COOC', 'COCO', 'OCOC']:
        box = {'O':6, 'C':4}
        ps = take_sq(box, sq)
        print '- {}: {}'.format(sq, ps)
        total_prb += ps
        print 'Ends up with', total_prb