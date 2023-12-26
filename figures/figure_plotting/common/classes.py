from .built_in_packages import enum
from .third_party_packages import np
from .config import float_type


class LineStyle(enum.Enum):
    normal = '-'
    dash = '--'
    dash_point = '-.'
    thin_dash = ':'

    def __str__(self):
        return self.value


class JoinStyle(enum.Enum):
    miter = 'miter'
    round = 'round'
    bevel = 'bevel'


class HorizontalAlignment(enum.Enum):
    center = 'center'
    right = 'right'
    left = 'left'


class VerticalAlignment(enum.Enum):
    center = 'center'
    top = 'top'
    bottom = 'bottom'
    baseline = 'baseline'
    center_baseline = 'center_baseline'


class FontStyle(enum.Enum):
    normal = 'normal'
    italic = 'italic'
    oblique = 'oblique'


class FontWeight(enum.Enum):
    ultralight = 'ultralight'
    light = 'light'
    normal = 'normal'
    regular = 'regular'
    book = 'book'
    medium = 'medium'
    roman = 'roman'
    semibold = 'semibold'
    demibold = 'demibold'
    demi = 'demi'
    bold = 'bold'
    heavy = 'heavy'
    extra_bold = 'extra bold'
    black = 'black'


class SubfigureLabelLoc(enum.Enum):
    upper_left = 'upper_left'
    bottom_left = 'bottom_left'
    upper_right = 'upper_right'
    bottom_right = 'bottom_right'


class Color(np.ndarray):
    @staticmethod
    def verify_alpha(input_alpha):
        if input_alpha is not None:
            assert 0 <= input_alpha <= 1
            alpha_set = True
        else:
            input_alpha = 1
            alpha_set = False
        return input_alpha, alpha_set

    def __new__(
            cls, r=None, g=None, b=None, a=None, *,
            array_255: np.ndarray = None, array_1: np.ndarray = None, text: str = None):
        alpha_set = False
        if not (r is None and g is None and b is None):
            if r is not None and g is not None and b is not None:
                if isinstance(r, int) or r > 1:
                    r /= 255
                if isinstance(g, int) or g > 1:
                    g /= 255
                if isinstance(b, int) or b > 1:
                    b /= 255
                a, alpha_set = cls.verify_alpha(a)
                obj = np.asarray([r, g, b, a], dtype=float_type).view(cls)
            else:
                raise ValueError('Please provide complete value of r, g and b')
        elif array_255 is not None or array_1 is not None:
            if array_255 is not None:
                raw_array = array_255
                ratio = 255
            else:
                raw_array = array_1
                ratio = 1
            assert isinstance(raw_array, np.ndarray) and len(raw_array.shape) == 1 \
                   and (len(raw_array) == 3 or len(raw_array) == 4)
            target_array = np.ones([4], dtype=float_type)
            if len(raw_array) == 3:
                rgb_raw_array = raw_array
            else:
                rgb_raw_array = raw_array[:3]
                # target_array[3] = raw_array[3]
                a, alpha_set = cls.verify_alpha(raw_array[3])
                target_array[3] = a
            target_array[:3] = rgb_raw_array / ratio
            obj = target_array.view(cls)
        elif text is not None:
            assert len(text) == 7 and text.startswith('#')
            r = int(text[1:3], 16)
            g = int(text[3:5], 16)
            b = int(text[5:7], 16)
            a, alpha_set = cls.verify_alpha(a)
            obj = np.asarray([r / 255, g / 255, b / 255, a], dtype=float_type).view(cls)
        else:
            raise TypeError('Initialization type not recognized!')
        obj.rgb_array = np.array(obj[:3])
        obj.alpha = obj[3]
        obj.alpha_set = alpha_set
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.rgb_array = getattr(obj, 'rgb_array', None)
        self.alpha = getattr(obj, 'alpha', None)
        self.alpha_set = getattr(obj, 'alpha_set', False)

    def __init__(
            self, r=None, g=None, b=None, a: float = 1, *,
            array_255: np.ndarray = None, array_1: np.ndarray = None, text: str = None):
        pass

    def is_valid(self):
        return np.all(self >= 0) and np.all(self <= 1)

    def transparency_mix(self, alpha, background=None):
        if background is None:
            background = white_color
        return Color(array_1=self * alpha + background * (1 - alpha))

    def solve_raw_color_from_mix(self, alpha, background=None):
        if background is None:
            background = white_color
        raw_color = Color(array_1=(self - background * (1 - alpha)) / alpha)
        assert raw_color.is_valid()
        return raw_color

    def add_transparency(self, alpha):
        new_color_array = np.zeros(4)
        new_color_array[:3] = self.rgb_array
        new_color_array[3] = alpha
        new_color = Color(array_1=new_color_array)
        new_color.alpha_set = True
        return new_color


