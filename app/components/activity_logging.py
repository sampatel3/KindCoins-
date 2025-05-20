import reflex as rx
from app.states.state import (
    AppState,
    Category,
    Activity,
    Child,
)
from app.components.LottiePlayer import lottie_player


def interactive_element_class(base_class: str = "") -> str:
    return f"{base_class} transform transition-all duration-150 ease-in-out hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-peach-500"


def category_card_component(
    category: Category,
) -> rx.Component:
    """Large, tappable emoji icon card for category selection."""
    return rx.el.button(
        rx.el.div(
            rx.el.span(
                category["icon"],
                class_name="text-6xl md:text-7xl",
            ),
            rx.el.p(
                category["name"],
                class_name="mt-2 text-lg md:text-xl font-semibold text-navy-700",
            ),
            class_name="flex flex-col items-center justify-center p-4 md:p-6",
        ),
        on_click=lambda: AppState.select_log_category(
            category["id"]
        ),
        class_name=interactive_element_class(
            f"w-40 h-48 md:w-48 md:h-56 rounded-2xl shadow-lg border-2 border-sky-200 hover:border-peach-400 hover:shadow-xl {category['background_class']}"
        ),
        aria_label=f"Select category: {category['name']}",
    )


def activity_button_component(
    activity: Activity,
) -> rx.Component:
    """Animated button for activity selection with emoji, phrase, and coin value."""
    return rx.el.button(
        rx.el.div(
            rx.el.span(
                activity["icon"], class_name="text-4xl mr-3"
            ),
            rx.el.div(
                rx.el.p(
                    activity["name"],
                    class_name="text-md font-medium text-navy-700 text-left",
                ),
                rx.el.p(
                    f"+{activity['coins']} ✨",
                    class_name="text-sm text-amber-600 font-bold animate-bounce-sm",
                ),
                class_name="flex-grow",
            ),
            class_name="flex items-center p-3",
        ),
        on_click=lambda: AppState.select_log_activity(
            activity["id"]
        ),
        class_name=interactive_element_class(
            "w-full bg-sky-50 hover:bg-sky-100 rounded-xl shadow border border-sky-200 mb-3"
        ),
        aria_label=f"Select activity: {activity['name']}, {activity['coins']} coins",
    )


def confirmation_display_component() -> rx.Component:
    """
    Shows success message, avatar growth preview, and action buttons.
    This component appears to be an older/unused version.
    The active one is updated_confirmation_display_component in ActivityLogComponent.py
    Fixing the error here just in case it's compiled.
    """
    child: Child | None = (
        AppState.selected_child_for_details
    )
    return rx.el.div(
        rx.el.h2(
            "Amazing Job!",
            class_name="text-3xl font-bold text-green-600 mb-4 text-center",
        ),
        rx.cond(
            AppState.show_coin_burst_lottie_path != "",
            lottie_player(
                path=AppState.show_coin_burst_lottie_path,
                width="150px",
                height="150px",
                loop=False,
                class_name="mx-auto",
            ),
            rx.el.div(
                "🪙🎉🪙🎉🪙",
                class_name="text-5xl text-center py-4 animate-ping",
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
                    AppState.show_growth_sparkle_lottie_path
                    != "",
                    lottie_player(
                        path=AppState.show_growth_sparkle_lottie_path,
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
                "Return to World",
                on_click=AppState.return_to_origin_view,
                class_name=interactive_element_class(
                    "bg-peach-500 hover:bg-peach-600 text-white font-semibold py-3 px-6 rounded-lg shadow-md w-full md:w-auto"
                ),
            ),
            class_name="mt-8 flex flex-col md:flex-row justify-center items-center",
        ),
        class_name="p-6 md:p-8 bg-white rounded-2xl shadow-2xl max-w-md mx-auto text-center",
    )


def custom_activity_creator_component() -> rx.Component:
    """Modal content for creating a custom activity."""
    return rx.el.div(
        rx.el.h3(
            "Create Your Own Activity",
            class_name="text-2xl font-bold text-navy-700 mb-6 text-center",
        ),
        rx.el.div(
            rx.el.label(
                "Activity Name:",
                htmlFor="custom_activity_name",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.input(
                id="custom_activity_name",
                on_change=AppState.set_custom_activity_name_input,
                placeholder="e.g., Built a LEGO castle",
                class_name="mt-1 block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm",
                default_value=AppState.custom_activity_name_input,
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Icon (Emoji):",
                htmlFor="custom_activity_icon",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.input(
                id="custom_activity_icon",
                on_change=AppState.set_custom_activity_icon_input,
                placeholder="💡",
                max_length=2,
                class_name="mt-1 block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm",
                default_value=AppState.custom_activity_icon_input,
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                f"Coins: {AppState.custom_activity_coins_slider_value} ✨",
                htmlFor="custom_activity_coins",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.input(
                type="range",
                id="custom_activity_coins",
                min="1",
                max="50",
                on_change=AppState.set_custom_activity_coins_slider_value,
                class_name="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-mint-500",
                default_value=AppState.custom_activity_coins_slider_value.to_string(),
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.button(
                "Save & Log Activity",
                on_click=AppState.save_custom_activity,
                class_name=interactive_element_class(
                    "bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg shadow-md w-full md:w-auto mb-2 md:mb-0 md:mr-2"
                ),
                is_disabled=AppState.custom_activity_name_input.strip()
                == "",
            ),
            rx.el.button(
                "Cancel",
                on_click=AppState.cancel_custom_activity_creation,
                class_name=interactive_element_class(
                    "bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-3 px-6 rounded-lg shadow w-full md:w-auto"
                ),
            ),
            class_name="mt-8 flex flex-col md:flex-row justify-center items-center",
        ),
        class_name="p-6 bg-white rounded-xl shadow-xl max-w-lg mx-auto",
    )