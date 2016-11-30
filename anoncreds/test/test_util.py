from collections import OrderedDict

from anoncreds.protocol.globals import PAIRING_GROUP
from anoncreds.protocol.utils import get_hash, toDictWithStrValues, \
    deserializeFromStr, serializeToStr, fromDictWithStrValues
from anoncreds.test.conftest import primes
from config.config import cmod


def testStrSerializeToFromStr():
    value = 'aaa'
    assert value == deserializeFromStr(serializeToStr(value))


def testIntSerializeToFromStr():
    value = 111
    assert value == deserializeFromStr(serializeToStr(value))


def testCryptoIntSerializeToFromStr():
    value = cmod.integer(44444444444444444)
    assert value == deserializeFromStr(serializeToStr(value))


def testCryptoIntModSerializeToFromStr():
    value = cmod.integer(44444444444444444) % 33
    assert value == deserializeFromStr(serializeToStr(value))


def testGroupElementSerializeToFromStr():
    value = cmod.PairingGroup(PAIRING_GROUP).random(cmod.G1)
    assert value == deserializeFromStr(serializeToStr(value))


def testGroupElementZRIdentitySerializeToFromStr():
    elem = cmod.PairingGroup(PAIRING_GROUP).init(cmod.ZR, 555)
    identity = elem / elem
    assert identity == deserializeFromStr(serializeToStr(identity))

def testGroupElementG1IdentitySerializeToFromStr():
    elem = cmod.PairingGroup(PAIRING_GROUP).random(cmod.G1)
    identity = cmod.PairingGroup(PAIRING_GROUP).init(cmod.G1, elem / elem)
    assert identity == deserializeFromStr(serializeToStr(identity))


def testListStrSerializeToFromStr():
    value = ['aaa', 'bbb', 'ccc']
    assert value == deserializeFromStr(serializeToStr(value))


def testSetStrSerializeToFromStr():
    value = {'aaa', 'bbb', 'ccc'}
    assert value == deserializeFromStr(serializeToStr(value))


def testListIntSerializeToFromStr():
    value = [111, 222, 333]
    assert value == deserializeFromStr(serializeToStr(value))


def testSetIntSerializeToFromStr():
    value = {111, 222, 333}
    assert value == deserializeFromStr(serializeToStr(value))


def testListCryptoIntSerializeToFromStr():
    value = [cmod.integer(111) % 11, cmod.integer(222), cmod.integer(333) % 45]
    assert value == deserializeFromStr(serializeToStr(value))


def testListMixedSerializeToFromStr():
    group = cmod.PairingGroup(PAIRING_GROUP)
    value = ['aaa', 111,
             cmod.integer(111) % 11, cmod.integer(222),
             group.init(cmod.ZR, 555), group.random(cmod.G1)]
    assert value == deserializeFromStr(serializeToStr(value))


def testToFromDictWithStrValues():
    group = cmod.PairingGroup(PAIRING_GROUP)
    dict = OrderedDict((
        ('4', {'aaa', 'bbb'}),
        ('2', OrderedDict((
            ('33',
             OrderedDict((('45', 45), ('11', 11)))
             ),
            ('23',
             OrderedDict((('47', 47), ('34', 34)))
             )
        ))),
        ('1', {}),
        ('3', 3),
        ('5', cmod.integer(111) % 11),
        ('7', [cmod.integer(111) % 11, cmod.integer(222), cmod.integer(333) % 45]),
        ('6', [group.init(cmod.ZR, 555), group.random(cmod.G1), group.random(cmod.G1)]),
        ('10', group.random(cmod.G1))
    ))
    assert dict == fromDictWithStrValues(toDictWithStrValues(dict))


def testGetHashInt():
    input = [0xb1134a647eb818069c089e7694f63e6d,
             0x57fbf9dc8c8e6acde33de98c6d747b28c,
             0x77fbf9dc8c8e6acde33de98c6d747b28c]

    _checkHashEqual(input)


def testGetHashInteger():
    P_PRIME1, Q_PRIME1 = primes.get("prime1")
    P_PRIME2, Q_PRIME2 = primes.get("prime2")
    input = [P_PRIME1, Q_PRIME1, P_PRIME2, Q_PRIME2]

    _checkHashEqual(input)


def testGetHashGroup():
    group = cmod.PairingGroup(PAIRING_GROUP)
    input = [group.random(cmod.G1),
             group.random(cmod.G1),
             group.random(cmod.G1)]

    _checkHashEqual(input)


def testGetHashMixed():
    group = cmod.PairingGroup(PAIRING_GROUP)
    P_PRIME1, Q_PRIME1 = primes.get("prime1")
    input = [P_PRIME1, Q_PRIME1,
             group.random(cmod.G1), group.random(cmod.G1),
             0xb1134a647eb818069c089e7694f63e6d,
             0x57fbf9dc8c8e6acde33de98c6d747b28c]

    _checkHashEqual(input)


def _checkHashEqual(input):
    h1 = get_hash(*input)
    h2 = get_hash(*reversed(input))
    assert h1 == h2
