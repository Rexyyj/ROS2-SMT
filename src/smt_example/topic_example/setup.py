from setuptools import setup

package_name = 'topic_example'

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
            'sensor_infrared = topic_example.sensor_infrared:main',
            'sensor_temperature = topic_example.sensor_temperature:main',
            'sensor_locator = topic_example.sensor_locator:main',
            'sensor_smoke = topic_example.sensor_smoke:main',
            'actuator_light = topic_example.actuator_light:main',
            'actuator_alarm = topic_example.actuator_alarm:main',
            'actuator_door = topic_example.actuator_door:main'
        ],
    },
)
