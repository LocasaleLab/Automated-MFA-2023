import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
from matplotlib.path import Path
import matplotlib.patches as patches


def convert_operation_to_str(path_operation, point_list):
    command_name_dict = {
        Path.MOVETO: 'PathOperation.moveto',
        Path.LINETO: 'PathOperation.lineto',
        Path.CURVE3: 'PathOperation.curve3',
        Path.CURVE4: 'PathOperation.curve4',
        Path.CLOSEPOLY: 'PathOperation.closepoly'
    }
    path_step_format_str = '    PathStep({path}{point_list}),'
    vector_format_str = 'Vector({}, {})'
    path_str = command_name_dict[path_operation]
    if path_operation == Path.CLOSEPOLY:
        point_list_str = ''
    else:
        point_list_str = ', {}'.format(
            ', '.join([
                vector_format_str.format(*point) for point in point_list
            ])
        )
    return path_step_format_str.format(path=path_str, point_list=point_list_str)


def svg_parse(path, width, height, trans=None, x_lim=None, y_lim=None, x_offset=0, y_offset=0):
    def bound_generator():
        x_lb = -np.inf
        x_ub = np.inf
        if x_lim is not None:
            tmp_lb, tmp_ub = x_lim
            if tmp_lb is not None:
                x_lb = tmp_lb
            if tmp_ub is not None:
                x_ub = tmp_ub
        y_lb = -np.inf
        y_ub = np.inf
        if y_lim is not None:
            tmp_lb, tmp_ub = y_lim
            if tmp_lb is not None:
                y_lb = tmp_lb
            if tmp_ub is not None:
                y_ub = tmp_ub
        lb = np.array([x_lb, y_lb])
        ub = np.array([x_ub, y_ub])
        return lb, ub

    # TODO: implement 'a' and 'A'
    commands = {'M': (Path.MOVETO,),
                'L': (Path.LINETO,),
                'Q': (Path.CURVE3,)*2,
                'C': (Path.CURVE4,)*3,
                'Z': (Path.CLOSEPOLY,)}
    lower_bound, upper_bound = bound_generator()
    vertices = []
    codes = []
    cmd_values = re.split("([A-Za-z])", path.strip())[1:]  # Split over commands.
    last_point = np.array([0, 0])
    for cmd, values in zip(cmd_values[::2], cmd_values[1::2]):
        # Numbers are separated either by commas, or by +/- signs (but not at
        # the beginning of the string).
        points = (
            [*map(float, re.split(" |,", values.strip()))] if values else [(0., 0.)])  # Only for "z/Z" (CLOSEPOLY).
        if cmd in {'a', 'A'}:
            raise ValueError()
        points = np.reshape(points, (-1, 2))
        if cmd != 'm' and cmd.islower() and cmd != 'z':
            points += vertices[-1][-1]
        if trans is not None:
            points = trans.transform(points)
        points = points * np.array([1, -1]) + np.array([0, height])
        points /= width
        points += np.array([x_offset, y_offset])

        points_num = points.shape[0]
        this_command_list = commands[cmd.upper()]
        this_command = this_command_list[0]
        this_command_len = len(this_command_list)
        if points_num % this_command_len != 0:
            raise ValueError()
        code_repeat_num = points_num // this_command_len
        if this_command == Path.CLOSEPOLY:
            print(convert_operation_to_str(this_command, None))
            print()
            codes.append(this_command)
            vertices.extend(points)
        else:
            for repeat_index in range(code_repeat_num):
                point_array = points[repeat_index * this_command_len:(repeat_index + 1) * this_command_len, :]
                if np.all(np.all(np.logical_and(point_array > lower_bound, point_array < upper_bound), axis=1)):
                    if len(codes) == 0 and this_command != Path.MOVETO:
                        codes.append(Path.MOVETO)
                        vertices.append(last_point)
                        print(convert_operation_to_str(Path.MOVETO, [last_point]))
                    print(convert_operation_to_str(this_command, point_array))
                    codes.extend(this_command_list)
                    vertices.extend(point_array)
            last_point = points[-1]
    return np.array(codes), np.array(vertices)


def transform_matrix_parse(transform_matrix_str):
    values = [*map(float, transform_matrix_str.split(" "))]
    if len(values) != 6:
        raise ValueError()
    matrix_array = np.reshape(values, [3, 2]).transpose()
    matrix_array = np.vstack([matrix_array, [0, 0, 1]])
    current_trans = transforms.Affine2D(matrix=matrix_array)
    return current_trans


def parse_func(path_dict, size_array, transform_dict, x_lim=None, y_lim=None, x_offset=0, y_offset=0):
    height_to_width = size_array[1] / size_array[0]
    print(f'Height to width: {height_to_width}')

    fig = plt.figure(figsize=(5, 5), facecolor="0.9")  # gray background
    ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1,
                      xlim=(0, 1),  # centering
                      ylim=(0, 1),  # centering, upside down
                      xticks=[], yticks=[])  # no ticks
    ax.axhline(2.3)

    for name, path_str_list in path_dict.items():
        if transform_dict is not None and name in transform_dict:
            transform_matrix_str = transform_dict[name]
            current_trans = transform_matrix_parse(transform_matrix_str)
        else:
            current_trans = None
        print(f"'{name}': {{ParameterName.path_step_list: [")
        for path_str in path_str_list:
            # SVG to Matplotlib
            codes, verts = svg_parse(
                path_str, size_array[0], size_array[1], current_trans, x_lim, y_lim, x_offset, y_offset)
            path = Path(verts, codes)

            ax.add_patch(patches.PathPatch(path, fill=False, edgecolor='k', lw=1))
        print("]},\n")

    plt.show()  # Display


def main():
    from svg_path_content import content_loader
    size_array, path_dict, transform_dict, bounds = content_loader()
    offsets = []
    parse_func(path_dict, size_array, transform_dict, *bounds, *offsets)


if __name__ == '__main__':
    main()
