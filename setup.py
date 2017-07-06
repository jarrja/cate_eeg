from distutils.core import setup

setup(
    name='CATE_EEG',
    version='1.0',
    packages=['cate_eeg'],
    install_requires=['numpy', 'scipy', 'scikit-learn', 'mne','pandas'],
    # url='https://github.com/pbashivan/EEGLearn',
    # license='GNU GENERAL PUBLIC LICENSE',
    author='Panuwat Janwattanapong',
    description='EEG Functional Connectivity Analysis'
)