black_color = Color(0.0, 0.0, 0.0)
white_color = Color(1.0, 1.0, 1.0)


class Vector(np.ndarray):
    def __new__(cls, x: float = None, y: float = None, *, array: np.ndarray = None, info=None):
        if x is not None and y is not None:
            obj = np.asarray([x, y], dtype=float_type).view(cls)
        elif array is not None:
            assert len(array.shape) == 1 and len(array) == 2
            obj = np.asarray(array, dtype=float_type).view(cls)
        else:
            raise TypeError('Initialization type not recognized! {}'.format(array))
        obj.info = info
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.info = getattr(obj, 'info', None)

    def __init__(self, x: float = None, y: float = None, *, array: np.ndarray = None, info=None):
        # super(Vector, self).__init__()
        pass

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def square_sum(self):
        return self[0] ** 2 + self[1] ** 2

    @property
    def length(self):
        return np.sqrt(self.square_sum)

    def unit_vector(self):
        vector_length = self.length
        return self / vector_length

    def vertical_vector(self):
        return Vector(-self[1], self[0])

    def vertical_vector_cw(self):
        return Vector(self[1], -self[0])

    def unit_vertical_vector(self):
        vector_length = self.length
        return Vector(-self[1] / vector_length, self[0] / vector_length)

    def rotate(self, sin, cos):
        new_x = cos * self.x - sin * self.y
        new_y = sin * self.x + cos * self.y
        return Vector(new_x, new_y)

    def to_tuple(self):
        return self[0], self[1]


class TransformDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, item):
        if super().__contains__(item):
            return super().__getitem__(item)
        else:
            return item


class LinearMapper(object):
    def __init__(self, input_min: float, input_max: float, output_min: float = 0, output_max: float = 1):
        self.input_min = input_min
        self.input_max = input_max
        self.input_diff = input_max - input_min
        self.output_min = output_min
        self.output_max = output_max
        self.output_diff = output_max - output_min

    def __call__(self, raw_value):
        if raw_value <= self.input_min:
            return self.output_min
        elif raw_value >= self.input_max:
            return self.output_max
        else:
            return (raw_value - self.input_min) / self.input_diff * self.output_diff + self.output_min


class SegmentedLinearMappers(object):
    def __init__(
            self, min_max_input_value_pair=None, absolute_value_output_dict=None,
            relative_ratio_output_value_dict=None, min_max_output_value_pair=(0, 1)):
        self.min_max_output_value_pair = min_max_output_value_pair
        self.min_max_input_value_pair = min_max_input_value_pair
        if absolute_value_output_dict is not None:
            self.absolute_value_output_dict = absolute_value_output_dict
        elif relative_ratio_output_value_dict is not None and min_max_input_value_pair is not None:
            mapper = LinearMapper(0, 1, *min_max_input_value_pair)
            absolute_value_output_dict = {
                mapper(relative_ratio): value
                for relative_ratio, value in relative_ratio_output_value_dict.items()
            }
            self.absolute_value_output_dict = absolute_value_output_dict
        else:
            raise ValueError('Absolute value dict and relative ratio value dict cannot be None simultaneously')
        self._construct_from_absolute_value_dict()

    def _construct_from_absolute_value_dict(self):
        constant_min_input_value = 0
        constant_max_input_value = 99999
        if self.min_max_input_value_pair is not None:
            min_input_value, max_input_value = self.min_max_input_value_pair
        else:
            min_input_value = None
            max_input_value = None
        if min_input_value is None:
            min_input_value = constant_min_input_value
        elif max_input_value is None:
            max_input_value = constant_max_input_value
        min_output_value, max_output_value = self.min_max_output_value_pair
        last_input_value = min_input_value
        last_output_value = min_output_value
        input_segment_list = []
        output_mapper_list = []
        for input_absolute_value, output_value in self.absolute_value_output_dict.items():
            input_segment_list.append(input_absolute_value)
            output_mapper_list.append(LinearMapper(
                last_input_value, input_absolute_value, last_output_value, output_value))
            last_input_value = input_absolute_value
            last_output_value = output_value
        input_segment_list.append(max_input_value)
        output_mapper_list.append(LinearMapper(
            last_input_value, max_input_value, last_output_value, max_output_value))
        self.input_segment_list = input_segment_list
        self.output_mapper_list = output_mapper_list

    def segment_linear_mapper_func(self, raw_input_value):
        for input_value_upper_bound, output_mapper in zip(self.input_segment_list, self.output_mapper_list):
            if raw_input_value <= input_value_upper_bound:
                return output_mapper(raw_input_value)
        raise ValueError(f'Cannot find appropriate conversion func: {raw_input_value}')
