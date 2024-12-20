# cds_ff_mpt
[BAG3++](https://github.com/ucb-art/bag) primitives for cds_ff_mpt technology.

This repository serves as a good example on how the process-specific component of BAG should be set up.

## Licensing

This library is licensed under the Apache-2.0 license.  However, some source files are licensed
under both Apache-2.0 and BSD-3-Clause license, meaning that the user must comply with the
terms and conditions of both licenses.  See [here](LICENSE.BSD-3-Clause) for full text of the
BSD license, and [here](LICENSE.Apache-2.0) for full text of the Apache license.  See individual
files to check if they fall under Apache-2.0, or both Apache-2.0 and BSD-3-Clause.


# Technology features and hints
- Layout resolution is in 0.5nm.
- Min channel length is 18nm, so min channel units is 36.
- This tech has standard, lvt, and hvt devices.
- Devices widths in this process are quantized in integer number of fins per finger/segment.
   The minimum is 1 and the maximum is 100. For practical usage, the recommend values are
   between 2 and 10.
- This tech has 8 metal layers and an "M0" (LiPo) layer.
- This tech has no pcell MOM caps. Manual ones can be drawn.
- This tech has pcell MIM caps (`cmim`) between M7-MT and M4-M5. Both provide ~2.2 fF / um^2.

SD pitch: 90 nm ~ 180 units. BAG quantizes vertical metal pitches to match the SD pitch ~ M1, M3, M5, M7.

## Resistors
- This tech has multiple flavors of poly resistors. Current BAG implements the `rspp` - P+ Poly resistor w/ salicide. Width is fixed at 18nm (36 units). Length is quantized to 1nm (2 unit).

# Configuration

To configure this repository for your own setup, the following files in the `workspace_setup` folder should be changed:

1. .cdsinit.personal

   change the simulation directory to a suitable location (defaults to be in the BAG working directory).

2. .cdsinit

   the "editor" variable should be changed to point to your favorite editor.

3. .bashrc

   modify so that Virtuoso/OpenAccess/cdsLibPlugin are setup properly.

4. .bashrc_bag

   modify so that they point to the right python/jupyter/pytest executable.

5. PDK

   should symlink to the cds_ff_mpt PDK library downloaded from [Cadence Support](support.cadence.com)

Finally, the "modelfile" entries in the `corners_setup.yaml` file in the top level directory should be modified to
point to the correct location.

# New repoitory installation

1. create a new git repo.

2. add `BAG_framework` and the technology repository as git submodules.

   ```
   git submodule add <BAG_framework URL>
   git submodule add <tech repo URL>
   ```

3. check out appropriate branches, update BAG_framework submodules.

4. in workspace folder, run:

   ```
   ./<tech repo>/install.sh
   ```

5. source `.bashrc`, edit bag_submodules.yaml, then run:

   ```
   ./setup_submdoules.py
   ```

6. commit and push all changes.  Now the workspace repo is set up.
