"""
VẬT LÝ CHILL - Xác định vị trí trên trục Ox (bản Short 9:16, ~1p30 - 2p)
==========================================================================

Video dọc (TikTok / YouTube Shorts / Reels) minh họa kịch bản gốc, có:

    1. Hook: câu hỏi mở đầu
    2. Hai ví dụ chuyển động thẳng: rơi tự do & trượt trên mặt phẳng nghiêng
       (khối vuông được XOAY NGHIÊNG theo đúng góc dốc để trượt mượt hơn)
    3. Trục tọa độ Ox: gốc O, chiều dương/âm, đơn vị mét
    4. Ba ví dụ vị trí: x = +5m, x = -5m, x = 0 (vật tại gốc)
    5. Vị trí là đại lượng VECTƠ: độ dài (độ lớn) + chiều (hướng)
    6. Hai ví dụ thực tế về chọn trục Ox: thang máy (thẳng đứng) & xe trượt
       dốc (mặt phẳng nghiêng)
    7. Tóm tắt + lời chào kết

Toàn bộ nội dung được canh giữa lại cho gọn trong khung 9:16 (không còn
văng ra sát mép trên/dưới).

Khung hình: 1080x1920 px (tỉ lệ 9:16, video dọc)
Thời lượng: ~100-120 giây (khoảng 1 phút 30 - 2 phút)

Render:
    manim -pqh vi_tri_full_short.py ViTriShortFull
    (dùng -pql thay -pqh để xem thử nhanh, chất lượng thấp)
"""

import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# CẤU HÌNH KHUNG HÌNH 9:16 (video dọc)
# ---------------------------------------------------------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30
config.frame_height = 16
config.frame_width = config.frame_height * config.pixel_width / config.pixel_height  # = 9

# ---------------------------------------------------------------------------
# FONT TIẾNG VIỆT
# ---------------------------------------------------------------------------
VIETNAMESE_FONT = "Be Vietnam Pro"


def vi_text(*args, **kwargs):
    """Wrapper quanh Text() của Manim, luôn dùng font hỗ trợ tiếng Việt."""
    kwargs.setdefault("font", VIETNAMESE_FONT)
    return Text(*args, **kwargs)


# ---------------------------------------------------------------------------
# Bảng màu
# ---------------------------------------------------------------------------
COLOR_AXIS = GREY_B
COLOR_POS = "#3DDC97"      # xanh lá - chiều dương
COLOR_NEG = "#FF6B6B"      # đỏ - chiều âm
COLOR_VECTOR = "#FFD93D"   # vàng - vectơ vị trí
COLOR_HIGHLIGHT = "#4D96FF"
COLOR_NEUTRAL = "#C9B6FF"  # tím nhạt - dùng cho ví dụ x = 0
BG_COLOR = "#111318"

# ---------------------------------------------------------------------------
# VÙNG BỐ CỤC (để mọi thứ được canh giữa, không văng ra sát mép khung 9:16)
# frame: rộng 9, cao 16  →  x: [-4.5, 4.5]   y: [-8, 8]
# ---------------------------------------------------------------------------
TITLE_Y = 6.6          # tiêu đề trên cùng
UPPER_Y = 4.6           # nội dung minh họa phía trên
CENTER_Y = 1.6          # trục / nội dung chính, gần giữa khung
NOTE_Y = -0.6           # ghi chú giải thích
LOWER_Y = -3.4          # ghi chú / tóm tắt phía dưới


def rotate_2d(vector, angle):
    """Xoay vector 2D (dạng np.array 3 phần tử) quanh gốc theo góc `angle` (rad)."""
    c, s = np.cos(angle), np.sin(angle)
    x, y, z = vector
    return np.array([c * x - s * y, s * x + c * y, z])


