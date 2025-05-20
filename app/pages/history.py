import reflex as rx
from app.states.state import AppState, HistoryEntry
from app.components.navbar import page_layout


def history_entry_card(entry: HistoryEntry) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                entry["category_icon"],
                class_name="text-2xl mr-3",
            ),
            rx.el.div(
                rx.el.p(
                    entry["activity_name"],
                    class_name="font-semibold text-navy-700",
                ),
                rx.el.p(
                    f"Category: {entry['category_name']}",
                    class_name="text-sm text-gray-600",
                ),
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.p(
                f"+{entry['coins_earned']} coins",
                class_name="font-bold text-amber-500 text-lg",
            ),
            rx.el.p(
                rx.el.span(
                    entry["timestamp"].split("T")[0]
                ),
                " ",
                rx.el.span(
                    entry["timestamp"]
                    .split("T")[1]
                    .split(".")[0]
                ),
                class_name="text-xs text-gray-500",
            ),
            class_name="text-right",
        ),
        class_name="bg-sky-50 p-4 rounded-lg shadow flex justify-between items-center hover:shadow-md transition-shadow",
    )


def history_page() -> rx.Component:
    """Page for viewing activity history."""
    content = rx.el.div(
        rx.el.h2(
            "Activity History",
            class_name="text-3xl font-bold text-navy-700 mb-6",
        ),
        rx.el.div(
            rx.el.label(
                "Select Child:",
                htmlFor="child_history_select",
                class_name="block text-sm font-medium text-gray-700 mb-1",
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
                id="child_history_select",
                class_name="mt-1 block w-full md:w-1/3 pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm rounded-md shadow-sm",
            ),
            class_name="mb-6",
        ),
        rx.cond(
            AppState.isLoading,
            rx.el.p(
                "Loading history...",
                class_name="text-gray-500",
            ),
            rx.cond(
                AppState.history_for_selected_child.length()
                > 0,
                rx.el.div(
                    rx.foreach(
                        AppState.history_for_selected_child,
                        history_entry_card,
                    ),
                    class_name="space-y-4",
                ),
                rx.el.p(
                    rx.cond(
                        AppState.selected_child_for_details,
                        f"No history found for {AppState.selected_child_for_details['name']}.",
                        "Select a child to view their history.",
                    ),
                    class_name="text-center text-gray-500 py-8 text-lg",
                ),
            ),
        ),
        class_name="max-w-2xl mx-auto",
        on_mount=AppState.load_initial_data,
    )
    return page_layout(
        content, title="Activity History - KindCoins"
    )