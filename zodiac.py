import google.cloud.dataflow as df

zodiac = dict(
    Aries=((3, 21), (4, 19)),
    Taurus=((4, 20), (5, 20)),
    Gemini=((5, 21), (6, 20)),
    Cancer=((6, 21), (7, 22)),
    Leo=((7, 23), (8, 22)),
    Virgo=((8, 23), (9, 22)),
    Libro=((9, 23), (10, 22)),
    Scorpio=((10, 23), (11, 21)),
    Sagittarius=((11, 22), (12, 21)),
    Capricron=((12, 21), (1, 19)),
    Aquarius=((1, 20), (2, 18)),
    Pisces=((2, 19), (3, 20))
)


def get_zodiac_sign(line):
    name, day, month = line.split(',')

    d = int(day)
    m = int(month)

    for sign, (s, e) in zodiac.iteritems():
        # special case for Capricorn
        if (m == 12 and d >= 21) or (m == 1 and d <= 19):
            return 'Capricorn'

        if s[0] <= m <= e[0]:
            if (m == s[0] and d >= s[1]) or (m == e[0] and d <= e[1]):
                return sign
    return


p = df.Pipeline('DirectPipelineRunner')
(p
 | df.Read('load messages', df.io.TextFileSource('./player_birth_dates.csv'))
 | df.Map('get zodiac sign', get_zodiac_sign)
 | df.combiners.Count.PerElement('count signscount words -> count ')
 | df.Write('save', df.io.TextFileSink('./results')))
p.run()
