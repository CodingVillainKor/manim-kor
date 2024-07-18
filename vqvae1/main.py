from manim import *
from manimdef import DefaultManimClass
from manimdef.nn import MLP, forward_prop, Tensor
from model import get_model, get_data

model = get_model()
data = get_data()
x_hat, _ = model(data)
c_hat = model.get_code(data).cpu().detach()
e_hat = model.get_emb(data).cpu().detach()
ce_hat = model.get_code_emb(data).cpu().detach()
codebook = model.get_codebook()
cb = codebook.cpu().detach().numpy()

def to_3d(v):
    return np.concatenate([v, np.zeros([1])])

class VQVAE(DefaultManimClass):
    def construct(self):
        nump = NumberPlane((-4.11111, 4.11111, 0.5), (-3.5, 3.5, 0.5)).set_opacity(0.5).scale(0.4).shift(RIGHT*3+DOWN)
        dots = []
        for i in range(7):
            for j in range(7):
                dots.append(Dot(nump.c2p(*e_hat[0, i, j].cpu().detach().numpy()), radius=DEFAULT_DOT_RADIUS*0.5, stroke_width=1, stroke_color=BLACK))
        
        mnist = []
        for i in range(0, 28, 4):
            row = []
            for j in range(0, 28, 4):
                d = data[0, 0, i:i+4, j:j+4].cpu().numpy()
                patch = get_4x4_pixel(d)
                row.append(patch)
            row = VGroup(*row).arrange(RIGHT, buff=0.05)
            mnist.append(row)
        mnist = VGroup(*mnist).arrange(DOWN, buff=0.05)

        dots = VGroup(*dots)
        self.playw(FadeIn(mnist))
        self.playw(mnist.animate.shift(LEFT*4).scale(0.6))

        encoder = MLP(16, 7, 2).rotate(-PI/2).scale(0.7).shift(RIGHT*3+UP*1.5)
        self.playw(FadeIn(encoder, nump))
        for i in range(len(dots)):
            r, c = divmod(i, 7)
            patch = VGroup(*[mnist[r][c][j] for j in range(4)])
            nn_in_buff = 0.25
            VGroup(*[r.arrange(RIGHT, buff=nn_in_buff) for r in patch.generate_target()]).arrange(RIGHT, buff=nn_in_buff).shift(RIGHT*3+UP*3)
            self.play(MoveToTarget(patch))
            self.play(FadeOut(patch, shift=DOWN*0.7))
            anims = forward_prop(encoder)
            for anim in anims:
                self.play(anim)
            
            tensor = Tensor(2, arrange=RIGHT, buff=0.2).scale(0.7).next_to(encoder, DOWN)
            self.play(FadeIn(tensor, shift=DOWN*0.5))
            self.play(tensor.to_numbers(numbers=e_hat[0, r, c], font_size=12))
            latent = Dot(nump.c2p(*e_hat[0, r, c]), radius=DEFAULT_DOT_RADIUS*0.3, stroke_width=0.3)
            self.play(Transform(tensor, latent))
            if i == 0:
                self.wait(2)

class AE(DefaultManimClass):
    def construct(self):
        x, z, x_hat = Tensor(16), Tensor(2), Tensor(16)
        encoder, decoder = MLP(16, 7, 2), MLP(2, 7, 16)
        ae = VGroup(x, encoder, z, decoder, x_hat).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3).scale(0.6)
        self.playw(FadeIn(ae))
        ae.save_state()
        ae.generate_target().set_opacity(0.2)
        ae.target[2].set_opacity(1).scale(1.2)
        self.playw(MoveToTarget(ae))
        self.playw(Restore(ae))
        for anim in forward_prop(ae):
            self.play(anim)
        self.wait()
        self.playw(FadeOut(encoder, z, decoder))
        loss = MathTex(r"||x - \hat{x}||^2").next_to(ae, UP)
        self.playw(VGroup(x, x_hat).animate.arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3), FadeIn(loss))

