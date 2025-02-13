import PySimpleGUI as sg
import util.colors as color
from util.CONSTANTS import *
import util.colors as color
import util.icons as ic
import util.installation_status as installation_status
from util.json_tools_projects import get_pref_project_data
from util.util import convert_string_to_list
import os
from util.path_handler import full_path

def create_layout(project,lang_data):
    main_key = '-selected_app_'
    selected_project_key = f"{main_key}{project['id']}_"
    git_Python_status = installation_status.check_git_python()

    project_pref_path_len = 0
    project_pref_def_args=""
    # project_pref_path = os.path.abspath(project['repo_name'])
    project_pref_path =  f"{full_path}\{project['repo_name']}"

    # project_pref_path_def = os.path.abspath(project['repo_name'])
    project_pref_path_def = f"{full_path}\{project['repo_name']}"

    project_pref = get_pref_project_data(project['id'])
    
    if project_pref:
        project_pref_isSet = project_pref['isSet']
        project_pref_path = project_pref['path']
        project_pref_path_len = len(project_pref_path)
        project_pref_def_args = project_pref['def_args']


    installation_status_val = installation_status.check_project(project)
    installation_status_venv = installation_status.check_project_venv(project)
    project_commit_hash = installation_status.get_last_commit_hash_local(project)

    if project_commit_hash == None:
        project_commit_hash = lang_data[LOCAL_NONE]

    launch_buttons_index = 0 if installation_status_val else 1
    launch_buttons_key = f"{main_key}func_{project['id']}_{project['launch_buttons'][launch_buttons_index]['key']}_btn-"
    launch_buttons_button_text = project['launch_buttons'][launch_buttons_index]['button_text']
    launch_buttons_disabled = not git_Python_status
    launch_buttons_button_color = (color.DIM_GREEN, color.GRAY)
    launch_buttons_mouseover_colors = (color.GRAY_9900, color.DIM_GREEN)

    launch_buttons_button = sg.Button(
        lang_data[launch_buttons_button_text],
        disabled=launch_buttons_disabled,
        button_color=launch_buttons_button_color,
        key=launch_buttons_key,
        font=FONT_H1,
        expand_x=True,
        mouseover_colors=launch_buttons_mouseover_colors
    )

    project_pref_def_args_load = convert_string_to_list(project_pref_def_args)
 
    layout = [
        [
            sg.Frame('',[        
                [
                    sg.Image(project['image_path'],key=f"{main_key}img-",background_color=color.DARK_GRAY),
                    sg.Text(project['title'],key=f"{main_key}name-",font=FONT,background_color=color.DARK_GRAY),
                    sg.Push(background_color=color.DARK_GRAY),
                ],        
                [
                    sg.Button(project['github_url'],k=f"{selected_project_key}github_btn-",font=FONT,expand_x=True,button_color=(color.DIM_BLUE,color.GRAY),mouseover_colors=(color.GRAY_9900,color.DIM_BLUE),disabled=False),
                ],                                         
                [
                    sg.Button(lang_data[LOCAL_INSTALLED_VERSION],k=f"{main_key}_{project['id']}_github_lbl-",visible=True,font=FONT,expand_x=True,size=(25,1),disabled=True),
                    sg.Button(project_commit_hash,visible=True,k=f"-{selected_project_key}commit_hash_lbl-",size=(50,1),font=FONT,expand_x=True,disabled=True)
                ],                        
                [ 
                    launch_buttons_button,
                    sg.Button(f'{lang_data[LOCAL_INSTALL]} ControlNet',visible=True if len(project['launch_buttons']) > 2 else False,
                              k=f"{selected_project_key}install_ext_btn-",font=FONT_H1,expand_x=False
                              ,mouseover_colors=launch_buttons_mouseover_colors,button_color=launch_buttons_button_color)
                ] 
                if len(project['launch_buttons']) > 2 else [
                    launch_buttons_button,
                ]
            ],key=f'{main_key}frame-',expand_x=True,expand_y=False,border_width=5,pad=(10,10),relief=sg.RELIEF_FLAT,element_justification="l",background_color=color.DARK_GRAY)
        ],  
        [
            sg.Frame("",[       
                [
                    sg.MLine(f"""{project['description'][0]}""",k=f"{main_key}description_{project['id']}_console_ml-",visible=True,text_color=color.DIM_BLUE,border_width=10,sbar_width=20,sbar_trough_color=0,
                            autoscroll=True, auto_refresh=True,expand_x=True,expand_y=True,font=FONT,no_scrollbar=False,disabled=True,size=(100,3),),
                ],                            
                ],expand_x=True,expand_y=False,border_width=5,pad=(10,10),relief=sg.RELIEF_FLAT,element_justification="l",background_color=color.DARK_GRAY)
        ] if project['description'] else [],         
        [
            sg.Frame("",[       
                [
                    sg.MLine(f"""{lang_data[LOCAL_INCOMPLETE]}""",k=f"{main_key}isIncomplete{project['id']}_console_ml-",visible=True,text_color=color.RED_ORANGE,border_width=10,sbar_width=20,sbar_trough_color=0,
                            autoscroll=True, auto_refresh=True,expand_x=True,expand_y=True,font=FONT,no_scrollbar=True,disabled=True,size=(100,3)),
                ],                            
                ],expand_x=True,expand_y=False,border_width=5,pad=(10,10),relief=sg.RELIEF_FLAT,element_justification="l",background_color=color.DARK_GRAY)
        ] if project['isIncomplete'] else [], 
        [
            sg.Frame("", [
                [
                    sg.Frame('', [
                        [
                            # sg.Image(ic.args, key=f"{main_key}args_img-", background_color=color.DARK_GRAY, size=(30, 30)),
                            sg.Text(lang_data[LOCAL_ARGUMENTS], key=f"{main_key}args_lbl-", text_color=color.LIGHT_GRAY,
                                    background_color=color.DARK_GRAY,font=FONT),
                        ],
                    ], key=f"{main_key}args_header_frame-", expand_x=True, expand_y=False, border_width=0, pad=(10, 3),
                        relief=sg.RELIEF_FLAT, element_justification="l", background_color=color.DARK_GRAY)
                ],
                [
                    sg.Column(
                        [
                            [
                                sg.Frame('', [
                                    [
                                        sg.Button(option["button_text"], disabled=False, size=(25, 1),
                                                button_color=((color.GRAY, color.DIM_GREEN) if option["button_text"] in project_pref_def_args_load else (color.DIM_BLUE, color.GRAY)),
                                                key=f"{main_key}args_{project['id']}_{option['button_text']}_btn-", font=FONT, expand_x=True,
                                                # mouseover_colors=(color.GRAY_9900, color.DIM_GREEN)
                                                ) 
                                                for option in arg
                                    ]
                                    for arg in project['args']
                                ], key=f"{main_key}_args_header_frame-", expand_x=True, expand_y=True, border_width=0,
                                    relief=sg.RELIEF_FLAT, element_justification="l", background_color=color.DARK_GRAY)
                            ]
                        ]
                        , key=f"-selected_app_scroll_frame-", element_justification='c', size=(50, 70), expand_x=True, expand_y=True,
                        visible=True, scrollable=True, vertical_scroll_only=True, background_color=color.DARK_GRAY)
                ],
            ], expand_x=True, expand_y=False, border_width=1, pad=(1, 1), relief=sg.RELIEF_FLAT, element_justification="l",
            background_color=color.DARK_GRAY)
        ] if project['args'] else [],
 
        [
            sg.Frame(lang_data[LOCAL_CUSTOM],[       
                [
                    sg.MLine(project_pref_def_args,k=f"{main_key}args_{project['id']}_console_ml-",visible=True,text_color=color.DIM_GREEN,border_width=10,sbar_width=20,sbar_trough_color=0,
                            autoscroll=True, auto_refresh=True,expand_x=True,expand_y=True,font=FONT,no_scrollbar=True),                     
                ],
                [
                            sg.Button(
                                    button_text=lang_data[LOCAL_SAVE],
                                    button_color=(color.DIM_BLUE, color.GRAY),
                                    key=f"{main_key}{project['id']}_project_save_def_args_btn-", 
                                    expand_x=True, 
                                    # expand_y=True, 
                                    font=FONT,
                                    mouseover_colors=(color.GRAY_9900, color.DIM_BLUE),
                                    # size=(10,2)
                                ),    
                ]
                                            
                ],key=f"{main_key}args_console_frame-",title_color=color.LIGHT_GRAY,expand_x=True,expand_y=True,border_width=5,pad=(5,0),relief=sg.RELIEF_FLAT,element_justification="c",background_color=color.GRAY_1111)
        ] if project['args'] else [],
        [
            sg.Frame('',[       
            [
                sg.Frame('',[       
                    [
                        # sg.Image(ic.args,key=f"{main_key}setup_img-",background_color=color.DARK_GRAY,size=(30,30)),
                        sg.Text(lang_data[LOCAL_SETUP],key=f"{main_key}setup_lbl-",text_color=color.LIGHT_GRAY,font=FONT,background_color=color.DARK_GRAY),
                    ],  
                ],key=f"{main_key}setup_header_frame-",expand_x=True,expand_y=False,border_width=0,pad=(10,3),relief=sg.RELIEF_FLAT,element_justification="l",background_color=color.DARK_GRAY)            
            ],  
            [
                sg.Frame(f"{lang_data[LOCAL_SET_CUSTOM_PROJECT_PATH]}",[      
                    [
                    sg.Button(f"{lang_data[LOCAL_IF_NOT_ACTIVATED]}, ({project_pref_path_def}) {lang_data[LOCAL_WILL_USED]}.",
                              k=f"{main_key}_{project['id']}_custom_path_lbl-",visible=True,expand_x=False,disabled=True,disabled_button_color=(color.LIGHT_GRAY, color.DIM_BLUE),button_color= (color.GRAY, color.DARK_GRAY)),
        
                    ], 
                    [
                        sg.In(default_text=project_pref_path,key=f"{main_key}{project['id']}_project_path_in-",
                              enable_events=True,expand_x=True,expand_y=True,
                              font=FONT,
                              text_color=color.GRAY if project_pref and project_pref_isSet else color.LIGHT_GRAY,  
                              background_color=color.DIM_GREEN if project_pref and project_pref_isSet else color.GRAY,  
                              ),
                        sg.FolderBrowse(button_text=lang_data[LOCAL_BROWSE],k=f"{main_key}{project['id']}_project_path_FolderBrowse-",
                            button_color=(color.DIM_BLUE, color.GRAY),
                            # size=(10,2)     
                            ),                                                  
                    ], 
                    [
                        sg.Button(
                                button_text=lang_data[LOCAL_ADD_PROJECT_NAME_FOLDER_TO_PATH],
                                button_color=(color.DIM_BLUE, color.GRAY),
                                key=f"{main_key}{project['id']}_project_path_add_folder_name_btn-", 
                                expand_x=True, 
                                mouseover_colors=(color.GRAY_9900, color.DIM_BLUE),
                                # size=(None,2)
                            ) ,        
                        sg.Button(
                                lang_data[LOCAL_SET_PATH],
                                button_color=(color.DIM_BLUE, color.GRAY),
                                key=f"{main_key}{project['id']}_project_path_set_btn-", 
                                expand_x=True, 
                                mouseover_colors=(color.GRAY_9900, color.DIM_BLUE),
                                # size=(None,2)
                            ) ,
                        sg.Button(
                                lang_data[LOCAL_ACTIVATED] if project_pref and project_pref_isSet else lang_data[LOCAL_ACTIVATE],
                                button_color= (color.DIM_GREEN, color.GRAY) if project_pref and project_pref_isSet else (color.DIM_BLUE, color.GRAY),
                                key=f"{main_key}{project['id']}_project_path_activate_btn-", 
                                expand_x=True, 
                                mouseover_colors=(color.GRAY_9900, color.DIM_BLUE),
                                disabled=False if project_pref_path_len else True,
                                # size=(55,1)
                            )    
                    ] ,
                ],key=f"{main_key}{project['id']}_project_path_frame-",title_color=color.DIM_GREEN,expand_x=True,expand_y=False,border_width=0,pad=(15,10),relief=sg.RELIEF_FLAT,element_justification="l",background_color=color.DARK_GRAY)            
            ] if project['type'] == 'app' else [
            ],             
            [
                sg.Frame("",[       
                        [
                            sg.Frame("", [
                                [
                                        sg.Button(
                                            lang_data[button['button_text']], 
                                            disabled=False if installation_status_val and git_Python_status else True,
                                            key=f"{main_key}func_{project['id']}_{button['key']}_btn-", 
                                            font=FONT, 
                                            expand_x=True, 
                                            button_color=(color.DIM_BLUE, color.GRAY), 
                                            mouseover_colors=(color.GRAY_9900, color.DIM_BLUE)
                                        )
                                    for button in project['buttons']
                                    if (installation_status_venv and button['key'] != "create_venv") or
                                    (not installation_status_venv and button['key'] != "delete_venv")
                                ]
                            ], expand_x=True, expand_y=False, relief=sg.RELIEF_FLAT, element_justification="l", background_color=color.DARK_GRAY)
                        ]
                        if installation_status_val and git_Python_status else [
                            sg.Frame("", [
                                [
                                    sg.Button(lang_data[button['button_text']], disabled=True, key=f"{main_key}func_{project['id']}_{button['key']}_btn-", font=FONT, expand_x=True, button_color=(color.DIM_BLUE, color.GRAY), mouseover_colors=(color.GRAY_9900, color.DIM_BLUE))
                                    for button in project['buttons']
                                    if (installation_status_venv and button['key'] != "create_venv") or
                                    (not installation_status_venv and button['key'] != "delete_venv")
                                ]
                            ], expand_x=True, expand_y=False, relief=sg.RELIEF_FLAT, element_justification="l", background_color=color.DARK_GRAY)
                        ]                              
                ],expand_x=True,expand_y=False,relief=sg.RELIEF_FLAT,element_justification="l",background_color=color.DARK_GRAY)
            ]             
            ],key=f"{main_key}setup_frame-",expand_x=True,expand_y=False,border_width=0,pad=(10,3),relief=sg.RELIEF_FLAT,element_justification="l",background_color=color.DARK_GRAY)            
        ],             
       
    ]
    return layout
