import reflex as rx
from app.states.state import AppState
from app.components.LottiePlayer import lottie_player


def mascot_guide_component() -> rx.Component:
    """
    A component to display the animated mascot guide.
    """
    return rx.el.div(
        lottie_player(
            path="/lottie/mascot_idle.json",
            width="150px",
            height="150px",
        ),
        rx.el.div(
            rx.el.p(
                AppState.mascot_message,
                class_name="text-sm text-navy-700 bg-sky-100 p-3 rounded-lg shadow-md border border-sky-200",
            ),
            class_name="max-w-xs",
        ),
        class_name="fixed bottom-4 right-4 flex flex-col items-center space-y-2 z-50 p-2 bg-white/80 backdrop-blur-sm rounded-xl shadow-lg",
    )