class AE2(DefaultManimClass):
    def construct(self):
        x, z = Tensor(16), Tensor(2)
        x_hat = x.copy().set_opacity(0.8)
        encoder, decoder = MLP(16, 7, 2), MLP(2, 7, 16)
        ae = VGroup(x, encoder, z, decoder, x_hat).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3).scale(0.6)
        x_x_hat = VGroup(x, x_hat)
        x_x_hat.save_state()
        model = VGroup(encoder, z, decoder)
        model.save_state()
        self.playw(Write(x), run_time=1)
        self.playw(LaggedStart(
            FadeIn(encoder),
            FadeIn(z, shift=RIGHT*0.4),
            lag_ratio=0.5
        ))
        self.playw(LaggedStart(
            FadeIn(decoder),
            FadeIn(x_hat, shift=RIGHT*0.4),
            lag_ratio=0.5
        ))
        self.playw(VGroup(encoder, z, decoder).animate.set_opacity(0))
        loss = MathTex(r"||x - \hat{x}||^2").next_to(ae, UP)
        self.playw(VGroup(x, x_hat).animate.arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3), FadeIn(loss))

        self.wait(2)

        self.playw(LaggedStart(Restore(x_x_hat), Restore(model), lag_ratio=0.5), FadeOut(loss))
        ae.save_state()
        self.playw(VGroup(encoder, z, decoder, x_hat).animate.set_opacity(0.2), x.animate.scale(1.2))
        self.playw(Restore(ae))
        for anim in forward_prop(ae):
            self.play(anim)
        self.wait()

        self.playw(encoder.animate.scale(1.2), VGroup(x, z, decoder, x_hat).animate.set_opacity(0.2))
        self.playw(decoder.animate.scale(1.2).set_opacity(1).set_fill(WHITE, opacity=0), encoder.animate.set_opacity(0.2).scale(1/1.2))
        self.playw(decoder.animate.scale(1/1.2).set_opacity(0.2))
        

