from __future__ import print_function
import logging
import os
from fusesoc.provider.provider import Provider
from fusesoc.utils import Launcher

logger = logging.getLogger(__name__)

class Buildrom(Provider):

    def _checkout(self, local_dir):
        core_files  = self.config.get('core_files')

        if not os.path.isdir(local_dir):
            os.mkdir(local_dir)

        for f_output, f_input in core_files.items():
            core_basename = os.path.basename(f_input)
            core_dirname = os.path.dirname(f_input)
            f_src = os.path.join(local_dir, core_dirname) + '/' + core_basename
            f_dst = os.path.join(local_dir, f_output)
            if os.path.exists(f_src):
                d_dst = os.path.dirname(f_dst)
                if not os.path.exists(d_dst):
                    os.makedirs(d_dst)
            else:
                logger.error('Cannot find file %s' % f_src)

        for out_filename, f_name in core_files.items():
            core_basename = os.path.basename(f_name)
            core_dirname = os.path.dirname(f_name)

            input_json_name = os.path.join(local_dir, core_dirname) + '/' + core_basename
            gen_build_rom_file = local_dir + '/' + out_filename

            logger.info("Using BuildRom to generate core " + input_json_name)
            logger.info("Using BuildRom to gen " + gen_build_rom_file)

            # config_rom args
            args = ['-v', gen_build_rom_file,
                    '-j', input_json_name]
            Launcher('build_rom.py', args, cwd=local_dir).run()
