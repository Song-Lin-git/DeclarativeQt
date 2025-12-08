import os
import shutil
from abc import ABC
from pathlib import Path
from typing import Union

from PyQt5.QtGui import QPixmap

from DeclarativeQt.Resource.FileTypes.RFileType import FilePath
from DeclarativeQt.Storage.RStorage import RStorage

_ThisFilePath = __file__

IconName = str


# https://fonts.google.com/icons
class IconSource(ABC):
    compress_x: IconName = "compress_x.png"
    compress_y: IconName = "compress_y.png"
    expand_x: IconName = "expand_x.png"
    expand_y: IconName = "expand_y.png"
    block_small: IconName = "block_small.png"
    block: IconName = "block.png"
    triangle: IconName = "triangle.png"
    dashdot_line: IconName = "dashdot_line.png"
    dash_line: IconName = "dash_line.png"
    solid_line: IconName = "solid_line.png"
    dot_line: IconName = "dot_line.png"
    circle: IconName = "circle.png"
    square: IconName = "square.png"
    diamond: IconName = "diamond.png"
    star: IconName = "star.png"
    format_paint: IconName = "format_paint.png"
    colors: IconName = "colors.png"
    backup_table: IconName = "backup_table.png"
    picture_as_pdf: IconName = "picture_as_pdf.png"
    docs: IconName = "docs.png"
    arrow_back: IconName = "arrow_back.png"
    sync_alt_pink: IconName = "sync_alt_pink.png"
    jump_to_element: IconName = "jump_to_element.png"
    point_scan: IconName = "point_scan.png"
    data_check: IconName = "data_check.png"
    cycle: IconName = "cycle.png"
    graph_analysis_blue: IconName = "graph_analysis_blue.png"
    monitoring_blue: IconName = "monitoring_blue.png"
    graph_analysis: IconName = "graph_analysis.png"
    content_cut: IconName = "content_cut.png"
    experiment_deepblue: IconName = "experiment_deepblue.png"
    content_copy_fill_lightblue: IconName = "content_copy_fill_lightblue.png"
    history_x: IconName = "history_x.png"
    check_circle: IconName = "check_circle.png"
    line_end_diamond: IconName = "line_end_diamond.png"
    line_start_diamond: IconName = "line_start_diamond.png"
    low_priority: IconName = "low_priority.png"
    rule_settings: IconName = "rule_settings.png"
    shift_down_fill: IconName = "shift_down_fill.png"
    shift_fill: IconName = "shift_fill.png"
    shift_down: IconName = "shift_down.png"
    shift: IconName = "shift.png"
    sync_alt_vertical: IconName = "sync_alt_vertical.png"
    manage_search_cyanblue: IconName = "manage_search_cyanblue.png"
    manage_search_green: IconName = "manage_search_green.png"
    gpp_bad: IconName = "gpp_bad.png"
    notification_important: IconName = "notification_important.png"
    notifications: IconName = "notifications.png"
    warning: IconName = "warning.png"
    join: IconName = "join.png"
    printer: IconName = "printer.png"
    image_search: IconName = "image_search.png"
    sync_alt: IconName = "sync_alt.png"
    table: IconName = "table.png"
    home_fill: IconName = "home_fill.png"
    home_fill_blue: IconName = "home_fill_blue.png"
    thermostat_carbon: IconName = "thermostat_carbon.png"
    globe_asia: IconName = "globe_asia.png"
    scale: IconName = "scale.png"
    translate: IconName = "translate.png"
    workspaces: IconName = "workspaces.png"
    settings: IconName = "settings.png"
    settings_applications: IconName = "settings_applications.png"
    toggle_on: IconName = "toggle_on.png"
    toggle_off: IconName = "toggle_off.png"
    add_chart: IconName = "add_chart.png"
    perm_media: IconName = "perm_media.png"
    monitoring: IconName = "monitoring.png"
    database_search: IconName = "database_search.png"
    share_windows_blue: IconName = "share_windows_blue.png"
    share_windows: IconName = "share_windows.png"
    menu: IconName = "menu.png"
    build: IconName = "build.png"
    content_copy_fill: IconName = "content_copy_fill.png"
    database: IconName = "database.png"
    file_export: IconName = "file_export.png"
    move_group: IconName = "move_group.png"
    document_search: IconName = "document_search.png"
    manage_search: IconName = "manage_search.png"
    description: IconName = "description.png"
    all_inclusive: IconName = "all_inclusive.png"
    vital_signs: IconName = "vital_signs.png"
    hourglass: IconName = "hourglass.png"
    compress: IconName = "compress.png"
    hourglass_top: IconName = "hourglass_top.png"
    biotech: IconName = "biotech.png"
    thermostat_arrow_down: IconName = "thermostat_arrow_down.png"
    thermostat_arrow_up: IconName = "thermostat_arrow_up.png"
    thermostat_arrow_up_orange: IconName = "thermostat_arrow_up_orange.png"
    thermostat_arrow_down_orange: IconName = "thermostat_arrow_down_orange.png"
    thermostat_arrow_up_blue: IconName = "thermostat_arrow_up_blue.png"
    thermostat_arrow_down_blue: IconName = "thermostat_arrow_down_blue.png"
    bluetooth: IconName = "bluetooth.png"
    table_chart_view: IconName = "table_chart_view.png"
    play_arrow: IconName = "play_arrow.png"
    file_copy: IconName = "file_copy.png"
    content_copy: IconName = "content_copy.png"
    backspace_red: IconName = "backspace_red.png"
    save_clock: IconName = "save_clock.png"
    experiment: IconName = "experiment.png"
    manage_accounts: IconName = "manage_accounts.png"
    person_operator: IconName = "person_operator.png"
    thermostat: IconName = "thermostat.png"
    quick_reference_all: IconName = "quick_reference_all.png"
    date_range: IconName = "date_range.png"
    today: IconName = "today.png"
    timer: IconName = "timer.png"
    disabled_by_default: IconName = "disabled_by_default.png"
    schedule: IconName = "schedule.png"
    edit_calendar: IconName = "edit_calendar.png"
    arrow_drop_down_light: IconName = "arrow_drop_down_light.png"
    arrow_drop_up_light: IconName = "arrow_drop_up_light.png"
    restart_alt: IconName = "restart_alt.png"
    data_table: IconName = "data_table.png"
    reset_image: IconName = "reset_image.png"
    history_blue: IconName = "history_blue.png"
    search: IconName = "search.png"
    mouse_cursor_colored: IconName = "mouse_cursor_colored.png"
    curve_colored: IconName = "curve_colored.png"
    package_random: IconName = "package_random.png"
    aspect_ratio: IconName = "aspect_ratio.png"
    visibility: IconName = "visibility.png"
    visibility_dark: IconName = "visibility_dark.png"
    visibility_off: IconName = "visibility_off.png"
    visibility_off_light: IconName = "visibility_off_light.png"
    open_in_full: IconName = "open_in_full.png"
    home_dark: IconName = "home_dark.png"
    delete_sweep: IconName = "delete_sweep.png"
    ink_eraser: IconName = "ink_eraser.png"
    edit_note: IconName = "edit_note.png"
    edit_square: IconName = "edit_square.png"
    edit_square_darkblue: IconName = "edit_square_darkblue.png"
    edit_square_orange: IconName = "edit_square_orange.png"
    edit_square_lightblue: IconName = "edit_square_lightblue.png"
    edit_square_mistgreen: IconName = "edit_square_mistgreen.png"
    history: IconName = "history.png"
    task_alt: IconName = "task_alt.png"
    cursor_on: IconName = "cursor_on.png"
    cursor_off: IconName = "cursor_off.png"
    expansion_panels: IconName = "expansion_panels.png"
    check_box: IconName = "check_box.png"
    check_box_outline_blank: IconName = "check_box_outline_blank.png"
    check_box_outline_blank_light: IconName = "check_box_outline_blank_light.png"
    select_check_box: IconName = "select_check_box.png"
    select_check_box_sereneblue: IconName = "select_check_box_sereneblue.png"
    check: IconName = "check.png"
    border_color: IconName = "border_color.png"
    mouse_cursor_grey: IconName = "mouse_cursor_grey.png"
    mouse_cursor_light: IconName = "mouse_cursor_light.png"
    output: IconName = "output.png"
    sync: IconName = "sync.png"
    download: IconName = "download.png"
    refresh: IconName = "refresh.png"
    view_compact: IconName = "view_compact.png"
    view_compact_grey: IconName = "view_compact_grey.png"
    border_inner_grey: IconName = "border_inner_grey.png"
    calendar_view_month: IconName = "calendar_view_month.png"
    calendar_view_month_grey: IconName = "calendar_view_month_grey.png"
    output_light: IconName = "output_light.png"
    edit_mistgreen: IconName = "edit_mistgreen.png"
    expand_circle_down: IconName = "expand_circle_down.png"
    expand_circle_up: IconName = "expand_circle_up.png"
    arrow_drop_down: IconName = "arrow_drop_down.png"
    arrow_drop_up: IconName = "arrow_drop_up.png"
    add_box: IconName = "add_box.png"
    add_circle: IconName = "add_circle.png"
    auto_awesome_mosaic: IconName = "auto_awesome_mosaic.png"
    switch_access_shortcut_add: IconName = "switch_access_shortcut_add.png"
    add_row_below: IconName = "add_row_below.png"
    delete_forever: IconName = "delete_forever.png"
    credit_score: IconName = "credit_score.png"
    backspace: IconName = "backspace.png"
    move_up: IconName = "move_up.png"
    move_down: IconName = "move_down.png"
    folder_open: IconName = "folder_open.png"
    note_add: IconName = "note_add.png"
    edit_document: IconName = "edit_document.png"
    broken_image: IconName = "broken_image.png"


