import reflex as rx
from app.states.state import Child, AppState
from app.components.LottiePlayer import lottie_player


def child_dashboard_card_component(
    child: Child,
) -> rx.Component:
    avatar_size = "100px"
    ring_size = "120px"
    progress_ring_style = {
        "width": ring_size,
        "height": ring_size,
        "border_radius": "50%",
        "background": f"conic-gradient(rgb(34 197 94) {child['current_goal_progress_percentage']}%, rgb(229 231 235) 0%)",
        "padding": "8px",
        "box_shadow": "inset 0 0 0 8px white",
    }
    coin_glow_style = {
        "text_shadow": "0 0 8px #fbbf24, 0 0 12px #fbbf24, 0 0 16px #fbbf24"
    }
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                lottie_player(
                    path=child["avatar_lottie_src"],
                    width=avatar_size,
                    height=avatar_size,
                    loop=True,
                    autoplay=True,
                ),
                class_name=f"w-[{avatar_size}] h-[{avatar_size}] rounded-full flex items-center justify-center overflow-hidden bg-white",
            ),
            style=progress_ring_style,
            class_name="relative flex items-center justify-center mx-auto mb-3",
        ),
        rx.el.h3(
            child["name"],
            class_name="text-xl font-bold text-navy-700 dark:text-sky-100 text-center truncate",
        ),
        rx.el.div(
            rx.el.span("💰", class_name="text-2xl mr-1"),
            rx.el.span(
                child["coin_balance"],
                style=coin_glow_style,
                class_name="text-2xl font-bold text-amber-400",
            ),
            class_name="flex items-center justify-center my-2",
        ),
        rx.el.p(
            child["current_streak_status"],
            class_name="text-sm text-peach-700 dark:text-peach-300 text-center font-medium",
        ),
        on_click=lambda: AppState.open_world_view(
            child["id"]
        ),
        class_name="bg-sky-50/70 dark:bg-navy-600/70 backdrop-blur-sm p-4 rounded-2xl shadow-lg w-full max-w-[200px] h-[280px] flex flex-col justify-center items-center cursor-pointer kindcoins-transition-fast transform hover:scale-105 active:scale-95 border border-sky-200 dark:border-navy-500 animate-wobble-on-tap animate-glow-on-hover",
    )