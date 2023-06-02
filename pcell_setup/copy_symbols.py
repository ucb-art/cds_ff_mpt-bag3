# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Silicon Austria Labs
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


import argparse
import os
import pathlib
import re
import shutil
import sys


def copy_symbols(ref_path: str, dest_path: str):
    def validate_bag_prim_path(purpose: str, path: str):
        dir_name = os.path.basename(path)
        if dir_name != "BAG_prim":
            raise ValueError(f"{purpose} BAG_prim path must have basename 'BAG_prim', but got {dir_name}")
        else:
            print(f"{purpose} BAG_prim: \n\t{path}")

    validate_bag_prim_path(purpose="Reference", path=ref_path)
    validate_bag_prim_path(purpose="Destination", path=dest_path)
    print("")

    for cell in os.listdir(dest_path):
        cell_path = os.path.join(dest_path, cell)
        if not os.path.isdir(cell_path):
            continue  # skip files

        destination_sch_path = os.path.join(cell_path, "schematic")
        if not os.path.isdir(destination_sch_path):
            print(f"WARNING: ignoring cell '{cell}', missing schematic")
            continue

        destination_symbol_path = os.path.join(dest_path, cell, "symbol")
        if os.path.isdir(destination_symbol_path):
            print(f"WARNING: skipping cell '{cell}', already has a symbol")
            continue

        mapping = {
            r'^nmos4_.*$': "nmos4_standard",
            r'^pmos4_.*$': "pmos4_standard",
            r'^res_standard$': "res_standard",
            r'^res_metal_.*$': "res_metal_1",
            r'^ndio_standard$': "ndio_standard",
            r'^pdio_standard$': "pdio_standard"
        }

        for pattern, ref_cell in mapping.items():
            if re.search(pattern, cell):
                src = os.path.join(ref_path, ref_cell, "symbol")
                print(f"Copying symbol for cell '{cell}' from ref cell '{ref_cell}', \n"
                      f"\t{src} ->\n"
                      f"\t{destination_symbol_path}")
                shutil.copytree(src, destination_symbol_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='copy_symbols',
        description='Copy BAG_prim symbols from reference BAG_prim'
    )
    parser.add_argument('-r', '--ref', type=pathlib.Path, required=True,
                        help='Path to reference BAG_prim (i.e. cds_ff_mpt)')
    parser.add_argument('-d', '--dest', type=pathlib.Path, required=True,
                        help='Path to destination BAG_prim')

    args = parser.parse_args()
    copy_symbols(ref_path=str(args.ref),
                 dest_path=str(args.dest))
