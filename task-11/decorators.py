def test(func):
    func._is_test = True
    return func


def skip(reason=""):
    def decorator(func):
        func._skip = True
        func._skip_reason = reason
        return func
    return decorator


def parametrize(arg_names, arg_values):
    def decorator(func):
        func._params = []
        names = [x.strip() for x in arg_names.split(",")]

        for vals in arg_values:
            param_dict = dict(zip(names, vals))
            func._params.append(param_dict)

        return func
    return decorator