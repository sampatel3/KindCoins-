import reflex as rx
from app.states.state import AppState
from app.components.navbar import page_layout


def login_page() -> rx.Component:
    """
    Page for kid-friendly access (PIN per child) and switching profiles.
    This is a placeholder as PIN logic and kid mode are not fully implemented.
    """
    content = rx.el.div(
        rx.el.h2(
            "Login / Switch Child (Placeholder)",
            class_name="text-3xl font-bold text-navy-700 mb-6 text-center",
        ),
        rx.el.p(
            "This page will allow children to log in using a PIN and switch between profiles.",
            class_name="text-center text-gray-600 mb-4",
        ),
        rx.el.p(
            "A 'Kid Mode' with a reduced UI to prevent access to settings will also be managed here.",
            class_name="text-center text-gray-600 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Select Child Profile",
                    class_name="text-xl font-semibold text-navy-700 mb-3",
                ),
                class_name="mb-6 p-4 bg-sky-50 rounded-lg shadow",
            ),
            rx.el.div(
                rx.el.h3(
                    "Enter PIN",
                    class_name="text-xl font-semibold text-navy-700 mb-3",
                ),
                rx.el.input(
                    type="password",
                    placeholder="****",
                    class_name="mt-1 block w-full md:w-1/2 mx-auto pl-3 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm",
                ),
                rx.el.button(
                    "Login",
                    class_name="mt-3 block mx-auto bg-mint-500 hover:bg-mint-600 text-white font-semibold py-2 px-6 rounded-lg shadow",
                ),
                class_name="mb-6 p-4 bg-sky-50 rounded-lg shadow",
            ),
            rx.el.div(
                rx.el.h3(
                    "Kid Mode",
                    class_name="text-xl font-semibold text-navy-700 mb-3",
                ),
                class_name="p-4 bg-sky-50 rounded-lg shadow",
            ),
            class_name="max-w-md mx-auto space-y-6",
        ),
        class_name="container mx-auto px-4 py-8",
    )
    return page_layout(content, title="Login - KindCoins")