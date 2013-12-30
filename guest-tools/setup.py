from setuptools import setup, find_packages

setup(
    name='guest-tools',
    version='0.0.1',
    packages=find_packages(),
    author='Dunrong Huang',
    author_email='riegamaths@gmail.com',
    description='A tools handling guest image',
    license='GPLv3',
    keywords='qemu tools',
    url='https://github.com/mathslinux/qemu-tools',
    entry_points={
        'command': [
            'img = img:make',
            'file = file:make',
            'network = config:make_network',
            'hostname = config:make_hostname',
            'ls = config:make_ls',
        ],
    }
)
