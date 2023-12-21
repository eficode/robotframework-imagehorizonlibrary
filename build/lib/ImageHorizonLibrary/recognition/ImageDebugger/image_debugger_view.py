import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from .image_manipulation import ImageFormat

class UILocatorView(Tk):
    def __init__(self, controller, image_container, image_horizon_instance):
        super().__init__()
        self.title("ImageHorizonLibrary - Debugger")
        self.resizable(False, False)
        self.controller = controller
        self.image_container = image_container
        self.image_horizon_instance = image_horizon_instance
        self.def_save_loc = tk.StringVar()
        self.ref_img_loc = tk.StringVar()
        self.needle_img_blank = ImageTk.PhotoImage(Image.new('RGB', (30, 30), color='white'))
        self.haystack_img_blank = ImageTk.PhotoImage(Image.new('RGB', (384, 216), color='white'))
        self._create_view()

    def main(self):
        self.mainloop()

    def _create_view(self):
        self._menu()
        self._frame_main()
        self._frame_load_reference_image()
        self._frame_computation_params()
        self._frame_results()
        self._frame_image_viewer()
        self._status_bar()

    def _menu(self):
        # ***************** Menu ******************* #
        menu = Menu(self)
        self.config(menu=menu)
        menu.add_command(label="Online Help", command=self.controller.help)

    def _frame_main(self):
        # *************** Frame Main *************** #
        self.frame_main = Frame(self)
        self.frame_main.pack(side=TOP, padx=2, pady=2)

    def _frame_load_reference_image(self):
        # ************ Frame Select image ************ #
        frame_import_ref_image = LabelFrame(self.frame_main, text="Select reference image (.png)", padx=2, pady=2)
        frame_import_ref_image.pack(side=TOP, padx=2, pady=2, fill=X)
        Label(frame_import_ref_image, text="Reference directory path:").pack(side=TOP, anchor=W)
        self.ref_dir_path = StringVar(frame_import_ref_image)
        self.label_ref_dir_path = Label(frame_import_ref_image, textvariable=self.ref_dir_path, fg='green')
        self.label_ref_dir_path.pack(side=TOP, anchor=W)
        
        self.combobox_needle_img_name = ttk.Combobox(frame_import_ref_image, width=70, state="readonly")
        self.controller.load_needle_image_names(self.combobox_needle_img_name)
        self.combobox_needle_img_name.pack(pady=(0,0), side=LEFT, anchor=W)
        self.combobox_needle_img_name.bind("<<ComboboxSelected>>", self.controller.on_select)
        self.btn_copy_strategy_snippet = Button(frame_import_ref_image, text='Refresh', command=self.controller.refresh)
        self.btn_copy_strategy_snippet.pack(side=RIGHT, padx=(2, 0), anchor=E)
    
    def _frame_computation_params(self):
        # ************ Frame Computation ************ #
        frame_computation = LabelFrame(self.frame_main, text="Computation", padx=2, pady=2)
        frame_computation.pack(side=TOP, padx=2, pady=2, fill=X)

        frame_computation.columnconfigure(0, weight=1)
        frame_computation.columnconfigure(1, weight=1)
        
        # ************ Frame default strategy (pyAutogui) ************* #
        self.frame_default_strat = LabelFrame(frame_computation, text="Default strategy", padx=2, pady=2)
        self.frame_default_strat.grid(row=0, column=0, padx=2, pady=2, sticky="WNS")

        self.frame_default_strat.columnconfigure(0, weight=3)
        self.frame_default_strat.columnconfigure(1, weight=1)

        self.frame_default_strat.bind("<Enter>", self._default_strategy_config_enter)
        self.frame_default_strat.bind("<Leave>", self._clear_statusbar)

        Label(self.frame_default_strat, text="Confidence factor").grid(row=0, column=0, sticky=SW)
        self.scale_conf_lvl_ag = Scale(self.frame_default_strat, from_=0.75, to=1.0, resolution=0.01, orient=HORIZONTAL)
        self.scale_conf_lvl_ag.grid(padx=(2, 0), row=0, column=1, sticky=E)

        self.btn_run_pyautogui = Button(frame_computation, text='Detect reference image', command=self.controller.on_click_run_default_strategy)
        self.btn_run_pyautogui.grid(row=1, column=0, padx=2, sticky=W)

        # ************ Frame edge detection strategy (edge) ************ #
        self.frame_edge_detec_strat = LabelFrame(frame_computation, text="Edge detection strategy", padx=2, pady=2)
        self.frame_edge_detec_strat.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        self.frame_edge_detec_strat.columnconfigure(0, weight=3)
        self.frame_edge_detec_strat.columnconfigure(1, weight=1)
        
        self.frame_edge_detec_strat.bind("<Enter>", self._edge_detec_strategy_config_enter)
        self.frame_edge_detec_strat.bind("<Leave>", self._clear_statusbar)

        Label(self.frame_edge_detec_strat, text="Gaussian width (sigma)").grid(row=0, column=0, sticky=SW)
        self.scale_sigma_skimage = Scale(self.frame_edge_detec_strat, from_=0.0, to=5.0, resolution=0.01, orient=HORIZONTAL)
        self.scale_sigma_skimage.grid(padx=(2, 0), row=0, column=1, sticky=E)

        Label(self.frame_edge_detec_strat, text="Lower hysteresis threshold").grid(row=1, column=0, sticky=SW)
        self.scale_low_thres_skimage = Scale(self.frame_edge_detec_strat, from_=0.0, to=10.0, resolution=0.01, orient=HORIZONTAL)
        self.scale_low_thres_skimage.grid(padx=(2, 0), row=1, column=1, sticky=E)

        Label(self.frame_edge_detec_strat, text="Higher hysteresis threshold").grid(row=2, column=0, sticky=SW)
        self.scale_high_thres_skimage = Scale(self.frame_edge_detec_strat, from_=0.0, to=10.0, resolution=0.01, orient=HORIZONTAL)
        self.scale_high_thres_skimage.grid(padx=(2, 0), row=2, column=1, sticky=E)

        Label(self.frame_edge_detec_strat, text="Confidence factor").grid(row=3, column=0, sticky=SW)
        self.scale_conf_lvl_skimage = Scale(self.frame_edge_detec_strat, from_=0.75, to=1.0, resolution=0.01, orient=HORIZONTAL)
        self.scale_conf_lvl_skimage.grid(padx=(2, 0), row=3, column=1, sticky=E)

        self.btn_run_skimage = Button(frame_computation, text='Detect reference image', command=self.controller.on_click_run_edge_detec_strategy)
        self.btn_run_skimage.grid(row=1, column=1, padx=2, sticky=W)
        self.btn_edge_detec_debugger = Button(frame_computation, text='Edge detection debugger', command=self.controller.on_click_plot_results_skimage)
        self.btn_edge_detec_debugger.grid(row=2, column=1, padx=2, sticky=W)

    def _frame_results(self):
        # ************ Frame Results ************ #
        frame_results = LabelFrame(self.frame_main, text="Results", padx=2, pady=2)
        frame_results.pack(side=TOP, padx=2, pady=2, fill=X)

        frame_results_details = Frame(frame_results)
        frame_results_details.pack(side=TOP, fill=X)
 
        Label(frame_results_details, text="Matches found / (Max peak value):").grid(pady=(2, 0), row=0, column=0, sticky=W)
        self.matches_found = StringVar(frame_results_details)
        self.label_matches_found = Label(frame_results_details, textvariable=self.matches_found)
        self.label_matches_found.grid(pady=(2, 0), row=0, column=1, sticky=W)

        frame_snippet = Frame(frame_results)
        frame_snippet.pack(side=TOP, fill=X)
        Label(frame_snippet, text="Keyword to use this strategy:").pack(pady=(2, 0), side=TOP, anchor=W)
        self.set_strategy_snippet = StringVar(frame_snippet)
        self.label_strategy_snippet = Entry(frame_snippet, textvariable=self.set_strategy_snippet, width=75)
        self.label_strategy_snippet.pack(pady=(0, 0), side=LEFT, anchor=W)
        self.btn_copy_strategy_snippet = Button(frame_snippet, text='Copy', command=self.controller.copy_to_clipboard)
        self.btn_copy_strategy_snippet.pack(side=RIGHT, padx=(2, 0), anchor=E)

    def _frame_image_viewer(self):
        # ************ Image viewer ************ #
        self.frame_image_viewer = LabelFrame(self.frame_main, text="Image viewer", padx=2, pady=2)
        self.frame_image_viewer.pack(side=TOP, padx=2, pady=2, fill=X)

        self.canvas_desktop_img = Canvas(self.frame_image_viewer, width=384, height=216)
        self.canvas_desktop_img.grid(row=3, column=0, sticky="WSEN")
        self.desktop_img = self.canvas_desktop_img.create_image(384/2, 216/2, image=self.haystack_img_blank)
        self.canvas_desktop_img.bind("<Button-1>", self._img_viewer_click)
        self.canvas_desktop_img.bind("<Enter>", self._img_viewer_hover_enter)
        self.canvas_desktop_img.bind("<Leave>", self._clear_statusbar)

        self.canvas_ref_img = Canvas(self.frame_image_viewer, width=1, height=1)
        self.canvas_ref_img.grid(row=3, column=1, sticky="WSEN")
        self.ref_img = self.canvas_ref_img.create_image(47.5, 216/2, image=self.needle_img_blank)

        Label(self.frame_image_viewer, text="Desktop").grid(pady=(0, 0), row=4, column=0, sticky="WSEN")
        Label(self.frame_image_viewer, text="Reference Image").grid(pady=(0, 0), row=4, column=1, sticky="WSEN")

    
    # ************* Status bar *************** #
    def _status_bar(self):
        self.frame_statusBar = Frame(self)
        self.frame_statusBar.pack(side=TOP, fill=X, expand=True)
        self.hint_msg = StringVar()
        self.label_statusBar = Label(self.frame_statusBar, textvariable=self.hint_msg, bd=1, relief=SUNKEN, anchor=W)
        self.label_statusBar.pack(side=BOTTOM, fill=X, expand=True)

    
    # ************** Bindings *************** #

    def _img_viewer_click(self, event=None):
        if (self.processing_done):
            self.haystack_img = self.image_container.get_haystack_image_orig_size(format=ImageFormat.IMAGETK)
            img_viewer_window = Toplevel(self)
            img_viewer_window.title("Image Viewer")
            label_img_viewer = Label(img_viewer_window, image=self.haystack_img)
            label_img_viewer.pack()

    # **** Bindings for hints (statusbar) **** #

    def _img_viewer_hover_enter(self, event=None):
        if (self.processing_done):
            self.label_statusBar.config(fg="BLACK")
            self.hint_msg.set("Click to view in full screen")
    
    def _default_strategy_config_enter(self, event=None):
        self.label_statusBar.config(fg="BLACK")
        self.hint_msg.set("Configure default strategy (default) parameters")

    def _edge_detec_strategy_config_enter(self, event=None):
        self.label_statusBar.config(fg="BLACK")
        self.hint_msg.set("Configure edge detection strategy (edge) parameters") 

    def _threshold_error(self):
        self.label_statusBar.config(fg="RED")
        self.hint_msg.set("Higher threshold value must be greater than the lower threshold value!")

    def _ready(self):
        self.label_statusBar.config(fg="BLACK")
        self.hint_msg.set("Ready")

    def _clear_statusbar(self, event=None):
        self.hint_msg.set("")
