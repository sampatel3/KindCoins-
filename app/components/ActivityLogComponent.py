import reflex as rx
from app.states.state import (
    AppState,
    Category,
    Activity,
    Child,
)
from app.components.LottiePlayer import lottie_player
from app.components.activity_logging import (
    category_card_component,
    activity_button_component,
    custom_activity_creator_component,
    interactive_element_class,
)


def updated_confirmation_display_component() -> (
    rx.Component
):
    child: Child | None = (
        AppState.selected_child_for_details
    )
    coin_burst_lottie = AppState.show_coin_burst_lottie_path
    growth_sparkle_lottie = (
        AppState.show_growth_sparkle_lottie_path
    )
    return rx.el.div(
        rx.el.h2(
            "Amazing Job!",
            class_name="text-3xl font-bold text-green-600 mb-4 text-center",
        ),
        rx.cond(
            coin_burst_lottie != None,
            lottie_player(
                path=coin_burst_lottie,
                width="150px",
                height="150px",
                loop=False,
                class_name="mx-auto",
            ),
            rx.el.div(
                "🪙🎉🪙🎉🪙",
                class_name="text-5xl text-center py-4",
            ),
        ),
        rx.el.p(
            AppState.activity_logged_success_message,
            class_name="text-xl text-navy-700 my-4 text-center font-semibold",
        ),
        rx.cond(
            child != None,
            rx.el.div(
                rx.el.p(
                    f"{child['name']}'s {child['avatar_type']} is growing!",
                    class_name="text-md text-peach-700 text-center",
                ),
                rx.el.image(
                    src=child["avatar_image_src"],
                    alt=f"{child['name']}'s avatar",
                    class_name="w-24 h-24 rounded-full mx-auto my-2 border-4 border-mint-400 shadow-lg",
                ),
                rx.cond(
                    growth_sparkle_lottie != None,
                    lottie_player(
                        path=growth_sparkle_lottie,
                        width="100px",
                        height="100px",
                        loop=False,
                        class_name="mx-auto",
                    ),
                    rx.fragment(),
                ),
                class_name="my-4 p-4 bg-sky-50 rounded-lg shadow",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.button(
                "Add Another Activity",
                on_click=AppState.add_another_activity,
                class_name=interactive_element_class(
                    "bg-mint-500 hover:bg-mint-600 text-white font-semibold py-3 px-6 rounded-lg shadow-md w-full md:w-auto mb-2 md:mb-0 md:mr-2"
                ),
            ),
            rx.el.button(
                "Return Home",
                on_click=AppState.return_to_origin_view,
                class_name=interactive_element_class(
                    "bg-peach-500 hover:bg-peach-600 text-white font-semibold py-3 px-6 rounded-lg shadow-md w-full md:w-auto"
                ),
            ),
            class_name="mt-8 flex flex-col md:flex-row justify-center items-center",
        ),
        class_name="p-6 md:p-8 bg-white rounded-2xl shadow-2xl max-w-md mx-auto text-center",
    )


def activity_log_component() -> rx.Component:
    """
    The main UI for the interactive activity logging flow, designed as an overlay.
    """
    child_selector_ui = rx.cond(
        (AppState.children.length() > 1)
        & (AppState.activity_log_step == "category_select")
        & (AppState.active_child_for_world_view_id == None),
        rx.el.div(
            rx.el.h3(
                "For whom are we logging?",
                class_name="text-xl font-semibold text-navy-700 mb-2 text-center",
            ),
            rx.el.select(
                rx.foreach(
                    AppState.children_options,
                    lambda option: rx.el.option(
                        option["label"],
                        value=option["value"],
                    ),
                ),
                default_value=AppState.current_child_id_for_details,
                on_change=AppState.set_current_child_id_for_details,
                class_name="block w-full max-w-xs mx-auto pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm rounded-md shadow-sm",
            ),
            class_name="mb-8 p-4 bg-sky-50 rounded-lg shadow",
        ),
        rx.fragment(),
    )
    category_selection_ui = rx.el.div(
        rx.el.h2(
            "What kind of awesome deed?",
            class_name="text-3xl font-bold text-navy-700 mb-8 text-center pt-8",
        ),
        child_selector_ui,
        rx.el.div(
            rx.foreach(
                AppState.categories, category_card_component
            ),
            class_name="grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-6 justify-items-center px-4 pb-8",
        ),
        class_name="w-full max-w-3xl mx-auto overflow-y-auto h-full",
    )
    activity_selection_panel_content = rx.el.div(
        rx.el.button(
            "← Back to Categories",
            on_click=AppState.close_activity_panel,
            class_name="absolute top-4 left-4 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-2 px-4 rounded-lg shadow text-sm z-20 kindcoins-transition-fast animate-wobble-on-tap",
        ),
        rx.el.h3(
            rx.cond(
                AppState.current_log_category,
                f"{AppState.current_log_category['icon']} {AppState.current_log_category['name']} Activities",
                "Select an Activity",
            ),
            class_name="text-2xl font-bold text-navy-700 mb-6 pt-16 text-center",
        ),
        rx.el.div(
            rx.foreach(
                AppState.activities_for_log_category,
                activity_button_component,
            ),
            rx.el.button(
                "🎨 Create Your Own Activity",
                on_click=AppState.start_custom_activity_creation,
                class_name="w-full bg-peach-500 hover:bg-peach-600 text-white font-semibold py-3 px-4 rounded-lg shadow-md mt-4 transition-colors kindcoins-transition-fast animate-wobble-on-tap",
            ),
            class_name="overflow-y-auto p-4 md:p-6 space-y-2",
            style={"scrollbar_width": "thin"},
        ),
        class_name=rx.cond(
            AppState.activity_panel_animation_state
            == "exited",
            "hidden",
            f"kindcoins-panel inset-y-0 right-0 w-full md:w-96 h-full overflow-y-auto {AppState.activity_panel_display_class}",
        ),
    )
    confirmation_dialog = rx.el.dialog(
        updated_confirmation_display_component(),
        class_name=f"bg-transparent p-0 border-none shadow-none {AppState.confirmation_modal_display_class}",
        open=(
            AppState.confirmation_modal_animation_state
            == "entering"
        )
        | (
            AppState.confirmation_modal_animation_state
            == "entered"
        ),
    )
    custom_activity_dialog = rx.el.dialog(
        custom_activity_creator_component(),
        class_name=f"bg-transparent p-0 border-none shadow-none {AppState.custom_activity_modal_display_class}",
        open=(
            AppState.custom_activity_modal_animation_state
            == "entering"
        )
        | (
            AppState.custom_activity_modal_animation_state
            == "entered"
        ),
    )
    return rx.cond(
        AppState.activity_log_overlay_animation_state
        != "exited",
        rx.el.div(
            rx.el.button(
                "X",
                on_click=AppState.close_activity_log_overlay,
                class_name="absolute top-4 right-4 bg-red-500 hover:bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center shadow-md z-50 kindcoins-transition-fast animate-wobble-on-tap",
            ),
            rx.match(
                AppState.activity_log_step,
                ("category_select", category_selection_ui),
                ("activity_select", category_selection_ui),
                ("confirmation", category_selection_ui),
                (
                    "custom_create_activity",
                    category_selection_ui,
                ),
                rx.el.p(
                    "Loading activity log...",
                    class_name="text-center text-gray-500",
                ),
            ),
            activity_selection_panel_content,
            confirmation_dialog,
            custom_activity_dialog,
            class_name=f"kindcoins-bottom-drawer h-[90vh] {AppState.activity_log_overlay_display_class} {AppState.current_activity_log_bg_class} transition-colors duration-500 ease-in-out",
            on_mount=AppState.start_activity_logging,
        ),
        rx.fragment(),
    )