#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/14

import os
import logging
import coloredlogs

from myimporter.utils.settings import MYIMPORTER_COLOREDLOGS_FORMAT, COLOREDLOGS_LEVEL_STYLES_CUSTOMIZED_COLOR_SETS


def setup_logging(files_names, envar_name=None):
    logger = logging.getLogger(files_names)

    # 如果已经有处理器了，说明日志系统已经配置好了，不需要重复配置
    if logger.handlers:
        return logger

    level = logging.INFO

    if envar_name and os.getenv(envar_name) == "1":
        level = logging.DEBUG

    level_styles = coloredlogs.DEFAULT_LEVEL_STYLES.copy()
    level_styles["debug"] = COLOREDLOGS_LEVEL_STYLES_CUSTOMIZED_COLOR_SETS["debug"]
    level_styles["info"] = COLOREDLOGS_LEVEL_STYLES_CUSTOMIZED_COLOR_SETS["info"]
    level_styles["warning"] = COLOREDLOGS_LEVEL_STYLES_CUSTOMIZED_COLOR_SETS["warning"]
    level_styles["error"] = COLOREDLOGS_LEVEL_STYLES_CUSTOMIZED_COLOR_SETS["error"]

    coloredlogs.install(level=level, logger=logger, level_styles=level_styles, fmt=MYIMPORTER_COLOREDLOGS_FORMAT)

    return logger
