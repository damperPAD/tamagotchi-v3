from ._anvil_designer import Form1Template
from anvil import *
import anvil.server


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btn_create_pet_click(self, **event_args):
    """This method is called when the button is clicked"""
    pet_type = self.drop_down_pet_type.selected_value
    name = self.text_box_name.text
    if pet_type and name:
        status = anvil.server.call('create_pet', pet_type, name)
        self.update_ui(status)

  def update_ui(self, status):
    if not status:
        return # do nothing if there's no valid status
    self.label_name.text = f"Name: {status['Name']}"
    self.label_type.text = f"Type: {status['Type']}"
    self.label_hunger.text = f"Hunger: {status['Hunger']}"
    self.label_happiness.text = f"Happiness: {status['Happiness']}"
    self.label_energy.text = f"Energy: {status['Energy']}"

  def btn_feed_click(self, **event_args):
    print("feed me")
    status = anvil.server.call('interact_with_pet', 'feed')
    self.update_ui(status)
  
  def btn_play_click(self, **event_args):
    print("Play with me")
    status = anvil.server.call('interact_with_pet', 'play')
    self.update_ui(status)
  
  def btn_sleep_click(self, **event_args):
    print("time to sleep")
    status = anvil.server.call('interact_with_pet', 'sleep')
    self.update_ui(status)

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    status = anvil.server.call('pet_tick')
    self.update_ui(status)
