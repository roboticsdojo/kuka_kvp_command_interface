from setuptools import find_packages, setup

package_name = 'kuka_kvp_command_interface'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ru3ll',
    maintainer_email='brian.macharia.wambui@gmail.com',
    description='ROS2 package interface to interact with kuka_kr6_r9002 robot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'send_to_robot= Scripts.send_to_robot_v3:main',
        ],
    },
)
