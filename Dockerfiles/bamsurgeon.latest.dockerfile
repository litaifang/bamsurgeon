FROM lethalfang/bamsurgeon:base-1.2.1

ENV HOME=/usr/local/
ENV PATH="/usr/local/novocraft:${PATH}"
WORKDIR /usr/local

RUN cd $HOME && wget https://www.dropbox.com/s/pzw7w2do6gcllp1/novocraftV3.08.02.Linux3.10.0.tar.gz && tar -xvf novocraftV3.08.02.Linux3.10.0.tar.gz && mv novocraft/* /usr/local/bin
RUN cd $HOME && git clone https://github.com/ltfang-bina/bamsurgeon.git && cd bamsurgeon && git checkout latest && python setup.py build && python setup.py install
