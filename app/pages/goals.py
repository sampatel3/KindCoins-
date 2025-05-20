import reflex as rx
from app.states.state import AppState, Goal
from app.components.navbar import page_layout


def goal_card(goal: Goal) -> rx.Component:
    child_coin_balance = rx.cond(
        AppState.selected_child_for_details,
        AppState.selected_child_for_details["coin_balance"],
        0,
    )
    progress_percentage = rx.cond(
        goal["target_coins"] > 0,
        (
            child_coin_balance.to(float)
            / goal["target_coins"].to(float)
            * 100
        ).to(int),
        0,
    )
    return rx.el.div(
        rx.el.h4(
            goal["description"],
            class_name="text-xl font-semibold text-navy-700 mb-2 truncate",
        ),
        rx.el.p(
            f"Target: {AppState.current_currency_symbol}{goal['target_coins']} coins",
            class_name="text-sm text-gray-600",
        ),
        rx.cond(
            goal["real_world_reward_note"],
            rx.el.p(
                f"Reward: {goal['real_world_reward_note']}",
                class_name="text-sm text-peach-700 italic",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.div(
                rx.cond(
                    progress_percentage > 10,
                    f"{progress_percentage}%",
                    rx.cond(
                        progress_percentage == 0, "", ""
                    ),
                ),
                style={
                    "width": rx.cond(
                        progress_percentage >= 100,
                        "100%",
                        f"{progress_percentage}%",
                    ),
                    "minWidth": "5%",
                },
                class_name="bg-mint-500 h-full rounded-full text-xs text-white text-center leading-none py-1 transition-all duration-500 ease-out",
            ),
            class_name="w-full bg-gray-200 rounded-full h-4 mt-2 mb-1 shadow-inner overflow-hidden",
        ),
        rx.el.p(
            rx.cond(
                progress_percentage >= 100,
                "Target Met!",
                f"{progress_percentage}% towards goal",
            ),
            class_name="text-xs text-gray-500 text-right",
        ),
        rx.cond(
            goal["is_achieved"],
            rx.el.div(
                rx.el.p(
                    "🎉 Goal Achieved! 🎉",
                    class_name="text-lg font-bold text-green-600 mt-3 text-center",
                )
            ),
            rx.el.button(
                "Mark as Complete",
                on_click=lambda: AppState.complete_goal(
                    goal["id"]
                ),
                class_name="mt-4 w-full bg-amber-500 hover:bg-amber-600 text-white font-semibold py-2 px-4 rounded-lg shadow transition-colors",
                is_disabled=progress_percentage < 100,
            ),
        ),
        class_name="bg-sky-50 p-5 rounded-lg shadow hover:shadow-md transition-shadow",
    )


def goals_page() -> rx.Component:
    """Page for viewing and managing goals."""
    add_goal_form = rx.el.form(
        rx.el.h3(
            "Add New Goal",
            class_name="text-2xl font-semibold text-navy-700 mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Goal Description:",
                htmlFor="goal_desc",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.input(
                type="text",
                default_value=AppState.form_goal_description,
                key=AppState.form_goal_description,
                id="goal_desc",
                name="goal_desc",
                placeholder="e.g., Save for a new LEGO set",
                class_name="mt-1 block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm",
                required=True,
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Target Coins:",
                htmlFor="goal_coins",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.input(
                type="number",
                default_value=AppState.form_goal_target_coins.to_string(),
                key=AppState.form_goal_target_coins.to_string(),
                id="goal_coins",
                name="goal_coins",
                placeholder="100",
                min="1",
                class_name="mt-1 block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm",
                required=True,
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Optional Reward Note:",
                htmlFor="goal_reward",
                class_name="block text-sm font-medium text-gray-700 mb-1",
            ),
            rx.el.input(
                type="text",
                id="goal_reward",
                name="reward_note",
                default_value=AppState.form_goal_reward_note,
                key=AppState.form_goal_reward_note,
                placeholder="e.g., A trip to the ice cream shop!",
                class_name="mt-1 block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm",
            ),
            class_name="mb-6",
        ),
        rx.el.button(
            "Add Goal",
            type="submit",
            class_name="w-full bg-mint-500 hover:bg-mint-600 text-white font-bold py-3 px-4 rounded-lg shadow-md transition-colors",
        ),
        on_submit=AppState.handle_add_goal_form_submit,
        reset_on_submit=True,
        class_name="p-6 bg-white rounded-xl shadow-xl mb-8",
    )
    content = rx.el.div(
        rx.el.h2(
            "My Goals",
            class_name="text-3xl font-bold text-navy-700 mb-6",
        ),
        rx.el.div(
            rx.el.label(
                "Select Child:",
                htmlFor="child_goal_select",
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
                id="child_goal_select",
                class_name="mt-1 block w-full md:w-1/3 pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-mint-500 focus:border-mint-500 sm:text-sm rounded-md shadow-sm",
            ),
            class_name="mb-8",
        ),
        rx.cond(
            AppState.selected_child_for_details,
            rx.el.div(
                add_goal_form,
                rx.el.h3(
                    f"Goals for {AppState.selected_child_for_details['name']}",
                    class_name="text-2xl font-semibold text-navy-700 mb-4 mt-8",
                ),
                rx.cond(
                    AppState.goals_for_selected_child.length()
                    > 0,
                    rx.el.div(
                        rx.foreach(
                            AppState.goals_for_selected_child,
                            goal_card,
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                    rx.el.p(
                        f"No goals set for {AppState.selected_child_for_details['name']} yet. Add one above!",
                        class_name="text-center text-gray-500 py-8 text-lg",
                    ),
                ),
            ),
            rx.el.p(
                "Select a child to view and manage their goals.",
                class_name="text-center text-gray-500 py-8 text-lg",
            ),
        ),
        on_mount=AppState.load_initial_data,
        class_name="max-w-5xl mx-auto",
    )
    return page_layout(content, title="Goals - KindCoins")