#!/usr/bin/env python3
"""
Created on March 17 2020

@author: Melchior du Lac
@description: Merge two SBML's together

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker


##
#
#
def main(inputfile,
         input_format,
         input_sbol,
         output,
         pathway_id,
         max_variants,
         lib_size,
         input_parts)
    docker_client = docker.from_env()
    image_str = 'brsynth/rpmergesbml-standalone:dev'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        shutil.copy(inputfile, tmpOutputFolder+'/input.dat')
        shutil.copy(target_sbml, tmpOutputFolder+'/target_sbml.dat')
        command = ['python /home/tool_rpMergeSBML.py',
                   '-target_sbml',
                   '/home/tmp_output/target_sbml.dat',
                   '-input',
                   '/home/tmp_output/input.dat',
                   '-input_format',
                   str(input_format),
                   '-sink_species_group_id',
                   str(sink_species_group_id),
                   '-species_group_id',
                   str(species_group_id),
                   '-input_format',
                   str(input_format),
                   '-output',
                   '/home/tmp_output/output.dat']
        container = docker_client.containers.run(image_str,
												 command,
												 detach=True,
                                                 stderr=True,
                                                 remove=True,
												 volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        container.wait()
        err = container.logs(stdout=False, stderr=True)
        print(err)
        shutil.copy(tmpOutputFolder+'/output.dat', outputTar)
        container.remove()



##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Convert the results of RP2 and rp2paths to SBML files')
    parser.add_argument('-target_sbml', type=str)
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-sink_species_group_id', type=str, default='rp_sink_species')
    parser.add_argument('-species_group_id', type=str, default='central_species')
    parser.add_argument('-output', type=str)
    params = parser.parse_args()
    main(params.input,
         params.input_format,
         params.input_sbol,
         params.output,
         params.pathway_id,
         params.max_variants,
         params.lib_size,
         params.input_parts)