
import sys
from time import strftime
import socket
import os
import platform
import subprocess
import tempfile
import shutil
import glob

class ProcessOutput(object):

    def __init__(self, stdout, stderr, errorcode):
        self.stdout = stdout
        self.stderr = stderr
        self.errorcode = errorcode
    
    def getError(self):
        if self.errorcode != 0:
            return("Errorcode: %d\n%s" % (self.errorcode, self.stderr))
        return None

def Popen(outdir, args):
    subp = subprocess.Popen([str(arg) for arg in args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=outdir, env={'SPARKSXDIR' : '/netapp/home/klabqb3backrub/tools/sparks-x'})
    output = subp.communicate()
    return ProcessOutput(output[0], output[1], subp.returncode) # 0 is stdout, 1 is stderr

def create_scratch_path():
    path = tempfile.mkdtemp(dir = '/scratch')
    if not os.path.isdir(path):
        raise os.error
    return path

print("<make_fragments>")

print("<start_tiime>")
print(strftime("%Y-%m-%d %H:%M:%S"))
print("</start_time>")

print("<host>")
print(socket.gethostname())
print("</host>")

print("<arch>")
print(platform.machine() + ', ' + platform.processor() + ', ' + platform.platform())
print("</arch>")

task_id = os.environ.get('SGE_TASK_ID')


job_root_dir = "/netapp/home/rpac/crispr_cas/data/fragments/4un3B"

# Set up scratch directory
scratch_path = create_scratch_path()
shutil.copy("/netapp/home/rpac/crispr_cas/data/fragments/4un3B/4un3B.fasta", scratch_path)

print("<cwd>")
print(scratch_path)
print("</cwd>")

print("<cmd>")
cmd_args = [c for c in ['/netapp/home/shaneoconner/fragments_test/bio/fragments/make_fragments_RAP_cluster.pl', '-verbose', '-id', '4un3B', '', '/netapp/home/rpac/crispr_cas/data/fragments/4un3B/4un3B.fasta'] if c]
print(' '.join(cmd_args))
print("</cmd>")

print("<output>")
subp = Popen(scratch_path, cmd_args)
sys.stdout.write(subp.stdout)
print("</output>")

if True:
    print("<gzip>")
    for f in glob.glob(os.path.join(scratch_path, "*mers")) + [os.path.join(scratch_path, 'ss_blast')]:
        if os.path.exists(f):
            subpzip = Popen(scratch_path, ['gzip', f])
            print(f)
    print("</gzip>")

# Copy files from scratch back to /netapp
#for f in glob.glob(os.path.join(scratch_path, "*")):
#    shutil.copy(f, job_root_dir)

# Copy files from scratch back to /netapp
os.remove("/netapp/home/rpac/crispr_cas/data/fragments/4un3B/4un3B.fasta")
os.rmdir(job_root_dir)
shutil.copytree(scratch_path, job_root_dir)
shutil.rmtree(scratch_path)



print("<end_time>")
print(strftime("%Y-%m-%d %H:%M:%S"))
print("</end_time>")

print("</make_fragments>")

if subp.errorcode != 0:
    sys.stderr.write(subp.stderr)
    sys.exit(subp.errorcode)
