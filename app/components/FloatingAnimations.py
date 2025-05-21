import reflex as rx
import random


def floating_element(
    element_type: str, index: int
) -> rx.Component:
    base_style = {
        "position": "fixed",
        "bottom": "-60px",
        "animation_delay": f"{random.uniform(0, 10)}s",
        "z_index": -10,
    }
    if element_type == "bubble":
        size = random.randint(15, 40)
        left_pos = random.randint(0, 95)
        duration = random.randint(8, 15)
        return rx.el.div(
            style={
                **base_style,
                "width": f"{size}px",
                "height": f"{size}px",
                "left": f"{left_pos}%",
                "animation_duration": f"{duration}s",
                "background_color": "rgba(224, 242, 254, 0.4)",
                "border_radius": "50%",
                "pointer_events": "none",
            }
        )
    elif element_type == "leaf":
        size_w = random.randint(15, 25)
        size_h = random.randint(20, 35)
        left_pos = random.randint(0, 95)
        duration = random.randint(10, 18)
        sway_x = random.randint(-60, 60)
        sway_rotate = random.randint(-25, 25)
        return rx.el.div(
            style={
                **base_style,
                "width": f"{size_w}px",
                "height": f"{size_h}px",
                "left": f"{left_pos}%",
                "animation_duration": f"{duration}s",
                "--sway-x": f"{sway_x}px",
                "--sway-rotate": f"{sway_rotate}deg",
                "background_color": "rgba(134, 239, 172, 0.5)",
                "clip_path": "ellipse(50% 40% at 50% 50%)",
            }
        )
    elif element_type == "star":
        top_pos = random.randint(5, 70)
        left_pos = random.randint(5, 95)
        duration = random.randint(3, 6)
        size = random.randint(1, 3)
        return rx.el.div(
            style={
                "position": "fixed",
                "top": f"{top_pos}%",
                "left": f"{left_pos}%",
                "width": f"{size}px",
                "height": f"{size}px",
                "animation_duration": f"{duration}s",
                "animation_delay": f"{random.uniform(0, 4)}s",
                "z_index": -10,
                "background_color": "rgba(251, 191, 36, 0.8)",
                "border_radius": "50%",
            }
        )
    return rx.fragment()


def floating_animations_component() -> rx.Component:
    """
    Creates a variety of floating elements for the background.
    Animations that were previously in animations.css are now removed.
    The elements will appear but will be static or rely on future inline animation styles if added.
    """
    num_bubbles = 7
    num_leaves = 5
    num_stars = 15
    elements = []
    for i in range(num_bubbles):
        elements.append(floating_element("bubble", i))
    for i in range(num_leaves):
        elements.append(floating_element("leaf", i))
    for i in range(num_stars):
        elements.append(floating_element("star", i))
    return rx.fragment(*elements)