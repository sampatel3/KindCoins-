import reflex as rx
from app.states.state import AppState
from app.components.ChildCard import (
    child_dashboard_card_component,
)
from app.components.FloatingAnimations import (
    floating_animations_component,
)
from app.components.WorldViewComponent import (
    world_view_component,
)
from app.components.ActivityLogComponent import (
    activity_log_component,
)
from app.components.MascotGuide import (
    mascot_guide_component,
)


def index_page() -> rx.Component:
    """The main dashboard page for KindCoins - ultra-minimal and child-friendly."""
    page_container_class = rx.cond(
        AppState.time_of_day == "day",
        "bg-gradient-to-br from-sky-300 via-sky-100 to-peach-100 min-h-screen transition-colors duration-1000 overflow-hidden relative",
        "bg-gradient-to-br from-navy-700 via-navy-900 to-purple-900 min-h-screen transition-colors duration-1000 overflow-hidden relative",
    )
    dashboard_content = rx.el.div(
        rx.cond(
            AppState.isLoading,
            rx.el.div(
                rx.el.p(
                    "Loading dashboard...",
                    class_name="text-center text-gray-600 text-lg",
                ),
                rx.el.div(
                    class_name="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-mint-500 mx-auto mt-4"
                ),
                class_name="flex flex-col items-center justify-center min-h-[200px] pt-20",
            ),
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        AppState.children,
                        child_dashboard_card_component,
                    ),
                    class_name="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6 p-4 md:p-8 justify-items-center items-start pt-10",
                ),
                rx.cond(
                    AppState.children.length() == 0,
                    rx.el.div(
                        rx.el.p(
                            "No children added yet. Go to 'Manage' to add a child.",
                            class_name="text-center text-gray-700 dark:text-gray-300 text-lg",
                        ),
                        rx.el.button(
                            "Manage Children",
                            on_click=rx.redirect("/manage"),
                            class_name="mt-4 bg-mint-500 hover:bg-mint-600 text-white font-semibold py-2 px-6 rounded-lg shadow-md transition-colors",
                        ),
                        class_name="text-center p-8 flex flex-col items-center justify-center h-full",
                    ),
                    rx.fragment(),
                ),
                class_name="w-full container mx-auto px-2 py-2",
            ),
        ),
        rx.el.button(
            rx.el.span(
                "+", class_name="text-3xl text-white"
            ),
            on_click=AppState.open_activity_log_overlay,
            class_name="fixed bottom-6 right-6 bg-peach-500 hover:bg-peach-600 rounded-full w-16 h-16 flex items-center justify-center shadow-xl z-20 transition-transform hover:scale-110 kindcoins-transition-fast animate-wobble-on-tap",
        ),
        class_name="flex-grow w-full overflow-y-auto",
    )
    return rx.el.div(
        rx.el.title("KindCoins Dashboard"),
        floating_animations_component(),
        rx.cond(
            AppState.current_view == "dashboard",
            dashboard_content,
            rx.fragment(),
        ),
        world_view_component(),
        activity_log_component(),
        mascot_guide_component(),
        class_name=page_container_class,
        on_mount=[
            AppState.load_initial_data,
            AppState.update_time_of_day,
        ],
    )