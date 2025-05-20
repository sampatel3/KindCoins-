import reflex as rx
from typing import TypedDict, List, Literal, Dict, cast
import datetime
import asyncio
import uuid

AVATAR_TYPES = Literal["tree", "rocket", "pet", "planet"]
CATEGORY_TYPES = Literal[
    "Kindness", "Chores", "Learning", "Health", "Custom"
]
CURRENCY_SYMBOLS: Dict[str, str] = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "AUD": "$",
    "CAD": "$",
}
ACTIVITY_LOG_STEP = Literal[
    "category_select",
    "activity_select",
    "confirmation",
    "custom_create_activity",
]
VIEW_TYPES = Literal[
    "dashboard",
    "world_view",
    "activity_log_overlay",
    "settings_modal",
]
ANIMATION_STATE = Literal[
    "idle", "entering", "entered", "exiting", "exited"
]


class Child(TypedDict):
    id: str
    name: str
    avatar_image_src: str
    avatar_lottie_src: str
    avatar_type: AVATAR_TYPES
    growth_stage: int
    coin_balance: int
    current_streak_status: str
    current_goal_progress_percentage: int


class Category(TypedDict):
    id: str
    name: CATEGORY_TYPES
    icon: str
    background_class: str


class Activity(TypedDict):
    id: str
    name: str
    category_id: str
    icon: str
    coins: int
    parent_configurable: bool


class Goal(TypedDict):
    id: str
    child_id: str
    description: str
    target_coins: int
    is_achieved: bool
    real_world_reward_note: str | None


class HistoryEntry(TypedDict):
    id: str
    child_id: str
    activity_name: str
    category_name: CATEGORY_TYPES
    category_icon: str
    coins_earned: int
    timestamp: str


