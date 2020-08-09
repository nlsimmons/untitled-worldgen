# https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2003GB002108
# http://www.gardeningplaces.com/articles/nutrition-per-hectare1.htm
# http://www.hundredyearswar.com/Books/History/Agricult.htm
# https://worldbuilding.stackexchange.com/questions/157161/medieval-crop-yields
# http://www.fao.org/3/s2022e/s2022e06.htm

# Cereals   barley  Hordeum spp. Varieties include with husk and without (naked).
# maize Zea mays. Includes hybrid and ordinary maize (with widely different yields).
# millet    Echinocloa frumentacea , Eleusine coracana , Eragrostis abyssinica , Panicum miliaceum , Paspalum scrobiculatum , Pennisetum glaucum , Setaria italica. Small‐grained cereals that include a large number of different botanical species.
# rice  Oryza spp. Mainly oryza sativa. Rice grain after threshing and winnowing. Also known as rice in the husk and rough rice.
# rye   Secale cereale.
# sorghum   Sorghum spp. Includes hybrid and other varieties.
# wheat Triticum spp. (T. durum and T. aestivum ). Includes durum and common wheat, the latter includes the varieties: spring, winter, hard, soft, red, and white.
# other cerealsb    Includes: oats, buckwheat, quinoa, fonio, triticale, canary seed, mixed grains.
# Roots and tubers  cassava Manihot spp. Other names: manioc, mandioca, yucca, yucca dulce.
# potatoes  Solanum tuberosum.
# other root/tuberb Includes: sweet potatoes, yautia, taro, and yams.
# Sugar crops   sugar beets Beta vulgaris var. altissima.
# sugar cane    Saccharum officinarum.
# Pulses    pulses  Includes: dry beans, dry broad beans, dry peas, chick‐peas, dry cow peas, pigeon peas, lentils, bambara beans, vetches, and lupins.
# Nuts  nutsb   Includes: Brazil nuts, cashew nuts, chestnuts, almonds, walnuts, pistachios, kola nuts, hazelnuts (filberts), and areca nuts.
# Oil‐bearing crops groundnuts  Arachis hypogaea. Other name: peanuts.
# rapeseed  Brassica napus var. oleifera. Other name: Canola.
# oil palm fruit    Elaeis guineensis.
# soybeans  Glycine soja.
# sunflower Helianthus annuus.
# other oil‐bearing cropsb  Includes: coconuts, olives, karate nuts, castor beans, tung nuts, safflower, sesame, mustard, poppy seed, melon seed, linseed, hempseed, tallow tree seeds, kapok fruit, seed cotton.
# Vegetables    vegetablesb Includes: cabbage, artichokes, asparagus, lettuce, spinach, cassava leaves, tomatoes, cauliflower, pumpkins, cucumbers and gherkins, eggplants, chilies and peppers, onions, garlic, leeks and other alliaceous vegetables, green beans, green peas, green broad beans, string beans, carrots, okra, green corn, mushrooms, watermelons, and cantaloupes.
# Fruit fruitb  Includes: bananas, plantains, oranges, tangerines, mandarins, clementines, satsumas, lemons, limes, grapefruit, pomelo, apples, pears, quinces, apricots, sour cherries, peaches, nectarines, plums, stone fruit, strawberries, raspberries, gooseberries, currants, blueberries, cranberries, grapes, figs, persimmons, kiwi fruit, mangoes, avocadoes, pineapple, dates, cashew apple, and papayas.
# Fibers    cotton  Gossypium spp.
# other fibersb Includes: flax fiber and tow, hemp fiber and tow, kapok fiber, jute‐like fibers, ramie, sisal, abaca, manila hemp, and coir.
# Spices    spicesb Includes: pepper, pimento, vanilla, cinnamon (or canela), nutmeg, mace, cardamoms, cloves, anise, badian, fennel, and ginger.
# Other crops   other cropsb    Includes: tea, coffee, cocoa, mate, tobacco, natural rubber, chicory roots, carobs, hops, peppermint and spearmint, pyrethrum, Arabic gum, and other resins.


"""
BIOMES

zone            rainfall    wet period (mo) vegetation
desert          -100        0-1             little to none
arid            100-400     1-3             some scrubs, some grassland
semiarid        400-600     3-4             scrubs, bushes, grassland
sub-humid       600-1200    4-6             bushes, woodland, grassland
moist sub-humid 1200-1500   6-9             forest, woodland
humid           +1500       9-12            tropical rainforest

desert/arid - irrigation is required for any farming to occur
semiarid - sorghum and millet (drought resistant crops), unreliable yields without irrigation
sub-humid - irrigation only required during dry season, may be too rainy for sorghum/millet
humid - irrigation not required unless for rice

"""

