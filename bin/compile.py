#!/usr/bin/env python

import os
import sys
import logging

import json

if __name__ == '__main__':

    whoami = sys.argv[0]
    whoami = os.path.abspath(whoami)
    
    bin = os.path.dirname(whoami)
    root = os.path.dirname(bin)

    source = os.path.join(root, 'sizes')
    spec = {}

    labels = {}
    sizes = {}

    required = ("id", "size", "label")

    for (root, dirs, files) in os.walk(source):

        for f in files:
    
            path = os.path.join(root, f)

            if not path.endswith('.json'):
                continue

            try:
                fh = open(path, 'r')
                data = json.load(fh)
            except Exception, e:
                logging.error("failed to parse %s, because %s" % (path, e))
                sys.exit()

            for k in required:
                if not data.get(k, False):
                    logging.error("%s is missing a %s key" % (path, k))
                    sys.exit()

            size = data['size']
            label = data['label']

            if size in sizes:
                logging.error("%s is trying to claim size '%s' (already assigned to %s)" % (path, size, sizes[size]))

            if label in labels:
                logging.error("%s is trying to claim size '%s' (already assigned to %s)" % (path, label, labels[label]))

            sizes[ size ] = path
            labels[ label ] = path

            spec[data['id']] = data

    print json.dumps(spec)
    sys.exit()
