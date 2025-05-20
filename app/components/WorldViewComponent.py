import reflex as rx
from app.states.state import AppState, Child
from app.components.LottiePlayer import lottie_player
from app.components.ProgressAvatar import progress_avatar


def world_view_component() -> rx.Component:
    """
    A full-screen overlay displaying the child's world.
    Shows animated avatar, coins, progress, and actions.
    """
    active_child: Child | None = (
        AppState.active_child_for_world_view
    )
    return rx.cond(
        AppState.active_child_for_world_view_id != None,
        rx.el.div(
            rx.el.button(
                "← Back to Dashboard",
                on_click=AppState.close_world_view,
                class_name="absolute top-4 left-4 bg-white/80 hover:bg-white text-navy-700 font-semibold py-2 px-4 rounded-lg shadow-md z-10 kindcoins-transition-fast animate-wobble-on-tap",
            ),
            rx.cond(
                active_child != None,
                rx.el.div(
                    rx.el.h2(
                        f"{active_child['name']}'s World",
                        class_name="text-4xl font-bold text-white mb-6 text-center [text-shadow:_2px_2px_4px_rgb(0_0_0_/_50%)]",
                    ),
                    rx.el.div(
                        lottie_player(
                            path=active_child[
                                "avatar_lottie_src"
                            ],
                            width="250px",
                            height="250px",
                            loop=True,
                            autoplay=True,
                            class_name="mx-auto mb-4",
                        ),
                        class_name="flex flex-col items-center p-6 bg-sky-100/70 backdrop-blur-sm rounded-xl shadow-xl mb-6",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "💰", class_name="text-4xl mr-2"
                        ),
                        rx.el.span(
                            active_child["coin_balance"],
                            class_name="text-5xl font-bold text-amber-300 [text-shadow:_2px_2px_4px_rgb(0_0_0_/_50%)]",
                        ),
                        class_name="flex items-center justify-center mb-4",
                    ),
                    rx.el.p(
                        f"Growth Stage: {active_child['growth_stage'] + 1}/8",
                        class_name="text-lg text-white/90 text-center mb-2 [text-shadow:_1px_1px_2px_rgb(0_0_0_/_50%)]",
                    ),
                    rx.el.p(
                        active_child[
                            "current_streak_status"
                        ],
                        class_name="text-md text-amber-200 text-center mb-6 font-semibold [text-shadow:_1px_1px_2px_rgb(0_0_0_/_50%)]",
                    ),
                    rx.el.button(
                        "Log a Good Deed!",
                        on_click=AppState.open_activity_log_overlay,
                        class_name="bg-peach-500 hover:bg-peach-600 text-white font-bold py-3 px-8 rounded-xl shadow-lg text-lg animate-wobble-on-tap kindcoins-transition-fast transform hover:scale-105",
                    ),
                    class_name="flex flex-col items-center justify-center text-center w-full max-w-lg",
                ),
                rx.el.p(
                    "Loading child's world...",
                    class_name="text-white text-xl",
                ),
            ),
            class_name=rx.cond(
                AppState.world_view_animation_state
                == "exited",
                "hidden",
                f"fixed inset-0 bg-gradient-to-br from-sky-400 via-mint-500 to-sky-600 flex flex-col items-center justify-center p-4 z-30 overflow-y-auto {AppState.world_view_display_class}",
            ),
        ),
        rx.fragment(),
    )