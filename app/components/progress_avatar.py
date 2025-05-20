import reflex as rx
from app.states.state import Child


def progress_avatar(child_data: Child) -> rx.Component:
    """
    Displays a child's avatar and their growth progress.
    rules.md: "Visual avatars (tree default, rocket, pet, planet)."
    rules.md: "8 SVG layers per avatar; progress % decides frame."
    For now, uses a placeholder image and text for growth stage.
    """
    return rx.el.div(
        rx.el.image(
            src=child_data["avatar_image_src"],
            alt=f"{child_data['name']}'s {child_data['avatar_type']} avatar",
            class_name="w-24 h-24 rounded-full object-cover border-4 border-mint-300 shadow-lg mx-auto",
        ),
        rx.el.p(
            f"{child_data['avatar_type'].capitalize()} Stage: {child_data['growth_stage'] + 1}/8",
            class_name="text-sm text-navy text-center mt-2 font-semibold",
        ),
        class_name="flex flex-col items-center",
    )