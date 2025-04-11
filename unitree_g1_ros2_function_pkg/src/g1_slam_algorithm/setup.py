from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'g1_slam_algorithm'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.*'))), 
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*.rviz'))),
        (os.path.join('share', package_name, 'map'), glob(os.path.join('maps', '*.*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='FLYivan',
    maintainer_email='luoyifan902008@126.com',
    description='slam in g1',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [


            'motion_to_tf  = g1_slam_algorithm.motion_to_tf:main',  
            'frame_id_modifier  = g1_slam_algorithm.frame_id_modifier:main',  
        ],
    },
)
