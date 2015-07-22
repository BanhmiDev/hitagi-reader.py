#!/usr/bin/env python3
if __name__ == '__main__':
    import sys
    from hitagilib import Hitagi

    if len(sys.argv) > 1:
        sys.exit(Hitagi.run(sys.argv[1]))
    else:
        sys.exit(Hitagi.run())
