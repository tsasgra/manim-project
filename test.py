from manim import *

class ViTriVector(Scene):
    def construct(self):

        # =========================
        # 1. Tạo tiêu đề ở giữa màn hình
        # =========================

        title = Text(
            "Vị trí",
            font="Arial",
            font_size=48
        )

        vector_text = Text(
            "(Vector)",
            font="Arial",
            font_size=42
        ).next_to(title, DOWN, buff=0.3)

        # Gom "Vị trí" + "(Vector)"
        header = VGroup(title, vector_text)

        # Đặt chính giữa màn hình
        header.move_to(ORIGIN)

        # Xuất hiện ở giữa
        self.play(
            FadeIn(header, shift=UP),
            run_time=1
        )

        self.wait(0.5)

        # =========================
        # 2. Di chuyển lên trên
        # =========================

        self.play(
            header.animate.shift(2.3 * UP),
            run_time=1
        )

        # =========================
        # 3. Tạo hai mũi tên
        # =========================

        left_arrow = Arrow(
            start=header.get_bottom() + 0.05 * DOWN + 0.05 * LEFT,
            end=header.get_bottom() + 2.0 * DOWN + 1.5 * LEFT,
            color="#FF6F61",
            buff=0
        )

        right_arrow = Arrow(
            start=header.get_bottom() + 0.05 * DOWN + 0.05 * RIGHT,
            end=header.get_bottom() + 2.0 * DOWN + 1.5 * RIGHT,
            color="#FF6F61",
            buff=0
        )

        # =========================
        # 4. Hai nhãn
        # =========================

        magnitude = Text(
            "Độ lớn",
            font="Arial",
            font_size=40
        ).next_to(left_arrow.get_end(), DOWN, buff=0.1)

        direction = Text(
            "Hướng",
            font="Arial",
            font_size=40
        ).next_to(right_arrow.get_end(), DOWN, buff=0.1)

        # =========================
        # 5. Vẽ hai mũi tên
        # =========================

        self.play(
            GrowArrow(left_arrow),
            GrowArrow(right_arrow),
            run_time=0.8
        )

        # Xuất hiện chữ
        self.play(
            FadeIn(magnitude),
            FadeIn(direction),
            run_time=0.5
        )

        # =========================
        # 6. Giữ hình cuối 3 giây
        # =========================

        self.wait(3)