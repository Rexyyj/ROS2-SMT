from setuptools import setup

package_name = 'ros2_smt'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Rex YU',
    maintainer_email='jiafish@outlook.com',
    description='TODO: Package description',
    license='Apache-2.0 License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'smt_run = ros2_smt.smt_run:main'
        ],
    },
)
