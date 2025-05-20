import reflex as rx
from app.states.state import AppState, Category


def select_category_component(
    categories: rx.Var[list[Category]],
    on_select: rx.event.EventHandler,
) -> rx.Component:
    """
    A component for selecting a category.
    """
    return rx.el.div(
        rx.el.h4(
            "Select Category",
            class_name="text-lg font-semibold text-navy-700 mb-2",
        ),
        rx.el.div(
            rx.foreach(
                categories,
                lambda category_item: rx.el.button(
                    category_item["icon"],
                    " ",
                    category_item["name"],
                    on_click=lambda: on_select(
                        category_item["id"]
                    ),
                    class_name="bg-peach-300 hover:bg-peach-400 text-navy-700 font-medium py-2 px-4 rounded-lg shadow text-left w-full mb-2 transition-colors",
                ),
            ),
            class_name="space-y-2",
        ),
        class_name="p-4 bg-white rounded-lg shadow",
    )