class AppState(rx.State):
    children: List[Child] = []
    categories: List[Category] = []
    activities: List[Activity] = []
    goals: List[Goal] = []
    history_entries: List[HistoryEntry] = []
    isLoading: bool = True
    current_child_id_for_details: str | None = None
    selected_currency: str = "USD"
    form_child_name: str = ""
    form_activity_name: str = ""
    form_activity_category: str = ""
    form_activity_coins: int = 10
    form_goal_description: str = ""
    form_goal_target_coins: int = 100
    form_goal_reward_note: str = ""
    activity_logged_success_message: str = ""
    mascot_message: str = (
        "Hi there! Let's do some good deeds!"
    )
    time_of_day: Literal["day", "night"] = "day"
    current_view: VIEW_TYPES = "dashboard"
    active_child_for_world_view_id: str | None = None
    world_view_animation_state: ANIMATION_STATE = "exited"
    activity_log_overlay_animation_state: (
        ANIMATION_STATE
    ) = "exited"
    activity_log_step: ACTIVITY_LOG_STEP = "category_select"
    selected_log_category_id: str | None = None
    selected_log_activity_id: str | None = None
    activity_panel_animation_state: ANIMATION_STATE = (
        "exited"
    )
    confirmation_modal_animation_state: ANIMATION_STATE = (
        "exited"
    )
    custom_activity_modal_animation_state: (
        ANIMATION_STATE
    ) = "exited"
    current_activity_log_bg_class: str = "bg-sky-100"
    custom_activity_name_input: str = ""
    custom_activity_icon_input: str = "✨"
    custom_activity_coins_slider_value: int = 5
    confirmed_activity_details: Activity | None = None
    confirmed_category_details: Category | None = None
    confirmed_coins_earned: int = 0
    show_coin_burst_lottie_path: str | None = None
    show_growth_sparkle_lottie_path: str | None = None

    @rx.var
    def current_currency_symbol(self) -> str:
        return CURRENCY_SYMBOLS.get(
            self.selected_currency, "$"
        )

    @rx.var
    def children_options(self) -> list[dict[str, str]]:
        return [
            {"label": child["name"], "value": child["id"]}
            for child in self.children
        ]

    @rx.var
    def category_options(self) -> list[dict[str, str]]:
        return [
            {
                "label": f"{cat['icon']} {cat['name']}",
                "value": cat["id"],
            }
            for cat in self.categories
        ]

    @rx.var
    def active_child_for_world_view(self) -> Child | None:
        if self.active_child_for_world_view_id:
            for child in self.children:
                if (
                    child["id"]
                    == self.active_child_for_world_view_id
                ):
                    return child
        return None

    @rx.var
    def selected_child_for_details(self) -> Child | None:
        if self.current_child_id_for_details:
            for child in self.children:
                if (
                    child["id"]
                    == self.current_child_id_for_details
                ):
                    return child
        return self.active_child_for_world_view

    @rx.var
    def goals_for_selected_child(self) -> List[Goal]:
        child_to_check = self.selected_child_for_details
        if not child_to_check:
            return []
        return [
            goal
            for goal in self.goals
            if goal["child_id"] == child_to_check["id"]
        ]

    @rx.var
    def history_for_selected_child(
        self,
    ) -> List[HistoryEntry]:
        child_to_check = self.selected_child_for_details
        if not child_to_check:
            return []
        child_history = [
            entry
            for entry in self.history_entries
            if entry["child_id"] == child_to_check["id"]
        ]
        return sorted(
            child_history,
            key=lambda x: x["timestamp"],
            reverse=True,
        )

    @rx.var
    def current_log_category(self) -> Category | None:
        if self.selected_log_category_id:
            for cat in self.categories:
                if (
                    cat["id"]
                    == self.selected_log_category_id
                ):
                    return cat
        return None

    @rx.var
    def activities_for_log_category(self) -> List[Activity]:
        if not self.selected_log_category_id:
            return []
        return [
            act
            for act in self.activities
            if act["category_id"]
            == self.selected_log_category_id
        ]

    @rx.var
    def current_log_activity(self) -> Activity | None:
        if self.selected_log_activity_id:
            for act in self.activities:
                if (
                    act["id"]
                    == self.selected_log_activity_id
                ):
                    return act
        return None

    @rx.var
    def world_view_display_class(self) -> str:
        if self.world_view_animation_state == "entering":
            return "animate-zoom-in"
        if self.world_view_animation_state == "exiting":
            return "animate-zoom-out"
        return ""

    @rx.var
    def activity_log_overlay_display_class(self) -> str:
        if (
            self.activity_log_overlay_animation_state
            == "entering"
        ):
            return "animate-slide-in-bottom"
        if (
            self.activity_log_overlay_animation_state
            == "exiting"
        ):
            return "animate-slide-out-bottom"
        return ""

    @rx.var
    def activity_panel_display_class(self) -> str:
        if (
            self.activity_panel_animation_state
            == "entering"
        ):
            return "animate-slide-in-right"
        if self.activity_panel_animation_state == "exiting":
            return "animate-slide-out-right"
        return ""

    @rx.var
    def confirmation_modal_display_class(self) -> str:
        if (
            self.confirmation_modal_animation_state
            == "entering"
        ):
            return "animate-fade-in"
        if (
            self.confirmation_modal_animation_state
            == "exiting"
        ):
            return "animate-fade-out"
        return ""

    @rx.var
    def custom_activity_modal_display_class(self) -> str:
        if (
            self.custom_activity_modal_animation_state
            == "entering"
        ):
            return "animate-fade-in"
        if (
            self.custom_activity_modal_animation_state
            == "exiting"
        ):
            return "animate-fade-out"
        return ""

    @rx.event
    def update_time_of_day(self):
        current_hour = datetime.datetime.now().hour
        self.time_of_day = (
            "day" if 6 <= current_hour < 19 else "night"
        )
        yield

    @rx.event
    async def load_initial_data(self):
        self.isLoading = True
        async with self:
            if not self.categories:
                self.categories = [
                    Category(
                        id="cat1",
                        name="Kindness",
                        icon="🌟",
                        background_class="bg-yellow-200/50",
                    ),
                    Category(
                        id="cat2",
                        name="Chores",
                        icon="🧹",
                        background_class="bg-blue-200/50",
                    ),
                    Category(
                        id="cat3",
                        name="Learning",
                        icon="📚",
                        background_class="bg-green-200/50",
                    ),
                    Category(
                        id="cat4",
                        name="Health",
                        icon="💪",
                        background_class="bg-red-200/50",
                    ),
                ]
            if not self.activities:
                self.activities = [
                    Activity(
                        id="act1",
                        name="Helped a friend",
                        category_id="cat1",
                        icon="🤝",
                        coins=15,
                        parent_configurable=True,
                    ),
                    Activity(
                        id="act2",
                        name="Shared toys",
                        category_id="cat1",
                        icon="🎁",
                        coins=10,
                        parent_configurable=True,
                    ),
                    Activity(
                        id="act3",
                        name="Cleaned room",
                        category_id="cat2",
                        icon="🏠",
                        coins=20,
                        parent_configurable=True,
                    ),
                    Activity(
                        id="act4",
                        name="Set the table",
                        category_id="cat2",
                        icon="🍽️",
                        coins=5,
                        parent_configurable=True,
                    ),
                    Activity(
                        id="act5",
                        name="Read a book for 20 mins",
                        category_id="cat3",
                        icon="📖",
                        coins=15,
                        parent_configurable=False,
                    ),
                    Activity(
                        id="act6",
                        name="Practiced math",
                        category_id="cat3",
                        icon="🧮",
                        coins=10,
                        parent_configurable=False,
                    ),
                    Activity(
                        id="act7",
                        name="Ate all veggies",
                        category_id="cat4",
                        icon="🥦",
                        coins=10,
                        parent_configurable=True,
                    ),
                    Activity(
                        id="act8",
                        name="Played outside for 30 mins",
                        category_id="cat4",
                        icon="⚽",
                        coins=15,
                        parent_configurable=True,
                    ),
                ]
            if not self.children:
                self.children = [
                    Child(
                        id="child1",
                        name="Alex",
                        avatar_image_src="/avatars/tree/tree_stage_4.svg",
                        avatar_lottie_src="/lottie/avatars/tree/stage_4.json",
                        avatar_type="tree",
                        growth_stage=3,
                        coin_balance=150,
                        current_streak_status="Day 3 Streak 🔥",
                        current_goal_progress_percentage=50,
                    ),
                    Child(
                        id="child2",
                        name="Bella",
                        avatar_image_src="/avatars/rocket/rocket_stage_8.svg",
                        avatar_lottie_src="/lottie/avatars/rocket/stage_8.json",
                        avatar_type="rocket",
                        growth_stage=7,
                        coin_balance=450,
                        current_streak_status="Growing Strong! 🌱",
                        current_goal_progress_percentage=50,
                    ),
                ]
            if not self.goals and self.children:
                self.goals = [
                    Goal(
                        id="goal1",
                        child_id=self.children[0]["id"],
                        description="Save for a new comic book",
                        target_coins=300,
                        is_achieved=False,
                        real_world_reward_note="Comic book store visit!",
                    ),
                    Goal(
                        id="goal2",
                        child_id=(
                            self.children[1]["id"]
                            if len(self.children) > 1
                            else self.children[0]["id"]
                        ),
                        description="Fund a charity donation",
                        target_coins=500,
                        is_achieved=True,
                        real_world_reward_note="Donated!",
                    ),
                ]
            if not self.history_entries and self.children:
                self.history_entries = [
                    HistoryEntry(
                        id="hist1",
                        child_id=self.children[0]["id"],
                        activity_name="Cleaned room",
                        category_name="Chores",
                        category_icon="🧹",
                        coins_earned=20,
                        timestamp=datetime.datetime.now(
                            datetime.timezone.utc
                        ).isoformat(),
                    ),
                    HistoryEntry(
                        id="hist2",
                        child_id=(
                            self.children[1]["id"]
                            if len(self.children) > 1
                            else self.children[0]["id"]
                        ),
                        activity_name="Shared toys",
                        category_name="Kindness",
                        category_icon="🌟",
                        coins_earned=10,
                        timestamp=(
                            datetime.datetime.now(
                                datetime.timezone.utc
                            )
                            - datetime.timedelta(days=1)
                        ).isoformat(),
                    ),
                ]
            if (
                not self.current_child_id_for_details
                and self.children
            ):
                self.current_child_id_for_details = (
                    self.children[0]["id"]
                )
            self.mascot_message = (
                "Welcome back! Ready to earn some coins?"
            )
            self.isLoading = False
        yield AppState.update_time_of_day

    @rx.event
    async def open_world_view(self, child_id: str):
        self.active_child_for_world_view_id = child_id
        self.world_view_animation_state = "entering"
        self.current_view = "world_view"
        await asyncio.sleep(0.05)
        async with self:
            self.world_view_animation_state = "entered"
        yield

    @rx.event
    async def close_world_view(self):
        self.world_view_animation_state = "exiting"
        await asyncio.sleep(0.3)
        async with self:
            self.world_view_animation_state = "exited"
            self.active_child_for_world_view_id = None
            self.current_view = "dashboard"
        yield

    @rx.event
    async def open_activity_log_overlay(self):
        self.activity_log_overlay_animation_state = (
            "entering"
        )
        self.current_view = "activity_log_overlay"
        await asyncio.sleep(0.05)
        async with self:
            self.activity_log_overlay_animation_state = (
                "entered"
            )
        yield AppState.start_activity_logging

    @rx.event
    async def close_activity_log_overlay(self):
        self.activity_log_overlay_animation_state = (
            "exiting"
        )
        await asyncio.sleep(0.3)
        async with self:
            self.activity_log_overlay_animation_state = (
                "exited"
            )
            self.current_view = "dashboard"
            self._reset_activity_log_state()
        yield

    def _reset_activity_log_state(self):
        self.activity_log_step = "category_select"
        self.selected_log_category_id = None
        self.selected_log_activity_id = None
        self.activity_panel_animation_state = "exited"
        self.confirmation_modal_animation_state = "exited"
        self.custom_activity_modal_animation_state = (
            "exited"
        )
        self.current_activity_log_bg_class = "bg-sky-100"
        self.activity_logged_success_message = ""

    @rx.event
    def add_child(
        self, name: str, avatar_type: AVATAR_TYPES
    ):
        if not name.strip():
            return rx.window_alert(
                "Child name cannot be empty."
            )
        new_id = f"child{len(self.children) + 1 + datetime.datetime.now(datetime.timezone.utc).microsecond}"
        new_child = Child(
            id=new_id,
            name=name.strip(),
            avatar_image_src=f"/avatars/{avatar_type.lower()}/{avatar_type.lower()}_stage_1.svg",
            avatar_lottie_src=f"/lottie/avatars/{avatar_type.lower()}/stage_1.json",
            avatar_type=avatar_type,
            growth_stage=0,
            coin_balance=0,
            current_streak_status="New Beginning! ✨",
            current_goal_progress_percentage=0,
        )
        self.children.append(new_child)
        if not self.current_child_id_for_details:
            self.current_child_id_for_details = new_id
        self.form_child_name = ""
        self.mascot_message = (
            f"Yay! {name} has joined KindCoins!"
        )
        yield rx.toast.success(f"{name} added!")

    @rx.event
    def handle_add_child_form_submit(self, form_data: dict):
        name = form_data.get("child_name", "").strip()
        avatar_type_str = form_data.get(
            "avatar_type", "tree"
        )
        avatar_type: AVATAR_TYPES = (
            cast(AVATAR_TYPES, avatar_type_str)
            if avatar_type_str
            in list(AVATAR_TYPES.__args__)
            else "tree"
        )
        yield AppState.add_child(
            name, avatar_type=avatar_type
        )

    @rx.event
    async def perform_activity_logging(
        self,
        child_id: str,
        activity_id: str,
        coins_override: int | None = None,
    ):
        child_idx_to_update = next(
            (
                i
                for i, c in enumerate(self.children)
                if c["id"] == child_id
            ),
            None,
        )
        if child_idx_to_update is None:
            self.activity_logged_success_message = (
                "Error: Child not found."
            )
            return
        activity_details = next(
            (
                act
                for act in self.activities
                if act["id"] == activity_id
            ),
            None,
        )
        if not activity_details:
            self.activity_logged_success_message = (
                "Error: Activity not found."
            )
            return
        category_details = next(
            (
                cat
                for cat in self.categories
                if cat["id"]
                == activity_details["category_id"]
            ),
            None,
        )
        if not category_details:
            self.activity_logged_success_message = (
                "Error: Category not found."
            )
            return
        async with self:
            self.confirmed_activity_details = (
                activity_details
            )
            self.confirmed_category_details = (
                category_details
            )
            coins_earned = (
                coins_override
                if coins_override is not None
                else activity_details["coins"]
            )
            self.confirmed_coins_earned = coins_earned
            child_to_update = self.children[
                child_idx_to_update
            ]
            updated_child_data = child_to_update.copy()
            updated_child_data[
                "coin_balance"
            ] += coins_earned
            updated_child_data[
                "current_goal_progress_percentage"
            ] = (updated_child_data["coin_balance"] % 100)
            self.show_coin_burst_lottie_path = (
                "/lottie/coin_burst.json"
            )
            old_growth_stage = updated_child_data[
                "growth_stage"
            ]
            new_growth_stage = min(
                7, updated_child_data["coin_balance"] // 100
            )
            if new_growth_stage > old_growth_stage:
                updated_child_data["growth_stage"] = (
                    new_growth_stage
                )
                avatar_type = updated_child_data[
                    "avatar_type"
                ]
                updated_child_data["avatar_image_src"] = (
                    f"/avatars/{avatar_type.lower()}/{avatar_type.lower()}_stage_{new_growth_stage + 1}.svg"
                )
                updated_child_data["avatar_lottie_src"] = (
                    f"/lottie/avatars/{avatar_type.lower()}/stage_{new_growth_stage + 1}.json"
                )
                self.show_growth_sparkle_lottie_path = (
                    "/lottie/growth_sparkle.json"
                )
            if (
                "Streak"
                in updated_child_data[
                    "current_streak_status"
                ]
            ):
                parts = updated_child_data[
                    "current_streak_status"
                ].split()
                if len(parts) > 1 and parts[1].isdigit():
                    day_num = int(parts[1]) + 1
                    updated_child_data[
                        "current_streak_status"
                    ] = f"Day {day_num} Streak 🔥"
            else:
                updated_child_data[
                    "current_streak_status"
                ] = "Day 1 Streak 🔥"
            self.children[child_idx_to_update] = (
                updated_child_data
            )
            new_history_entry = HistoryEntry(
                id=f"hist{str(uuid.uuid4())[:8]}",
                child_id=child_id,
                activity_name=activity_details["name"],
                category_name=category_details["name"],
                category_icon=category_details["icon"],
                coins_earned=coins_earned,
                timestamp=datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat(),
            )
            self.history_entries.append(new_history_entry)
            self.activity_logged_success_message = (
                f"New Leaf! +{coins_earned} Coins 🍃"
            )
            self.mascot_message = f"Super! {updated_child_data['name']} earned {coins_earned} coins!"
        yield AppState.clear_lottie_animations_after_delay

    @rx.event
    async def clear_lottie_animations_after_delay(self):
        await asyncio.sleep(2)
        async with self:
            self.show_coin_burst_lottie_path = None
            self.show_growth_sparkle_lottie_path = None
        yield

    @rx.event
    def start_activity_logging(self):
        child_id_context = (
            self.active_child_for_world_view_id
            or self.current_child_id_for_details
        )
        if not child_id_context and self.children:
            child_id_context = self.children[0]["id"]
        if not child_id_context:
            self.mascot_message = "Please select a child from the dashboard first!"
            return
        self.current_child_id_for_details = child_id_context
        self._reset_activity_log_state()
        self.activity_log_step = "category_select"
        self.mascot_message = "Let's log something awesome!"
        yield

    @rx.event
    async def select_log_category(self, category_id: str):
        self.selected_log_category_id = category_id
        selected_cat = self.current_log_category
        if selected_cat:
            self.current_activity_log_bg_class = (
                selected_cat["background_class"]
            )
            self.mascot_message = f"Great choice! What kind of {selected_cat['name']} deed?"
        self.activity_log_step = "activity_select"
        self.activity_panel_animation_state = "entering"
        await asyncio.sleep(0.05)
        async with self:
            self.activity_panel_animation_state = "entered"
        yield

    @rx.event
    async def select_log_activity(self, activity_id: str):
        self.selected_log_activity_id = activity_id
        self.activity_log_step = "confirmation"
        self.activity_panel_animation_state = "exiting"
        await asyncio.sleep(0.3)
        async with self:
            self.activity_panel_animation_state = "exited"
        if (
            self.current_child_id_for_details
            and self.selected_log_activity_id
        ):
            current_activity = self.current_log_activity
            if current_activity:
                yield AppState.perform_activity_logging(
                    self.current_child_id_for_details,
                    self.selected_log_activity_id,
                    current_activity["coins"],
                )
                self.mascot_message = (
                    "Amazing! Look what you earned!"
                )
                self.confirmation_modal_animation_state = (
                    "entering"
                )
                await asyncio.sleep(0.05)
                async with self:
                    self.confirmation_modal_animation_state = (
                        "entered"
                    )
            else:
                self.mascot_message = "Oh no, something went wrong selecting the activity."
                self.activity_log_step = "activity_select"
        else:
            self.mascot_message = (
                "Hmm, child or activity is missing."
            )
            self.activity_log_step = "category_select"
        yield

    @rx.event
    async def close_activity_panel(self):
        self.activity_panel_animation_state = "exiting"
        await asyncio.sleep(0.3)
        async with self:
            self.activity_panel_animation_state = "exited"
            self.activity_log_step = "category_select"
            self.selected_log_category_id = None
            self.current_activity_log_bg_class = (
                "bg-sky-100"
            )
            self.mascot_message = (
                "Changed your mind? Pick a category!"
            )
        yield

    @rx.event
    async def add_another_activity(self):
        self.confirmation_modal_animation_state = "exiting"
        await asyncio.sleep(0.3)
        async with self:
            self.confirmation_modal_animation_state = (
                "exited"
            )
            self._reset_activity_log_state()
            self.activity_log_step = "category_select"
            self.mascot_message = (
                "Awesome! Let's log another great deed!"
            )
        yield

    @rx.event
    async def return_to_origin_view(self):
        if self.confirmation_modal_animation_state in [
            "entering",
            "entered",
        ]:
            self.confirmation_modal_animation_state = (
                "exiting"
            )
            await asyncio.sleep(0.3)
            async with self:
                self.confirmation_modal_animation_state = (
                    "exited"
                )
        self.activity_log_overlay_animation_state = (
            "exiting"
        )
        await asyncio.sleep(0.3)
        async with self:
            self.activity_log_overlay_animation_state = (
                "exited"
            )
            self._reset_activity_log_state()
            if self.active_child_for_world_view_id:
                self.current_view = "world_view"
                self.mascot_message = f"Back to {self.active_child_for_world_view['name']}'s world!"
            else:
                self.current_view = "dashboard"
                self.mascot_message = (
                    "Great job today! See your world grow!"
                )
        yield

    @rx.event
    async def start_custom_activity_creation(self):
        if not self.selected_log_category_id:
            self.mascot_message = "First, pick a category for your new activity!"
            yield rx.toast.error(
                "Please select a category first."
            )
            return
        if self.activity_panel_animation_state in [
            "entering",
            "entered",
        ]:
            self.activity_panel_animation_state = "exiting"
            await asyncio.sleep(0.3)
            async with self:
                self.activity_panel_animation_state = (
                    "exited"
                )
        async with self:
            self.activity_log_step = (
                "custom_create_activity"
            )
            self.custom_activity_name_input = ""
            self.custom_activity_icon_input = "💡"
            self.custom_activity_coins_slider_value = 5
            self.custom_activity_modal_animation_state = (
                "entering"
            )
            self.mascot_message = (
                "Let's create a brand new activity!"
            )
        await asyncio.sleep(0.05)
        async with self:
            self.custom_activity_modal_animation_state = (
                "entered"
            )
        yield

    @rx.event
    async def save_custom_activity(self):
        if not self.custom_activity_name_input.strip():
            yield rx.window_alert(
                "Activity name cannot be empty."
            )
            return
        if not self.selected_log_category_id:
            yield rx.window_alert("Category not selected.")
            self.custom_activity_modal_animation_state = (
                "exiting"
            )
            await asyncio.sleep(0.3)
            async with self:
                self.custom_activity_modal_animation_state = (
                    "exited"
                )
                self.activity_log_step = "category_select"
            return
        new_activity_id = (
            f"custom-act-{str(uuid.uuid4())[:8]}"
        )
        new_activity = Activity(
            id=new_activity_id,
            name=self.custom_activity_name_input.strip(),
            category_id=self.selected_log_category_id,
            icon=self.custom_activity_icon_input or "✨",
            coins=self.custom_activity_coins_slider_value,
            parent_configurable=True,
        )
        self.activities.append(new_activity)
        self.custom_activity_modal_animation_state = (
            "exiting"
        )
        await asyncio.sleep(0.3)
        async with self:
            self.custom_activity_modal_animation_state = (
                "exited"
            )
            self.mascot_message = f"'{new_activity['name']}' added! Now let's log it."
        yield AppState.select_log_activity(new_activity_id)

    @rx.event
    async def cancel_custom_activity_creation(self):
        self.custom_activity_modal_animation_state = (
            "exiting"
        )
        await asyncio.sleep(0.3)
        async with self:
            self.custom_activity_modal_animation_state = (
                "exited"
            )
            self.activity_log_step = "activity_select"
            self.mascot_message = "Okay, let's pick an existing activity then."
            if self.selected_log_category_id:
                self.activity_panel_animation_state = (
                    "entering"
                )
        if (
            self.selected_log_category_id
            and self.activity_panel_animation_state
            == "entering"
        ):
            await asyncio.sleep(0.05)
            async with self:
                self.activity_panel_animation_state = (
                    "entered"
                )
        yield

    @rx.event
    def handle_add_goal_form_submit(self, form_data: dict):
        child_id = self.current_child_id_for_details
        if not child_id:
            return rx.window_alert(
                "A child must be selected."
            )
        description = form_data.get("goal_desc", "").strip()
        reward_note_str = form_data.get("reward_note", "")
        target_coins_str = form_data.get("goal_coins")
        if not target_coins_str:
            return rx.window_alert(
                "Target coins value is required."
            )
        try:
            target_coins = int(target_coins_str)
        except ValueError:
            return rx.window_alert(
                "Invalid target coin value."
            )
        if not description or target_coins <= 0:
            return rx.window_alert(
                "Goal description and positive target coins required."
            )
        new_goal = Goal(
            id=f"goal{str(uuid.uuid4())[:8]}",
            child_id=child_id,
            description=description,
            target_coins=target_coins,
            is_achieved=False,
            real_world_reward_note=(
                reward_note_str.strip()
                if reward_note_str
                and reward_note_str.strip()
                else None
            ),
        )
        self.goals.append(new_goal)
        self.form_goal_description = ""
        self.form_goal_target_coins = 100
        self.form_goal_reward_note = ""
        selected_child_name = next(
            (
                c["name"]
                for c in self.children
                if c["id"] == child_id
            ),
            "The child",
        )
        self.mascot_message = f"A new goal for {selected_child_name}! Exciting!"
        yield rx.toast.info(
            f"New goal added for {selected_child_name}!"
        )

    @rx.event
    def complete_goal(self, goal_id: str):
        goal_idx = next(
            (
                i
                for i, g in enumerate(self.goals)
                if g["id"] == goal_id
            ),
            None,
        )
        if goal_idx is not None:
            if not self.goals[goal_idx]["is_achieved"]:
                updated_goal = self.goals[goal_idx].copy()
                updated_goal["is_achieved"] = True
                self.goals[goal_idx] = updated_goal
                child_name = next(
                    (
                        c["name"]
                        for c in self.children
                        if c["id"]
                        == updated_goal["child_id"]
                    ),
                    "Someone",
                )
                self.mascot_message = f"Hooray! {child_name} achieved goal: '{updated_goal['description']}'!"
                yield rx.toast.success(
                    f"Goal '{updated_goal['description']}' completed!"
                )
            else:
                yield rx.toast.info(
                    f"Goal '{self.goals[goal_idx]['description']}' was already complete."
                )
        else:
            yield rx.window_alert("Goal not found.")

    @rx.event
    def change_currency(self, new_currency: str):
        if new_currency in CURRENCY_SYMBOLS:
            self.selected_currency = new_currency
            self.mascot_message = f"Currency changed to {new_currency} ({self.current_currency_symbol})!"
        yield

    @rx.event
    def set_current_child_id_for_details(
        self, child_id: str | None
    ):
        self.current_child_id_for_details = child_id
        if child_id and self.selected_child_for_details:
            self.mascot_message = f"Viewing details for {self.selected_child_for_details['name']}."
        elif not child_id:
            self.mascot_message = (
                "Select a child to see more."
            )
        yield