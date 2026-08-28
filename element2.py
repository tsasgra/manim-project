from manim import *

class VectorPositionScene(Scene):
    def construct(self):
        # 1. Khởi tạo các đoạn text
        
        text_vi_tri = Text("Vị trí", font="Times New Roman", font_size=65, color=WHITE)
        text_vector = Text("(Vector)", font="Times New Roman", font_size=55, color=WHITE).next_to(text_vi_tri, DOWN, buff=0.3)
        
        text_do_lon = Text("Độ lớn", font="Times New Roman", font_size=55, color=WHITE)
        text_huong = Text("Hướng", font="Times New Roman", font_size=55, color=WHITE)

        # 2. Sắp xếp vị trí cho "Độ lớn" và "Hướng"
        text_do_lon.next_to(text_vector, DOWN, buff=2.5).shift(LEFT * 2)
        text_huong.next_to(text_vector, DOWN, buff=2.5).shift(RIGHT * 2)

        # 3. Tạo 2 mũi tên (Mã màu cam/hồng giống ảnh)
        arrow_color = "#FF8B66" 
        arrow_left = Arrow(start=text_vector.get_bottom(), end=text_do_lon.get_top(), color=arrow_color, buff=0.2)
        arrow_right = Arrow(start=text_vector.get_bottom(), end=text_huong.get_top(), color=arrow_color, buff=0.2)

        # 4. Gom tất cả vào 1 group và căn giữa
        transition_group = VGroup(
            text_vi_tri, text_vector, 
            arrow_left, arrow_right, 
            text_do_lon, text_huong
        ).move_to(ORIGIN)

        # 5. Hiệu ứng xuất hiện
        self.play(FadeIn(transition_group, scale=0.8), run_time=1.0)
        
        # 6. Chờ 3 giây
        self.wait(3.0)
        
        # 7. Hiệu ứng biến mất
        self.play(FadeOut(transition_group, scale=1.5), run_time=1.0)