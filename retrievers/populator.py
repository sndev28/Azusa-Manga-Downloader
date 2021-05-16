from retrievers.helpers import chapter_list_generator
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label


def chapter_list_populator(kivy_object):

    print('meh')

    chapter_list = chapter_list_generator(kivy_object.ids.url.text)

    chapter_list.reverse()

    checkboxes = []

    for chapter in chapter_list:

        checkbox = CheckBox(color = 'black', height = 10, size_hint_y = None, size_hint_x = .05)
        label = Label(text = chapter['Chapter Name'],  color = 'black', size_hint_x = None, font_size = 14, size_hint_y = None, height = 10, valign = 'middle', halign = 'left', width = 320)
        checkbox.active = True
        checkboxes.append(checkbox)

        kivy_object.ids.chapter_list_scroll.add_widget(checkbox)
        kivy_object.ids.chapter_list_scroll.add_widget(label)

    return checkboxes