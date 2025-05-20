import reflex as rx
from app.states.state import Child
from app.components.progress_avatar import progress_avatar


def child_card(child: Child) -> rx.Component:
    """
    A card component to display information about a single child.
    Shows avatar, name, coin balance, and growth stage (via progress_avatar).
    """
    return rx.el.div(
        rx.el.h3(
            child["name"],
            class_name="text-2xl font-bold text-navy mb-3 text-center",
        ),
        progress_avatar(child_data=child),
        rx.el.div(
            rx.el.p(
                "Coins:",
                class_name="text-md text-gray-700 font-semibold",
            ),
            rx.el.p(
                f"💰 {child['coin_balance']}",
                class_name="text-2xl font-bold text-amber-500",
            ),
            class_name="mt-4 flex flex-col items-center",
        ),
        rx.el.button(
            "Log Activity",
            class_name="mt-6 bg-mint-500 hover:bg-mint-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md w-full transition-colors duration-150 ease-in-out",
        ),
        class_name="bg-sky-50 p-6 rounded-xl shadow-lg border border-sky-200 w-full max-w-xs hover:shadow-xl transition-shadow duration-200 ease-in-out",
    )