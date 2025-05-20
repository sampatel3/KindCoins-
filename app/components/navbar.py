import reflex as rx
from app.states.state import AppState
import datetime


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.a(
                "KindCoins",
                href="/",
                class_name="text-2xl font-bold text-white hover:text-mint-200",
            ),
            rx.el.div(
                rx.el.a(
                    "Dashboard",
                    href="/",
                    class_name="text-white hover:text-mint-200 px-3 py-2 rounded-md text-sm font-medium",
                ),
                rx.el.a(
                    "Log Activity",
                    href="/add",
                    class_name="text-white hover:text-mint-200 px-3 py-2 rounded-md text-sm font-medium",
                ),
                rx.el.a(
                    "Goals",
                    href="/goals",
                    class_name="text-white hover:text-mint-200 px-3 py-2 rounded-md text-sm font-medium",
                ),
                rx.el.a(
                    "History",
                    href="/history",
                    class_name="text-white hover:text-mint-200 px-3 py-2 rounded-md text-sm font-medium",
                ),
                rx.el.a(
                    "Manage",
                    href="/manage",
                    class_name="text-white hover:text-mint-200 px-3 py-2 rounded-md text-sm font-medium",
                ),
                class_name="flex space-x-4",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16",
        ),
        class_name="bg-navy-700 shadow-md sticky top-0 z-50",
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.p(
                f"© {datetime.date.today().year} KindCoins. All rights reserved.",
                class_name="text-sm text-gray-400",
            ),
            rx.el.div(
                rx.el.a(
                    "Privacy Policy",
                    href="/legal/privacy.html",
                    target="_blank",
                    class_name="text-sm text-mint-500 hover:text-mint-400",
                )
            ),
            class_name="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center space-y-2 sm:space-y-0",
        ),
        class_name="bg-navy-800 border-t border-navy-700",
    )


def page_layout(
    content: rx.Component, title: str
) -> rx.Component:
    return rx.el.div(
        rx.el.title(title),
        navbar(),
        rx.el.main(
            content,
            class_name="flex-grow container mx-auto px-4 py-8",
        ),
        footer(),
        class_name="min-h-screen flex flex-col bg-sky-100",
    )