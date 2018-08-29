from __future__ import print_function
import logging
import os
import shutil
from fusesoc.provider.provider import Provider
from fusesoc.utils import Launcher

logger = logging.getLogger(__name__)

class Newad2json(Provider):

    def _checkout(self, local_dir):
        core_files  = self.config.get('core_files')
        search_dirs  = self.config.get('search_dirs')

        if not os.path.isdir(local_dir):
            os.mkdir(local_dir)
        src_files = core_files.values()

        for f in src_files:
            f_src = os.path.join(self.core_root, f)
            f_dst = os.path.join(local_dir, f)
            if os.path.exists(f_src):
                d_dst = os.path.dirname(f_dst)
                if not os.path.exists(d_dst):
                    os.makedirs(d_dst)
                shutil.copyfile(f_src, f_dst)
            else:
                logger.error('Cannot find file %s' % f_src)

        for mod_name, f_name in core_files.items():
            core_basename = os.path.basename(f_name)
            core_dirname = os.path.dirname(f_name)

            core_filename, core_fileext  = os.path.splitext(core_basename)

            gen_json_file = local_dir + '/' + core_dirname + '/' + core_filename + '.json'

            logger.info("Using Newad2JSON to generate core " + f_name)

            newad_dirs = ''
            for dir in search_dirs:
                newad_dir_dst = os.path.join(local_dir, dir)
                newad_dirs += newad_dir_dst + ','

            # newad to JSON decriptor.
            args = ['-i', f_name,
                    '-r', gen_json_file,
                    '-b', '0',
                    '-l', '-w', '23', '-d', newad_dirs]
            Launcher('newad.py', args, cwd=local_dir).run()
