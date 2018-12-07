from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
  import tkinter as tk
  import tkinter.ttk as ttk

  from tframe.utils.note import Note
  from tframe.utils.viewer_base.main_frame import Viewer

  from tframe.utils.summary_viewer import key_events
  from tframe.utils.summary_viewer.context import Context
  from tframe.utils.summary_viewer.header_control import HeaderControl
  from tframe.utils.summary_viewer.config_control import ConfigPanel
  from tframe.utils.summary_viewer.criterion_control import CriteriaPanel

  from tframe.utils.summary_viewer.wisdoms import rand_wisdom

except Exception as e:
  print(' ! {}'.format(e))
  print(' ! Summary Viewer is disabled, install tkinter to enable it')


class SummaryViewer(Viewer):
  """Summary Viewer for tframe summary"""
  ROOT_HEIGHT = 565
  ROOT_WIDTH = 860

  def __init__(self, summary_path=None, **kwargs):
    # Call parent's constructor
    Viewer.__init__(self)
    self.master.resizable(False, False)

    # Attributes
    self.context = Context(
      kwargs.get('default_inactive_flags', ()),
      kwargs.get('default_inactive_criteria', ()))

    # Layout
    self.header = HeaderControl(self)
    self.main_panel = ttk.Frame(self)
    self.config_panel = ConfigPanel(self.main_panel)
    self.criteria_panel = CriteriaPanel(self.main_panel)

    # Create layout and bind key events
    self._set_global_style()
    self._bind_key_events()
    self._create_layout()

    # Try to load summary
    if summary_path is not None:
      assert isinstance(summary_path, str)
      self.set_notes_by_path(summary_path)
    else:
      self.global_refresh()

    # Debug option
    self.in_debug_mode = False

  # region : Properties

  @property
  def proper_height(self):
    padding = 5
    # h_header = self.header.winfo_height()
    h_header = 31
    h_configs = self.config_panel.minimum_height
    return padding * 2 + h_header + h_configs

  # endregion : Properties

  # region : Public Methods

  def set_notes_by_path(self, summary_path):
    # Set context
    self.context.set_notes_by_path(summary_path)
    # Refresh
    self.global_refresh()

  def global_refresh(self):
    # Refresh title
    title = 'Summary Viewer'
    if self.context.summary_file_name is not None:
      title += ' - {}'.format(self.context.summary_file_name)
    self.form.title(title)

    # Initialize main panel
    self.config_panel.initialize_config_controls()
    self.criteria_panel.initialize_criteria_controls()

    # Refresh header
    self.header.refresh()

    # Do local refresh
    self.local_refresh()

    # Adjust size
    self.ROOT_HEIGHT = self.proper_height
    self._move_to_center()

  def local_refresh(self):
    # Refresh config panel
    # self.config_panel.refresh()
    self.criteria_panel.refresh()

  # endregion : Public Methods

  # region : Private Methods

  def _set_global_style(self):
    # Set white background
    set_white_bg = lambda name: self.set_style(name, background='white')

    set_white_bg(self.WidgetNames.TLabel)
    set_white_bg(self.WidgetNames.TFrame)
    set_white_bg(self.WidgetNames.TLabelframe)
    self.set_style(self.WidgetNames.TLabelframe, 'Label', background='white',
                   reverse=False)

  def _bind_key_events(self):
    # Bind Key Events
    self.form.bind('<Key>', lambda e: key_events.on_key_press(self, e))
    self.form.bind('<Control-o>', lambda e: key_events.load_notes(self, e))
    self.form.bind(
      '<Control-d>', lambda e: key_events.toggle_debug_mode(self, e))

  def _create_layout(self):
    # Header
    self.header.configure(height=50, width=600, padding=5)
    HeaderControl.COLOR = 'orange'
    self.header.load_to_master(expand=False)

    # Main panel for config panel and criterion panel
    self.main_panel.configure(height=600)
    self.main_panel.pack(fill=tk.BOTH, expand=True)

    # Config panel
    self.config_panel.configure(height=600, width=400, padding=5)
    self.config_panel.load_to_master(expand=False)

    # Criteria panel
    self.criteria_panel.configure(padding=5)
    self.criteria_panel.load_to_master(side=tk.LEFT, fill=tk.BOTH)

    # Something at the bottom
    bg_color = 'orange'
    bottom = ttk.Frame(
      self, style=self.set_style(
        self.WidgetNames.TFrame, 'bottom', background=bg_color))
    bottom.configure(height=54)
    bottom.pack(expand=True, fill=tk.BOTH)
    self.bottom = bottom

    text = rand_wisdom()
    bottom_label = ttk.Label(bottom, text=text, style=self.set_style(
      self.WidgetNames.TLabel, 'bottom', background='orange',
      foreground='orange red'), anchor=tk.CENTER)
    bottom_label.pack(fill=tk.X, expand=True)
    self.bottom_label = bottom_label

    # Pack self
    self.pack(fill=tk.BOTH, expand=True)

  # endregion : Private Methods


if __name__ == '__main__':
  from tframe.utils.summary_viewer import main_frame

  summ_path = None
  viewer = main_frame.SummaryViewer(
    summary_path=summ_path,
    default_inactive_flags=(
      'patience',
      'shuffle',
      'epoch',
      'early_stop',
      'warm_up_thres',
      'mark',
      'batch_size',
      'save_mode',
    ),
    default_inactive_criteria=(
      'Mean Record',
      # 'Record',
    )
  )
  viewer.show()


