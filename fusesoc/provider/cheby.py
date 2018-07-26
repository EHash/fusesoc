import logging
import os
import shutil
from fusesoc.provider.provider import Provider
from fusesoc.utils import Launcher

logger = logging.getLogger(__name__)

class Cheby(Provider):

    def _checkout(self, local_dir):
        core_file  = self.config.get('core_file')
        gen_file_type = self.config.get('generated_file_type')
        core_file_name, core_file_ext  = os.path.splitext(core_file)

        # We only support verilog or vhdl generated files
        if gen_file_type is not None and \
            gen_file_type != 'verilogSource' and \
            gen_file_type != 'vhdlSource':
            raise SyntaxError("Unsuported option '{}' in Cheby provider section".format(gen_file_type))

        gen_vhdl_file = local_dir + '/' + core_file_name + '.vhd'
        gen_verilog_file = local_dir + '/' + core_file_name + '.v'

        logger.info("Using Cheby to generate core " + core_file)
        if not os.path.isdir(local_dir):
            os.mkdir(local_dir)
        src_files = [core_file]

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

        # Cheby does not support native Verilog generation, so the only option
        # is to generate a VHDL file and then convert it, if needed.
        with open(gen_vhdl_file, 'w+') as f:
            args = ['--gen-vhdl', core_file]
            Launcher('cheby', args, cwd=local_dir, stdout=f).run()
            f.close()
        if gen_file_type is None or gen_file_type == 'verilogSource':
            with open(gen_verilog_file, 'w+') as f:
                args = [gen_vhdl_file, gen_verilog_file]
                Launcher('vhd2vl', args, cwd=local_dir).run()
                os.remove(gen_vhdl_file)
                f.close()

