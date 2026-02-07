from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from datetime import datetime

# Set window size
Window.size = (360, 800)


# ---------- Login Screen ----------
class LoginScreen(Screen):
    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=15)

        title = Label(
            text="Welcome to Hillmead Farm",
            font_size="22sp",
            size_hint_y=None,
            height=60
        )
        root.add_widget(title)

        # Form card
        card = BoxLayout(orientation="vertical", padding=20, spacing=12, size_hint=(1, None))
        card.height = 320

        # Light background card look
        with card.canvas.before:
            Color(1, 1, 1, 1)
            self.card_rect = Rectangle(pos=card.pos, size=card.size)
        card.bind(pos=self._update_card_rect, size=self._update_card_rect)

        self.username = TextInput(
            hint_text="username or email",
            multiline=False,
            size_hint_y=None,
            height=45
        )
        self.password = TextInput(
            hint_text="password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=45
        )

        remember_row = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=35)
        self.remember = CheckBox(active=False, size_hint=(None, None), size=(35, 35))
        remember_row.add_widget(self.remember)
        remember_row.add_widget(Label(text="Remember Me", halign="left", valign="middle"))
        remember_row.add_widget(Label(text=""))  # spacer

        login_btn = Button(
            text="LOG IN",
            size_hint_y=None,
            height=45
        )
        login_btn.bind(on_press=self.try_login)

        card.add_widget(self.username)
        card.add_widget(self.password)
        card.add_widget(remember_row)
        card.add_widget(login_btn)

        root.add_widget(card)

        help_lbl = Label(
            text="Help? Click on ? at the top of each page.",
            size_hint_y=None,
            height=40
        )
        root.add_widget(help_lbl)

        return root

    def _update_card_rect(self, instance, _):
        self.card_rect.pos = instance.pos
        self.card_rect.size = instance.size

    def on_pre_enter(self, *args):
        # Build UI once when the screen is shown first time
        if not self.children:
            self.add_widget(self.build_ui())

    def try_login(self, *_):
        user = self.username.text.strip()
        pw = self.password.text

        # TODO: Replace with real authentication
        if user and pw:
            self.manager.current = "main"
        else:
            Popup(
                title="Login failed",
                content=Label(text="Enter a username/email and password."),
                size_hint=(0.8, 0.3),
            ).open()


# ---------- Main Screen (your existing UI) ----------
class MainScreen(Screen):
    def on_pre_enter(self, *args):
        if not self.children:
            self.add_widget(self.build_ui())

    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        header_layout = BoxLayout(size_hint_y=0.1, spacing=20)
        header_layout.add_widget(Label(text='←', font_size='24sp', size_hint_x=0.1))
        header_layout.add_widget(Label(text='Hillmead Farm', font_size='20sp', bold=True, size_hint_x=0.8))
        header_layout.add_widget(Label(text='👤\n1', font_size='16sp', size_hint_x=0.1))
        main_layout.add_widget(header_layout)

        today = datetime.now().strftime('%A %B %d').lstrip("0")
        date_label = Label(
            text=f'⚠ {today}',
            font_size='16sp',
            size_hint_y=0.08,
            color=(1, 1, 1, 1)
        )

        # IMPORTANT: keep rectangle synced with label pos/size
        with date_label.canvas.before:
            Color(0.9, 0.2, 0.2, 0.8)
            rect = Rectangle(size=date_label.size, pos=date_label.pos)

        def update_rect(_instance, _value):
            rect.size = date_label.size
            rect.pos = date_label.pos

        date_label.bind(size=update_rect, pos=update_rect)
        main_layout.add_widget(date_label)

        grid = GridLayout(cols=3, spacing=15, padding=10, size_hint_y=0.82)

        buttons_data = [
            ('🐴', 'Horses', '1'),
            ('✓', 'Visits', '1'),
            ('🍎', 'Feeds', '1'),
            ('💉', 'Vaccines', '3'),
            ('⚗️', 'Worming', '0'),
            ('🔨', 'Farrier', '5'),
            ('🦷', 'Dentist', '0'),
            ('📋', 'Member', '1'),
            ('📄', 'Lists', '0'),
            ('⚙️', 'Turnout', '1'),
            ('🏆', 'Shows', '0'),
            ('🏠', 'Stables', '1'),
        ]

        for icon, label_text, notification in buttons_data:
            btn_layout = RelativeLayout()

            btn = Button(
                text=f'{icon}\n{label_text}',
                font_size='14sp',
                background_color=(0.6, 0.5, 0.7, 1),
                size_hint=(1, 1)
            )
            btn.bind(on_press=lambda _x, text=label_text: self.on_button_click(text))
            btn_layout.add_widget(btn)

            if notification != '0':
                badge = Label(
                    text=notification,
                    font_size='12sp',
                    size_hint=(None, None),
                    size=(30, 30),
                    pos_hint={'right': 1, 'top': 1},
                    color=(1, 1, 1, 1)
                )
                with badge.canvas.before:
                    Color(1, 0.2, 0.2, 1)
                    badge_rect = Rectangle(size=badge.size, pos=badge.pos)

                def update_badge_rect(_instance, _value, b=badge, r=badge_rect):
                    r.size = b.size
                    r.pos = b.pos

                badge.bind(size=update_badge_rect, pos=update_badge_rect)
                btn_layout.add_widget(badge)

            grid.add_widget(btn_layout)

        main_layout.add_widget(grid)
        return main_layout

    def on_button_click(self, button_name):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=f'{button_name} section opened!', font_size='18sp'))

        close_btn = Button(text='Close', size_hint_y=0.3)
        popup_layout.add_widget(close_btn)

        popup = Popup(title=button_name, content=popup_layout, size_hint=(0.9, 0.5))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


# ---------- App ----------
class HillmeadFarmApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MainScreen(name="main"))
        sm.current = "login"
        return sm


if __name__ == '__main__':
    HillmeadFarmApp().run()
