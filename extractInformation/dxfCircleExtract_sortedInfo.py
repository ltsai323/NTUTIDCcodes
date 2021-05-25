#!/usr/bin/env python3
#https://ezdxf.mozman.at/docs/introduction.html

from __future__ import division

import os, sys
import ezdxf
import argparse


def tostr(f):
    return '%.2f' % f
def transformer_effectiveDigits(val):
    return float( int(val*100) )/100
def transformer_correction(x,y,z):
    return (-1*x,y,z)

def transformer_coorindate(x,y,z):
    return (-1*y,x,z)
def formater_dict(x,y):
    return {x:[y]}
def dictupdater(d,x,y):
    if x in d.keys(): d[x].append(y)
    else: d.update( {x:[y]} )


def strformatter_floats(*floats):
    return '\t'.join( [ tostr(f)for f in floats] ) + '\n'

def strformatter_writeline(str1,str2):
    return str1+'\t'+str2+'\n'

def CircleFinder_writeToDict(e,d,last_end, makeCorrection=False):
    if e.dxftype() == 'CIRCLE':
        correct =transformer_correction(*e.dxf.center)
        if makeCorrection:
            correct =transformer_coorindate(*correct )

        dictupdater(d, transformer_effectiveDigits(correct[0]), correct[1])

'''
# helper function
def print_entity(e):
    if e.dxftype() == 'LINE':
        print("LINE on layer: %s" % e.dxf.layer)
        print("start point: %s" % e.dxf.start)
        print("end point: %s\n" % e.dxf.end)
    elif e.dxftype() == 'CIRCLE':
        print("CIRCLE on layer: %s" % e.dxf.layer)
        print("center point: %s" % e.dxf.center)
        print("radius: %s\n" % e.dxf.radius)
    elif e.dxftype() == 'ARC':
        print("ARC on layer: %s" % e.dxf.layer)
        print("center point: %s" % e.dxf.center)
        print("radius: %s" % e.dxf.radius)
        print("start point: %s" % e.start_point)
        print("end point: %s\n" % e.end_point)
        ''
def write_entity(e, f, last_end):
    # isDispense, cw/ccw, speed, start point x, start point y, end point x, end point y, center point x, center point y
    if e.dxftype() == 'LINE':
        f.write("{}\t{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n".format('LINE', 0, 0, 20, e.dxf.start[0], e.dxf.start[1], e.dxf.end[0], e.dxf.end[1], 0, 0) )
    if e.dxftype() == 'CIRCLE':
        f.write("{}\t{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n".format('CIRCLE', 0, 0, 20, last_end[0], last_end[1], last_end[0], last_end[1], e.dxf.center[0]-last_end[0], e.dxf.center[1]-last_end[1]) )
    elif e.dxftype() == 'ARC':
        f.write("{}\t{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n".format('ARC', 0, 0, 20, e.start_point[0], e.start_point[1], e.end_point[0], e.end_point[1], e.dxf.center[0]-e.start_point[0], e.dxf.center[1]-e.start_point[1]) )
def origcode():

    parser = argparse.ArgumentParser(description='read dxf files and convert to glue pattern')
    parser.add_argument('in_filenames',nargs="+",help='input filenames')
    args = parser.parse_args()

    try:
        doc = ezdxf.readfile("{}".format(args.in_filenames[0]))
    except IOError:
        print('Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print('Invalid or corrupted DXF file.')
        sys.exit(2)

    f = open("output.txt", "w")
    f.write("Type, Dispense, cw/ccw, speed, start_x, start_y, end_x, end_y, center_x, center_y\n")

    # iterate over all entities in modelspace
    msp = doc.modelspace()
    last_end=(0,0,0)
    for e in msp:
        print_entity(e)
        write_entity(e, f, last_end)
        if e.dxftype() == 'LINE':
            last_end = e.dxf.end
        elif e.dxftype() == 'ARC':
            last_end = e.end_point
'''


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='read dxf files and convert to glue pattern')
    parser.add_argument('in_filenames',nargs="+",help='input filenames')
    args = parser.parse_args()

    try:
        doc = ezdxf.readfile("{}".format(args.in_filenames[0]))
    except IOError:
        print('Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print('Invalid or corrupted DXF file.')
        sys.exit(2)

    f = open("output.txt", "w")
    ''' f.write("Type, Dispense, cw/ccw, speed, start_x, start_y, end_x, end_y, center_x, center_y\n") '''
    f.write("x:y\n") # ':' is the separater used in TTree::ReadFile

    # iterate over all entities in modelspace
    msp = doc.modelspace()
    last_end=(0,0,0)
    d={}
    for e in msp:
        '''
        print_entity(e)
        write_entity(e, f, last_end)
        '''

        CircleFinder_writeToDict(e, d, last_end, makeCorrection=True)

        if e.dxftype() == 'LINE':
            last_end = e.dxf.end
        elif e.dxftype() == 'ARC':
            last_end = e.end_point

    for key,vals in sorted( d.items() ):
        for val in sorted(vals):
            f.write( strformatter_floats(key,val) )
