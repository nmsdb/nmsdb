from nmsdb.core.models.navigation import (
    NavigationGroup,
    NavigationItem,
    NavigationItemChild,
    NavLink,
)

NAV = [
    NavigationGroup(
        nav_items=[
            NavigationItem(
                title="Resources and Items",
                children=[
                    NavigationItemChild(
                        title="Substances",
                        route=NavLink(url="ui_substances_page"),
                    ),
                    NavigationItemChild(
                        title="Products",
                        route=NavLink(url="ui_products_page"),
                    ),
                ],
                logo="fa-solid fa-boxes-stacked",
            ),
            NavigationItem(
                title="Building Technologies",
                children=[
                    NavigationItemChild(
                        title="Coming Soon!",
                        route=NavLink(type="href", url="#"),
                    ),
                ],
                logo="fa-solid fa-hammer",
            ),
            NavigationItem(
                title="Weapons and Tools",
                children=[
                    NavigationItemChild(
                        title="Coming Soon!",
                        route=NavLink(type="href", url="#"),
                    ),
                ],
                logo="fa-solid fa-screwdriver-wrench",
            ),
        ]
    ),
    NavigationGroup(
        nav_items=[
            NavigationItem(
                title="Ships",
                route=NavLink(type="url_for", url="account_page"),
                children=[
                    NavigationItemChild(
                        title="Active Subscriptions",
                        route=NavLink(type="href", url="#"),
                    ),
                    NavigationItemChild(
                        title="Settings",
                        route=NavLink(type="href", url="#"),
                    ),
                    NavigationItemChild(
                        title="Invoices",
                        route=NavLink(type="href", url="#"),
                    ),
                ],
                logo="fa-solid fa-rocket",
            ),
            NavigationItem(
                title="Place Holder",
                route=NavLink(type="href", url="#"),
                logo="fa-regular fa-square",
            ),
        ],
        has_top_border=True,
    ),
]
