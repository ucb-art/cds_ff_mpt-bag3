#! /usr/bin/env tcsh

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
setenv PYTHONPATH ""

### Setup BAG
source .cshrc_bag

# location of various tools
setenv CDS_INST_DIR /tools/cadence/ICADVM/ICADVM181
setenv PVS_HOME=/tools/cadence/PVS/PVS151
setenv SPECTRE_HOME /tools/cadence/SPECTRE/SPECTRE181_ISR7
setenv QRC_HOME /tools/cadence/EXT/EXT191_ISR3
setenv SRR_HOME /tools/cadence/SRR/SRR_0618
setenv CDSLIB_HOME /tools/projects/erichang/BAG_2.0/cdslib_plugin
setenv CMAKE_HOME /tools/B/ayan_biswas/programs/cmake-3.17.0-Linux-x86_64

setenv CDSHOME $CDS_INST_DIR
setenv CDSLIB_TOOL ${CDSLIB_HOME}/tools.lnx86
setenv MMSIM_HOME ${SPECTRE_HOME}

# OA settings
setenv OA_SRC_ROOT /tools/B/ayan_biswas/programs/oa_new
setenv OA_LINK_DIR ${OA_SRC_ROOT}/lib/linux_rhel70_gcc83x_64/opt
setenv OA_CDS_ROOT ${CDS_INST_DIR}/oa_v22.60.s007
setenv OA_INCLUDE_DIR ${OA_SRC_ROOT}/include
setenv OA_PLUGIN_PATH ${CDSLIB_HOME}/share/oaPlugIns:${OA_CDS_ROOT}/data/plugins:${OA_PLUGIN_PATH:-}
setenv OA_BIT=64

# PATH setup
setenv PATH ${CDSLIB_TOOL}/bin:${PATH}
setenv PATH ${PVS_HOME}/bin:${PATH}
setenv PATH ${QRC_HOME}/bin:${PATH}
setenv PATH ${CDS_INST_DIR}/tools/plot/bin:${PATH}
setenv PATH ${CDS_INST_DIR}/tools/dfII/bin:${PATH}
setenv PATH ${CDS_INST_DIR}/tools/bin:${PATH}
setenv PATH ${MMSIM_HOME}/bin:${PATH}
setenv PATH ${CMAKE_HOME}/bin:${PATH}
setenv PATH ${BAG_TOOLS_ROOT}/bin:${PATH}
setenv PATH /tools/B/ayan_biswas/programs/bag_tools/bin:${PATH}

# LD_LIBRARY_PATH setup
setenv LD_LIBRARY_PATH ${CDSLIB_TOOL}/lib/64bit:${LD_LIBRARY_PATH}
setenv LD_LIBRARY_PATH ${OA_LINK_DIR}:${LD_LIBRARY_PATH}
setenv LD_LIBRARY_PATH ${SRR_HOME}/tools/lib/64bit:${LD_LIBRARY_PATH:-}
setenv LD_LIBRARY_PATH ${BAG_TOOLS_ROOT}/lib64:${LD_LIBRARY_PATH}
setenv LD_LIBRARY_PATH ${BAG_TOOLS_ROOT}/lib:${LD_LIBRARY_PATH}

# Virtuoso options
setenv SPECTRE_DEFAULTS -E
setenv CDS_Netlisting_Mode "Analog"
setenv CDS_AUTO_64BIT ALL

# License setup
source /tools/flexlm/flexlm.cshrc

# pybag compiler settings
setenv CMAKE_PREFIX_PATH ${BAG_TOOLS_ROOT}
# NOTE for HDF5: srr_to_hdf5 requires 1.10.5, but anaconda7 has 1.10.4. This disables the check
setenv HDF5_DISABLE_VERSION_CHECK 1
