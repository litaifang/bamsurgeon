FROM lethalfang/bamsurgeon:base-1.2

ENV HOME=/usr/local/
WORKDIR /usr/local
RUN cd $HOME && git clone https://github.com/ltfang-bina/bamsurgeon.git && cd bamsurgeon && python setup.py build && python setup.py install
