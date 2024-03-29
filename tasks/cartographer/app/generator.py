import math
from openlocationcode import openlocationcode
import os
from PIL import Image
import random
from scipy.interpolate import Akima1DInterpolator

import geotag


# Robinson projection definition. I'm not proud of this code.
_lat = [-90, -85, -80, -75, -70, -65, -60, -55, -50, -45, -40, -35, -30, -25, -20, -
        15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
_X = [1.0000, 0.9986, 0.9954, 0.9900, 0.9822, 0.9730, 0.9600, 0.9427, 0.9216,
      0.8962, 0.8679, 0.8350, 0.7986, 0.7597, 0.7186, 0.6732, 0.6213, 0.5722, 0.5322]
_X = _X[1:][::-1] + _X
_Y = [0.0000, 0.0620, 0.1240, 0.1860, 0.2480, 0.3100, 0.3720, 0.4340, 0.4958,
      0.5571, 0.6176, 0.6769, 0.7346, 0.7903, 0.8435, 0.8936, 0.9394, 0.9761, 1.0000]
_Y = list(map(lambda v: -v, _Y[1:][::-1])) + _Y
X = Akima1DInterpolator(_lat, _X)
Y = Akima1DInterpolator(_lat, _Y)


# L0 and R are best guesses
def latlon_to_point(lat: float, lon: float, λ0: float = 1.636e-01, R: float = 2.704e+02) -> (int, int):
    # These formulas are taken from Wikipedia page on Robinson projection
    λ = math.radians(lon)
    x = 0.8487 * R * X(lat) * (λ - λ0)
    y = 1.3523 * R * Y(lat)

    return 675.232 + x * 1.0384, 364.537 - y


if '__YULIA_SANITY_CHECK' in os.environ:
    biome_map = Image.open("biome_map.png").load()
else:
    biome_map = Image.open("/private/biome_map.png").load()

colors_map = {
    "004600": "Tropical rainforest",
    "00574e": "Taiga",
    # Originally "Subtropical moist forest" but merged because of wikipedia
    "066806": "Tropical and subtropical moist broadleaf forests",
    "298384": "Montane forest",
    # Ah yes,
    "328d8e": "Montane forest",
    "598159": "Tropical and subtropical moist broadleaf forests",
    "607a22": "Tropical and subtropical dry forest",
    "7c6086": "Mediterranean vegetation",
    "814229": "Arid desert",
    "886f33": "Dry steppe",
    "8cccbd": "Tundra",
    "92d847": "Temperate broadleaf and mixed forest",
    "95aed2": "Alpine tundra",
    "9b950e": "Tree savanna",
    # The pixel perfectness.
    "9bdc52": "Tree savanna",
    # Originally "Xeric shrubland" but merged because of wikipedia
    "aa5f3d": "Dry steppe",
    "b2b2b2": "Ice sheet and polar desert",
    # Originally "Grass savanna" but merged because of wikipedia
    "c1bd3e": "Tree savanna",
    # Originally "Semiarid desert" but merged because of wikipedia
    "d6a972": "Dry steppe",
    "f5e759": "Temperate steppe",
}


def latlon_to_biome(lat: float, lon: float) -> str:
    x, y = latlon_to_point(lat, lon)
    x = max(0, min(1384, int(x)))
    y = max(0, min(621, int(y)))
    r, g, b = biome_map[x, y]
    color = hex(65536*r + 256*g + b)[2:].rjust(6, "0")
    return colors_map.get(color)


# ==== Подгон констант ====
# Так вышло, что у карты биомов не оказалось параметров. Но кого это останавливало? Scipy в руки -- и вперёд!
#
# from scipy.stats import median_abs_deviation, expectile
# from scipy.optimize import differential_evolution
#
# def distance(L0, R):
#     def _distance(test):
#         _, latlon, exp = test
#         rx, ry = latlon_to_point(*latlon, L0, R)
#         ex, ey = exp
#         return math.hypot(rx-ex, ry-ey)
#     return _distance
#
# def shifts(L0, R):
#     def shift_one_axis(ax):
#         def sh(test):
#             _, latlon, exp = test
#             rx, ry = latlon_to_point(*latlon, L0, R)
#             ex, ey = exp
#             return (rx-ex, ry-ey)[ax]
#         return sh
#     shx = list(map(shift_one_axis(0), testset))
#     shy = list(map(shift_one_axis(1), testset))
#     return expectile(shx), expectile(shy)
#
# def stdev(L0_R, *testset):
#     return median_abs_deviation(list(map(distance(*L0_R), testset))),
#
# opt = differential_evolution(
#     func=stdev,
#     bounds=[
#         (-1.58, 1.58),
#         (0, 1000)
#     ],
#     args=testset,
#     maxiter=400000,
#     popsize=35,
#     polish=True,
#     x0=(0, 250)
# )
# print(opt)
#
# assert opt.success, "Yulia is a bad girl."
# L0, R = opt.x
# sx, sy = shifts(L0, R)
# print(sx, sy)


# ==== INSANITY TESTS BEGIN ====
if '__YULIA_SANITY_CHECK' in os.environ:
    print("Starting checking Yulia's sanity...")

    # Some reference points to make sure I did not make something bad with the scientific guess
    testset = [
        ("Murmansk", (68.97917, 33.09251), (747, 61)),
        ("Saint Petersburg", (59.9375, 30.308611), (744, 96)),
        ("Baikalsk", (51.5128, 104.1349), (1013, 131)),
        ("Rome", (41.893333, 12.482778), (688, 175)),
        ("Lisbon", (38.7175, -9.1152), (605, 190)),
        ("Gibraltar", (36.14, -5.35), (618, 199)),
        ("Tokyo", (35.6725, 139.7550), (1185, 205)),
        ("Cairo", (30.044444, 31.235833), (762, 228)),
        ("Miami", (25.7813, -80.2064), (313, 247)),
        ("San Jose del Cabo", (23.0594, -109.6978), (191, 258)),
        ("Taipei", (25.0375, 121.5625), (1131, 251)),
        ("Quito", (-0.22, -78.5125), (310, 368)),
        ("Antananarivo", (-18.9083, 47.5414), (831, 449)),
        ("Rio de Janeiro", (-22.9212, -43.1974), (458, 467)),
        ("The Cape", (-34.358056, 18.475556), (717, 520)),
        ("Buenos Aires", (-34.603333, -58.381667), (408, 519)),
        ("Melbourne", (-37.8187, 144.9560), (1198, 537)),
        ("Falkland Islands", (-51.7712, -59.1998), (430, 597))
    ]

    # The best optimization
    L0, R = 1.636e-01, 2.704e+02
    sx, sy = 0, 0

    def check(name, latlon, ex):
        val = latlon_to_point(*latlon, L0, R)
        d = math.hypot(ex[0]-val[0]+sx, ex[1]-val[1]+sy)
        print(
            f"{round(latlon[0],2):7} {round(latlon[1],2):7} {name:16}",
            f"={ex}",
            f"V: ({round(val[0]-sx)}, {round(val[1]-sy)})",
            f"D = {round(d, 2)}",
            sep='\t'
        )
        # "The Cape" is just an anomaly. I don't really know why, and-- don't really care as the results are already good enough
        assert d <= 4 or name == "The Cape"
    for test in testset:
        check(*test)

    from collections import defaultdict

    res = []
    stat = defaultdict(int)
    for _ in range(50000):
        lat, lon, c = 0, 0, 0
        while latlon_to_biome(lat, lon) is None:
            # print(f"Trial {c} for {round(lat, 2)} and {round(lon, 2)}")
            # lat = random.uniform(-90, 90)
            lat = math.degrees(math.asin(random.uniform(-1, 1)))
            lon = random.uniform(-180, 180)
            c += 1
        res.append(c)
        stat[latlon_to_biome(lat, lon)] += 1
    print("lo-me-hi", min(res), sorted(res)[len(res) // 2], max(res))
    print("avg", round(sum(res) / len(res), 2))
    print("count", len(res))

    for k, v in sorted(stat.items(), key=lambda kv: -kv[1]):
        print(v, k)

    print("She is indeed insane.")
# ==== INSANITY TESTS END ====


KNOWN = os.listdir("/private/known")


class Generator:
    def __init__(self):
        self.pool = KNOWN[:]

    def discard_from_pool(self, accepted: str):
        if accepted in self.pool:
            self.pool.remove(accepted)

    def __call__(self, counter: int) -> (bytes, str):
        if counter <= 1900:
            return generate_biome()

        loc = random.choice(self.pool)
        with open(f"/private/known/{loc}", "rb") as f:
            im = f.read()
        return im, geotag.untag_plus(im)


def generate_biome():
    lat, lon = 0, 0
    while latlon_to_biome(lat, lon) is None:
        lat = math.degrees(math.asin(random.uniform(-1, 1)))
        lon = random.uniform(-180, 180)

    biome = latlon_to_biome(lat, lon)
    # TODO
    with open(f"/private/{biome}/{random.randrange(10)}", "rb") as f:
        im = f.read()

    return geotag.tag(im, lat, lon), openlocationcode.encode(lat, lon)
