import os

import doodad as dd
import doodad.ec2 as ec2
import doodad.ssh as ssh
import doodad.mount as mount
import colored_traceback.always
from doodad.utils import EXAMPLES_DIR, REPO_DIR

# Local docker
mode_docker = dd.mode.LocalDocker(
    image='thanard/pytorch:latest',
)

# or this! Run experiment via docker on another machine through SSH
mode_ssh = None
# mode_ssh = dd.mode.SSHDocker(
#     image='python:3.5',
#     credentials=ssh.SSHCredentials(hostname='my.machine.name', username='my_username', identity_file='~/.ssh/id_rsa'),
# )

# or use this!
# mode_ec2 = None
mode_ec2 = dd.mode.EC2AutoconfigDocker(
    image='thanard/pytorch:latest',
    region='us-east-1',
    zone='us-east-1b',
    instance_type='p2.xlarge',
    spot_price=1.0,
    s3_log_prefix='secret',
    gpu=True,
    terminate=False
)

MY_RUN_MODE = mode_ec2  # CHANGE THIS

# Set up code and output directories
OUTPUT_DIR = '/example/outputs'  # this is the directory visible to the target
mounts = [
    mount.MountLocal(local_dir=REPO_DIR, mount_point='/root/code/doodad', pythonpath=True), # Code
    # mount.MountLocal(local_dir='/home/thanard/Downloads/rllab/sandbox/thanard/infoGAN', pythonpath=True),
    mount.MountLocal(local_dir=os.path.join(EXAMPLES_DIR, 'secretlib'), pythonpath=True),  # Code
]

if MY_RUN_MODE == mode_ec2:
    output_mount = mount.MountS3(s3_path='outputs', mount_point=OUTPUT_DIR, output=True)  # use this for ec2
else:
    output_mount = mount.MountLocal(local_dir=os.path.join(EXAMPLES_DIR, 'tmp_output'),
                                    mount_point=OUTPUT_DIR, output=True)
mounts.append(output_mount)

print(mounts)

THIS_FILE_DIR = os.path.realpath(os.path.dirname(__file__))
dd.launch_python(
    target=os.path.join(THIS_FILE_DIR, 'app_main.py'),
    # point to a target script. If running remotely, this will be copied over
    mode=MY_RUN_MODE,
    mount_points=mounts,
    args={
        'arg1': 50,
        'arg2': 25,
        'output_dir': OUTPUT_DIR,
    }
)
#
# LOG_DIR = '/home/thanard/Downloads/rllab/data/test-ec2/'
# THIS_FILE_DIR = '/home/thanard/Downloads/rllab/sandbox/thanard/infoGAN'
# # DEMO_FILE= '/home/giulia/NIPS/softqlearning/softqlearning/environments/goals/ant_10_goals.pkl'
# # ENV_FILE = '/home/giulia/NIPS/softqlearning/low_gear_ratio_ant.xml'
# dd.launch_tools.launch_python(
#     target=os.path.join(THIS_FILE_DIR, 'infogan_2d.py'),
#     mode=MY_RUN_MODE,
#     mount_points=mounts,
#     args={
#         'log_dir': OUTPUT_DIR,
#         # 'file_goals' : DEMO_FILE,
#         # 'file_env' : ENV_FILE,
#         'save_file': OUTPUT_DIR,
#     },
#     verbose=True
# )