"""
CROPS

desert - Hunters and gatherers, nomadic pastoralists, sedentary irrigators around oases, no rainfed agriculture.

hunter-gatherers
nomadic pastoralists
sedentism 0

arid - Extensive grazing (nomadic pastoralists),
    some millet and sorghum under flood irrigation in moist depressions.
millet - 1.4
sorghum - 2.1

nomadic pastoralists supplemented by some cultivation

avg 1.8 w/ irrigation, else 0

0 or 2
sedentism 1

semiarid, warm - Both nomadic pastoralists and cultivators.
    Mainly millet and sorghum, also short cycle cowpea, phaseolus beans and groundnuts. No fodder or sown pasture. In cooler parts maize.
millet - 1.4
sorghum - 2.1
cowpeas - 1.8
maize - 7.5

1.8 in warm

semiarid, cool
3.2 in cooler (capable of supporting maize)

2 or 4
sedentism 2

subhumid - Traditional nomadic pastoralists in dry season and drought years.
    Crops grown by settlers: millet, sorghum, maize, groundnuts;
    also cassava, cowpeas, cotton, sweet potatoes, tobacco, rainfed rice, soybean, mango, cashewnuts. Fodder and sown pasture possible.
millet - 1.4
sorghum - 2.1
maize - 7.5
groundnuts (peanuts) - 3.7

3.7

cassava - 7.9
cowpeas - 1.8
sweet potato - 4.6
rainfed rice - 0.9
soybean - 4.2
cashewnuts - 3.7
mango - 3.0

3.7

sedentism 2 in dry season, 3 otherwise

moist subhumid - Transition zone for agriculture: too wet for seasonal crops, too dry for tree crops.
    Tropics: maize, cassava; also yams, bananas, pineapple, sugarcane and rice.
    Winter rainfall areas and East African highlands: wheat and barley.
maize - 7.5
cassava - 7.9
yams - 4.9
banana - 4.4
pineapple - 2.5
sugarcane - 11.3
rice - 6.0
wheat - 4.4
barley - 4.0

5.9
sedentism 3

humid - Tree crops: oilpalm, rubber, cacao; shifting cultivation based on root crops (yams, cassava, etc.).
    Also some sorghum, maize, banana, sugarcane, rice. Some tropical hard woods.
cassava - 7.9
yams - 4.9
sorghum - 2.1
maize - 7.5
banana - 4.4
sugarcane - 11.3
rice - 6.0

6.3

sedentism 4

yearly kcal/acre (very rough estimate)

millet - 1.4
sorghum - 2.1
cowpea - 1.8
maize - 7.5
groundnuts (peanuts) - 3.7
cassava - 7.9
sweet potato - 4.6
rainfed rice - 0.9
soybean - 4.2
mango - 3.0
cashewnuts - 3.7
yams - 4.9
banana - 4.4
pineapple - 2.5
sugarcane - 11.3
rice - 6.0
wheat - 4.4
barley - 4.0
potato - 5.3

types of rice
Lowland, rainfed, which is drought prone, favors medium depth; waterlogged, submergence, and flood prone
Lowland, irrigated, grown in both the wet season and the dry season
Deep water or floating rice
Coastal wetland
Upland rice is also known as Ghaiya rice, well known for its drought tolerance[39]

tobacco
cotton -

One liter of wheat flour converted to kilogram equals to 0.53 kg

the average yield for the years 1350–1399 was 4.34 seeds produced for each seed sown for wheat, 4.01 for barley, and 2.87 for oats

wheat would yield 250 to 300 liters of grain per acre
125 - 150 kg/ac
100 net
3509 kcal
350,000 kcal/acre

Barley would bring 700-720 liters per acre
500 net
250 kg/ac * 3536 kcal/kg
800,000 kcal/ac




Oats yielded 360-400 liters

1.3mil kcal/acre

Peas 300-340 liters per acre
150 - 170 kg/ac
120 kg/ac net
803 kcal/kg
96360


One pound of flax seed will plant about 300-400 square feet

potatoes - plants less than 10 bushels per acre and get more than 200
5443 kg/acre at 763 kcal / kg
= 4 mil kcal/acre

Grain yields of slightly under four times seed grain sown were the norm until the 18th century.(So take your yield and divide by four of under)

the Medieval period was one of poor communications and strong traditions. The new techniques were not broadcast far and wide and, even if they were, most farmers would be reluctant to change their ancient (and reliable) methods


potatoes - ~850 cal / kg


NUTRITION (in million calories per acre per year) (people need 1 million per year)

This is modern numbers and will likely need adjustment
Wheat       6.4 (irrigated)
Corn        12.3 (irrigated)
Potatoes    17.8 (irrigated)
Soybeans    2.1 (irrigated)

"""


