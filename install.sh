#!/usr/bin/env bash
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


export TECH_DIR="cds_ff_mpt"
export ROOT_DIR="${TECH_DIR}/workspace_setup"

# files to copy from workspace_setup
cp_files=( ".cdsenv.personal"
           ".cdsinit.personal"
           "bag_submodules.yaml" )

# files to link from workspace_setup
ln_files=( "bag_config.yaml"
           ".cdsenv"
           ".cdsinit"
           ".bashrc"
           ".bashrc_bag"
           "cds.lib.core"
           "display.drf"
           "models"
           ".gitignore"
           "leBindKeys.il"
           "pvtech.lib"
           "tutorial_files"
           "start_tutorial.sh" )

# user configuration files; copy
for f in "${cp_files[@]}"; do
    cp ${ROOT_DIR}/${f} .
    git add -f ${f}
done

# standard configuration files; symlink
for f in "${ln_files[@]}"; do
    ln -s ${ROOT_DIR}/${f} .
    git add -f ${f}
done

# setup .ipython
export CUR_DIR=".ipython/profile_default"
mkdir -p ${CUR_DIR}
ln -s "../../${ROOT_DIR}/ipython_config.py" "${CUR_DIR}/ipython_config.py"
git add -f ${CUR_DIR}/ipython_config.py

# setup gen_libs folder
mkdir gen_libs
touch gen_libs/.gitignore
git add -f gen_libs/.gitignore

# setup cds.lib
echo 'INCLUDE $BAG_WORK_DIR/cds.lib.core' > cds.lib

# link BAG run scripts
ln -s BAG_framework/run_scripts/start_bag_ICADV12d3.il start_bag.il
ln -s BAG_framework/run_scripts/start_bag.sh .
ln -s BAG_framework/run_scripts/run_bag.sh .
ln -s BAG_framework/run_scripts/virt_server.sh .
ln -s BAG_framework/run_scripts/setup_submodules.py .
git add start_bag.il
git add start_bag.sh
git add run_bag.sh
git add virt_server.sh
git add setup_submodules.py

# copy over transistor characterization examples
# cp -r ${TECH_DIR}/specs_mos_char .
# git add specs_mos_char
# cp -r ${TECH_DIR}/scripts_char .
# git add scripts_char
# mkdir data
# cp -r ${TECH_DIR}/mos_data/nch_w4 data/
# cp -r ${TECH_DIR}/mos_data/pch_w4 data/
