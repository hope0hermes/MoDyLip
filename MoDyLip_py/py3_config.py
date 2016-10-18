#!/usr/bin/python3
#encoding-utf8

class Configuration():
    """
    System configuration.

    Stores the complete information of the system configuration for a particular
    time step. The information is read from an input configuration file, which
    is assumed to have the following format::

        # L=%f %f %f t=%f blocks=%d
        # v=%f ...  w=%f ...
        # a2=%f a3=%f Re=%f N=%d ks=%f kb=%f l0=%f
        # n=%d N=%d name=%s
        %f %f %f %f %f %f %d
        %f %f %f %f %f %f %d
        %f %f %f %f %f %f %d
        .  .  .  .  .  .  .
        .  .  .  .  .  .  .
        .  .  .  .  .  .  .
        %f %f %f %f %f %f %d
        %f %f %f %f %f %f %d
        %f %f %f %f %f %f %d

    """
    def __init__(self):
        """
        This is the 1st class

        """
        self.num = 1

def main():
    """
    Pero mira que programita.

    """

if __name__ == '__main__':
    main()