# constants



# -------------------------------------- static --------------------------------------

bw_values = {
    0: 0,
    1: 10.4e3,
    2: 15.6e3,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 125e3,
    8: 250e3,
    9: 500e3,
}

# TODO: find better name
packet_length_scalar = 30.25

# TODO: find better way to set these, maybe in a lorapy.set_constants('default' | 'benchtop') or something?
# inter-packet padding
# padding_length = 17_000
padding_length = 2200

# sampling frequency
# Fs = int(1e6)
Fs = int(20e3)

# number of preamble symbols
num_symbols = 8