class AE3(DefaultManimClass):
    def construct(self):
        np.random.seed(41)
        x, z = Tensor(16), Tensor(2)
        x_hat = x.copy().set_opacity(0.8)
        encoder, decoder = MLP(16, 7, 2), MLP(2, 7, 16)
        ae = VGroup(x, encoder, z, decoder, x_hat).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3).scale(0.6)

        mnist = []
        for i in range(0, 28, 4):
            row = []
            for j in range(0, 28, 4):
                d = data[0, 0, i:i+4, j:j+4].cpu().numpy()
                patch = get_4x4_pixel(d)
                row.append(patch)
            row = VGroup(*row).arrange(RIGHT, buff=0.05)
            mnist.append(row)
        mnist = VGroup(*mnist).arrange(DOWN, buff=0.05).shift(LEFT*11)
        self.playw(FadeIn(encoder, mnist))

        nump = NumberPlane((-4.11111, 4.11111, 0.5), (-3.5, 3.5, 0.5)).set_opacity(0.5).scale(0.6).shift(RIGHT*3)
        
        dots = []
        for i in range(7):
            for j in range(7):
                dots.append(Dot(nump.c2p(*e_hat[0, i, j].cpu().detach().numpy()), radius=DEFAULT_DOT_RADIUS*0.5, stroke_width=1, stroke_color=BLACK))

        ce_dots = []
        for i in range(7):
            for j in range(7):
                ce_dots.append(Dot(nump.c2p(*ce_hat[0, i, j].cpu().detach().numpy()), radius=DEFAULT_DOT_RADIUS*0.5, stroke_width=1, stroke_color=BLACK))


        for i in range(len(dots)):
            r, c = divmod(i, 7)
            patch = VGroup(*[mnist[r][c][j] for j in range(4)])
            nn_in_buff = 0.25
            self.playw(Transform(patch, x))
            self.playw(LaggedStart(
                FadeOut(patch, shift=RIGHT*0.5),
                *forward_prop(encoder),
                FadeIn(z, shift=RIGHT*0.5),
                lag_ratio=1
            ))
            break
        
        
        self.playw(FadeIn(nump))
        self.playw(Transform(z, dots[i]))
        self.play(z.animate.shift(UP+0.3*RIGHT), run_time=0.7)
        self.play(z.animate.shift(DOWN*0.2+0.9*LEFT), run_time=0.7)
        self.play(z.animate.shift(DOWN*1.2+0.3*RIGHT), run_time=0.7)
        self.play(z.animate.shift(UP*0.4+0.3*RIGHT), run_time=0.7)

        square = Square(side_length=1.25).move_to(nump.c2p(0, 0))
        self.playw(FadeIn(square))
        self.camera.frame.save_state()
        self.playw(self.camera.frame.animate.move_to(square).scale(0.5))
        z.save_state()
        self.play(z.animate.move_to(nump.c2p(0.5, 0.7)))
        self.play(z.animate.move_to(nump.c2p(-0.5, 0.2)))
        self.play(z.animate.move_to(nump.c2p(0.2, -0.9)))
        self.playw(Restore(z))
        self.playw(Restore(self.camera.frame), FadeOut(square))

        codebook = VGroup(*[
            Star(5, outer_radius=0.1, inner_radius=0.03, stroke_width=2, color=GREY).move_to(nump.c2p(*item)).set_fill(RED, opacity=1.0) for item in cb
        ])
        self.camera.frame.save_state()
        self.playw(FadeIn(codebook), self.camera.frame.animate.move_to(square).scale(0.7))

        z = Tensor(2).scale(0.6)
        self.playw(Restore(self.camera.frame))
        for i in range(1, len(ce_dots)):
            r, c = divmod(i, 7)
            patch = VGroup(*[mnist[r][c][j] for j in range(4)])
            nn_in_buff = 0.25
            self.playw(Transform(patch, x))
            self.playw(LaggedStart(
                FadeOut(patch, shift=RIGHT*0.5),
                *forward_prop(encoder),
                FadeIn(z, shift=RIGHT*0.5),
                lag_ratio=1
            ))
            self.playw(Transform(z, ce_dots[i]))
            break

        for i in range(2, len(ce_dots)):
            z = Tensor(2).scale(0.6)
            r, c = divmod(i, 7)
            patch = VGroup(*[mnist[r][c][j] for j in range(4)])
            nn_in_buff = 0.25
            self.play(Transform(patch, x))
            self.play(LaggedStart(
                FadeOut(patch, shift=RIGHT*0.5),
                *forward_prop(encoder),
                FadeIn(z, shift=RIGHT*0.5),
                lag_ratio=1
            ))
            self.play(Transform(z, ce_dots[i]))
            if i == 9:
                break
        
        for i in range(10, len(ce_dots)):
            z = Tensor(2).scale(0.6)
            r, c = divmod(i, 7)
            patch = VGroup(*[mnist[r][c][j] for j in range(4)])
            nn_in_buff = 0.25
            self.playw(Transform(patch, x))
            self.playw(LaggedStart(
                FadeOut(patch, shift=RIGHT*0.5),
                *forward_prop(encoder),
                FadeIn(z, shift=RIGHT*0.5),
                lag_ratio=1
            ))
            dots[i].set_color(PURE_GREEN)
            self.playw(Transform(z, dots[i]))
            arrows = VGroup(*[Arrow(dots[i], nump.c2p(*cb[j]), stroke_width=1, buff=0, tip_length=0.1, max_tip_length_to_length_ratio=1) for j in range(len(codebook))])
            self.playw(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.2))
            break
        
        self.camera.frame.save_state()
        self.playw(self.camera.frame.animate.move_to(square).scale(0.45))
        self.playw(FadeOut(arrows[1:]), codebook[0].animate.set_color(PURE_RED))
        self.playw(FadeOut(arrows[0]), z.animate.move_to(nump.c2p(*cb[0])))

def color_pixel(value):
    h = hex(int(value*255))[2:].zfill(2)
    color = f"#{h}{h}{h}"
    return Square(0.2, color=GREY, stroke_width=1, stroke_opacity=0.6).set_fill(color, opacity=1)

def get_4x4_pixel(arr):
    return VGroup(*[VGroup(*[color_pixel(arr[i, j]) for j in range(4)]).arrange(RIGHT, buff=0.05) for i in range(4)]).arrange(DOWN, buff=0.05)