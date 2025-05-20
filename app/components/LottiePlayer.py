import reflex as rx


def lottie_player(
    path: str,
    speed: float = 1,
    loop: bool = True,
    autoplay: bool = True,
    renderer: str = "svg",
    width: str = "100%",
    height: str = "100%",
    class_name: str = "",
) -> rx.Component:
    """
    A placeholder component for Lottie animations.
    Displays the path of the Lottie file.
    """
    return rx.el.div(
        rx.el.p(f"Lottie Animation: {path}"),
        style={
            "width": width,
            "height": height,
            "border": "1px dashed #ccc",
            "display": "flex",
            "align_items": "center",
            "justify_content": "center",
            "text_align": "center",
        },
        class_name=class_name,
    )