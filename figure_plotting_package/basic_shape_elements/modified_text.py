from .config import np, transforms, logging, mtext, martist, ParameterName, Color, Vector, black_color, \
    VerticalAlignment, HorizontalAlignment, FontStyle, FontWeight
from .config import initialize_vector_input, check_enum_obj, clip_angle_to_normal_range

from .basic_region import Region
from .shapes import Rectangle

Affine2D = transforms.Affine2D
Bbox = transforms.Bbox

_log = logging.getLogger(__name__)


# Modified from Axes.text in site-packages/matplotlib/axes/_axes.py
def ax_text(ax, x, y, s, width, height, fontdict=None, **kwargs):
    effective_kwargs = {
        'verticalalignment': 'baseline',
        'horizontalalignment': 'left',
        'transform': ax.transData,
        'clip_on': False,
        **(fontdict if fontdict is not None else {}),
        **kwargs,
    }
    # t = mtext.Text(x, y, text=s, **effective_kwargs)
    t = MyText(x, y, text=s, width=width, height=height, **effective_kwargs)
    t.set_clip_path(ax.patch)
    ax._add_text(t)
    return t


class MyText(mtext.Text):
    def __init__(self, *args, width: float = None, height: float = None, **kwargs):
        super().__init__(*args, **kwargs)
        assert width > 0
        assert height > 0
        self._width = width
        self._height = height
        self._x_padding = 0.1
        self._y_padding = 0.1
        self._text_rotation_trans = None

    def _get_layout(self, renderer):
        """
        Return the extent (bbox) of the text together with
        multiple-alignment information. Note that it returns an extent
        of a rotated text when necessary.
        """
        cached = True
        try:
            key = self._get_layout_cache_key(renderer=renderer)
            key = (*key, 'MyText')      # Make this key to distinct from built-in matplotlib Text class
            if key in self._cached:
                return self._cached[key]
        except AttributeError:
            cached = False

        thisx, thisy = 0.0, 0.0
        lines = self.get_text().split("\n")  # Ensures lines is not empty.

        # Figure is rendered from left to right, from bottom to top. Therefore,
        # x_offset < 0 requires xs > 0, and y_offset > 0 requires ys < 0.

        ws = []
        hs = []
        xs = []
        ys = []

        # Full vertical extent of font, including ascenders and descenders:
        _, lp_h, lp_d = renderer.get_text_width_height_descent(
            "lp", self._fontproperties,
            ismath="TeX" if self.get_usetex() else False)
        min_dy = (lp_h - lp_d) * self._linespacing
        baseline = 0

        for i, line in enumerate(lines):
            clean_line, ismath = self._preprocess_math(line)
            if clean_line:
                w, h, d = renderer.get_text_width_height_descent(
                    clean_line, self._fontproperties, ismath=ismath)
            else:
                w = h = d = 0

            # For multiline text, increase the line spacing when the text
            # net-height (excluding baseline) is larger than that of a "l"
            # (e.g., use of superscripts), which seems what TeX does.
            h = max(h, lp_h)
            d = max(d, lp_d)

            ws.append(w)
            hs.append(h)

            # Metrics of the last line that are needed later:
            baseline = (h - d) - thisy

            if i == 0:
                # position at baseline
                thisy = -(h - d)
            else:
                # put baseline a good distance from bottom of previous line
                thisy -= max(min_dy, (h - d) * self._linespacing)

            xs.append(thisx)  # == 0.
            ys.append(thisy)

            thisy -= d

        # Metrics of the last line that are needed later:
        descent = d

        # Bounding box definition:
        text_box_width = max(ws)

        # get the rotation matrix
        rotate_trans = Affine2D().rotate_deg(self.get_rotation())

        # now offset the individual text lines within the box
        malign = self._get_multialignment()
        if malign == 'left':
            line_offset_layout = [(x, y) for x, y in zip(xs, ys)]
        elif malign == 'center':
            line_offset_layout = [
                (x + text_box_width / 2 - w / 2, y) for x, y, w in zip(xs, ys, ws)]
        elif malign == 'right':
            line_offset_layout = [
                (x + text_box_width - w, y) for x, y, w in zip(xs, ys, ws)]
        else:
            raise ValueError()
        rot_line_offset_layout = rotate_trans.transform(line_offset_layout)

        # rot_xmin = corners_rotated[:, 0].min()
        # rot_xmax = corners_rotated[:, 0].max()
        # rot_ymin = corners_rotated[:, 1].min()
        # rot_ymax = corners_rotated[:, 1].max()

        # Now move the box to the target position offset the display
        # bbox by alignment
        halign = self._horizontalalignment
        valign = self._verticalalignment

        xmin = 0
        xmax = text_box_width
        ymax = 0
        ymin = ys[-1] - descent  # baseline of last line minus its descent

        if halign == HorizontalAlignment.center.value:
            offsetx = (xmin + xmax) / 2.0
        elif halign == HorizontalAlignment.right.value:
            offsetx = xmax
        elif halign == HorizontalAlignment.left.value:
            offsetx = xmin
        else:
            raise ValueError()

        if valign == VerticalAlignment.center.value:
            offsety = (ymin + ymax) / 2.0
        elif valign == VerticalAlignment.top.value:
            offsety = ymax
        elif valign == VerticalAlignment.baseline.value:
            offsety = ymax - baseline
        elif valign == VerticalAlignment.center_baseline.value:
            offsety = ymax - baseline / 2.0
        elif valign == VerticalAlignment.bottom.value:
            offsety = ymin
        else:
            raise ValueError()

        rot_offsetx, rot_offsety = rotate_trans.transform((offsetx, offsety))

        # rot_xmin -= offsetx
        # rot_ymin -= offsety

        # bbox = Bbox.from_bounds(rot_xmin, rot_ymin, rot_width, rot_height)
        bbox = None

        # now rotate the positions around the first (x, y) position
        xys = rot_line_offset_layout - (rot_offsetx, rot_offsety)
        # xys = rot_line_offset_layout

        ret = bbox, list(zip(lines, zip(ws, hs), *xys.T)), descent
        if cached:
            self._cached[key] = ret
        return ret

    @martist.allow_rasterization
    def draw(self, renderer):
        # docstring inherited

        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible():
            return
        if self.get_text() == '':
            return

        renderer.open_group('text', self.get_gid())

        with self._cm_set(text=self._get_wrapped_text()):
            bbox, info, descent = self._get_layout(renderer)
            trans = self.get_transform()

            # don't use self.get_position here, which refers to text
            # position in Text:
            posx = float(self.convert_xunits(self._x))
            posy = float(self.convert_yunits(self._y))

            ####################################################
            # Add width and height information into posx and posy
            width = self._width
            height = self._height
            halign = self._horizontalalignment
            valign = self._verticalalignment

            if halign == HorizontalAlignment.center.value:
                offsetx = 0
            elif halign == HorizontalAlignment.right.value:
                offsetx = width / 2
            elif halign == HorizontalAlignment.left.value:
                offsetx = -width / 2
            else:
                raise ValueError()

            if valign == VerticalAlignment.center.value or valign == VerticalAlignment.center_baseline.value:
                offsety = 0
            elif valign == VerticalAlignment.top.value:
                offsety = height / 2
            elif valign == VerticalAlignment.bottom.value or valign == VerticalAlignment.baseline.value:
                offsety = -height / 2
            else:
                raise ValueError()

            rotate_trans = Affine2D().rotate_deg(self.get_rotation())
            self._text_rotation_trans = rotate_trans
            rot_offsetx, rot_offsety = rotate_trans.transform((offsetx, offsety))

            posx += rot_offsetx
            posy += rot_offsety
            ####################################################

            posx, posy = trans.transform((posx, posy))
            if not np.isfinite(posx) or not np.isfinite(posy):
                _log.warning("posx and posy should be finite values")
                return
            canvasw, canvash = renderer.get_canvas_width_height()

            # Update the location and size of the bbox
            # (`.patches.FancyBboxPatch`), and draw it.
            if self._bbox_patch:
                self.update_bbox_position_size(renderer)
                self._bbox_patch.draw(renderer)

            gc = renderer.new_gc()
            gc.set_foreground(self.get_color())
            gc.set_alpha(self.get_alpha())
            gc.set_url(self._url)
            self._set_gc_clip(gc)

            angle = self.get_rotation()

            for line, wh, x, y in info:

                mtext = self if len(info) == 1 else None
                x = x + posx
                y = y + posy
                if renderer.flipy():
                    y = canvash - y
                clean_line, ismath = self._preprocess_math(line)

                if self.get_path_effects():
                    from matplotlib.patheffects import PathEffectRenderer
                    textrenderer = PathEffectRenderer(
                        self.get_path_effects(), renderer)
                else:
                    textrenderer = renderer

                if self.get_usetex():
                    textrenderer.draw_tex(gc, x, y, clean_line,
                                          self._fontproperties, angle,
                                          mtext=mtext)
                else:
                    textrenderer.draw_text(gc, x, y, clean_line,
                                           self._fontproperties, angle,
                                           ismath=ismath, mtext=mtext)

        gc.restore()
        renderer.close_group('text')
        self.stale = False


