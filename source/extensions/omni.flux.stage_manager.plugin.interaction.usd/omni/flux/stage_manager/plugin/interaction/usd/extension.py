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

import carb
import carb.settings
import omni.ext
from omni.flux.stage_manager.factory import get_instance as _get_factory_instance

from .all_lights import AllLightsInteractionPlugin as _AllLightsInteractionPlugin
from .all_materials import AllMaterialsInteractionPlugin as _AllMaterialsInteractionPlugin
from .all_prims import AllPrimsInteractionPlugin as _AllPrimsInteractionPlugin
from .all_skeletons import AllSkeletonsInteractionPlugin as _AllSkeletonsInteractionPlugin
from .all_tags import AllTagsInteractionPlugin as _AllTagsInteractionPlugin


class StageManagerUSDInteractionPluginsExtension(omni.ext.IExt):

    _PLUGINS = [
        _AllLightsInteractionPlugin,
        _AllMaterialsInteractionPlugin,
        _AllPrimsInteractionPlugin,
        _AllSkeletonsInteractionPlugin,
        _AllTagsInteractionPlugin,
    ]

    def on_startup(self, _):
        carb.log_info("[omni.flux.stage_manager.plugin.interaction.usd] Startup")

        _get_factory_instance().register_plugins(self._PLUGINS)

    def on_shutdown(self):
        carb.log_info("[omni.flux.stage_manager.plugin.interaction.usd] Shutdown")

        _get_factory_instance().unregister_plugins(self._PLUGINS)
