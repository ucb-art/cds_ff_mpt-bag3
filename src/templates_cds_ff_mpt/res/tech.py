# BSD 3-Clause License
#
# Copyright (c) 2018, Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import Any, Optional, List, Tuple, Sequence, Mapping

from pybag.enum import Orient2D
from pybag.core import BBox

from bag.util.immutable import ImmutableSortedDict, Param
from bag.layout.routing.grid import TrackSpec
from bag.layout.tech import TechInfo

from xbase.layout.data import LayoutInfo, LayoutInfoBuilder, CornerLayInfo, ViaInfo
from xbase.layout.array.data import ArrayLayInfo, ArrayEndInfo
from xbase.layout.res.tech import ResTech


class ResTechCDSFFMPT(ResTech):
    def __init__(self, tech_info: TechInfo, metal: bool = False) -> None:
        ResTech.__init__(self, tech_info, metal=metal)
        if metal:
            raise RuntimeError("Metal resistors currently not supported")

    def get_width(self, **kwargs) -> int:
        if "unit_specs" not in kwargs:
            raise RuntimeError("Please add unit_specs")
        w_unit: int = kwargs['unit_specs']['params']['w']
        w: int = self._res_config['w']
        if w_unit != w:
            raise ValueError(f'w={w_unit} has to be exactly equal to {w}.')
        return w_unit

    def get_length(self, **kwargs) -> int:
        if "unit_specs" not in kwargs:
            raise RuntimeError("Please add unit_specs")
        l_unit: int = kwargs['unit_specs']['params']['l']
        l_min: int = self._res_config['l_min']
        if l_unit < l_min:
            raise ValueError(f'l={l_unit} has to be greater than or equal to l_min={l_min}.')
        return l_unit

    @property
    def min_size(self) -> Tuple[int, int]:
        return self._res_config['min_size']

    @property
    def blk_pitch(self) -> Tuple[int, int]:
        return self._res_config['blk_pitch']

    def get_track_specs(self, conn_layer: int, top_layer: int) -> List[TrackSpec]:
        grid_info: Sequence[Tuple[int, int, int]] = self._res_config['grid_info']

        return [TrackSpec(layer=lay, direction=Orient2D.y, width=vm_w, space=vm_sp, offset=(vm_w + vm_sp) // 2)
                for lay, vm_w, vm_sp in grid_info if conn_layer < lay <= top_layer]

    def get_edge_width(self, info: ImmutableSortedDict[str, Any], arr_dim: int, blk_pitch: int) -> int:
        edge_margin: int = self._res_config['edge_margin']
        return -(- edge_margin // blk_pitch) * blk_pitch

    def get_end_height(self, info: ImmutableSortedDict[str, Any], arr_dim: int, blk_pitch: int) -> int:
        end_margin: int = self._res_config['end_margin']
        return -(- end_margin // blk_pitch) * blk_pitch

    def get_blk_info(self, conn_layer: int, w: int, h: int, nx: int, ny: int, **kwargs: Any
                     ) -> Optional[ArrayLayInfo]:
        po_exty: int = self._res_config['po_exty']
        po_spy: int = self._res_config['po_spy']

        # unit resistor dimensions
        w_unit = self.get_width(**kwargs)
        l_unit = self.get_length(**kwargs)

        w_pitch, h_pitch = self.blk_pitch
        w_blk = self.min_size[0]
        h_blk = -(-(l_unit + (2 * po_exty + po_spy)) // h_pitch) * h_pitch
        if w < w_blk or h < h_blk:
            return None

        res_lay_table = self._tech_info.config['res_lay_table']

        # --- Compute layout --- #
        top_bbox = BBox(0, 0, w, h)
        builder = LayoutInfoBuilder()

        # add threshold layer
        res_type: str = kwargs['unit_specs']['params']['res_type']
        for _lp in self.tech_info.get_threshold_layers('', res_type, res_type):
            builder.add_rect_arr(_lp, top_bbox)

        # draw poly
        w2 = w // 2
        w_unit2 = w_unit // 2
        h2 = h // 2
        l_unit2 = l_unit // 2
        po_bbox = BBox(w2 - w_unit2, h2 - l_unit2 - po_exty, w2 + w_unit2, h2 + l_unit2 + po_exty)
        po_lp = res_lay_table['PO']
        builder.add_rect_arr(po_lp, po_bbox)

        # draw res layer
        res_bbox = BBox(w2 - w_unit2, h2 - l_unit2, w2 + w_unit2, h2 + l_unit2)
        res_lp = res_lay_table['RES']
        builder.add_rect_arr(res_lp, res_bbox)

        # connect to conn_layer ports
        via_specs: Mapping[str, Any] = self._res_config['via_specs']
        via_name: str = via_specs['name']
        via_w, via_h = via_specs['dim']
        bot_encx, bot_ency = via_specs['bot_enc']
        top_encx, top_ency = via_specs['top_enc']

        enc_b = (bot_encx, bot_encx, bot_ency, bot_ency)
        enc_t = (top_encx, top_encx, top_ency, top_ency)
        via_m_ym = res_bbox.yl - bot_ency - via_h // 2
        via_m_info = ViaInfo(via_name, w2, via_m_ym, via_w, via_h, enc_b, enc_t)
        builder.add_via(via_m_info)
        via_p_ym = res_bbox.yh + bot_ency + via_h // 2
        via_p_info = ViaInfo(via_name, w2, via_p_ym, via_w, via_h, enc_b, enc_t)
        builder.add_via(via_p_info)

        conn_lp = self._tech_info.get_lay_purp_list(self.conn_layer)[0]
        via_w2 = via_w // 2
        via_h2 = via_h // 2
        bbox_m = BBox(w2 - via_w2 - top_encx, via_m_ym - via_h2 - top_ency,
                      w2 + via_w2 + top_encx, via_m_ym + via_h2 + top_ency)
        builder.add_rect_arr(conn_lp, bbox_m)
        bbox_p = BBox(w2 - via_w2 - top_encx, via_p_ym - via_h2 - top_ency,
                      w2 + via_w2 + top_encx, via_p_ym + via_h2 + top_ency)
        builder.add_rect_arr(conn_lp, bbox_p)
        ports = dict(MINUS=[(conn_lp[0], [bbox_m])], PLUS=[(conn_lp[0], [bbox_p])])

        lay_info = builder.get_info(top_bbox)
        edge_info = Param(dict(od_margin=0))
        end_info = Param(dict(od_margin=0))
        ports = Param(ports)
        return ArrayLayInfo(lay_info, ports, edge_info, end_info)

    def get_edge_info(self, w: int, h: int, info: ImmutableSortedDict[str, Any], **kwargs: Any
                      ) -> LayoutInfo:
        builder = LayoutInfoBuilder()
        return builder.get_info(BBox(0, 0, w, h))

    def get_end_info(self, w: int, h: int, info: ImmutableSortedDict[str, Any], **kwargs: Any
                     ) -> ArrayEndInfo:
        builder = LayoutInfoBuilder()
        return ArrayEndInfo(builder.get_info(BBox(0, 0, w, h)), ImmutableSortedDict())

    def get_corner_info(self, w: int, h: int, info: ImmutableSortedDict[str, Any], **kwargs: Any) -> CornerLayInfo:
        x_margins = dict(well=0, base=0)
        y_margins = dict(well=0, base=0)
        edgel = Param(dict(margins=x_margins))
        edgeb = Param(dict(margins=y_margins))
        builder = LayoutInfoBuilder()
        blk_bbox = BBox(0, 0, w, h)
        return CornerLayInfo(builder.get_info(blk_bbox), (0, 0), edgel, edgeb)
