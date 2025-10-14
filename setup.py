from setuptools import find_packages, setup

package_name = 'kuka_kvp_command_interface'

setup(
    name=package_name,
    version='0.2.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Lenny Ng\'ang\'a',
    maintainer_email='codewithlennylen254@gmail.com',
    description='This ROS2 package provides an interface for the KUKA Agilus KR6 R900-2 robot arm. It enables users to programmatically control the arm, facilitating the development of complex automation scripts and programs within the ROS ecosystem. The package is based on the KVP (KUKA Variable Protocol) for communication with the robot controller',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'kuka_kvp_interface = kuka_kvp_command_interface.kuka_kvp_interface:main',
        ],
    },
)
