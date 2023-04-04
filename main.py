#!/usr/bin/env python
"""
Solve the Chinese-Postman problem.

For a given graph, determine the minimum amount of backtracking
required to complete an Eularian circuit.

"""
import argparse
import sys

import data.data
from chinesepostman import eularian, network


def setup_args():
    """ Setup argparse to take graph name argument. """
    parser = argparse.ArgumentParser(description='Find an Eularian Cicruit.')
    parser.add_argument('graph', nargs='?', help='Name of graph to load')
    parser.add_argument('start', nargs='?', help='The staring node. Random if none provided.', type=int)
    args = parser.parse_args()
    return args


def main():
    """ Make it so. """
    edges = None
    args = setup_args()
    graph_name = args.graph
    try:
        print('Loading graph: {}'.format(graph_name))
        edges = getattr(data.data, graph_name)
    except (AttributeError, TypeError):
        print('\nInvalid graph name. Available graphs:\n\t{}\n'.format(
            '\n\t'.join([x for x in dir(data.data)
            if not x.startswith('__')])))
        sys.exit()

    original_graph = network.Graph(edges)

    print('<{}> edges'.format(len(original_graph)))
    if not original_graph.is_eularian:
        print('Converting to Eularian path...')
        graph, num_dead_ends = eularian.make_eularian(original_graph)
        print('Conversion complete')
        print('\tAdded {} edges'.format(len(graph) - len(original_graph) + num_dead_ends))
        print('\tTotal cost is {}'.format(graph.total_cost))
    else:
        graph = original_graph

    start = args.start if args.start else None
    print('Attempting to solve Eularian Circuit...')
    route, attempts = eularian.eularian_path(graph, start=start)
    if not route:
        print('\tGave up after <{}> attempts.'.format(attempts))
    else:
        print('\tSolved in <{}> attempts'.format(attempts, route))
        print('Solution: (<{}> edges)'.format(len(route) - 1))
        print('\t{}'.format(route))


if __name__ == '__main__':
    main()
