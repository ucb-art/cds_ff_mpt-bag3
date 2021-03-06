# SPDX-License-Identifier: Apache-2.0
# Copyright 2020 Blue Cheetah Analog Design Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

from typing import Any


from bag.design.module import ResMetalModule
from bag.design.database import ModuleDB
from bag.util.immutable import Param


# noinspection PyPep8Naming
class BAG_prim__res_metal_8(ResMetalModule):
    """design module for BAG_prim__res_metal_8.
    """

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        ResMetalModule.__init__(self, '', database, params, **kwargs)

