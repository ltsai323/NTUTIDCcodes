#!/usr/bin/env python3
#https://ezdxf.mozman.at/docs/introduction.html

from __future__ import division

import os, sys
import ezdxf
import argparse


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
def transformer_correction(x,y,z):
    return (-1*x,y,z)

def transformer_coorindate(x,y,z):
    return (-1*y,x,z)
def output_formater(mylist):
    return '\t '.join( ['%.2f'%f for f in mylist] ) + '\n'

def write_entity(e, f, last_end):
    # isDispense, cw/ccw, speed, start point x, start point y, end point x, end point y, center point x, center point y
    if e.dxftype() == 'LINE':
        f.write("{}\t{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n".format('LINE', 0, 0, 20, e.dxf.start[0], e.dxf.start[1], e.dxf.end[0], e.dxf.end[1], 0, 0) )
    if e.dxftype() == 'CIRCLE':
        f.write("{}\t{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n".format('CIRCLE', 0, 0, 20, last_end[0], last_end[1], last_end[0], last_end[1], e.dxf.center[0]-last_end[0], e.dxf.center[1]-last_end[1]) )
    elif e.dxftype() == 'ARC':
        f.write("{}\t{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n".format('ARC', 0, 0, 20, e.start_point[0], e.start_point[1], e.end_point[0], e.end_point[1], e.dxf.center[0]-e.start_point[0], e.dxf.center[1]-e.start_point[1]) )

def write_circle(e,f,last_end):
    if e.dxftype() == 'CIRCLE':
        correct1=transformer_correction(*e.dxf.center)
        correct =transformer_coorindate(*correct1)
        outstr=output_formater(correct)
        f.write(outstr)
        #f.write("{}\t{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n".format('CIRCLE', 0, 0, 20, last_end[0], last_end[1], last_end[0], last_end[1], e.dxf.center[0]-last_end[0], e.dxf.center[1]-last_end[1]) )

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
    #f.write("Type, Dispense, cw/ccw, speed, start_x, start_y, end_x, end_y, center_x, center_y\n")
    f.write("x:y:z\n")

    # iterate over all entities in modelspace
    msp = doc.modelspace()
    last_end=(0,0,0)
    for e in msp:
        #print_entity(e)
        #write_entity(e, f, last_end)
        write_circle(e, f, last_end)
        if e.dxftype() == 'LINE':
            last_end = e.dxf.end
        elif e.dxftype() == 'ARC':
            last_end = e.end_point