class RIcon:
    Src = IconSource
    IconSourceAt = "Icons"
    SourceDirAt = Path(_ThisFilePath).parent / IconSourceAt
    CacheDirAt = RStorage().getDir(RStorage.dirIconCache)

    @staticmethod
    def loadIconPixmap(iconName: str) -> Union[QPixmap, None]:
        cachePath = RIcon.getIconCachePath(iconName)
        if not os.path.exists(cachePath):
            if RIcon.cacheIconSource(iconName) is None:
                return None
        return QPixmap(cachePath)

    @staticmethod
    def loadIconPath(iconName: str) -> Union[str, None]:
        cachePath = RIcon.getIconCachePath(iconName)
        if not os.path.exists(cachePath):
            if RIcon.cacheIconSource(iconName, pix=False) is None:
                return None
        return str(cachePath)

    @staticmethod
    def cacheIconSource(sourceName: str, pix: bool = True) -> Union[str, None]:
        sourcePath = RIcon.getIconSourcePath(sourceName)
        if not os.path.exists(sourcePath):
            return None
        cachePath = RIcon.getIconCachePath(sourceName)
        shutil.copy(sourcePath, cachePath)
        return str(sourcePath) if not pix else QPixmap(sourcePath)

    @staticmethod
    def getIconCachePath(iconName: str) -> FilePath:
        path = os.path.join(RIcon.CacheDirAt, iconName)
        return str(path)

    @staticmethod
    def getIconSourcePath(iconName: str) -> FilePath:
        path = os.path.join(RIcon.SourceDirAt, iconName)
        return str(path)
