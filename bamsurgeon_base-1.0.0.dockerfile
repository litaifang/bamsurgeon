FROM ubuntu:16.04

ENV HOME=/usr/local/
WORKDIR /usr/local

RUN apt-get update
RUN apt-get install -y zlib1g-dev git wget libncurses5-dev unzip python python-pip libbz2-dev liblzma-dev pkg-config automake libglib2.0-dev default-jre software-properties-common bowtie2
RUN apt-get clean
RUN pip install numpy scipy cython pysam

RUN cd $HOME
RUN wget https://www.ebi.ac.uk/~zerbino/velvet/velvet_1.2.10.tgz && tar xvzf velvet_1.2.10.tgz && make -C velvet_1.2.10 && cp velvet_1.2.10/velvetg $HOME/bin && cp velvet_1.2.10/velveth $HOME/bin
RUN wget https://github.com/lh3/bwa/archive/v0.7.15.tar.gz && tar -xvf v0.7.15.tar.gz && make -C bwa-0.7.15 && cp bwa-0.7.15/bwa $HOME/bin
RUN git clone https://github.com/samtools/htslib.git && make -C htslib
RUN git clone https://github.com/samtools/samtools.git && make -C samtools && cp samtools/samtools $HOME/bin && cp samtools/misc/wgsim $HOME/bin
RUN git clone https://github.com/samtools/bcftools.git && make -C bcftools && cp bcftools/bcftools $HOME/bin
RUN wget https://github.com/broadinstitute/picard/releases/download/1.131/picard-tools-1.131.zip && unzip picard-tools-1.131.zip
RUN wget http://ftp.gnu.org/gnu/automake/automake-1.14.1.tar.gz && tar -xvf automake-1.14.1.tar.gz && cd automake-1.14.1 && ./configure && make && make install
RUN cd $HOME && git clone https://github.com/adamewing/exonerate.git && cd exonerate && git checkout v2.4.0 && autoreconf -i && ./configure && make && make install
RUN cd $HOME && wget http://research-pub.gene.com/gmap/src/gmap-gsnap-2017-06-20.tar.gz && tar -xvf gmap-gsnap-2017-06-20.tar.gz && cd gmap-2017-06-20/ && ./configure && make && make install
