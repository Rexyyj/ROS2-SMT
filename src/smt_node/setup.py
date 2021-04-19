from setuptools import setup

package_name = 'smt_node'

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
    maintainer='Rex Yu',
    maintainer_email='jiafish@outlook.com',
    description='A simple node to obtain node relationships in running ros2 system',
    license='Apache-2.0 License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'smt_node = smt_node.smt_node:main'
        ],
    },
)