class ViTriShortFull(Scene):
    """Video dọc 9:16, khoảng 1 phút 30 - 2 phút."""

    def construct(self):
        self.camera.background_color = BG_COLOR

        # =====================================================================
        # 1) HOOK — câu hỏi mở đầu                                     (~6s)
        # =====================================================================
        question = vi_text(
            "Làm sao để xác định\nvị trí của một vật\ntrong chuyển động thẳng?",
            font_size=40,
            color=COLOR_HIGHLIGHT,
            weight=BOLD,
            line_spacing=1.25,
        ).move_to(UP * 1.0)
        self.play(Write(question), run_time=1.8)
        self.wait(2.6)
        self.play(FadeOut(question, shift=UP * 0.5), run_time=0.6)

        # =====================================================================
        # 2) VÍ DỤ MỞ ĐẦU — rơi tự do & trượt trên mặt phẳng nghiêng    (~18s)
        # =====================================================================

        examples_title = vi_text("Hai ví dụ quen thuộc", font_size=36, color=WHITE, weight=BOLD)
        examples_title.move_to(UP * TITLE_Y)
        self.play(FadeIn(examples_title, shift=DOWN * 0.3), run_time=0.7)

        # --- Rơi tự do (nửa trên khung hình) ---
        free_fall_label = vi_text("Rơi tự do", font_size=30, color=COLOR_POS)
        free_fall_label.move_to(UP * (UPPER_Y + 0.9))
        line1 = DashedLine(UP * (UPPER_Y + 0.2), UP * (CENTER_Y + 0.6), color=COLOR_AXIS)
        ball1 = Dot(radius=0.18, color=COLOR_POS).move_to(UP * (UPPER_Y))

        self.play(Write(free_fall_label), Create(line1), run_time=1.0)
        self.play(FadeIn(ball1), run_time=0.4)
        self.play(
            ball1.animate.move_to(UP * (CENTER_Y + 0.6)),
            run_time=1.6,
            rate_func=rate_functions.ease_in_quad,
        )
        self.wait(0.6)

        # --- Trượt trên mặt phẳng nghiêng (nửa dưới khung hình) ---
        incline_label = vi_text("Trượt trên mặt phẳng nghiêng", font_size=26, color=COLOR_NEG)
        incline_label.move_to(UP * (NOTE_Y + 1.4))
        incline = Line(
            LEFT * 2.2 + UP * (NOTE_Y + 0.8),
            RIGHT * 2.2 + DOWN * (1.0 - NOTE_Y),
            color=COLOR_AXIS,
        )

        # Khối vuông được XOAY theo đúng góc của mặt phẳng nghiêng, và trượt
        # dọc theo phương của dốc (thay vì đi chéo cứng nhắc như trước) để
        # chuyển động trông mượt và tự nhiên hơn.
        incline_angle = incline.get_angle()
        block = Square(side_length=0.35, color=COLOR_NEG, fill_opacity=1)
        block.rotate(incline_angle)
        normal_offset = rotate_2d(UP, incline_angle) * (block.side_length / 2)
        block.move_to(incline.get_start() + normal_offset)

        self.play(Write(incline_label), Create(incline), run_time=1.0)
        self.play(FadeIn(block), run_time=0.4)
        self.play(
            block.animate.move_to(incline.get_end() + normal_offset),
            run_time=1.6,
            rate_func=rate_functions.ease_in_quad,
        )
        self.wait(0.6)

        conclusion = vi_text(
            "Đều là ví dụ điển hình\ncủa CHUYỂN ĐỘNG THẲNG",
            font_size=28,
            color=COLOR_VECTOR,
            weight=BOLD,
            line_spacing=1.2,
        )
        conclusion.move_to(DOWN * (5.4))
        self.play(Write(conclusion), run_time=1.2)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # =====================================================================
        # 3) TRỤC Ox — gốc O, chiều dương/âm                           (~15s)
        # =====================================================================

        title = vi_text("Trục tọa độ Ox", font_size=44, color=WHITE, weight=BOLD)
        title.move_to(UP * TITLE_Y)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.6)

        axis = NumberLine(
            x_range=[-6, 6, 1],
            length=8,
            color=COLOR_AXIS,
            include_numbers=True,
            font_size=22,
        )
        axis.move_to(UP * CENTER_Y)
        self.play(Create(axis), run_time=1.4)

        origin_dot = Dot(axis.number_to_point(0), color=WHITE)
        origin_label = MathTex("O", color=WHITE, font_size=34)
        origin_label.next_to(origin_dot, UP, buff=0.2)
        self.play(FadeIn(origin_dot), Write(origin_label), run_time=0.7)
        self.wait(0.6)

        pos_arrow = Arrow(
            axis.number_to_point(0), axis.number_to_point(4),
            color=COLOR_POS, buff=0.15, stroke_width=6,
        )
        pos_text = vi_text("Chiều dương", font_size=28, color=COLOR_POS)
        pos_text.next_to(axis, DOWN, buff=0.5).shift(RIGHT * 1.6)

        neg_arrow = Arrow(
            axis.number_to_point(0), axis.number_to_point(-4),
            color=COLOR_NEG, buff=0.15, stroke_width=6,
        )
        neg_text = vi_text("Chiều âm", font_size=28, color=COLOR_NEG)
        neg_text.next_to(axis, DOWN, buff=0.5).shift(LEFT * 1.6)

        self.play(GrowArrow(pos_arrow), Write(pos_text), run_time=1.1)
        self.play(GrowArrow(neg_arrow), Write(neg_text), run_time=1.1)
        self.wait(2.6)
        self.play(
            FadeOut(pos_text), FadeOut(neg_text),
            FadeOut(pos_arrow), FadeOut(neg_arrow),
            run_time=0.6,
        )

        # =====================================================================
        # 4) BA VÍ DỤ VỊ TRÍ: x=+5m, x=-5m, x=0                        (~24s)
        # =====================================================================

        p5 = axis.number_to_point(5)
        vec5 = Arrow(axis.number_to_point(0), p5, color=COLOR_POS, buff=0, stroke_width=7)
        label5 = MathTex("x=+5m", color=COLOR_POS, font_size=32)
        label5.next_to(p5, UP, buff=0.35)
        self.play(GrowArrow(vec5), Write(label5), run_time=1.0)
        note5 = vi_text("Cách gốc O 5 mét,\nvề phía chiều dương", font_size=26, color=WHITE, line_spacing=1.2)
        note5.move_to(UP * NOTE_Y)
        self.play(Write(note5), run_time=1.1)
        self.wait(1.8)
        self.play(FadeOut(note5), run_time=0.4)


        p_neg5 = axis.number_to_point(-5)
        vec_neg5 = Arrow(axis.number_to_point(0), p_neg5, color=COLOR_NEG, buff=0, stroke_width=7)
        label_neg5 = MathTex("x=-5m", color=COLOR_NEG, font_size=32)
        label_neg5.next_to(p_neg5, UP, buff=0.35)
        self.play(GrowArrow(vec_neg5), Write(label_neg5), run_time=1.0)
        note_neg5 = vi_text("Cũng cách gốc O 5 mét,\nnhưng về phía chiều âm", font_size=26, color=WHITE, line_spacing=1.2)
        note_neg5.move_to(UP * NOTE_Y)
        self.play(Write(note_neg5), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(note_neg5), FadeOut(vec5), FadeOut(vec_neg5), FadeOut(label5), FadeOut(label_neg5), run_time=0.6)

        # --- Ví dụ đặc biệt: x = 0 (vật ngay tại gốc tọa độ) ---

        dot0 = Dot(axis.number_to_point(0), color=COLOR_NEUTRAL, radius=0.14)
        label0 = MathTex("x=0", color=COLOR_NEUTRAL, font_size=32)
        label0.next_to(axis.number_to_point(0), UP, buff=0.35)
        self.play(FadeIn(dot0, scale=1.5), Write(label0), run_time=0.9)
        note0 = vi_text(
            "Vật trùng với gốc tọa độ\n→ không có vectơ vị trí\n(vectơ có độ dài bằng 0)",
            font_size=25, color=COLOR_NEUTRAL, line_spacing=1.2,
        )
        note0.move_to(UP * NOTE_Y)
        self.play(Write(note0), run_time=1.2)
        self.wait(2.4)

        self.play(
            *[FadeOut(m) for m in (title, note0, label0, dot0, origin_dot, origin_label, axis)],
            run_time=0.7,
        )

        # =====================================================================
        # 5) VỊ TRÍ LÀ MỘT ĐẠI LƯỢNG VECTƠ                              (~19s)
        # =====================================================================

        title2 = vi_text("Vị trí là một VECTƠ", font_size=40, color=COLOR_VECTOR, weight=BOLD)
        title2.move_to(UP * TITLE_Y)
        self.play(Write(title2), run_time=1.2)

        axis2 = NumberLine(x_range=[-6, 6, 1], length=8, color=COLOR_AXIS, include_numbers=True, font_size=20)
        axis2.move_to(UP * (UPPER_Y - 0.6))
        origin_dot2 = Dot(axis2.number_to_point(0), color=WHITE)
        self.play(Create(axis2), FadeIn(origin_dot2), run_time=1.2)

        p5b = axis2.number_to_point(5)
        vec5b = Arrow(axis2.number_to_point(0), p5b, color=COLOR_VECTOR, buff=0, stroke_width=8)
        self.play(GrowArrow(vec5b), run_time=0.9)

        brace_len = Brace(vec5b, direction=UP, color=COLOR_VECTOR)
        len_text = vi_text("Độ dài = Độ lớn\ncủa vị trí", font_size=24, color=COLOR_VECTOR, line_spacing=1.15)
        len_text.next_to(brace_len, UP, buff=0.2)
        self.play(GrowFromCenter(brace_len), Write(len_text), run_time=1.4)
        self.wait(2.6)
        self.play(FadeOut(brace_len), FadeOut(len_text), run_time=0.5)

        dir_text = vi_text("Chiều = Dấu của vị trí\n(vật ở phía nào so với gốc)", font_size=24, color=COLOR_POS, line_spacing=1.15)
        dir_text.move_to(UP * NOTE_Y)
        self.play(Indicate(vec5b, color=COLOR_POS, scale_factor=1.15), Write(dir_text), run_time=1.4)
        self.wait(2.6)
        self.play(FadeOut(dir_text), run_time=0.4)

        summary = VGroup(
            vi_text("Chiều dương  →  dấu \"+\"", font_size=26, color=COLOR_POS),
            vi_text("Chiều âm  →  dấu \"-\"", font_size=26, color=COLOR_NEG),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        summary.move_to(DOWN * 2.6)
        self.play(Write(summary[0]), run_time=0.9)
        self.play(Write(summary[1]), run_time=0.9)
        self.wait(1.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        # =====================================================================
        # 6) VÍ DỤ THỰC TẾ — chọn trục Ox theo hướng chuyển động        (~22s)
        # =====================================================================

        title3 = vi_text("Chọn trục Ox phù hợp\nvới chuyển động thực tế", font_size=32, color=WHITE, weight=BOLD, line_spacing=1.2)
        title3.move_to(UP * (TITLE_Y - 0.4))
        self.play(Write(title3), run_time=1.2)

        # --- Ví dụ A: thang máy (chuyển động thẳng đứng) ---
        lift_label = vi_text("Ví dụ: thang máy đi lên", font_size=26, color=COLOR_POS)
        lift_label.move_to(UP * (UPPER_Y + 0.4))
        v_axis = Line(UP * (UPPER_Y - 0.1), UP * (CENTER_Y - 0.4), color=COLOR_AXIS, stroke_width=5)
        lift_box = Square(side_length=0.5, color=COLOR_POS, fill_opacity=1)
        lift_box.move_to(UP * (CENTER_Y - 0.2))
        self.play(Write(lift_label), Create(v_axis), run_time=1.0)
        self.play(FadeIn(lift_box), run_time=0.4)
        self.play(lift_box.animate.move_to(UP * (UPPER_Y - 0.2)), run_time=1.6, rate_func=rate_functions.ease_out_quad)

        note_lift = vi_text("Vật đi thẳng đứng\n→ đặt trục Ox thẳng đứng", font_size=22, color=COLOR_POS, line_spacing=1.15)
        note_lift.move_to(UP * NOTE_Y)
        self.play(Write(note_lift), run_time=1.0)
        self.wait(1.6)
        self.play(
            *[FadeOut(m) for m in (lift_label, v_axis, lift_box, note_lift)],
            run_time=0.6,
        )

        # --- Ví dụ B: xe trượt trên dốc (mặt phẳng nghiêng) ---

        slope_label = vi_text("Ví dụ: xe trượt xuống dốc", font_size=26, color=COLOR_NEG)
        slope_label.move_to(UP * (UPPER_Y + 0.4))
        slope_line = Line(
            UP * (UPPER_Y - 0.1) + LEFT * 1.8,
            UP * (CENTER_Y - 1.0) + RIGHT * 1.8,
            color=COLOR_AXIS,
            stroke_width=5,
        )

        # Xe cũng dùng khối vuông xoay theo đúng góc dốc để trượt mượt mà,
        # tự nhiên hơn thay vì chỉ là một chấm tròn di chuyển chéo.
        slope_angle = slope_line.get_angle()
        car = Square(side_length=0.32, color=COLOR_NEG, fill_opacity=1)
        car.rotate(slope_angle)
        car_offset = rotate_2d(UP, slope_angle) * (car.side_length / 2)
        car.move_to(slope_line.get_start() + car_offset)

        self.play(Write(slope_label), Create(slope_line), run_time=1.0)
        self.play(FadeIn(car), run_time=0.4)
        self.play(car.animate.move_to(slope_line.get_end() + car_offset), run_time=1.6, rate_func=rate_functions.ease_in_quad)
        note_slope = vi_text("Vật trượt theo phương nghiêng\n→ đặt trục Ox nghiêng theo dốc", font_size=22, color=COLOR_NEG, line_spacing=1.15)
        note_slope.move_to(UP * NOTE_Y)
        self.play(Write(note_slope), run_time=1.0)
        self.wait(1.6)

        take_away = vi_text(
            "Chọn trục phù hợp giúp\nphân tích chuyển động\nchính xác và dễ dàng hơn!",
            font_size=26, color=COLOR_VECTOR, weight=BOLD, line_spacing=1.2,
        )
        take_away.move_to(DOWN * 3.0)
        self.play(Write(take_away), run_time=1.2)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        # =====================================================================
        # 7) TÓM TẮT + OUTRO                                            (~14s)
        # =====================================================================

        recap_title = vi_text("Tóm lại...", font_size=40, color=COLOR_HIGHLIGHT, weight=BOLD)
        recap_title.move_to(UP * (TITLE_Y - 0.6))
        self.play(Write(recap_title), run_time=0.9)

        points = VGroup(
            vi_text("• Trục Ox: gốc O, chiều dương/âm", font_size=25),
            vi_text("• Vị trí x là một đại lượng vectơ", font_size=25),
            vi_text("  (có độ lớn và hướng)", font_size=25),
            vi_text("• Chọn trục Ox theo hướng", font_size=25),
            vi_text("  chuyển động thực tế", font_size=25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        points.next_to(recap_title, DOWN, buff=0.8)
        for p in points:
            self.play(Write(p), run_time=0.55)
        self.wait(1.6)

        self.play(FadeOut(points), FadeOut(recap_title), run_time=0.5)

        simple = vi_text("Rất là đơn giản\nđúng ko nào? 😄", font_size=36, color=WHITE, line_spacing=1.2)
        simple.move_to(UP * 1.0)
        self.play(Write(simple), run_time=1.3)
        self.wait(1.6)
        self.play(FadeOut(simple), run_time=0.4)

        bye = vi_text("Byeeeeeeee 👋", font_size=42, color=COLOR_HIGHLIGHT, weight=BOLD)
        sub = vi_text("Ủng hộ Vật Lý Chill & PiMA nhé!", font_size=24, color=COLOR_VECTOR)
        bye.move_to(UP * 1.0)
        sub.next_to(bye, DOWN, buff=0.5)
        self.play(Write(bye), run_time=1.1)
        self.play(Write(sub), run_time=1.1)
        self.wait(4.0)