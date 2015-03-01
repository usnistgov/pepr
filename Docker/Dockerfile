FROM ipython/ipython

#MAINTAINER IPython Project <ipython-dev@scipy.org>
MAINTAINER Nate Olson <nolson@nist.gov>
#modified ipython/notebook

# Adding Bioinformatics Tools
RUN apt-get update
RUN apt-get install -y -q   \ 
                            #git \
                            automake \
                            #pkg-config \
                            curl \
                            wget \
                            bwa \
                            unzip \
                            #zlib1g-dev \
                            libbz2-dev \
                            libncurses5-dev \
                            libyaml-dev \
                            openjdk-7-jdk \
                            openjdk-7-jre

# install bowtie2 
RUN wget http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.2.2/bowtie2-2.2.2-linux-x86_64.zip;\
    unzip bowtie2-2.2.2-linux-x86_64.zip && rm -rf bowtie2-2.2.2-linux-x86_64.zip;\
    ln -s `pwd`/bowtie*/bowtie* /usr/local/bin

# install picard
# this also sets the jars as 'executable' and puts them in the path so they can be found with the 'which ' command - not working correctly
RUN wget http://downloads.sourceforge.net/project/picard/picard-tools/1.111/picard-tools-1.111.zip;\
    unzip picard-tools-1.111.zip && rm -rf picard-tools-1.111.zip;\
    chmod +x picard*/*.jar && ln -s `pwd`/picard*/*.jar /usr/local/bin/

# install htslib samtools and bcftools
RUN wget http://sourceforge.net/projects/samtools/files/samtools/1.1/samtools-1.1.tar.bz2;\
    tar -xaf samtools-1.1.tar.bz2 && rm -rf samtools-1.1.tar.bz2 ;\
    cd samtools-1.1;\
    make && ln -f -s `pwd`/* /usr/bin && cd ../

RUN wget http://sourceforge.net/projects/samtools/files/samtools/1.1/bcftools-1.1.tar.bz2;\
    tar -xaf bcftools-1.1.tar.bz2 && rm -rf bcftools-1.1.tar.bz2 ;\
    cd bcftools-1.1;\
    make && ln -f -s `pwd`/bcftools /usr/bin && cd ../

# install Pilon
RUN wget https://github.com/broadinstitute/pilon/releases/download/v1.10/pilon-1.10.jar;\
    chmod +x pilon-1.10.jar; \
    ln -s `pwd`/pilon-1.10.jar /usr/local/bin/

# install TMAP
RUN git clone git://github.com/iontorrent/TMAP.git; \
	cd TMAP; \
	git submodule init && git submodule update; \
	sh autogen.sh && ./configure && make; \
	make install && ln -f -s `pwd`/tmap /usr/bin && cd ../

# install sratoolkit
RUN wget http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.4.5/sratoolkit.2.4.5-ubuntu64.tar.gz &&\
        tar -xf sratoolkit.2.4.5-ubuntu64.tar.gz &&\
        rm -rf sratoolkit.2.4.5-ubuntu64.tar.gz;\
        ln -f -s `pwd`/sratoolkit.2.4.5-ubuntu64/bin/* /usr/bin/

# install fastqc
RUN wget http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.2.zip;\
    unzip fastqc_v0.11.2.zip && cd FastQC;\
    chmod +x fastqc;\
    ln -sf `pwd`/fastqc /usr/bin/ && cd ../

# install varscan
RUN wget http://sourceforge.net/projects/varscan/files/VarScan.v2.3.7.jar;\
    chmod +x VarScan.v2.3.7.jar; \
    ln -s `pwd`/VarScan.v2.3.7.jar /usr/local/bin/

# installing cement
RUN pip install cement
RUN pip install pyYAML

VOLUME /pepr-data
WORKDIR /pepr-data

# EXPOSE 8888

# # You can mount your own SSL certs as necessary here
# # ENV PEM_FILE /key.pem
# # $PASSWORD will get `unset` within notebook.sh, turned into an IPython style hash
# ENV PASSWORD micro_rm_pw

# # ADD notebook.sh /
# # RUN chmod u+x /notebook.sh

# # CMD ["/notebook.sh"]

