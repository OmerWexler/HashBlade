import communication.MessageParser as mp


class MessageFormat:
    def __init__(self, mid: int, args_names: list):
        self.__mid = str(mid).zfill(2)
        self.__args_names = args_names
        self.__raw_format = self.__build_raw_format(self.__mid, args_names)


    def __build_raw_format(self, mid, args_names):
        sep = mp.MessageParser.seperator
        wrapped_args = []

        for arg in args_names:
            arg = '{' + arg + '}'
            wrapped_args.append(arg)
 
        raw_format = mid
        if len(wrapped_args) > 0:
            raw_format += sep + sep.join(wrapped_args)  
        
        return raw_format


    def get_mid(self):
        return self.__mid


    def get_args_names(self):
        return self.__args_names


    def get_raw_format(self):
        return self.__raw_format


    def build(self, args_values):
        msg = self.__raw_format.format(**args_values)
        msg = str(len(msg)).zfill(2) + msg
        return msg