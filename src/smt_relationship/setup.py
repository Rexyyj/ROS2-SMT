from setuptools import setup

package_name = 'smt_relationship'

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
    description='Package to analysis node relationship in ROS-SMT project',
    license='Apache-2.0 License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'smt_relationship = smt_relationship.smt_relationship:main'
        ],
    },
)
