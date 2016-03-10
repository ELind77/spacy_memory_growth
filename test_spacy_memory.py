#! /usr/bin/env python2


from spacy.en import English
import codecs
import resource


__author__ = 'Eric Lind'


def get_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def main(fil='tweets.txt'):
    NLP = English(entity=False, load_vectors=False, tagger=False, parser=False)
    print "loaded parser"
    init_mem = get_usage()


    with open('stats.out', 'w') as stats:
        stats.write("%s\n" % init_mem)

        with codecs.open(fil, encoding='utf-8') as _f:
            for i, line in enumerate(_f):
                if i % 10000 == 0:
                    mem = get_usage()
                    stats.write("%s\n" % mem)
                NLP(line)

        # Final stats
        final_mem = get_usage()
        stats.write("%s\n" % final_mem)
    
    print "Mem diff: %s" % (final_mem - init_mem)
    print "DONE"


if __name__ == '__main__':
    import sys
    main(sys.argv[1])