class TextBox(Region):
    def __init__(
            self, string: str, center: Vector, width: float, height: float,
            font: str = None, font_size: float = 1, font_color: Color = black_color, font_style=FontStyle.normal,
            font_weight=FontWeight.normal,
            horizontal_alignment=HorizontalAlignment.center, vertical_alignment=VerticalAlignment.center,
            line_space=1.2, angle=0, wrap=False, z_order=None, name=None, text_box=False, text_box_config=None,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1):
        self.string = string
        self.center = initialize_vector_input(center)
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.font_style = check_enum_obj(font_style, FontStyle)
        self.font_weight = check_enum_obj(font_weight, FontWeight)
        self.angle = angle
        self.horizontal_alignment = check_enum_obj(horizontal_alignment, HorizontalAlignment)
        self.vertical_alignment = check_enum_obj(vertical_alignment, VerticalAlignment)
        self.line_space = line_space
        self.wrap = wrap
        self.z_order = z_order
        self.text_box = None
        self.text_box_bool = text_box
        self.text_box_config = text_box_config

        self.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)

        size_vector = Vector(self.width, self.height)
        bottom_left = self.center - size_vector / 2
        if self.text_box_bool:
            if self.text_box_config is None:
                self.text_box_config = {}
            width, height, angle = clip_angle_to_normal_range(self.width, self.height, self.angle)
            text_box_config = {
                ParameterName.center: self.center,
                ParameterName.width: width,
                ParameterName.height: height,
                ParameterName.angle: angle,
                ParameterName.z_order: self.z_order,
                ParameterName.face_color: None,
                ParameterName.edge_width: 1,
                ParameterName.edge_color: black_color,
                **self.text_box_config
            }
            self.text_box = Rectangle(**text_box_config)
        super(TextBox, self).__init__(bottom_left, size_vector, name=name)

    def move_and_scale(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1):
        # if scale == 1 and bottom_left_offset is None:
        #     return
        super().move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)
        if self.text_box is not None:
            self.text_box.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)

    def add_to_mpl_axes(self, ax, transformation):
        if self.string == '' or self.string is None:
            return None
        text_obj = ax_text(
            ax, self.center.x, self.center.y, self.string, self.width, self.height,
            fontfamily=self.font, fontsize=self.font_size, color=self.font_color,
            fontstyle=self.font_style, fontweight=self.font_weight,
            horizontalalignment=self.horizontal_alignment, verticalalignment=self.vertical_alignment,
            linespacing=self.line_space, rotation=self.angle, rotation_mode='anchor', wrap=self.wrap,
            zorder=self.z_order, transform=transformation
        )
        return text_obj

    def draw(self, fig, parent_ax=None, parent_transformation=None):
        assert parent_ax is not None
        if self.text_box_bool:
            text_box_obj = self.text_box.draw(fig, parent_ax, parent_transformation)
        else:
            text_box_obj = None
        text_obj = self.add_to_mpl_axes(parent_ax, parent_transformation)
        return text_obj, text_box_obj


def draw_text(
        ax, center, string, width, height, font: str = None, font_size: float = 1,
        font_color: Color = black_color, font_style=FontStyle.normal, font_weight=FontWeight.normal,
        horizontal_alignment=HorizontalAlignment.center, vertical_alignment=VerticalAlignment.center,
        line_space=1.2, angle=0, wrap=True, z_order=None, transform=None):
    text_obj = ax_text(
        ax, center.x, center.y, string, width, height,
        fontfamily=font, fontsize=font_size, color=font_color,
        fontstyle=font_style.value, fontweight=font_weight.value,
        horizontalalignment=horizontal_alignment.value, verticalalignment=vertical_alignment.value,
        linespacing=line_space, rotation=angle, rotation_mode='anchor', wrap=wrap, zorder=z_order,
        transform=transform
    )
    return text_obj