"""
LIVESTOCK

Chickens - everywhere
Buffalo - subhumid, moist subhumid, humid (where there is rice)
cows everywhere with grass
ducks are preferred in coastal regions
horses - steppe regions
goats - idk
pigs - idk
"""


"""
zone            rainfall(mm)    wet period (mo) vegetation
desert          -100            0-1             little to none
arid            100-400         1-3             some scrubs, some grassland
semiarid        400-600         3-4             scrubs, bushes, grassland
sub-humid       600-1200        4-6             bushes, woodland, grassland
moist sub-humid 1200-1500       6-9             forest, woodland
humid           +1500           9-12            tropical rainforest
"""

# https://en.wikipedia.org/wiki/Biome#/media/File:Vegetation.png
# Crops by biome and the number of people that can be fed per given unit land
BIOMES = {
    'desert': {
        'crops': {

        },
        'rainfall': {
            'avg_rainy_months': 0.5,
            'low': 0,
            'high': 100,
        },
        # 'temperature': '20-30',
        'vegetation': 'none',
    },
    'steppe': {
        'crops': [
            {'millet': 1.4},
            {'sorghum': 2.0},
        ],
        'average_nutrition': 1.7,
        'sedentism': 1,
        'temperature': '0-20',
        'rainfall': {
            'avg_rainy_months': 1.5,
            'low': 100,
            'high': 400,
        },
        'vegetation': 'grassland scrub',
    },
    'semiarid': {
        'crops': [
            {'millet': 1.4},
            {'sorghum': 2.1},
            {'cowpeas': 1.8},
            {'maize': 7.5},
        ],
        'average_nutrition': 2.5,
        'sedentism': 2,
        'temperature': '15-25',
        'rainfall': {
            'avg_rainy_months': 3.5,
            'low': 400,
            'high': 600,
        },
        'vegetation': 'scrub, bush, grassland'
    },
    'subhumid': {
        'crops': [
            {'millet': 1.4},
            {'sorghum': 2.1},
            {'maize': 7.5},
            {'peanuts': 3.7},
            {'cassava': 7.9},
            {'cowpeas': 1.8},
            {'sweet potato': 4.6},
            {'rainfed rice': 0.9},
            {'soybean': 4.2},
            {'cashewnuts': 3.7},
            {'mango': 3.0},
        ],
        'average_nutrition': 3.7,
        'temperature': '0-20',
        'sedentism': '2-3',
        'rainfall': {
            'avg_rainy_months': 5.0,
            'low': 600,
            'high': 1200,
        },
        'vegetation': 'bushes, woodland, grassland'
    },
    'tropical savanna': {
        'desc': 'wet summer, dry winter',
        'crops': [
            {'maize': 7.5},
            {'cassava': 7.9},
            {'yams': 4.9},
            {'banana': 4.4},
            {'pineapple': 2.5},
            {'sugarcane': 11.3},
            {'rice': 6.0},
            {'wheat': 4.4},
            {'barley': 4.0},
        ],
        'average_nutrition': 5.9,
        'sedentism': 3,
        'rainfall': {
            'avg_rainy_months': 7.5,
            'low': 1200,
            'high': 1500,
        },
        'vegetation': 'forest, woodland',
        'temperature': '20-30',
    },
    'tropical rainforest': {
        'crops': [
            {'cassava': 7.9},
            {'yams': 4.9},
            {'sorghum': 2.1},
            {'maize': 7.5},
            {'banana': 4.4},
            {'sugarcane': 11.3},
            {'rice': 6.0},
        ],
        'average_nutrition': 6.3,
        'sedentism': 4,
        'rainfall': {
            'avg_rainy_months': 10.5,
            'low': 1500,
            'high': 5000,
        },
        'vegetation': 'tropical rainforest',
        'temperature': '30'
    }
}
