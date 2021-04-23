from setuptools import setup
from setuptools import find_packages
package_name = 'smt_relationship'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Rex Yu',
    maintainer_email='jiafish@outlook.com',
    description='Package to analysis node relationship in ROS-SMT project',
    license='Apache-2.0 License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'smt_relationship = smt_relationship.smt_relationship:main'
        ],
    },
)
