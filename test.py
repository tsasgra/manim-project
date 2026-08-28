from manim import *

# Cấu hình khung hình 9:16 (Độ phân giải 1080x1920)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

class PhysicsVideo(Scene):
    def construct(self):
        # 1. Tải và hiển thị hình ảnh (Chữ trắng hoàn toàn theo ảnh mẫu)
        text_vi_tri = Text("Vị trí", font="Times New Roman", font_size=65, color=WHITE)
        text_vector = Text("(Vector)", font="Times New Roman", font_size=55, color=WHITE).next_to(text_vi_tri, DOWN, buff=0.3)
        
        transition_group = VGroup(text_vi_tri, text_vector).move_to(ORIGIN)

        self.play(FadeIn(transition_group, scale=0.8), run_time=1.0)
        self.wait(0.5)

        # 2. Di chuyển nội dung lên phía trên trong 3 giây
        self.play(transition_group.animate.shift(UP * 3), run_time=1.7)

        # 3. Tạo các Text "Độ lớn" và "Hướng"
        text_do_lon = Text("Độ lớn", font="Times New Roman", font_size=55, color=WHITE)
        text_huong = Text("Hướng", font="Times New Roman", font_size=55, color=WHITE)

        # Định vị trí cho hai text ở dưới, tủa ra hai bên
        text_do_lon.next_to(transition_group, DOWN, buff=4).shift(LEFT * 2)
        text_huong.next_to(transition_group, DOWN, buff=4).shift(RIGHT * 2)

        # 4. Vẽ mũi tên với màu cam/đỏ nhạt giống ảnh gốc
        arrow_color = "#FF7F50" # Màu Coral tương đồng với ảnh
        
        # Lấy tọa độ mép dưới của chữ (Vector) để làm điểm bắt đầu mũi tên
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

        # 5. Hiệu ứng hiển thị mũi tên và chữ
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
        
        # 6. FadeOut tất cả cùng lúc
        all_elements = VGroup(transition_group, arrow_left, arrow_right, text_do_lon, text_huong)
        self.play(FadeOut(all_elements, scale=1.5), run_time=1.0)