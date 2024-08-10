#!/usr/bin/env python3
import i3ipc

i3 = i3ipc.Connection()

def get_windows_in_workspace(workspace_num):
    tree = i3.get_tree()
    windows = []
    for node in tree.descendants():
        if node.window and node.workspace():
            workspace = node.workspace()
            if workspace and workspace.num == workspace_num:
                windows.append(node)
    return windows

def rename_workspaces():
    workspaces = i3.get_workspaces()
    for ws in workspaces:
        windows = get_windows_in_workspace(ws.num)
        if not windows:
            new_name = f"{ws.num}: Empty"
        else:
            window_names = [w.window_class for w in windows if w.window_class]
            unique_window_names = list(set(window_names))
            new_name = f"{ws.num}: {' + '.join(unique_window_names)}"
        i3.command(f'rename workspace "{ws.name}" to "{new_name}"')

def on_window_event(i3, event):
    rename_workspaces()

# Initial rename
rename_workspaces()

# Listen for window events
i3.on("window::new", on_window_event)
i3.on("window::close", on_window_event)
i3.on("window::move", on_window_event)
i3.on("window::title", on_window_event)

i3.main()

