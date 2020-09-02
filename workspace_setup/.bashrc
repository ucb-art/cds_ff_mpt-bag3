#! /usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2019 Blue Cheetah Analog Design Inc.
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
# clear out PYTHONPATH
export PYTHONPATH=""

### Setup BAG
source .bashrc_bag

# location of various tools
export CDS_INST_DIR=/tools/cadence/ICADVM/ICADVM181
export PVS_HOME=/tools/cadence/PVS/PVS151
export SPECTRE_HOME=/tools/cadence/SPECTRE/SPECTRE181_ISR7
export QRC_HOME=/tools/cadence/EXT/EXT191_ISR3
export SRR_HOME=/tools/cadence/SRR/SRR_0618
export CDSLIB_HOME=/tools/projects/erichang/BAG_2.0/cdslib_plugin
export CMAKE_HOME=/tools/B/ayan_biswas/programs/cmake-3.17.0-Linux-x86_64

export CDSHOME=${CDS_INST_DIR}
export CDSLIB_TOOL=${CDSLIB_HOME}/tools.lnx86
export MMSIM_HOME=${SPECTRE_HOME}

# OA settings
export OA_SRC_ROOT=/tools/B/ayan_biswas/programs/oa_new
export OA_LINK_DIR=${OA_SRC_ROOT}/lib/linux_rhel70_gcc83x_64/opt
export OA_CDS_ROOT=${CDS_INST_DIR}/oa_v22.60.s007
export OA_INCLUDE_DIR=${OA_SRC_ROOT}/include
export OA_PLUGIN_PATH=${CDSLIB_HOME}/share/oaPlugIns:${OA_CDS_ROOT}/data/plugins:${OA_PLUGIN_PATH:-}
export OA_BIT=64

# PATH setup
export PATH=${CDSLIB_TOOL}/bin:${PATH:-}
export PATH=${PVS_HOME}/bin:${PATH}
export PATH=${QRC_HOME}/bin:${PATH}
export PATH=${CDS_INST_DIR}/tools/plot/bin:${PATH}
export PATH=${CDS_INST_DIR}/tools/dfII/bin:${PATH}
export PATH=${CDS_INST_DIR}/tools/bin:${PATH}
export PATH=${MMSIM_HOME}/bin:${PATH}
export PATH=${CMAKE_HOME}/bin:${PATH}
export PATH=${BAG_TOOLS_ROOT}/bin:${PATH}
export PATH=/tools/B/ayan_biswas/programs/bag_tools/bin:${PATH}

# LD_LIBRARY_PATH setup
export LD_LIBRARY_PATH=${CDSLIB_TOOL}/lib/64bit:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${OA_LINK_DIR}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${SRR_HOME}/tools/lib/64bit:${LD_LIBRARY_PATH:-}
export LD_LIBRARY_PATH=${BAG_TOOLS_ROOT}/lib64:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${BAG_TOOLS_ROOT}/lib:${LD_LIBRARY_PATH}

# Virtuoso options
export SPECTRE_DEFAULTS=-E
export CDS_Netlisting_Mode="Analog"
export CDS_AUTO_64BIT=ALL

# License setup
source /tools/flexlm/flexlm.sh

# pybag compiler settings
export CMAKE_PREFIX_PATH=${BAG_TOOLS_ROOT}
# NOTE for HDF5: srr_to_hdf5 requires 1.10.5, but anaconda7 has 1.10.4. This disables the check
export HDF5_DISABLE_VERSION_CHECK=1
