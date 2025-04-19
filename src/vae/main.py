from manim import *
from manimdef import DefaultManimClass
from vae import model, data
import torch


class AutoEncoderReview(DefaultManimClass):
    def construct(self):
        num_row, num_col = 9, 9
        mnists_list = []
        data_input = (
            data[: num_row * num_col].to(torch.float).view(num_row * num_col, -1) / 255
        ).cuda()
        model.load_state_dict(torch.load("ae.ckpt"))
        z = model[0](data_input)
        zs = z[..., :2]
        data_hat = (model[1](zs).view(-1, 28, 28).cpu().detach() * 255).to(torch.int)
        for i in range(num_row):
            row = []
            for j in range(num_col):
                image = ImageMobject(data[i * num_col + j])
                row.append(image)
                if i == 0 and j == 0:
                    continue
                elif j == 0:
                    image.next_to(mnists_list[i - 1][0], DOWN)
                elif j > 0:
                    image.next_to(row[j - 1], RIGHT)
            mnists_list.append(row)
        camera_center = mnists_list[num_row // 2][num_col // 2].get_center()
        self.camera.frame.move_to(camera_center)
        flattened_mnists_list = sum(mnists_list, [])
        self.playw(FadeIn(*flattened_mnists_list))
        shape = Text("28 * 28", font="Consolas", color=YELLOW).move_to(camera_center)
        self.playw(
            AnimationGroup(
                *[item.animate.set_opacity(0.5) for item in flattened_mnists_list]
            ),
            FadeIn(shape, scale=1.2),
        )
        shape_result = Text("784", font="Consolas", color=YELLOW).move_to(camera_center)
        self.playw(Transform(shape, shape_result))
        shape_encoded = Text("2", font="Consolas", color=PURE_RED).move_to(
            camera_center
        )
        self.playw(Transform(shape, shape_encoded))

        neural_net = ImageMobject("neuralnetCode.png").next_to(
            mnists_list[num_row // 2][-1],
            RIGHT,
            buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 3,
        )
        self.playw(
            FadeIn(neural_net),
            FadeOut(shape),
        )

        nump = (
            NumberPlane(
                x_range=[-18.0, 10.0],
                y_range=[-18.3, 10],
                color=GREY_D,
                background_line_style={
                    "stroke_color": TEAL,
                    "stroke_width": 4,
                    "stroke_opacity": 0.3,
                },
            )
            .scale(0.25)
            .next_to(
                neural_net,
                RIGHT,
                buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 3,
            )
        )
        self.playw(
            AnimationGroup(
                *[item.animate.set_opacity(1.0) for item in flattened_mnists_list]
            ),
            FadeIn(nump),
            self.camera.frame.animate.scale(1.6).move_to(neural_net),
        )

        dots = VGroup(
            *[
                Dot(
                    nump.c2p(*s.cpu().detach().numpy()),
                    color=YELLOW,
                    radius=DEFAULT_DOT_RADIUS * 0.5,
                )
                for s in zs
            ]
        )
        encoding = LaggedStart(
            *[
                FadeTransform(flattened_mnists_list[i], dots[i])
                for i in range(num_row * num_col)
            ],
        )
        recon_data = []
        for i in range(num_row):
            row = []
            for j in range(num_col):
                image = ImageMobject(data_hat[i * num_col + j]).move_to(
                    mnists_list[i][j]
                )
                row.append(image)
            recon_data.append(row)
        flattened_recon_data = sum(recon_data, [])
        self.playw(encoding)
        decoding = LaggedStart(
            *[
                FadeTransform(dots[i], flattened_recon_data[i])
                for i in range(num_row * num_col)
            ]
        )
        self.play(decoding)
        self.remove(*flattened_mnists_list)
        self.playw(
            AnimationGroup(
                *[item.animate.set_opacity(1.0) for item in flattened_recon_data]
            )
        )
        self.wait()
        self.playw(FadeIn(dots))
        arrows = VGroup(
            *[
                Arrow(
                    dots[i],
                    nump.c2p(0, 0, 0),
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.1,
                    buff=MED_SMALL_BUFF * 0.5,
                ).set_opacity(0.5)
                for i in range(num_row * num_col)
            ]
        )
        self.playw(LaggedStart(*[GrowArrow(arrow) for arrow in arrows]))
        dots.save_state()
        self.playw(
            FadeOut(arrows), self.camera.frame.animate.move_to(nump).scale(1 / 1.6)
        )
        self.playw(
            AnimationGroup(
                *[dots[i].animate.move_to(nump.c2p(0, 0, 0)) for i in range(len(dots))]
            )
        )
        self.wait(2)
        self.playw(Restore(dots))


class AutoEncoderZloss(DefaultManimClass):
    def construct(self):
        num_row, num_col = 9, 9
        mnists_list = []
        data_input = (
            data[: num_row * num_col].to(torch.float).view(num_row * num_col, -1) / 255
        ).cuda()
        model.load_state_dict(torch.load("aez1.ckpt"))
        z = model[0](data_input)
        zs = z[..., :2]
        data_hat = (model[1](zs).view(-1, 28, 28).cpu().detach() * 255).to(torch.int)
        for i in range(num_row):
            row = []
            for j in range(num_col):
                image = ImageMobject(data[i * num_col + j])
                row.append(image)
                if i == 0 and j == 0:
                    continue
                elif j == 0:
                    image.next_to(mnists_list[i - 1][0], DOWN)
                elif j > 0:
                    image.next_to(row[j - 1], RIGHT)
            mnists_list.append(row)
        camera_center = mnists_list[num_row // 2][num_col // 2].get_center()
        self.camera.frame.move_to(camera_center)
        flattened_mnists_list = sum(mnists_list, [])
        self.playw(FadeIn(*flattened_mnists_list))
        shape = Text("28 * 28", font="Consolas", color=YELLOW).move_to(camera_center)
        self.playw(
            AnimationGroup(
                *[item.animate.set_opacity(0.5) for item in flattened_mnists_list]
            ),
            FadeIn(shape, scale=1.2),
        )
        shape_result = Text("784", font="Consolas", color=YELLOW).move_to(camera_center)
        self.playw(Transform(shape, shape_result))
        shape_encoded = Text("2", font="Consolas", color=PURE_RED).move_to(
            camera_center
        )
        self.playw(Transform(shape, shape_encoded))

        neural_net = ImageMobject("neuralnetCode.png").next_to(
            mnists_list[num_row // 2][-1],
            RIGHT,
            buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 3,
        )
        self.playw(
            FadeIn(neural_net),
            FadeOut(shape),
        )

        nump = NumberPlane(
            x_range=[-3, 3],
            y_range=[-3, 3],
            color=GREY_D,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.3,
            },
        ).next_to(
            neural_net,
            RIGHT,
            buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 3,
        )
        self.playw(
            AnimationGroup(
                *[item.animate.set_opacity(1.0) for item in flattened_mnists_list]
            ),
            FadeIn(nump),
            self.camera.frame.animate.move_to(neural_net).scale(1.4),
        )

        dots = VGroup(
            *[
                Dot(
                    nump.c2p(*s.cpu().detach().numpy()),
                    color=YELLOW,
                    radius=DEFAULT_DOT_RADIUS * 0.5,
                )
                for s in zs
            ]
        )
        encoding = LaggedStart(
            *[
                FadeTransform(flattened_mnists_list[i], dots[i])
                for i in range(num_row * num_col)
            ],
        )
        recon_data = []
        for i in range(num_row):
            row = []
            for j in range(num_col):
                image = ImageMobject(data_hat[i * num_col + j]).move_to(
                    mnists_list[i][j]
                )
                row.append(image)
            recon_data.append(row)
        flattened_recon_data = sum(recon_data, [])
        self.playw(encoding)
        self.playw(FadeOut(dots))
        zs_sampled = torch.randn_like(zs, device=zs.device)
        data_hat_sampled = (
            model[1](zs_sampled).view(-1, 28, 28).cpu().detach() * 255
        ).to(torch.int)
        dots_sampled = VGroup(
            *[
                Dot(
                    nump.c2p(*s.cpu().detach().numpy()),
                    color=PURE_GREEN,
                    radius=DEFAULT_DOT_RADIUS * 0.5,
                )
                for s in zs_sampled
            ]
        )
        self.playw(FadeIn(dots_sampled))

        recon_data_sampled = []
        for i in range(num_row):
            row = []
            for j in range(num_col):
                image = ImageMobject(data_hat_sampled[i * num_col + j]).move_to(
                    mnists_list[i][j]
                )
                row.append(image)
            recon_data_sampled.append(row)
        flattened_recon_data_sampled = sum(recon_data_sampled, [])

        decoding = LaggedStart(
            *[
                FadeTransform(dots_sampled[i], flattened_recon_data_sampled[i])
                for i in range(num_row * num_col)
            ]
        )
        self.play(decoding)
        self.remove(*flattened_mnists_list)
        self.playw(
            AnimationGroup(
                *[
                    item.animate.set_opacity(1.0)
                    for item in flattened_recon_data_sampled
                ]
            )
        )
        self.wait()
        self.playw(self.camera.frame.animate.move_to(camera_center).scale(0.7))
        return
        self.playw(FadeIn(dots))
        arrows = VGroup(
            *[
                Arrow(
                    dots[i],
                    nump.c2p(0, 0, 0),
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.1,
                    buff=MED_SMALL_BUFF * 0.5,
                ).set_opacity(0.5)
                for i in range(num_row * num_col)
            ]
        )
        self.playw(LaggedStart(*[GrowArrow(arrow) for arrow in arrows]))
        dots.save_state()
        self.playw(
            FadeOut(arrows), self.camera.frame.animate.move_to(nump).scale(1 / 1.6)
        )
        self.playw(
            AnimationGroup(
                *[dots[i].animate.move_to(nump.c2p(0, 0, 0)) for i in range(len(dots))]
            )
        )
        self.wait(2)
        self.playw(Restore(dots))


class AutoEncoderPerturbed(DefaultManimClass):
    def construct(self):
        num_row, num_col = 9, 9
        mnists_list = []
        data_input = (
            data[: num_row * num_col].to(torch.float).view(num_row * num_col, -1) / 255
        ).cuda()
        model.load_state_dict(torch.load("aez1.ckpt"))
        z = model[0](data_input)
        zs = z[..., :2]
        data_hat = (model[1](zs).view(-1, 28, 28).cpu().detach() * 255).to(torch.int)
        for i in range(num_row):
            row = []
            for j in range(num_col):
                image = ImageMobject(data[i * num_col + j])
                row.append(image)
                if i == 0 and j == 0:
                    continue
                elif j == 0:
                    image.next_to(mnists_list[i - 1][0], DOWN)
                elif j > 0:
                    image.next_to(row[j - 1], RIGHT)
            mnists_list.append(row)
        camera_center = mnists_list[num_row // 2][num_col // 2].get_center()
        self.camera.frame.move_to(camera_center)
        flattened_mnists_list = sum(mnists_list, [])
        self.playw(FadeIn(*flattened_mnists_list))

        neural_net = ImageMobject("neuralnetCode.png").next_to(
            mnists_list[num_row // 2][-1],
            RIGHT,
            buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 3,
        )
        self.playw(FadeIn(neural_net))

        nump = NumberPlane(
            x_range=[-3, 3],
            y_range=[-3, 3],
            color=GREY_D,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.3,
            },
        ).next_to(
            neural_net,
            RIGHT,
            buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 3,
        )
        self.playw(
            FadeIn(nump),
            self.camera.frame.animate.move_to(neural_net).scale(1.4),
        )

        dots = VGroup(
            *[
                Dot(
                    nump.c2p(*s.cpu().detach().numpy()),
                    color=YELLOW,
                    radius=DEFAULT_DOT_RADIUS * 0.5,
                )
                for s in zs
            ]
        )
        encoding = LaggedStart(
            *[
                FadeTransform(flattened_mnists_list[i], dots[i])
                for i in range(num_row * num_col)
            ],
        )
        recon_data = []
        for i in range(num_row):
            row = []
            for j in range(num_col):
                image = ImageMobject(data_hat[i * num_col + j]).move_to(
                    mnists_list[i][j]
                )
                row.append(image)
            recon_data.append(row)
        flattened_recon_data = sum(recon_data, [])
        self.playw(encoding)
        zs_sampled = zs + 0.1 * torch.randn_like(zs, device=zs.device)
        data_hat_sampled = (
            model[1](zs_sampled).view(-1, 28, 28).cpu().detach() * 255
        ).to(torch.int)
        dots_sampled = VGroup(
            *[
                Dot(
                    nump.c2p(*s.cpu().detach().numpy()),
                    color=PURE_GREEN,
                    radius=DEFAULT_DOT_RADIUS * 0.5,
                )
                for s in zs_sampled
            ]
        )
        self.playw(
            *[
                dots[i].animate.move_to(
                    nump.c2p(*zs_sampled[i].cpu().detach().tolist())
                )
                for i in range(len(dots))
            ]
        )

        recon_data_sampled = []
        for i in range(num_row):
            row = []
            for j in range(num_col):
                image = ImageMobject(data_hat_sampled[i * num_col + j]).move_to(
                    mnists_list[i][j]
                )
                row.append(image)
            recon_data_sampled.append(row)
        flattened_recon_data_sampled = sum(recon_data_sampled, [])

        decoding = LaggedStart(
            *[
                FadeTransform(dots[i], flattened_recon_data_sampled[i])
                for i in range(num_row * num_col)
            ]
        )
        self.play(decoding)
        self.remove(*flattened_mnists_list)
        self.playw(
            AnimationGroup(
                *[
                    item.animate.set_opacity(1.0)
                    for item in flattened_recon_data_sampled
                ]
            )
        )
        self.wait()
        self.playw(self.camera.frame.animate.move_to(camera_center).scale(0.7))
        return
