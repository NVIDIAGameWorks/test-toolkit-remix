"""
* SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
* SPDX-License-Identifier: Apache-2.0
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
"""

__all__ = ["FluxPyCharmDebuggerExtension"]

import carb
import omni.ext

from .core import PyCharmDebuggerCore


class FluxPyCharmDebuggerExtension(omni.ext.IExt):
    def __init__(self):
        self._core = None

        super().__init__()

    def on_startup(self, ext_id):
        carb.log_info("[omni.flux.debug.pycharm] Flux PyCharm Debugger startup")

        self._core = PyCharmDebuggerCore(ext_id)
        self._core.setup()

    def on_shutdown(self):
        carb.log_info("[omni.flux.debug.pycharm] Flux PyCharm Debugger startup")

        self._core = None
