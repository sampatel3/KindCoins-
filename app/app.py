import reflex as rx
from app.pages.index import index_page
from app.pages.history import history_page
from app.pages.goals import goals_page
from app.pages.manage import manage_page
from app.pages.login import login_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/tailwind_colors.css"],
)
app.add_page(
    index_page, route="/", title="KindCoins Dashboard"
)
app.add_page(
    history_page,
    route="/history",
    title="History - KindCoins",
)
app.add_page(
    goals_page, route="/goals", title="Goals - KindCoins"
)
app.add_page(
    manage_page, route="/manage", title="Manage - KindCoins"
)
app.add_page(
    login_page, route="/login", title="Login - KindCoins"
)