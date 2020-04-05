# lora symbol processing



def generate_preamble_endpoints_lc(num_symbols: int, samp_per_sym: int) -> list:
    return [
        (start, stop)
        for start, stop in zip(
            range(0, num_symbols * samp_per_sym, samp_per_sym),
            range(samp_per_sym, num_symbols * samp_per_sym + samp_per_sym, samp_per_sym)
        )
    ]
