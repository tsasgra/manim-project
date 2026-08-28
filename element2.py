from manim import *


class Position1D(Scene):
    def construct(self):

        # =========================================================
        # CÀI ĐẶT CHUNG
        # =========================================================
        self.camera.background_color = BLACK

        # Màu sắc
        AXIS_COLOR = GREY_B
        GREEN = "#86C67A"
        RED = "#FF806F"
        DOT_COLOR = "#48BCEB"
        BALL_COLOR = YELLOW

        # =========================================================
        # PHẦN 1: x = +5 m
        # =========================================================

        # Trục tọa độ phía trên
        axis_top = Line(
            LEFT * 5.2 + UP * 1.5,
            RIGHT * 5.2 + UP * 1.5,
            color=AXIS_COLOR,
            stroke_width=1.5
        )

        # Gốc O tại x = 0
        x0_top = LEFT * 4.8 + UP * 1.5

        # Khoảng cách giữa các đơn vị
        unit = 0.98

        # Các vạch chia
        ticks_top = VGroup()

        for i in range(9):
            x = x0_top + RIGHT * i * unit
            tick = Line(
                x + DOWN * 0.07,
                x + UP * 0.07,
                color=WHITE,
                stroke_width=1
            )
            ticks_top.add(tick)

        # Nhãn số 0 -> 8
        labels_top = VGroup()

        for i in range(9):
            x = x0_top + RIGHT * i * unit

            if i == 0:
                label = MathTex("O", color=WHITE).scale(0.65)
                label.next_to(x, DOWN, buff=0.18)
            else:
                label = MathTex(str(i), color=WHITE).scale(0.65)
                label.next_to(x, DOWN, buff=0.18)

            labels_top.add(label)

        # Nhãn x(m)
        x_label_top = MathTex("x\\;(\\mathrm{m})", color=WHITE).scale(0.7)
        x_label_top.move_to(RIGHT * 4.2 + UP * 1.88)

        # Vị trí ban đầu x = 0
        start_top = Dot(
            x0_top,
            radius=0.085,
            color=DOT_COLOR
        )

        # Vị trí cuối x = +5
        end_top = x0_top + RIGHT * 5 * unit

        end_dot_top = Dot(
            end_top,
            radius=0.085,
            color=DOT_COLOR
        )

        # Vật
        ball_top = Circle(
            radius=0.30,
            color=BALL_COLOR,
            fill_color=BALL_COLOR,
            fill_opacity=1,
            stroke_width=0
        )
        ball_top.move_to(start_top.get_center())

        # Mũi tên màu xanh
        arrow_top = Arrow(
            start_top.get_center(),
            end_top.get_center(),
            buff=0.05,
            color=GREEN,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.12
        )

        # Text x = +5 m
        displacement_top = MathTex(
            "x = +5\\;\\mathrm{m}",
            color=GREEN
        ).scale(0.72)

        displacement_top.move_to(
            (start_top.get_center() + end_top.get_center()) / 2
            + UP * 0.43
        )

        # =========================================================
        # PHẦN 2: x = -5 m
        # =========================================================

        # Trục tọa độ phía dưới
        axis_bottom = Line(
            LEFT * 5.2 + DOWN * 2.4,
            RIGHT * 5.2 + DOWN * 2.4,
            color=AXIS_COLOR,
            stroke_width=1.5
        )

        # Trong hình dưới, O nằm bên phải
        x0_bottom = RIGHT * 4.8 + DOWN * 2.4

        # Các vạch chia từ -8 đến 0
        ticks_bottom = VGroup()

        for i in range(9):
            x = x0_bottom + LEFT * i * unit

            tick = Line(
                x + DOWN * 0.07,
                x + UP * 0.07,
                color=WHITE,
                stroke_width=1
            )
            ticks_bottom.add(tick)

        # Nhãn -8 -> 0
        labels_bottom = VGroup()

        for i in range(9):
            value = -8 + i
            x = x0_bottom + RIGHT * i * unit

            # Đảo vị trí vì trục chạy từ -8 ở trái đến 0 ở phải
            x = x0_bottom + LEFT * (8 - i) * unit

            if value == 0:
                label = MathTex("O", color=WHITE).scale(0.65)
            else:
                label = MathTex(str(value), color=WHITE).scale(0.65)

            label.next_to(x, DOWN, buff=0.18)
            labels_bottom.add(label)

        # Nhãn x(m)
        x_label_bottom = MathTex(
            "x\\;(\\mathrm{m})",
            color=WHITE
        ).scale(0.7)

        x_label_bottom.move_to(
            LEFT * 4.2 + DOWN * 2.02
        )

        # Vị trí O
        start_bottom = Dot(
            x0_bottom,
            radius=0.085,
            color=DOT_COLOR
        )

        # Vị trí x = -5
        end_bottom = x0_bottom + LEFT * 5 * unit

        end_dot_bottom = Dot(
            end_bottom,
            radius=0.085,
            color=DOT_COLOR
        )

        # Vật
        ball_bottom = Circle(
            radius=0.30,
            color=BALL_COLOR,
            fill_color=BALL_COLOR,
            fill_opacity=1,
            stroke_width=0
        )

        ball_bottom.move_to(start_bottom.get_center())

        # Mũi tên màu đỏ
        arrow_bottom = Arrow(
            start_bottom.get_center(),
            end_bottom.get_center(),
            buff=0.05,
            color=RED,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.12
        )

        # Text x = -5 m
        displacement_bottom = MathTex(
            "x = -5\\;\\mathrm{m}",
            color=RED
        ).scale(0.72)

        displacement_bottom.move_to(
            (start_bottom.get_center() + end_bottom.get_center()) / 2
            + UP * 0.43
        )

        # =========================================================
        # HIỂN THỊ PHẦN TRÊN
        # =========================================================

        self.play(
            Create(axis_top),
            Create(ticks_top),
            Write(labels_top),
            Write(x_label_top),
            run_time=1.5
        )

        self.play(
            FadeIn(start_top),
            FadeIn(ball_top)
        )

        # Xuất hiện mũi tên
        self.play(
            GrowArrow(arrow_top),
            Write(displacement_top),
            run_time=1
        )

        # Cho vật chuyển động từ 0 -> +5
        self.play(
            ball_top.animate.move_to(end_top),
            run_time=2,
            rate_func=smooth
        )

        self.play(
            FadeIn(end_dot_top)
        )

        self.wait(1)

        # =========================================================
        # HIỂN THỊ PHẦN DƯỚI
        # =========================================================

        self.play(
            Create(axis_bottom),
            Create(ticks_bottom),
            Write(labels_bottom),
            Write(x_label_bottom),
            run_time=1.5
        )

        self.play(
            FadeIn(start_bottom),
            FadeIn(ball_bottom)
        )

        # Mũi tên sang trái
        self.play(
            GrowArrow(arrow_bottom),
            Write(displacement_bottom),
            run_time=1
        )

        # Cho vật chuyển động từ 0 -> -5
        self.play(
            ball_bottom.animate.move_to(end_bottom),
            run_time=2,
            rate_func=smooth
        )

        self.play(
            FadeIn(end_dot_bottom)
        )

        self.wait(2)