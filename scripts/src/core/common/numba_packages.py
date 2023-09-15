numba_jit_mode = True
try:
    import numba
except ModuleNotFoundError:
    numba = None
    numba_jit = None
    nb_list = None
    set_num_threads = None
else:
    def numba_jit(mode=True, *args, **kwargs):
        def identity(func):
            return func

        if mode:
            return numba.njit(debug=True, cache=True, *args, **kwargs)
        else:
            return identity
    from numba.typed import List as nb_list
    from numba import set_num_threads

