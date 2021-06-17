from setuptools import setup

package_name = 'smt_example'

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
            'sensor_infrared = smt_example.sensor_infrared:main',
            'sensor_temperature = smt_example.sensor_temperature:main',
            'sensor_locator = smt_example.sensor_locator:main',
            'sensor_smoke = smt_example.sensor_smoke:main'
        ],
    },
)
