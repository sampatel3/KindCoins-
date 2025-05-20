import reflex as rx
from app.states.state import Child


def progress_avatar(child_data: Child) -> rx.Component:
    """
    Displays a child's avatar and their growth progress.
    Uses pre-defined SVG paths for different stages.
    """
    return rx.el.div(
        rx.el.div(
            rx.el.image(
                src=child_data["avatar_image_src"],
                alt=f"{child_data['name']}'s {child_data['avatar_type']} avatar",
                class_name="w-24 h-24 md:w-32 md:h-32 rounded-full object-contain border-4 border-mint-400 shadow-lg p-1 bg-white",
            ),
            class_name="relative w-28 h-28 md:w-36 md:h-36 mx-auto flex items-center justify-center",
        ),
        rx.el.p(
            f"{child_data['avatar_type']} Stage: {child_data['growth_stage'] + 1}/8",
            class_name="text-sm text-navy-700 text-center mt-2 font-semibold capitalize",
        ),
        rx.el.p(
            rx.cond(
                child_data["growth_stage"] == 7,
                "🎉 Fully Grown! 🎉",
                "",
            ),
            class_name="text-center text-sm text-amber-600 font-bold mt-1 h-5",
        ),
        class_name="flex flex-col items-center",
    )