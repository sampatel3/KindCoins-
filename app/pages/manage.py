import reflex as rx
from app.states.state import (
    AppState,
    AVATAR_TYPES,
    CURRENCY_SYMBOLS,
)
from app.components.navbar import page_layout


def manage_page() -> rx.Component:
    """Page for managing children, categories, activities, and app settings."""
    avatar_options_list: list[dict[str, str]] = [
        {
            "label": avatar_type.capitalize(),
            "value": avatar_type,
        }
        for avatar_type in AVATAR_TYPES.__args__
    ]
    currency_options: list[dict[str, str]] = [
        {"label": f"{code} ({symbol})", "value": code}
        for code, symbol in CURRENCY_SYMBOLS.items()
    ]
    add_child_form = rx.el.form(
        rx.el.h3(
            "Add New Child",
            class_name="text-xl font-semibold text-navy-700 mb-3",
        ),
        rx.el.div(
            rx.el.label(
                "Child's Name:",
                htmlFor="child_name",
                class_name="block text-sm font-medium text-gray-700",
            ),
            rx.el.input(
                type="text",
                id="child_name",
                name="child_name",
                default_value=AppState.form_child_name,
                key=f"child_name_input_{AppState.form_child_name}",
                placeholder="e.g., Alex",
                class_name="mt-1 block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm",
                required=True,
            ),
            class_name="mb-3",
        ),
        rx.el.div(
            rx.el.label(
                "Avatar Type:",
                htmlFor="avatar_type_select",
                class_name="block text-sm font-medium text-gray-700",
            ),
            rx.el.select(
                rx.foreach(
                    avatar_options_list,
                    lambda opt: rx.el.option(
                        opt["label"], value=opt["value"]
                    ),
                ),
                id="avatar_type_select",
                name="avatar_type",
                default_value="tree",
                class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm rounded-md shadow-sm",
                required=True,
            ),
            class_name="mb-4",
        ),
        rx.el.button(
            "Add Child",
            type="submit",
            class_name="w-full bg-mint-500 hover:bg-mint-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition-colors",
        ),
        on_submit=AppState.handle_add_child_form_submit,
        reset_on_submit=True,
        class_name="p-4 bg-sky-50 rounded-lg shadow space-y-3",
    )
    children_management = rx.el.div(
        rx.el.h3(
            "Manage Children",
            class_name="text-xl font-semibold text-navy-700 mb-3",
        ),
        rx.cond(
            AppState.children.length() > 0,
            rx.el.ul(
                rx.foreach(
                    AppState.children,
                    lambda child: rx.el.li(
                        rx.el.span(
                            child["name"],
                            class_name="font-medium",
                        ),
                        rx.el.span(
                            f"({child['avatar_type'].capitalize()}, Balance: {AppState.current_currency_symbol}{child['coin_balance']})"
                        ),
                        class_name="flex justify-between items-center p-2 border-b border-gray-200",
                    ),
                ),
                class_name="bg-white rounded-md shadow divide-y divide-gray-200",
            ),
            rx.el.p(
                "No children added yet.",
                class_name="text-gray-500",
            ),
        ),
        class_name="mb-6",
    )
    app_settings = rx.el.div(
        rx.el.h3(
            "App Settings",
            class_name="text-xl font-semibold text-navy-700 mb-3",
        ),
        rx.el.div(
            rx.el.label(
                "Display Currency:",
                htmlFor="currency_select",
                class_name="block text-sm font-medium text-gray-700",
            ),
            rx.el.select(
                rx.foreach(
                    currency_options,
                    lambda opt: rx.el.option(
                        opt["label"], value=opt["value"]
                    ),
                ),
                id="currency_select",
                value=AppState.selected_currency,
                on_change=AppState.change_currency,
                class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm rounded-md shadow-sm",
            ),
            class_name="mb-4 p-4 bg-sky-50 rounded-lg shadow",
        ),
        rx.el.p(
            "Daily reminders, privacy toggles, cloud-sync (Coming Soon)",
            class_name="text-gray-400 italic",
        ),
        class_name="mb-6",
    )
    categories_management = rx.el.div(
        rx.el.h3(
            "Manage Categories (Coming Soon)",
            class_name="text-xl font-semibold text-navy-700 mb-3 opacity-50",
        ),
        rx.el.p(
            "Functionality to add, edit, and delete categories will be here.",
            class_name="text-gray-400 italic p-4 bg-sky-50 rounded-lg shadow",
        ),
        class_name="mb-6",
    )
    activities_management = rx.el.div(
        rx.el.h3(
            "Manage Activities (Coming Soon)",
            class_name="text-xl font-semibold text-navy-700 mb-3 opacity-50",
        ),
        rx.el.p(
            "Functionality to add, edit, and delete activities, and set default coin values.",
            class_name="text-gray-400 italic p-4 bg-sky-50 rounded-lg shadow",
        ),
        class_name="mb-6",
    )
    content = rx.el.div(
        rx.el.h2(
            "Manage Data & Settings",
            class_name="text-3xl font-bold text-navy-700 mb-8",
        ),
        rx.el.div(
            add_child_form,
            children_management,
            app_settings,
            categories_management,
            activities_management,
            class_name="space-y-8",
        ),
        on_mount=AppState.load_initial_data,
        class_name="max-w-3xl mx-auto",
    )
    return page_layout(content, title="Manage - KindCoins")