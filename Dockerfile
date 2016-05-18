FROM ubuntu:latest

MAINTAINER Fernando Aguilar <aguilarf@ifca.unican.es>

RUN sed '3 a\91.189.88.152 archive.ubuntu.com' /etc/hosts 

RUN apt-get update
RUN apt-get -y upgrade

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install subversion libtool libltdl7 libltdl-dev libexpat1-dev gcc gfortran g++ mpich byacc flex openssl ruby libreadline6-dev libnetcdf-dev autoconf automake autotools-dev wget

RUN wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.4.0.tar.gz
RUN tar -zxvf netcdf-4.4.0.tar.gz
RUN cd netcdf-4.4.0 && ./configure --disable-netcdf-4 --prefix=/usr && make && make install

RUN wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-4.4.3.tar.gz
RUN tar -zxvf netcdf-fortran-4.4.3.tar.gz 
RUN cd netcdf-fortran-4.4.3 && ./configure --disable-netcdf-4 --prefix=/usr && make && make install

RUN svn checkout https://svn.oss.deltares.nl/repos/delft3d/tags/6075/ delft3d_repository --username ferag.x --password indigo

RUN sed -i "s/addpath PATH \/opt\/mpich2-1.4.1-gcc-4.6.2\/bin/addpath PATH \/usr\/bin/" delft3d_repository/src/build.sh
RUN sed -i "s/export MPI_INCLUDE=\/opt\/mpich2-1.4.1-gcc-4.6.2\/include/export MPI_INCLUDE=\/usr\/include/" delft3d_repository/src/build.sh
RUN sed -i "s/export MPILIBS_ADDITIONAL=\"-L\/opt\/mpich2-1.4.1-gcc-4.6.2\/lib -lfmpich -lmpich -lmpl\"/export MPILIBS_ADDITIONAL=\"-L\/usr\/lib -lfmpich -lmpich -lmpl\"/" delft3d_repository/src/build.sh
RUN sed -i "s/export MPIFC=\/opt\/mpich2-1.4.1-gcc-4.6.2\/bin\/mpif90/export MPIFC=\/usr\/bin\/mpif90/" delft3d_repository/src/build.sh
Run sed -i "s/addpath PATH \/opt\/gcc\/bin/addpath PATH \/usr\/bin/" delft3d_repository/src/build.sh
RUN sed -i "s/addpath LD_LIBRARY_PATH \/opt\/gcc\/lib \/opt\/gcc\/lib64/addpath LD_LIBRARY_PATH \usr\/lib \/usr\/lib64/" delft3d_repository/src/build.sh
RUN sed -i "s/make ds-install &> \$log/make ds-install/" delft3d_repository/src/build.sh
RUN sed -i "s/-lfmpich -lmpich -lmpl/-lmpich -lmpl/" delft3d_repository/src/build.sh

RUN cat delft3d_repository/src/build.sh | grep ds-install

#command="./autogen.sh --verbose &> $log"
#        ./configure --prefix=`pwd` $configureArgs &> $log \

ENV NETCDF_LIBS -I/usr/lib
ENV NETCDF_CFLAGS -I/usr/include

RUN ls /usr/lib

RUN delft3d_repository/src/build.sh -gnu -64bit -debug
CMD cat delft3d_repository/src/logs/*
#RUN delft3d_repository/src/autogen.sh
#RUN CFLAGS='-O2' CXXFLAGS='-O2' FFLAGS='-O2' FCFLAGS='-O2' delft3d_repository/src/configure --prefix=`pwd`
#RUN make ds-install -C delft3d_repository/src/

ENV MODEL_ID model2
ENV BASE_MODEL_PATH delft3d_repository/examples/06_delwaq
ENV INP_FILE com-tut_fti_waq.inp

RUN cp -rf $BASE_MODEL_PATH $BASE_MODEL_PATH/../$MODEL_ID
ADD com-tut_fti_waq.inp $BASE_MODEL_PATH/../$MODEL_ID/com-tut_fti_waq.inp

RUN cd $BASE_MODEL_PATH/../$MODEL_ID && ./run_delwaq.sh && ls
