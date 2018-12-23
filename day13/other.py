from collections import namedtuple
from itertools   import chain, accumulate, repeat, cycle
from numpy       import array

flatten = chain.from_iterable

def tangent_map(tracks):
    maps = flatten(_tangent_map(j, t) for j, t in enumerate(tracks))
    return dict(maps)

def _tangent_map(j, track):
    return (((i, j), tmap[t]) for i, t in enumerate(track) if t in tmap)

def take_fork(vector, fork):
    f = next(fork)
    return f(vector), fork

identity = lambda *xs: xs

turn_corner_slash  = {'>':'^', '^':'>', '<':'v', 'v':'<'}
turn_corner_bslash = {'>':'v', '^':'<', '<':'^', 'v':'>'}

tmap = {'-' : identity,
        '|' : identity,
        '+' : take_fork,
        '/' : lambda v, f: (turn_corner_slash[v], f),
        '\\': lambda v, f: (turn_corner_bslash[v], f),
        '>' : identity,
        '^' : identity,
        '<' : identity,
        'v' : identity}


Cart = namedtuple('Cart', 'site, vector, fork')

def iterate(f, init):
    apply = lambda x, _: f(x)
    return accumulate(repeat(init), apply)

def ticker(tracks):
    "Make a function that advances carts along the tracks."
    tm = tangent_map(tracks)
    def move(cart):
        site = next_site(cart)
        vector, fork = tm[site](cart.vector, cart.fork)
        return Cart(site=site, vector=vector, fork=fork)
    def tick(carts):
        carts.sort(key=row_column)
        return [move(cart) for cart in carts]
    return tick

def row_column(cart):
    return cart.site[::-1]

def next_site(cart):
    return tuple(array(cart.site) + shift[cart.vector])

shift = {'>': array(( 1,  0)),
         '^': array(( 0, -1)),
         '<': array((-1,  0)),
         'v': array(( 0,  1))}

def first_crash(tracks):
    orbit = iterate(ticker(tracks), carts(tracks))
    sites = (crash_site(carts) for carts in orbit)
    return next(filter(bool, sites))

def crash_site(carts):
    sites = (c.site for c in carts)
    return first_duplicate(sites)

def first_duplicate(xs):
    seen = set()
    for x in xs:
        if x in seen: return x
        seen.add(x)
    return None

def carts(tracks):
    carts = flatten(carts_in_row(j, t) for j, t in enumerate(tracks))
    return list(carts)
    
def carts_in_row(j, track):
    return (Cart(site=(i, j), vector=v, fork=forks())
            for i, v in enumerate(track) if v in shift)

turn_left  = {'>':'^', '^':'<', '<':'v', 'v':'>'}
turn_right = {'>':'v', '^':'>', '<':'^', 'v':'<'}

go_left     = lambda v: turn_left[v]
go_right    = lambda v: turn_right[v]
go_straight = lambda v: v

forks = lambda: cycle((go_left, go_straight, go_right))

tracks_test = r'''
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
'''

with open('input.txt', 'r') as f:
    tracks = [line.rstrip() for line in list(f)]

first_crash(tracks)
print(first_crash(tracks))
