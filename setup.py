from setuptools import setup, find_packages

setup(name='bamsurgeon',
	version='1.0',
	author='Adam Ewing',
	license='MIT',
	scripts=['bin/addindel.py',
		'bin/addsnv.py',
		'bin/addsv.py',
		'bin/bamregions_from_vcf.py',
		'bin/bamsplit.py',
		'bin/bamsplit_proportion.py',
		'bin/bsrg.py',
		'bin/comparemapping.py',
		'bin/covered_segments.py',
		'bin/dedup.py',
		'bin/evaluator.py',
		'bin/fix_mapsplice_bam.py',
		'bin/makevcf.py',
		'bin/makevcf_indels.py',
		'bin/makevcf_sv.py',
		'bin/postprocess.py',
		'bin/randomsites.py',
		'bin/remove_unpaired.py',
		'bin/rename_reads.py',
		'bin/seperation.py'],
	packages=find_packages(),
	)