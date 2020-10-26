class Utils:
    @staticmethod
    def scale(value, min_value, max_value, is_reverse=False, scale=1.0):
        if max_value == min_value:
            return 1.0
        
        scaled = scale * round((float(value - min_value))/(max_value - min_value), 5)

        if is_reverse: 
            return scale - scaled
        else:
            return scaled