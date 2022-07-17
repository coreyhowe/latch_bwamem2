FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

RUN apt-get update -y &&\
    apt-get install -y wget curl unzip git zlib1g-dev

#RUN git clone --recursive https://github.com/bwa-mem2/bwa-mem2
#WORKDIR bwa-mem2
#RUN make
#WORKDIR /root
#RUN ls bwa-mem2

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 


RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge

RUN conda install -c bioconda bwa-mem2

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
