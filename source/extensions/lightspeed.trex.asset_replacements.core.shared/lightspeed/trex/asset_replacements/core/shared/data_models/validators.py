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

__all__ = ["AssetReplacementsValidators"]

import re
from pathlib import Path

import omni.usd
from lightspeed.common import constants
from lightspeed.trex.utils.common.asset_utils import is_asset_ingested
from lightspeed.trex.utils.common.prim_utils import is_material_prototype
from omni.flux.utils.common import path_utils
from omni.flux.utils.common.omni_url import OmniUrl
from pxr import Sdf


class AssetReplacementsValidators:
    @classmethod
    def is_valid_prim(cls, prim_path: str, context_name: str):
        try:
            path = Sdf.Path(prim_path)
            if not path:
                raise ValueError("Invalid prim path")
        except Exception as e:
            raise ValueError(f"The string is not a valid prim path: {prim_path}") from e

        if not omni.usd.get_context(context_name).get_stage().GetPrimAtPath(path):
            raise ValueError(f"The prim path does not exist in the current stage: {prim_path}")

        return prim_path

    @classmethod
    def is_valid_mesh(cls, prim_path: str):
        if not re.match(constants.REGEX_MESH_PATH, prim_path):
            raise ValueError(f"The prim path does not point to a model: {prim_path}")

        return prim_path

    @classmethod
    def is_valid_material(cls, prim_path: str, context_name: str):
        prim = omni.usd.get_context(context_name).get_stage().GetPrimAtPath(prim_path)
        if not prim:
            raise ValueError(f"The prim path does not exist in the current stage: {prim_path}")

        if not is_material_prototype(prim):
            raise ValueError(f"The prim path does not point to a material: {prim_path}")

        return prim_path

    @classmethod
    def has_at_least_one_ref(cls, prim_path: str, context_name: str):
        prim = omni.usd.get_context(context_name).get_stage().GetPrimAtPath(prim_path)
        references = omni.usd.get_composed_references_from_prim(prim)

        if not references:
            raise ValueError("The selected prim has no references")

        return prim_path

    @classmethod
    def ref_exists_in_prim(cls, asset_path: Path, layer_id: Path, prim_path: str, context_name: str):
        prim = omni.usd.get_context(context_name).get_stage().GetPrimAtPath(prim_path)
        references = omni.usd.get_composed_references_from_prim(prim)

        for reference, layer in references:
            if (
                OmniUrl(reference.assetPath).path == OmniUrl(asset_path).path
                and OmniUrl(layer.identifier).path == OmniUrl(layer_id).path
            ):
                return prim_path

        raise ValueError(f"The reference ({asset_path}) does not exist for prim: {prim_path}")

    @classmethod
    def is_valid_file_path(cls, asset_path: Path):
        if not path_utils.is_file_path_valid(str(asset_path), log_error=False):
            raise ValueError(f"The file path is invalid: {asset_path}")
        return asset_path

    @classmethod
    def is_asset_ingested(cls, asset_path: Path):
        if not is_asset_ingested(asset_path):
            raise ValueError(
                f"The asset path is not valid. Assets must be ingested before they can be referenced: {asset_path}"
            )

        return asset_path

    @classmethod
    def layer_is_in_project(cls, layer_id: Path | None, context_name: str):
        if layer_id is None:
            return layer_id

        layer = Sdf.Layer.FindOrOpen(str(layer_id))
        if not layer:
            raise ValueError(f"The layer does not exist: {layer_id}")

        stage = omni.usd.get_context(context_name).get_stage()
        project_layer_ids = [
            _layer.identifier for _layer in stage.GetLayerStack(includeSessionLayers=False)
        ] + stage.GetMutedLayers()

        # Make sure the layer is in the currently opened project
        if layer.identifier not in project_layer_ids:
            raise ValueError(f"The layer is not present in the loaded project's layer stack: {layer_id}")

        return layer_id
