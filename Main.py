from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle
from datetime import datetime

# Set window size to mobile dimensions
Window.size = (360, 800)

class HillmeadFarmApp(App):
    def build(self):
        # Main screen
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header with title and notification icon
        header_layout = BoxLayout(size_hint_y=0.1, spacing=20)
        header_layout.add_widget(Label(text='←', font_size='24sp', size_hint_x=0.1))
        header_layout.add_widget(Label(text='Hillmead Farm', font_size='20sp', bold=True, size_hint_x=0.8))
        header_layout.add_widget(Label(text='👤\n1', font_size='16sp', size_hint_x=0.1))
        
        main_layout.add_widget(header_layout)
        
        # Date section
        today = datetime.now().strftime('%A %B %#d').replace('#', '')
        date_label = Label(
            text=f'⚠ {today}',
            font_size='16sp',
            size_hint_y=0.08,
            color=(1, 1, 1, 1)
        )
        with date_label.canvas.before:
            Color(0.9, 0.2, 0.2, 0.8)
            Rectangle(size=date_label.size, pos=date_label.pos)
        main_layout.add_widget(date_label)
        
        # Grid of icons/buttons (3 columns, 4 rows)
        grid = GridLayout(cols=3, spacing=15, padding=10, size_hint_y=0.82)
        
        # Define buttons with their notifications
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
            
            # Main button
            btn = Button(
            text=f'{icon}\n{label_text}',
            font_size='14sp',
            font_name='C:/Windows/Fonts/seguiemj.ttf',
            background_color=(0.6, 0.5, 0.7, 1),
            size_hint=(1, 1)
        )
            
            # Bind click event
            btn.bind(on_press=lambda x, text=label_text: self.on_button_click(text))
            btn_layout.add_widget(btn)
            
            # Notification badge
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
                    Rectangle(size=badge.size, pos=badge.pos)
                btn_layout.add_widget(badge)
            
            grid.add_widget(btn_layout)
        
        main_layout.add_widget(grid)
        
        return main_layout
    
    def on_button_click(self, button_name):
        """Handle button clicks"""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=f'{button_name} section opened!', font_size='18sp'))
        
        close_btn = Button(text='Close', size_hint_y=0.3)
        popup_layout.add_widget(close_btn)
        
        popup = Popup(title=button_name, content=popup_layout, size_hint=(0.9, 0.5))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    HillmeadFarmApp().run()