from manim import *
import numpy as np
import random

# Cấu hình tỷ lệ màn hình 9:16 (Video dọc)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0   # Mở rộng chiều rộng khung hình logic để chứa vừa trục số dài
config.frame_height = 16.0 

class CombinedPhysicsScene(Scene):
    def construct(self):
        # ==========================================
        # PHẦN 1: KHỞI TẠO CÁC ĐỐI TƯỢNG HOẠT ẢNH CHIA MÀN HÌNH
        # ==========================================
        # 1. NỬA DƯỚI - KHỐI LẬP PHƯƠNG TRÊN DỐC
        theta = 40 * DEGREES
        ramp_length = 7.0  
        cube_side = 0.4    
        
        pivot = np.array([3.0, -7.0, 0])
        top_left = pivot + np.array([-ramp_length * np.cos(theta), ramp_length * np.sin(theta), 0])
        bottom_left = np.array([top_left[0], pivot[1], 0])
        
        triangle_ramp = Polygon(
            bottom_left, pivot, top_left, 
            color=WHITE, stroke_width=4, fill_color=GRAY, fill_opacity=0.3
        )
        
        cube = Square(side_length=cube_side, color=BLUE_D, fill_opacity=0.8)
        
        path_line = Line(top_left, pivot)
        normal_vector = np.array([np.sin(theta), np.cos(theta), 0])
        
        start_pos = path_line.point_from_proportion(0.1) + normal_vector * (cube_side / 2)
        end_pos = path_line.point_from_proportion(0.85) + normal_vector * (cube_side / 2)
        
        cube.move_to(start_pos)
        cube.rotate(-theta)

        # ==========================================
        # 2. NỬA TRÊN - BÓNG VÀ CHẤM TRÒN
        # ==========================================
        ball = Circle(radius=0.6, color=RED, fill_opacity=1)
        ball.set_stroke(color=WHITE, width=2)
        
        # Đặt quả bóng cố định ở chính giữa phần màn hình phía trên
        ball.move_to(UP * 4.0)

        dots = VGroup()
        num_dots = 60 
        random.seed(42)
        for _ in range(num_dots):
            x = random.uniform(-4.5, 4.5)
            y = random.uniform(0.2, 8.0) 
            dot = Dot(point=[x, y, 0], radius=random.uniform(0.03, 0.06), color=WHITE)
            dot.set_opacity(random.uniform(0.15, 0.5)) 
            dot.speed = random.uniform(4.0, 8.0) 
            dot.start_x = x 
            dot.start_y = y 
            dots.add(dot)

        # 3. GIAO DIỆN CHIA MÀN HÌNH (Y = 0)
        solid_line = Line(LEFT * 5.0, RIGHT * 5.0, color=WHITE, stroke_width=2)

        center_text = Text("Chuyển động thẳng", font="Times New Roman", font_size=42, color=WHITE)
        center_text.move_to(ORIGIN) 
        left_line = Line(LEFT * 5.0, center_text.get_left() + LEFT * 0.2, color=WHITE, stroke_width=2)
        right_line = Line(center_text.get_right() + RIGHT * 0.2, RIGHT * 5.0, color=WHITE, stroke_width=2)
        divider_group = VGroup(left_line, center_text, right_line)

        # ==========================================
        # PHẦN 2: CHẠY HOẠT ẢNH CHIA MÀN HÌNH (8 GIÂY)
        # ==========================================
        self.add(solid_line, triangle_ramp, cube, dots, ball) 
        
        alpha_tracker = ValueTracker(0)

        def update_cube(mob):
            alpha = alpha_tracker.get_value()
            eased_alpha = rate_functions.ease_in_quad(alpha) 
            current_pos = (1 - eased_alpha) * start_pos + eased_alpha * end_pos
            mob.move_to(current_pos)

        def update_dots(mob):
            alpha = alpha_tracker.get_value()
            time_elapsed = alpha * 8.0 
            
            for dot in mob:
                raw_y = dot.start_y + dot.speed * time_elapsed
                new_y = 0.1 + ((raw_y - 0.1) % 8.4)
                dot.move_to(np.array([dot.start_x, new_y, 0]))

        cube.add_updater(update_cube)
        dots.add_updater(update_dots) 

        # ---> ĐÃ SỬA: CHIA TIẾN TRÌNH THÀNH 3 GIAI ĐOẠN LIÊN TỤC KHÔNG KHỰNG
        
        # 1. Chạy 4.5 giây đầu
        self.play(alpha_tracker.animate.set_value(4.5 / 8.0), run_time=4.5, rate_func=linear)

        # 2. Đổi giao diện trong 0.5 giây ĐỒNG THỜI tiếp tục chạy alpha_tracker 
        self.play(
            alpha_tracker.animate.set_value(5.0 / 8.0), # Tiếp tục chạy thời gian
            FadeOut(solid_line), 
            FadeIn(divider_group), 
            run_time=0.5, 
            rate_func=linear
        )

        # 3. Chạy 3.0 giây cuối cùng
        self.play(alpha_tracker.animate.set_value(1.0), run_time=3.0, rate_func=linear)

        cube.remove_updater(update_cube)
        dots.remove_updater(update_dots)

        # ==========================================
        # PHẦN 3: VĂN BẢN CHUYỂN TIẾP
        # ==========================================
        self.play(
            FadeOut(triangle_ramp, shift=DOWN),
            FadeOut(cube, shift=DOWN),
            FadeOut(dots, shift=UP),
            FadeOut(ball, shift=UP),
            FadeOut(divider_group, scale=0.5),
            run_time=1.2
        )

        ending_text = Paragraph(
            "Xác định vị trí của vật",
            "trong không gian", 
            font="Times New Roman", 
            font_size=50, 
            color=WHITE,
            line_spacing=1.5,
            alignment="center"
        ).move_to(ORIGIN)
        
        self.play(Write(ending_text), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(ending_text, scale=1.2), run_time=1.0)
        self.wait(0.5)
        # ==========================================
        # PHẦN 4: VẼ TRỤC TOẠ ĐỘ Ox
        # ==========================================
        # Đưa "Trục Ox" lên cao (tọa độ Y = 6.5, gần sát mép trên)
        title = Text("Trục Ox", font="Arial").move_to(UP * 6.5)
        self.play(FadeIn(title, shift=DOWN))

        ox_axis = NumberLine(
            x_range=[-8.7, 8.7, 1],
            length=17,
            color=WHITE,
            numbers_to_exclude=[0]
        )
        ox_axis.add_numbers()
        
        x_label = Tex("$x$ (m)").next_to(ox_axis.n2p(8), UP, buff=0.3)

        origin_dot = Dot(ox_axis.n2p(0), color="#00FFFF", radius=0.1)
        o_label = MathTex("O").next_to(origin_dot, DOWN, buff=0.3)

        self.play(Create(ox_axis), Write(x_label), run_time=1.5)
        self.play(FadeIn(origin_dot, scale=0.5), Write(o_label))
        
        # -----------------------------------------------------
        # Mũi tên chỉ lên và nội dung x = 0
        # -----------------------------------------------------
        point_0 = ox_axis.n2p(0)
        
        arrow_0 = Arrow(
            start=point_0 + UP * 0.2, 
            end=point_0 + UP * 1.0, 
            color=YELLOW,
            buff=0
        )
        label_0 = MathTex("x = 0", color=YELLOW).next_to(arrow_0, UP, buff=0.2)

        self.play(GrowArrow(arrow_0), FadeIn(label_0, shift=DOWN))
        self.wait(1.5)
        
        self.play(FadeOut(arrow_0, shift=UP), FadeOut(label_0, shift=UP), run_time=0.5)
        # -----------------------------------------------------

        # Đặt dòng chữ ngay dưới tiêu đề "Trục Ox"
        infinite_label = Text("Kéo dài vô hạn về 2 phía", font="Arial", font_size=36, color=YELLOW).next_to(title, DOWN, buff=0.3)
        self.play(Write(infinite_label))
        self.wait(2)
        
        self.play(FadeOut(infinite_label, shift=UP), run_time=0.5)

        pos_start = ox_axis.n2p(0.8) + DOWN * 1.5
        pos_end = ox_axis.n2p(4.2) + DOWN * 1.5
        pos_arrow = Line(start=pos_start, end=pos_end, color="#77B077", stroke_width=6).add_tip()
        pos_text = Text("Chiều dương", font="Arial", font_size=30, color="#77B077").next_to(pos_arrow, DOWN)

        neg_start = ox_axis.n2p(-0.8) + DOWN * 1.5
        neg_end = ox_axis.n2p(-4.2) + DOWN * 1.5
        neg_arrow = Line(start=neg_start, end=neg_end, color="#E26D5A", stroke_width=6).add_tip()
        neg_text = Text("Chiều âm", font="Arial", font_size=30, color="#E26D5A").next_to(neg_arrow, DOWN)

        self.play(Create(pos_arrow), FadeIn(pos_text, shift=LEFT), run_time=1)
        self.wait(2)
        
        self.play(Create(neg_arrow), FadeIn(neg_text, shift=RIGHT), run_time=1)
        self.wait(2.1)

        moving_group = VGroup(
            ox_axis, x_label, origin_dot, o_label,
            pos_arrow, pos_text, neg_arrow, neg_text
        )
        
        self.play(moving_group.animate.shift(LEFT * 4), run_time=1.8)

        point_5 = ox_axis.n2p(5)  
        arrow_5 = Arrow(
            start=point_5 + UP * 1.0,   
            end=point_5 + UP * 0.2,     
            color=YELLOW,
            buff=0
        )
        label_5 = MathTex("x = 5", color=YELLOW).next_to(arrow_5, UP, buff=0.2)

        self.play(GrowArrow(arrow_5), FadeIn(label_5, shift=DOWN))
        self.wait(3)

        self.play(FadeOut(arrow_5, shift=UP), FadeOut(label_5, shift=UP), run_time=0.5)

        self.play(moving_group.animate.shift(RIGHT * 8), run_time=1.8)

        point_minus_5 = ox_axis.n2p(-5)  
        arrow_minus_5 = Arrow(
            start=point_minus_5 + UP * 1.0,   
            end=point_minus_5 + UP * 0.2,     
            color=YELLOW,
            buff=0
        )
        label_minus_5 = MathTex("x = -5", color=YELLOW).next_to(arrow_minus_5, UP, buff=0.2)

        self.play(GrowArrow(arrow_minus_5), FadeIn(label_minus_5, shift=DOWN))
        self.wait(3)

        self.play(
            FadeOut(title, shift=UP),
            FadeOut(moving_group, scale=0.8),
            FadeOut(arrow_minus_5, shift=UP),
            FadeOut(label_minus_5, shift=UP),
            run_time=1.2
        )
        self.wait(0.3)
        # ==========================================
        # PHẦN 5: HIỆU ỨNG CHUYỂN CẢNH "Vị trí (Vector)"
        # ==========================================
        text_vi_tri = Text("Vị trí", font="Times New Roman", font_size=65, color=WHITE)
        text_vector = Text("(Vector)", font="Times New Roman", font_size=55, color=WHITE).next_to(text_vi_tri, DOWN, buff=0.3)
        
        transition_group = VGroup(text_vi_tri, text_vector).move_to(ORIGIN)

        self.play(FadeIn(transition_group, scale=0.8), run_time=1.0)
        self.wait(0.5)

        self.play(transition_group.animate.shift(UP * 3), run_time=1.7)

        text_do_lon = Text("Độ lớn", font="Times New Roman", font_size=55, color=WHITE)
        text_huong = Text("Hướng", font="Times New Roman", font_size=55, color=WHITE)

        text_do_lon.next_to(transition_group, DOWN, buff=4).shift(LEFT * 2)
        text_huong.next_to(transition_group, DOWN, buff=4).shift(RIGHT * 2)

        arrow_color = "#FF7F50" 
        
        start_point_left = text_vector.get_bottom() + LEFT * 0.2 + DOWN * 0.2
        start_point_right = text_vector.get_bottom() + RIGHT * 0.2 + DOWN * 0.2

        arrow_left = Arrow(
            start=start_point_left, 
            end=text_do_lon.get_top() + UP * 0.2, 
            color=arrow_color, 
            stroke_width=6,
            buff=0.3
        )
        
        arrow_right = Arrow(
            start=start_point_right, 
            end=text_huong.get_top() + UP * 0.2, 
            color=arrow_color, 
            stroke_width=6,
            buff=0.3
        )

        self.play(
            Create(arrow_left),
            Create(arrow_right),
            run_time=0.7
        )
        self.play(
            FadeIn(text_do_lon, shift=UP * 0.5),
            FadeIn(text_huong, shift=UP * 0.5),
            run_time=0.7
        )

        self.wait(2.0)
        
        all_elements = VGroup(transition_group, arrow_left, arrow_right, text_do_lon, text_huong)
        self.play(FadeOut(all_elements, scale=1.5), run_time=1.0)
        self.wait(0.5)

        # ==========================================
        # PHẦN 6: TRỤC TỌA ĐỘ VÀ VECTOR VỊ TRÍ (TỪ CODE 2)
        # ==========================================
        # TRỤC TỌA ĐỘ TRÊN (TOP)
        axis_top = NumberLine(
            x_range=[0, 8.7, 1],
            length=8.5,
            color=WHITE,
            numbers_to_exclude=[0]
        ).shift(UP * 4)
        axis_top.add_numbers()
        
        x_label_top = MathTex(r"x \text{ (m)}").next_to(axis_top, UP, aligned_edge=RIGHT).shift(LEFT * 0.2)
        
        dot_O_top = Dot(axis_top.n2p(0), color=BLUE)
        label_O_top = MathTex("O").next_to(dot_O_top, DOWN)
        
        vec_green_start = axis_top.n2p(0)
        vec_green_end = axis_top.n2p(5)
        vec_green = Arrow(
            start=vec_green_start, 
            end=vec_green_end, 
            color=GREEN_C, 
            buff=0, 
            stroke_width=6, 
            max_tip_length_to_length_ratio=0.1
        )
        
        dot_5_top = Dot(axis_top.n2p(5), color=BLUE)
        
        point_5_top = axis_top.n2p(5)
        arrow_down_top = Arrow(
            start=point_5_top + UP * 1.0, 
            end=point_5_top + UP * 0.2, 
            color=YELLOW, 
            buff=0
        )
        
        text_green = MathTex(r"x = +5 \text{ m}", color=GREEN_C).next_to(arrow_down_top, UP)


        # TRỤC TỌA ĐỘ DƯỚI (BOTTOM)
        axis_bottom = NumberLine(
            x_range=[-8.7, 0, 1],
            length=8.5,
            color=WHITE,
            numbers_to_exclude=[0]
        ).shift(DOWN * 4)
        axis_bottom.add_numbers()

        x_label_bottom = MathTex(r"x \text{ (m)}").next_to(axis_bottom, UP, aligned_edge=LEFT).shift(RIGHT * 0.2)

        dot_O_bottom = Dot(axis_bottom.n2p(0), color=BLUE)
        label_O_bottom = MathTex("O").next_to(dot_O_bottom, DOWN)

        vec_red_start = axis_bottom.n2p(0)
        vec_red_end = axis_bottom.n2p(-5)
        vec_red = Arrow(
            start=vec_red_start, 
            end=vec_red_end, 
            color=RED_C, 
            buff=0, 
            stroke_width=6, 
            max_tip_length_to_length_ratio=0.1
        )

        dot_minus_5_bottom = Dot(axis_bottom.n2p(-5), color=BLUE)

        point_minus_5_bottom = axis_bottom.n2p(-5)
        arrow_down_bottom = Arrow(
            start=point_minus_5_bottom + UP * 1.0, 
            end=point_minus_5_bottom + UP * 0.2, 
            color=YELLOW, 
            buff=0
        )
        
        text_red = MathTex(r"x = -5 \text{ m}", color=RED_C).next_to(arrow_down_bottom, UP)


        # KỊCH BẢN CHẠY ANIMATION CHO PHẦN 6
        self.play(
            Create(axis_top), FadeIn(x_label_top), FadeIn(dot_O_top), FadeIn(label_O_top),
            Create(axis_bottom), FadeIn(x_label_bottom), FadeIn(dot_O_bottom), FadeIn(label_O_bottom),
            run_time=2
        )
        self.wait(0.5)

        self.play(
            GrowArrow(vec_green),
            GrowArrow(vec_red),
            run_time=2
        )
        
        # Gắn ngay các chấm xanh ở đầu vector
        self.add(dot_5_top, dot_minus_5_bottom)

        self.wait(0.7)

        # Mũi tên vàng và text xuất hiện
        self.play(
            GrowArrow(arrow_down_top), FadeIn(text_green),
            GrowArrow(arrow_down_bottom), FadeIn(text_red),
            run_time=1.5
        )
        
        self.wait(2)